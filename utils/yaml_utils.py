import yaml
from pathlib import Path

def load_yaml(file_path):
    """加载 YAML 文件并返回数据"""
    try:
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise ValueError(f"YAML 文件不存在: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"YAML 解析错误: {str(e)}")