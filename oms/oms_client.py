import logging

import requests
from constants.oms_path import QUERY_INVENTORY, COMMON_ORDER_CREATE, DIRECT_ORDER_CREATE
from utils.random_number import CustomSnowflake
import os

class OmsClient:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": os.getenv("Authorization")})

    def create_common_order(self, order_data):
        """
        创建普通订单
        """
        url = f"{self.base_url}{COMMON_ORDER_CREATE}"
        response = self.session.post(url, json=order_data)
        return response.json()
        order_data ={
        "saleChannelCode": "EBAY",
        "isRegistered": 1,
        "isInsured": 0, # 是否保价 0-否 1-是
        "insuranceAmount": 2, # 保险金额
        "isConfirm": 1,
        "consigneeCountryCode": "GB",
        "consigneeCity": "TATTI",
        "consigneeEmail": "1@163.com",
        "consigneeName": "test",
        "consigneePostcode": "UK11 1",
        "consigneeStreetOne": "宝安大道",
        "consigneeTel": 11,
        "saleTime": "2024-01-01",
        # "labelUrl": "https://gw.lingxingerp.com/erp/api/getOrderSeparationInfo?company_id=901261311413408256&encryptedStr=cd95zJL%2BekSG7xkrzBjmcYBm3uNFwTu5go4xZN9JDz7iPE%2FlAPml2Rhqb%2FPf%2BRIkcx599dqqFu%2FenBaq6d5bKq0fLdwa04t133g3adE0Vs5l9eMCbDRR%2BuDiwg",
        # "labelUrl": "https://erp.sweetnight.com.cn/api/filecenter/download/withFileSuffix/1934866/faceUrl-0.pdf",
        # "labelUrl": "http://oa.tenflyer.net:1216/filedata/lms/label//temu/2025/07/04/SN250704017950.pdf",
        "labelUrl": "http://oa.tenflyer.net:1216/filedata/lms/label//temu/2025/07/04/SN250704005811.pdf",
        "warehouseCode": "SZTEST",
        "logisticsServiceCode": "JD-1DD",
        # "returnLogisticsFlag": 1,
        # "returnLogisticsServiceCode": "XOD",
        "orderNo": "1",
        "referenceNo": "1",
        "trackNumber": "1",
        "details": [{"qty": 1, "sku": sku}]
    }
        order_no = str(CustomSnowflake().next_id())
        order_data.update({
            "orderNo": order_no,
            "referenceNo": order_no,
            "trackNumber": order_no
        })
        # order_data = load_order_template("EBAY")
        response = oms_client.create_common_order(order_data)
        logging.info("创建普通订单结果: %s", response)
    def create_direct_order(self, order_data):
        """
        创建普通订单
        """
        url = f"{self.base_url}{DIRECT_ORDER_CREATE}"
        response = self.session.post(url, json=order_data)
        return response.json()
        order_no = str(CustomSnowflake().next_id())
        order_data.update({
            "orderNo": order_no,
            "referenceNo": order_no,
            "trackNumber": order_no
        })
        # order_data = load_order_template("EBAY")
        response = oms_client.create_common_order(order_data)
        logging.info("创建普通订单结果: %s", response)
    def query_inventory(self, sku_ids):
        """
        查询商品库存
        """
        url = f"{self.base_url}{QUERY_INVENTORY}"
        body = dict(warehouseCode="SZTEST", pageNum=1, pageSize=10, skus=sku_ids
                    , startUpdateTime="2020-05-01 00:00:00",
                    endUpdateTime="2026-05-23 00:00:00")

        response = self.session.post(url, json=body)
        return response.json()

