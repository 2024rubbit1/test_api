from api.wms_client import WmsClient
from api.oms_client import OmsClient
from utils.yaml_utils import load_yaml
from utils.config_utils import load_env_config
# 使用pathlib处理路径
from pathlib import Path
# 新增：添加环境变量加载相关依赖
import os
import logging
from dotenv import load_dotenv  # 确保已安装 python-dotenv 包


class InboundProcessFlow:
    # 通过构造函数注入客户端，复用conftest中的全局client
    def __init__(self):

        env = os.getenv("ENV", "test")
        oms_config = load_env_config(env, "configs/oms", ["oms_base_url", "Authorization"])
        self.oms_client = OmsClient(base_url=oms_config["oms_base_url"], auth_token=oms_config["Authorization"])
        wms_config = load_env_config(env, "configs/wms", ["wms_base_url", "username", "password"])
        self.wms_client = WmsClient(base_url=wms_config["wms_base_url"])

    def complete_inbound_flow(self):
        """完整入库上架流程：创建入库单→边卸边上架→查询上架结果
        单个SKU入库上架流程
        """
        # 调用wms_client中的单个API方法组合成流程
        inbound_case = next(
            case for case in load_yaml("../../testdata/oms/inbound/inbound_cases.yaml")
            if case["case_name"] == "single_sku_inbound"
        )
        create_result = self.oms_client.create_inbound(inbound_case=inbound_case)
        self.oms_client.logger.info(create_result)
        # 增强断言，确保data字段存在且不为None
        assert create_result["code"] == 200 and create_result.get("data") is not None, \
            f"创建入库单失败: 状态码{create_result['code']}, 消息{create_result['msg']}, 数据{create_result.get('data')}"
        confirm_result = self.oms_client.confirm_inbound(we_no=create_result["data"])
        self.oms_client.logger.info(confirm_result)
        # 增强断言，确保data字段存在且不为None
        assert confirm_result["code"] == 200 and confirm_result.get("msg") == "操作成功", \
            f"确认入库单失败: 状态码{confirm_result['code']}, 消息{confirm_result['msg']}"
        detail_table_data = inbound_case["warehouse_entry_box_data"][0]["detailTableData"]
        sku = detail_table_data[0]["sku"]
        qty = detail_table_data[0]["qty"]
        we_no = create_result["data"]
        shelf_result = self.wms_client.shelf_by_sku_and_we_no(sku, we_no, qty)
        self.oms_client.logger.info(shelf_result)
        # 增强断言，确保data字段存在且不为None
        assert shelf_result["code"] == 200 and shelf_result["msg"] == "上架成功", \
            f"上架失败: 状态码{shelf_result['code']}, 消息{shelf_result['msg']}"
        inventory_trans_result = self.wms_client.query_inventory_transaction(we_no)
        self.oms_client.logger.info(inventory_trans_result)
        # 增强断言，确保data字段存在且不为None
        assert inventory_trans_result["code"] == 200 and inventory_trans_result["msg"] == "查询成功", \
            f"查询库存流水记录失败: 状态码{inventory_trans_result['code']}, 消息{inventory_trans_result['msg']}"
        # 验证库存流水中的数量等于上架数量
        assert inventory_trans_result["rows"][0]["fromQty"] == qty, \
            f"库存流水记录数量与上架数量不一致: 库存流水记录数量{inventory_trans_result['rows'][0]['fromQty']}, 上架数量{qty}"
        self.oms_client.logger.info("上架后，库存验证无误，入库上架流程验证完成")


if __name__ == "__main__":
    i = InboundProcessFlow()
    i.complete_inbound_flow()
