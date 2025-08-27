# tests/utils/data_loader.py
import yaml
import uuid
import pandas as pd
from pathlib import Path


def load_order_template(channel, template_dir="order_templates"):
    """加载订单模板并处理动态字段

    Args:
        channel: 销售渠道（如'EBAY'）
        template_dir: 模板存放目录

    Returns:
        填充后的订单字典
    """
    template_path = Path(__file__).parent.parent / template_dir / f"{channel.lower()}_order.yaml"

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            base = yaml.safe_load(f) or {}

        # 动态字段处理
        if base.get("dynamic_fields", {}).get("orderNo") == "generate:uuid":
            base["orderNo"] = str(uuid.uuid4())

        if base.get("dynamic_fields", {}).get("details") == "import:skus.csv":
            sku_path = Path(__file__).parent.parent / "dynamic_params/skus.csv"
            base["details"] = pd.read_csv(sku_path).to_dict('records')

        return base

    except FileNotFoundError as e:
        raise ValueError(f"模板文件不存在: {template_path}") from e