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

    def generate_order_no(self, env: str, prefix: str = "ORDER") -> str:
        """生成唯一订单号"""
        self.order_counter += 1
        timestamp = int(uuid.uuid1().time)
        return f"{prefix}_{env}_{timestamp}_{self.order_counter:06d}"

    def get_skus_for_scenario(self, env: str, scenario: str) -> List[Dict]:
        """根据场景配置获取SKU列表"""
        scenario_config = self.config['test_scenarios'][scenario]
        env_config = self.config['environments'][env]

        sku_details = []

        if 'sku_config' in scenario_config:
            # 单一SKU配置
            config = scenario_config['sku_config']
            sku_pool = env_config['sku_pool'][config['category']]
            selected_skus = random.sample(sku_pool, min(config['count'], len(sku_pool)))

            for sku in selected_skus:
                sku_details.append({
                    'sku': sku,
                    'qty': config['quantity']
                })

        elif 'items' in scenario_config:
            # 多物品配置
            for item_config in scenario_config['items']:
                sku_pool = env_config['sku_pool'][item_config['category']]
                selected_skus = random.sample(sku_pool, min(item_config['count'], len(sku_pool)))

                for sku in selected_skus:
                    sku_details.append({
                        'sku': sku,
                        'qty': item_config['quantity']
                    })

        return sku_details

    def create_order(
            self,
            env: str = "test",
            scenario: str = "single_normal",
            custom_order_no: Optional[str] = None,
            include_optional: bool = False,
            **overrides
    ) -> Dict:
        """
        创建订单数据

        Args:
            env: 环境类型 (test/staging/production)
            scenario: 测试场景
            custom_order_no: 自定义订单号
            include_optional: 是否包含可选字段
            **overrides: 覆盖字段

        Returns:
            订单数据字典
        """
        # 生成订单号
        order_no = custom_order_no or self.generate_order_no(env)

        # 获取环境配置
        env_config = self.config['environments'][env]

        # 构建基础订单数据
        order_data = copy.deepcopy(self.config['order_template'])
        order_data.update({
            'warehouseCode': env_config['warehouseCode'],
            'logisticsServiceCode': env_config['logisticsServiceCode'],
            'orderNo': order_no,
            'details': self.get_skus_for_scenario(env, scenario)
        })

        # 添加可选字段
        if include_optional and 'optional_fields' in self.config:
            optional_data = {}
            for key, value in self.config['optional_fields'].items():
                if isinstance(value, dict) and env in value:
                    # 环境特定的模板字段
                    optional_data[key] = value[env].format(order_no=order_no)
                else:
                    # 固定值字段
                    optional_data[key] = value

            order_data.update(optional_data)

        # 应用覆盖字段
        if overrides:
            order_data.update(overrides)

        return order_data

    def create_multiple_orders(
            self,
            env: str = "test",
            scenarios: List[str] = None,
            count_per_scenario: int = 1,
            **kwargs
    ) -> List[Dict]:
        """创建多个订单"""
        if scenarios is None:
            scenarios = list(self.config['test_scenarios'].keys())

        orders = []
        for scenario in scenarios:
            for _ in range(count_per_scenario):
                orders.append(self.create_order(env, scenario, **kwargs))

        return orders

if __name__ == "__main__":
    factory = OrderDataFactory()
    orders = factory.create_multiple_orders(
        env="test",
        scenarios=["single_normal"],
        count_per_scenario=2
    )
    for order in orders:
        print(order)
