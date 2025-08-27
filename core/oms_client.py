import requests
from utils.request_util import RequestUtil
from utils.log_util import get_logger
from utils.config_util import load_env
from constants.oms_path import COMMON_ORDER_CREATE, RETURN_ORDER_CREATE


class OmsClient:
    def __init__(self, env):
        self.config = load_env(module="oms", env=env)
        self.oms_session = requests.Session()
        self.oms_session.headers.update({"Authorization": self.config["Authorization"]})
        self.logger = get_logger(__name__)
        self.request_util = RequestUtil(base_url=self.config["base_url"], session=self.oms_session)

    def create_common_order(self, order_data):
        """
        创建普通订单
        """
        response = self.request_util.post_json(COMMON_ORDER_CREATE, json=order_data)
        return response.json()

    def create_return_order(self, order_data):
        """
        创建退货订单
        """
        response = self.request_util.post_json(RETURN_ORDER_CREATE, json=order_data)
        return response.json()
oms = OmsClient("test")
oms.create_common_order(order_data={})
