import yaml
import copy
import random
import uuid
import os
from typing import Dict, List, Any, Optional


class OrderDataFactory:
    def __init__(self, config_path: str = "configs/oms/order_config.yaml"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        full_config_path = os.path.join(project_root, config_path)
        self.config = self._load_config(full_config_path)
        self.order_counter = 0

    def _load_config(self, config_path: str) -> Dict:
        """加载YAML配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def generate_order_no(self, env: str, order_type: str = "standard") -> str:
        """生成唯一订单号"""
        self.order_counter += 1
        timestamp = int(uuid.uuid1().time)
        type_prefix = order_type.upper() if order_type != "standard" else "STD"
        return f"{type_prefix}_{env}_{timestamp}_{self.order_counter:06d}"

    def get_environment_value(self, env: str, field: str, key: str) -> str:
        """获取环境特定的值，如果不存在映射则返回原值"""
        env_config = self.config['environments'][env]
        mapping = env_config.get(f"{field}_mapping", {})
        return mapping.get(key, key)

    def determine_order_type(self, logistics_code: str, sku_category: str) -> str:
        """根据物流和SKU类别确定订单类型"""
        logistics_config = self.config['logistics_services'].get(logistics_code, {})

        # 如果物流是自提服务，强制为自提订单（thirdType=4）
        if logistics_code == "SELF_PICKUP":
            return "self_pickup"

        # 如果SKU类别是fba，确定为FBA订单（thirdType=1）
        if sku_category == "fba":
            return "fba"

        # 默认标准订单（不传thirdType）
        return "standard"

    def get_warehouse_code(self, env: str, base_warehouse: str, order_type: str, logistics_code: str) -> str:
        """获取最终的仓库代码"""
        order_type_config = self.config['order_types'].get(order_type, {})
        logistics_config = self.config['logistics_services'].get(logistics_code, {})

        # 处理仓库后缀
        warehouse = base_warehouse

        # 物流强制配置优先
        if logistics_config.get('force_warehouse_suffix'):
            warehouse += logistics_config['force_warehouse_suffix']
        elif order_type_config.get('warehouse_suffix'):
            warehouse += order_type_config['warehouse_suffix']

        # 获取环境特定的映射值
        return self.get_environment_value(env, 'warehouse', warehouse)

    def get_logistics_code(self, env: str, logistics_config: str) -> str:
        """获取最终的物流代码"""
        if logistics_config == "default":
            logistics = self.config['environments'][env]['base_logistics']
        else:
            logistics = logistics_config

        # 获取环境特定的映射值
        return self.get_environment_value(env, 'logistics', logistics)

    def get_skus(self, env: str, scenario_config: Dict) -> List[Dict]:
        """获取SKU详情"""
        env_config = self.config['environments'][env]
        details = []

        if 'sku_mix' in scenario_config:
            # 混合SKU配置
            for item in scenario_config['sku_mix']:
                sku_pool = env_config['sku_pool'][item['category']]
                selected_skus = random.sample(sku_pool, min(item['count'], len(sku_pool)))
                for sku in selected_skus:
                    details.append({'sku': sku, 'qty': item['quantity']})
        else:
            # 单一SKU配置
            sku_category = scenario_config['sku_category']
            sku_count = scenario_config.get('sku_count', 1)
            quantity = scenario_config.get('quantity', 1)

            sku_pool = env_config['sku_pool'][sku_category]
            selected_skus = random.sample(sku_pool, min(sku_count, len(sku_pool)))

            for sku in selected_skus:
                details.append({'sku': sku, 'qty': quantity})

        return details

    def create_order(
            self,
            env: str = "test",
            scenario: str = "standard_order",
            custom_order_no: Optional[str] = None,
            include_optional: bool = False,
            **overrides
    ) -> Dict:
        """创建订单数据"""
        # 获取场景配置
        scenario_config = self.config['test_scenarios'][scenario]
        env_config = self.config['environments'][env]

        # 生成订单号
        order_no = custom_order_no or self.generate_order_no(env, scenario_config['order_type'])

        # 获取物流代码
        logistics_code = self.get_logistics_code(env, scenario_config['logistics'])

        # 确定订单类型（考虑物流的影响）
        final_order_type = self.determine_order_type(
            logistics_code,
            scenario_config.get('sku_category', 'standard')
        )

        # 获取仓库代码
        warehouse_config = scenario_config['warehouse']
        base_warehouse = env_config['base_warehouse'] if warehouse_config == "default" else warehouse_config
        warehouse_code = self.get_warehouse_code(env, base_warehouse, final_order_type, logistics_code)

        # 获取SKU详情
        details = self.get_skus(env, scenario_config)

        # 构建基础订单数据
        order_data = copy.deepcopy(self.config['base_order_template'])

        # 添加订单类型相关字段
        order_type_config = self.config['order_types'][final_order_type]
        if order_type_config['thirdType'] is not None:
            order_data['thirdType'] = order_type_config['thirdType']

        # 添加动态字段
        order_data.update({
            'warehouseCode': warehouse_code,
            'logisticsServiceCode': logistics_code,
            'orderNo': order_no,
            'details': details
        })

        # 添加可选字段
        if include_optional and 'optional_fields' in self.config:
            optional_data = {}
            for key, value in self.config['optional_fields'].items():
                if isinstance(value, dict) and env in value:
                    optional_data[key] = value[env].format(order_no=order_no)
                else:
                    optional_data[key] = value
            order_data.update(optional_data)

        # 应用覆盖字段
        if overrides:
            order_data.update(overrides)

        return order_data

    def create_test_suite(self, env: str = "test") -> List[Dict]:
        """创建完整的测试套件"""
        test_suite = []

        for scenario in self.config['test_scenarios']:
            order = self.create_order(env, scenario)
            order['test_scenario'] = scenario
            order['test_description'] = self.config['test_scenarios'][scenario]['description']
            test_suite.append(order)

        return test_suite

if __name__ == "__main__":
    order_factory = OrderDataFactory()
    test_suite = order_factory.create_test_suite()
    for order in test_suite:
        print(order)
