import logging
import os

import requests

from constants.oms_path import *
from utils.random_number import CustomSnowflake


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
        # logging.info(url)
        return response.json()
        order_data = {
            "saleChannelCode": "EBAY",
            "isRegistered": 1,
            "isInsured": 0,  # 是否保价 0-否 1-是
            "insuranceAmount": 2,  # 保险金额
            "isConfirm": 1,
            "consigneeCountryCode": "GB",
            "consigneeCity": "TATTI",
            "consigneeEmail": "1@163.com",
            "consigneeName": "test",
            "consigneePostcode": "UK11 1",
            "consigneeStreetOne": "宝安大道",
            "consigneeTel": 11,
            "saleTime": "2024-01-01",
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
        logging.info(url)
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

    def expense_settle_fee_calculate(self):
        """
        费用计算
        """
        url = f"{self.base_url}{EXPENSE_SETTLE_FEE_CALCULATE}"
        body = {
            "warehouseCodes": [
                "SZTEST"
            ],
            "logisticsServiceCodes": [
                "JD-1DD"
            ],
            "countryCode": "GB",
            "postcode": "UK1 1",
            "state": "string",
            "city": "string",
            "length": 1,
            "width": 2,
            "height": 3,
            "weight": 1,
            "orderNo": "11"
        }

        response = self.session.post(url, json=body)
        return response.json()

    def query_order(self, fo_nos: list):
        url = f"{self.base_url}{QUERY_ORDER}"
        body = {
            # "beginCreateTime": "2022-05-18",
            # "endCreateTime": "2022-05-28",
            # "beginStockOutTime": "2022-05-18",
            # "endStockOutTime": "2022-05-28",
            "foNos": fo_nos,
            # "orderNos": [
            #   "FR17420"
            # ],
            "pageNum": 1,
            "pageSize": 10,
            # "referenceNos": [
            #   "RF2022050101"
            # ],
            # "amazonOrderNoList": [
            #    "FBA456465465"
            # ],
            # "amazonReferenceNoList": [
            #    "FBA456465465"
            # ]
        }

        response = self.session.post(url, json=body)
        logging.info(url)
        return response.json()

    def query_location_inventory(self, location: str, sku: str, warehouse_code):
        """
        查询位置库存
        """
        url = f"{self.base_url}{QUERY_LOCATION_INVENTORY}"
        body = dict(pageNum=1, pageSize=10, warehouseCode=warehouse_code, sku=sku, location=location,
                    manufactureBatch="")
        response = self.session.post(url, json=body)
        logging.info(response.json())
        return response.json()

    def query_logistics_service_list(self):
        """
        查询物流渠道派送
        """
        url = f"{self.base_url}{LOGISTICS_SERVICE_LIST}"
        response = self.session.get(url)
        return response.json()
    def upload_tracking_no_and_shipment(self, order_no: str, track_number: str):
        """
        上传物流单号和发货
        """
        url = f"{self.base_url}{UPLOAD_TRACKING_NO_AND_SHIPMENT}"
        body = dict(orderNo=order_no, trackNumber=track_number)
        response = self.session.post(url, json=body)
        return response.json()

    def create_inbound(self, warehousingEntryBoxDatas=None):
        """
        创建入库单
        :param details: 订单详情列表
        :param is_insured: 是否保价，默认为0
        :param insurance_amount: 保价金额，默认为0
        :return: 订单号
        """
        try:
            # body = get_inbound_order_template()
            body = {
                "billAmount": 0,
                "boxSpecification": "40HQ",
                "confirmWarehousing": 0,
                "deliverDate": "2024-08-16",
                "estimatedArrivalDate": "2024-08-16",
                "filesUrl": "",
                "imageUrl": "",
                "insuredAmount": 0,
                "logisticTrackNo": " string ",
                "logisticsCompany": "string",
                "notes": "string",
                "pickUp": 0,
                "referenceNo": str(CustomSnowflake().next_id()),
                "transportModeCode": 2,
                "warehouseCode": "SZTEST",
                "warehousingEntryBoxData": [
                    {
                        "boxNo": 1,
                        "detailTableData": [{
                            "qty": 1,
                            "sku": "TEST-IPING0021",
                            "manufactureBatch": "1001"
                        }],
                        "height": 0,
                        "length": 0,
                        "notes": "string",
                        "weight": 0,
                        "width": 0
                    }
                ]
            }

            # body["warehousingEntryBoxDatas"] = warehousingEntryBoxDatas
            url = f"{self.base_url}{CREATE_INBOUND}"
            resp = self.session.post(url, json=body)
            resp.raise_for_status()
            response_json = resp.json()
            return response_json
            # Assert.equals(response_json["code"], 200)
            # return response_json['data']
        except Exception as e:
            logging.info(f"创建入库单出错: {e}")
            return None

    def query_inbound_order(self, we_nos: list):
        url = f"{self.base_url}{SEARCH_INBOUND_LIST}"
        body = {
            "warehouse": ["SZTEST"],
            "pageNum": 1,
            "pageSize": 10,
            "weNo": we_nos
        }

        response = self.session.post(url, json=body)
        logging.info(url)
        logging.info(body)
        return response.json()

    def edit_order(self, referenceNo):
        url = f"{self.base_url}{EDIT_ORDER}"
        body = {
  "referenceNo": referenceNo,
  "attachmentUrl": "http://www.a.com/appli/etiquette-2580980-20231016092916.pdf"
}
        response = self.session.post(url, json=body)
        return response.json()


    def query_intercept(self, reference_no,fo_code: str):
        url = f"{self.base_url}{QUERY_INTERCEPT}?referenceNo={reference_no}&foCode={fo_code}"
        response = self.session.get(url)
        return response.json()

    def intercept_order(self, reference_no,fo_code: str):
        url = f"{self.base_url}{INTERCEPT_ORDER}?referenceNo={reference_no}&foCode={fo_code}&reason=测试拦截"
        logging.info(url)
        response = self.session.get(url)
        return response.json()