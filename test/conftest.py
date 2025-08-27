# conftest.py

import pytest
from dotenv import load_dotenv
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def api_oms_config(env):
    """根据命令行参数加载不同环境的.env文件"""
    logging.info(f"Loading environment: {env}")
    env_file = f"configs/oms/{env}.env"  # 例如 configs/oms/test.env 或 configs/oms/prod.env
    load_dotenv(env_file)
    a = os.getenv("BASE_URL")
    return {
        "base_url": os.getenv("BASE_URL"),
        "auth_token": os.getenv("Authorization")
    }

# @pytest.fixture(scope="session")
# def api_wms_config(env):
def pytest_addoption(parser):
    parser.addoption("--env", default="test", help="test|prod")





# @pytest.fixture(scope="session")
# def api_wms_config(env):
#     """根据命令行参数加载不同环境的.env文件"""
#     env_file = f"configs/wms/{env}.env"  # 例如 configs/wms/test.env 或 configs/wms/prod.env
#     load_dotenv(env_file)
#
#     return {
#         "base_url": os.getenv("BASE_URL"),
#         "auth_token": os.getenv("Authorization")
#     }