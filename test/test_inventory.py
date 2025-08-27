import logging
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))

from oms.oms_client import OmsClient
from utils.random_number import CustomSnowflake


@pytest.mark.skip("先不测库存了")
def test_query_inventory(api_oms_config):
    oms_client = OmsClient()
    response = oms_client.query_inventory(["TEST1-Chair-173131859177"])
    logging.info("查询商品库存结果: %s", response)
    assert response["code"] == 200


# 定义多个 SKU 作为测试数据
# @pytest.mark.skip("先不测普通订单了")
@pytest.mark.parametrize("sku", [
    "TEST-IPING0020",
    # "TEST-0302-001",
    # "Test-02-04098",
    # "NEW-BLACK-YK-LY-2001",
    # "TEST-PICK-00002",
    # "IT-TEST-202402501"
    # "TEST1-Chair-173131859177"
])
def test_create_common_order(api_oms_config, sku):
    oms_client = OmsClient()
    order_data = {
        "saleChannelCode": "EBAY",
        "isRegistered": 1,
        "isInsured": 0,  # 是否保价 0-否 1-是
        "insuranceAmount": 2,  # 保险金额
        "isConfirm": 1,
        "consigneeCountryCode": "GB",
        "consigneeCity": "Ablis",
        # "thirdType": "1",  # 1-FBA订单 2-FBC订单 4-自提订单 5-直发订单
        "consigneeEmail": "test@163.com",
        "consigneeName": "test",
        "consigneePostcode": "UK11 1",
        "consigneeStreetOne": "宝安大道",
        "consigneeTel": 33649383330,
        "saleTime": "2024-01-01",
        # "labelUrl": "https://gw.lingxingerp.com/erp/api/getOrderSeparationInfo?company_id=901261311413408256&encryptedStr=cd95zJL%2BekSG7xkrzBjmcYBm3uNFwTu5go4xZN9JDz7iPE%2FlAPml2Rhqb%2FPf%2BRIkcx599dqqFu%2FenBaq6d5bKq0fLdwa04t133g3adE0Vs5l9eMCbDRR%2BuDiwg",
        # "labelUrl": "https://erp.sweetnight.com.cn/api/filecenter/download/withFileSuffix/1934866/faceUrl-0.pdf",
        # "labelUrl": "http://oa.tenflyer.net:1216/filedata/lms/label//temu/2025/07/04/SN250704017950.pdf",
        # "labelUrl": "http://oa.tenflyer.net:1216/filedata/lms/label//temu/2025/07/04/SN250704005811.pdf",
        "warehouseCode": "SZTEST",
        "logisticsServiceCode": "JD-3DD",
        # "returnLogisticsFlag": 1,
        # "returnLogisticsServiceCode": "XOD",
        "orderNo": "1",
        "referenceNo": "1",
        # "trackNumber": "1",
        "details": [{"qty": 1, "sku": sku}]
    }
    order_no = str(CustomSnowflake().next_id())
    order_data.update({
        "orderNo": order_no,
        "referenceNo": order_no,
        "trackNumber": order_no
    })
    # order_data = load_order_template("EBAY")
    logging.info(order_data)
    response = oms_client.create_common_order(order_data)
    logging.info("创建普通订单结果: %s", response)
    assert response["code"] == 200


@pytest.mark.skip("先不测FBA订单了")
@pytest.mark.parametrize("sku", [
    "TEST-IPING0020",
    # "TEST-0302-001",
    # "Test-02-04098",
    # "NEW-BLACK-YK-LY-2001",
    # "TEST-PICK-00002",
    # "IT-TEST-202402501"
    # "TEST1-Chair-173131859177"
])
def test_create_fba_order(api_oms_config, sku):
    oms_client = OmsClient()
    order_data = {
        "saleChannelCode": "EBAY",
        "isRegistered": 1,
        "isInsured": 0,  # 是否保价 0-否 1-是
        "insuranceAmount": 2,  # 保险金额
        "isConfirm": 1,
        "consigneeCountryCode": "GB",
        "consigneeCity": "Ablis",
        "thirdType": "4",  # 1-FBA订单 2-FBC订单 4-自提订单 5-直发订单
        "consigneeEmail": "test@163.com",
        "consigneeName": "test",
        "consigneePostcode": "UK11 1",
        "consigneeStreetOne": "宝安大道",
        "consigneeTel": 33649383330,
        "saleTime": "2024-01-01",
        # "labelUrl": "https://erp.sweetnight.com.cn/api/filecenter/download/withFileSuffix/1934866/faceUrl-0.pdf",
        # "labelUrl": "http://oa.tenflyer.net:1216/filedata/lms/label//temu/2025/07/04/SN250704017950.pdf",
        # "labelUrl": "http://oa.tenflyer.net:1216/filedata/lms/label//temu/2025/07/04/SN250704005811.pdf",
        "warehouseCode": "SZTEST",
        "logisticsServiceCode": "JD-1DD",
        # "returnLogisticsFlag": 1,
        # "returnLogisticsServiceCode": "XOD",
        "orderNo": "1",
        "referenceNo": "1",
        # "trackNumber": "1",
        "details": [{"qty": 1, "sku": sku}]
    }
    order_no = str(CustomSnowflake().next_id())
    order_data.update({
        "orderNo": order_no,
        "referenceNo": order_no,
        # "trackNumber": order_no
    })
    # order_data = load_order_template("EBAY")
    logging.info(order_data)
    response = oms_client.create_common_order(order_data)
    logging.info("创建普通订单结果: %s", response)
    assert response["code"] == 200


@pytest.mark.skip("1")
def test_create_direct_order(api_oms_config):
    oms_client = OmsClient()
    order_data = {"consignee": {"city": "Royston", "companyName": "", "countryCode": "GB",
                                "email": "2084fd1bc5d8935cb072@members.ebay.com", "name": "Ricky Manen",
                                "postcode": "SG8 5JE", "state": "Hertfordshire", "streetOne": "12c Nightingale Avenue",
                                "streetTwo": "Bassingbourn", "tel": "07951537169"},
                  "details": [{"height": 13.0, "length": 195.0, "qty": 1, "sku": "OC0000035074824", "weight": 15174.0,
                               "width": 20.0}], "isConfirm": 1, "isInsured": 0, "isRegistered": 0,
                  "logisticsServiceCode": "JD-1DD",
                  "orderNo": "1067409525646033543", "parcelHeight": 13.000, "parcelLength": 195.000,
                  "parcelWeight": 15174.000, "parcelWidth": 20.000, "referenceNo": "EF0000636313005",
                  "saleChannelCode": "OTHER", "saleTime": 1756080000000,
                  "shipper": {"city": "Birmingham", "countryCode": "GB",
                              "email": "InboundUK.fulfillment@orangeconnex.com",
                              "name": "Orange Connex Fulfilment Centre-UK05", "postcode": "B6 7AP", "state": "England",
                              "streetOne": "Unit 6 Nexus Point, Elliot Way", "streetTwo": "", "tel": "01212744296",
                              "timezone": 0},
                  "warehouseCode": "SZTEST"}
    order_no = str(CustomSnowflake().next_id())
    order_data.update({
        "orderNo": order_no,
        "referenceNo": order_no,
        # "trackNumber": order_no
    })
    response = oms_client.create_direct_order(order_data)
    logging.info("创建直发订单结果: %s", response)
    assert response["code"] == 200
