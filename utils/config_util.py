# utils/config_util.py
from dotenv import load_dotenv
import os


def load_env(module="oms", env="dev"):
    """加载指定模块和环境的配置"""
    # 获取当前脚本的目录，并向上找到项目根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # 假设 .env 在项目根目录的 configs/oms/ 下
    env_path = os.path.join(project_root, "configs", module, f"{env}.env")
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Env file not found: {env_path}")
    load_dotenv(env_path)
    return {
        "base_url": os.getenv("BASE_URL"),
        "Authorization": os.getenv("Authorization"),
        # 其他需要提取的变量...
    }
