# conftest.py

# 添加项目根目录到Python路径
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))  # 指向test_api目录

import pytest
from oms.oms_client import OmsClient
from dotenv import load_dotenv
import os
import logging
import requests

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def wms_auth(api_wms_config):
    login_url = f"{os.getenv('BASE_URL')}/auth/login"
    login_data = {
    "username": os.getenv("username"),
    "password": os.getenv("password"),
    "rememberMe": True,
    # "uuid": "acf0f7c0b83549eab486e03ab44100c0",
    "captcha": False,
    "applicationId": 1
}
    response = requests.post(login_url, json=login_data)
    assert response.status_code == 200

    auth_data = response.json()
    wms_auth = auth_data["data"]["access_token"]
    assert wms_auth is not None, "Failed to get auth token"

    return wms_auth

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


# @pytest.fixture(scope="module")
# def oms_client():
#     return OmsClient()
@pytest.fixture(scope="session")
def global_oms_client():
    """全局唯一的API客户端实例"""
    client = OmsClient()
    yield client
    client.session.close()  # 测试结束释放资源
@pytest.fixture(scope="session")
def api_wms_config(env):
    """根据命令行参数加载不同环境的.env文件"""
    logging.info(f"Loading environment: {env}")
    env_file = f"configs/wms/{env}.env"  # 例如 configs/wms/test.env 或 configs/wms/prod.env
    load_dotenv(env_file)
    login_url = f"{os.getenv('BASE_URL')}/auth/login"
    login_data = {
        "username": os.getenv("username"),
        "password": os.getenv("password"),
        "rememberMe": True,
        # "uuid": "acf0f7c0b83549eab486e03ab44100c0",
        "captcha": False,
        "applicationId": 1
    }
    logging.info(login_data)
    logging.info(f"username: {os.getenv('username')}")
    response = requests.post(login_url, json=login_data)
    assert response.status_code == 200
    logging.info(response)
    # auth_data = response.json()
    # wms_auth = auth_data["data"]["access_token"]
    # assert wms_auth is not None, "Failed to get auth token"
    return {
        "base_url": os.getenv("BASE_URL"),
        "username": os.getenv("username"),
        "password": os.getenv("password"),
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