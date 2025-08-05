import requests

class OmsClient:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config["headers"])

    def create_common_order(self, order_data):
        """
        创建普通订单
        """
        url = f"{self.config['base_url']}/order/createCommonOrder"
        response = self.session.post(url, json=order_data)
        return response.json()
