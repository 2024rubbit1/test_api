import logging
import os

import requests

from constants.wms_path import UPLOAD_TRACKING_NO_AND_WAYBILL, PAGE_LIST
from utils.random_number import CustomSnowflake


class WmsClient:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": os.getenv("wms_auth")})

    def upload_tracking_no_and_waybill(self, fo_no):
        """
        上传订单的物流信息
        :param order_data: 订单数据，包含订单号、物流信息等
        :return: 响应数据，包含上传结果
        """
        url = f"{self.base_url}{UPLOAD_TRACKING_NO_AND_WAYBILL}?id={self.query_order_id(fo_no)}&trackNo={fo_no}"
        response = self.session.post(url, files="http://oa.tenflyer.net:1216/filedata/lms/label//temu/2025/07/04/SN250704005811.pdf")
        # logging.info(url)
        return response.json()

    def query_order_id(self, order_data):
        """
        查询订单
        :param order_data: 订单数据，包含订单号等
        :return: 响应数据，包含订单信息
        """
        url = f"{self.base_url}{PAGE_LIST}"
        body = dict(pageNum=1, pageSize=10, multipleNos=[
            "FO2509250002-NODIT"
        ])
        response = self.session.post(url, json=order_data)
        logging.info(response)
        return response.json()

    def create_pick_wave_by_single(self, foNo, wareHouseId):
        """
        创建单品单拣波次。

        :param foNo: 履约订单号
        :param wareHouseId: 仓库 ID
        :return: 拣货波次创建的响应
        """
        if not isinstance(foNo, str) or not isinstance(wareHouseId, int):
            logger.error("create_pick_wave_by_single 参数错误：foNo 必须为字符串，wareHouseId 必须为整数")
            raise ValueError("foNo 必须为字符串，wareHouseId 必须为整数")

        try:
            body = self._generate_pick_wave_body(foNo, wareHouseId, self.yaml_read.read_test_data("pick_wave_body")["pick_wave_body_by_single"])
            res = self._send_pick_wave_request(body)
            return res.json()
        except requests.RequestException as e:
            logger.error(f"创建单品单拣波次时发生错误: {e}")
            # raise
            return None
        except ValueError as e:
            logger.error(f"获取单品单拣波次时发生错误: {e}")
            # raise
            return None



class PickWaveConfig:
    # SINGLE_PICK_WAVE_CONFIG = {
    #     "fulfilmentOrderType": 0,
    #     "packageType": 11,
    #     "snFlag": False,
    #     "statuss": [30],
    #     "isGenerate": 1,
    #     "dictType": "package_type",
    #     "pickWaveType": "PP",
    #     "generateMode": 1,
    #     "pickStrategy": 1
    # }
    MULTI_PICK_WAVE_CONFIG = {
        "fulfilmentOrderType": 0,
        "packageType": 12,
        "snFlag": False,
        "statuss": [30],
        "isGenerate": 1,
        "dictType": "package_type",
        "pickWaveType": "PM",
        "generateMode": 1,
        "pickStrategy": 1
    }
    ORDER_PICK_WAVE_CONFIG = {
        "fulfilmentOrderType": 1,
        "packageType": 13,
        "snFlag": False,
        "statuss": [30],
        "isGenerate": 1,
        "dictType": "package_type",
        "pickWaveType": "PB",
        "generateMode": 1,
        "pickStrategy": 1
    }

class CreatePickWave:

    def __init__(self, base_url):
        self.api_client = ApiClient(base_url)
        # self.headers = get_wms_headers()
        self.env = os.getenv("TEST_ENV", "test")
        self.yaml_read = YamlReader()# 默认测试环境
        self.config = self.yaml_read.read_config("wms", self.env)
        self.path = self.yaml_read.read_config("wms", "api_paths")
        self.pick_wave_body = self.yaml_read.read_test_data("pick_wave_body")
        # 全局Session对象（推荐）
        self.session = requests.Session()
        self.session.headers.update(get_wms_headers())

    def _generate_pick_wave_body(self, foNos, wareHouseId, config):
        """
        生成拣货波次请求体。

        :param foNos: 履约订单号列表
        :param wareHouseId: 仓库 ID
        :param config: 拣货波次配置
        :return: 拣货波次请求体
        """
        return {
            **config,
            "wareHouseId": wareHouseId,
            "codes": foNos
        }



    def create_pick_wave_by_transfer(self, foNo):
        """
                创建按单拣货波次。

                :param foNo: 履约订单号
                :param wareHouseId: 仓库 ID
                :return: 拣货波次创建的响应
                """
        warehouse_id = self.config["warehouseId"]
        if not isinstance(foNo, str) or not isinstance(warehouse_id, int):
            logger.error("create_pick_wave_by_multi_item 参数错误：foNo 必须为字符串，wareHouseId 必须为整数")
            raise ValueError("foNo 必须为字符串，wareHouseId 必须为整数")

        try:
            body = get_common_wave_template(foNo, warehouse_id)
            res = self._send_pick_wave_request(body)
            return res.json()
        except requests.RequestException as e:
            logger.error(f"创建按单拣货波次时发生错误: {e}")
            # raise
            return None
        except ValueError as e:
            logger.error(f"获取按单拣货波次时发生错误: {e}")
            # raise
            return None

    def create_pick_wave_by_order(self, foNo):
        """
                创建按单拣货波次。

                :param foNo: 履约订单号
                :param wareHouseId: 仓库 ID
                :return: 拣货波次创建的响应
                """
        warehouse_id = self.config["warehouseId"]
        if not isinstance(foNo, str) or not isinstance(warehouse_id, int):
            logger.error("create_pick_wave_by_multi_item 参数错误：foNo 必须为字符串，wareHouseId 必须为整数")
            raise ValueError("foNo 必须为字符串，wareHouseId 必须为整数")

        try:
            body = get_common_wave_template(foNo, warehouse_id)
            res = self._send_pick_wave_request(body)
            return res.json()
        except requests.RequestException as e:
            logger.error(f"创建按单拣货波次时发生错误: {e}")
            # raise
            return None
        except ValueError as e:
            logger.error(f"获取按单拣货波次时发生错误: {e}")
            # raise
            return None

    def create_pick_wave_by_multi_item(self, foNo, wareHouseId):
        """
                创建多品合拣波次。

                :param foNo: 履约订单号
                :param wareHouseId: 仓库 ID
                :return: 拣货波次创建的响应
                """

        if not isinstance(foNo, str) or not isinstance(wareHouseId, int):
            logger.error("create_pick_wave_by_multi_item 参数错误：foNo 必须为字符串，wareHouseId 必须为整数")
            raise ValueError("foNo 必须为字符串，wareHouseId 必须为整数")

        try:
            body = self._generate_pick_wave_body(foNo, wareHouseId, PickWaveConfig.MULTI_PICK_WAVE_CONFIG)
            return self._send_pick_wave_request(body)
        except Exception as e:
            logger.error(f"创建多品合拣波次时发生错误: {e}")
            raise

    def _send_pick_wave_request(self, body):
        """
        发送创建拣货波次的请求。

        :param body: 请求体
        :return: 拣货波次创建的响应
        """
        try:
            response = self.api_client.request("POST", self.yaml_read.read_config("wms", "api_paths")["pick_wave"],
                                               json=body, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.error(f"发送创建拣货波次请求时发生错误: {e}")
            raise


if __name__ == "__main__":
    a = CreatePickWave("http://wmstest.newouda.com/prod-api")
    # 调用函数并打印结果
    b = a.create_pick_wave_by_single("FO2504230013-NODIT", 13)
    print(b.json())
