import logging
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))

from oms.oms_client import OmsClient
from utils.random_number import CustomSnowflake


@pytest.mark.skip("先不测库存了")
def test_query_inventory(api_oms_config, global_oms_client):
    response = global_oms_client.query_inventory(["TEST1-Chair-173131859177"])
    logging.info("查询商品库存结果: %s", response)
    assert response["code"] == 200


# 定义多个 SKU 作为测试数据
@pytest.mark.skip("先不测普通订单了")
@pytest.mark.parametrize("sku, logisticsServiceCode", [
    ("TEST-0302-001","JD-1DD"),
    ("TEST-0302-001", "JD-11DD"),
# ("TEST-0302-001", "JD-1DD"),
# ("TEST-0302-001", "JD-1DD"),
# ("TEST-0302-001", "JD-1DD"),
# ("TEST-0302-001", "JD-1DD"),
# ("TEST-0302-001", "JD-1DD"),
#     ("Test-02-04098", "JD-1DD")
    # "NEW-BLACK-YK-LY-2001",
    # "TEST-PICK-00002",
    # "IT-TEST-202402501"
    # "TEST1-Chair-173131859177"
])
def test_create_common_order(api_oms_config, global_oms_client, sku, logisticsServiceCode):
    order_data = {
        "saleChannelCode": "EBAY",
        "isRegistered": 1,
        "isInsured": 0,  # 是否保价 0-否 1-是
        "insuranceAmount": 2,  # 保险金额
        "isConfirm": 1,
        "consigneeCountryCode": "GB",
        "consigneeCity": "Ablis",
        "consigneeEmail": "test@163.com",
        "consigneeName": "test",
        "consigneePostcode": "UK11 1",
        "consigneeStreetOne": "宝安大道",
        "consigneeTel": 33649383330,
        "saleTime": "2024-01-01",
        # "labelUrl":  "https://wms.newouda.com/statics/label/2025/09/01/a9b451ca-7390-4007-b7e2-d6bdba7def22.pdf",
        "warehouseCode": "SZTEST",
        "logisticsServiceCode": logisticsServiceCode,
        # "returnLogisticsFlag": 1,
        # "returnLogisticsServiceCode": "XOD",
        "orderNo": "1",
        "referenceNo": "1",
        # "trackNumber": "",
        "details": [{"qty": 1, "sku": sku}]
        # "details": [{"qty": 1, "sku": sku},{"qty": 1, "sku": "NEW-BLACK-YK-LY-2001"}]
    }
    order_no = str(CustomSnowflake().next_id())
    order_data.update({
        "orderNo": order_no,
        "referenceNo": order_no,
        # "trackNumber": order_no
        # "amazonOrderNo": order_no,
        # "amazonReferenceNo": order_no
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
def test_create_fba_order(api_oms_config, global_oms_client, sku):
    order_data = {
        "saleChannelCode": "EBAY",
        "isRegistered": 1,
        "isInsured": 0,  # 是否保价 0-否 1-是
        "insuranceAmount": 2,  # 保险金额
        "isConfirm": 1,
        "consigneeCountryCode": "GB",
        "consigneeCity": "Ablis",
        "thirdType": "1",  # 1-FBA订单 2-FBC订单 4-自提订单 5-直发订单
        "consigneeEmail": "test@163.com",
        "consigneeName": "test",
        "consigneePostcode": "UK11 1",
        "consigneeStreetOne": "宝安大道",
        "consigneeTel": 33649383330,
        "saleTime": "2024-01-01",
        "labelUrl": "https://wms.newouda.com/statics/label/2025/09/01/a9b451ca-7390-4007-b7e2-d6bdba7def22.pdf",
        "warehouseCode": "SZTEST",
        "logisticsServiceCode": "XOD",
        # "returnLogisticsFlag": 1,
        # "returnLogisticsServiceCode": "XOD",
        "orderNo": "1",
        "referenceNo": "1",
        # "trackNumber": "1",
        # "details": [{"qty": 2, "sku": sku}, {"qty": 1, "sku": "TEST-0302-001"}],
        # "amazonOrderNo": "FBA456465465",
        # "amazonReferenceNo": "FBA456465465"
        "details": [{"qty": 1, "sku": sku}]
    }
    order_no = str(CustomSnowflake().next_id())
    order_data.update({
        "orderNo": order_no,
        "referenceNo": order_no,
        # "trackNumber": order_no,
        "amazonOrderNo": order_no,
        "amazonReferenceNo": order_no
    })
    # order_data = load_order_template("EBAY")
    logging.info(order_data)
    response = oms_client.create_common_order(order_data)
    logging.info("创建FBA订单结果: %s", response)
    assert response["code"] == 200


@pytest.mark.skip("1")
def test_create_direct_order(api_oms_config, global_oms_client):
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
@pytest.mark.skip("1")
def test_expense_settle_fee_calculate(api_oms_config, global_oms_client):
    response = global_oms_client.expense_settle_fee_calculate()
    logging.info("费用计算结果: %s", response)

@pytest.mark.skip("1")
@pytest.mark.parametrize("fo_nos", [
    ["FO2511070032-A550"]
    # "TEST-0302-001",
    # "Test-02-04098",
    # "NEW-BLACK-YK-LY-2001",
    # "TEST-PICK-00002",
    # "IT-TEST-202402501"
    # "TEST1-Chair-173131859177"
])
def test_query_order(api_oms_config, global_oms_client, fo_nos):
    response = global_oms_client.query_order(fo_nos)
    logging.info("查询订单结果: %s", response)


@pytest.mark.skip("1")
@pytest.mark.parametrize("location, sku, warehouse_code", [
    # ("", "", "SZTEST"),
    # ("A1", "", ""),
    # ("", "NEW-BLACK-YK-LY-2006", ""),
    # ("", "", ""),
    ("A1", "NEW-BLACK-YK-LY-2001", "SZTEST"),
])
def test_query_location_inventory(api_oms_config, global_oms_client, location, sku, warehouse_code):
    response = global_oms_client.query_location_inventory(location, sku, warehouse_code)
    logging.info("库位库存查询结果: %s", response)
    assert response["code"] == 200
@pytest.mark.skip("跳过订单编辑")
@pytest.mark.parametrize("referenceNo, status", [
    # ("", "", "SZTEST"),
    # ("A1", "", ""),
    ("7365924759768403968", "新建"),
    ("5766982376683317", "分配完成"),
    ("7382355080621592576", "待拣货"),
    ("7373957959606341633", "拣货中"),
    ("20250602300122", "拣货完成"),
    ("202508260032", "包装中"),
    ("7376921606897012736", "包装完成"),
])
def test_edit_order(api_oms_config, global_oms_client, referenceNo, status):
    response = global_oms_client.edit_order(referenceNo)
    logging.info(f"订单状态为{status}，编辑订单{referenceNo}结果: %s", response)
    # assert response["code"] == 200

@pytest.mark.skip("跳过订单拦截查询")
@pytest.mark.parametrize("referenceNo, fo_code", [
    ("20251028002", "FBA2510280002-NODIT")

])
def test_query_intercept(api_oms_config, global_oms_client, referenceNo, fo_code):
    response = global_oms_client.query_intercept(referenceNo, fo_code)
    logging.info(f"查询订单{referenceNo}拦截结果: %s", response)
    assert response["code"] == 200

@pytest.mark.skip("跳过订单拦截")
@pytest.mark.parametrize("referenceNo, fo_code", [
    # ("7389841513028521984", "FBA2510310010-NODIT")
])
def test_intercept_order(api_oms_config, referenceNo, fo_code, global_oms_client):
    response = global_oms_client.intercept_order(referenceNo, fo_code)
    logging.info(f"拦截订单{fo_code}结果: %s", response)
    assert response["code"] == 200
    # 第二步：立即查询拦截结果（可根据接口响应时间增加短暂等待，如time.sleep(1)）
    query_response = global_oms_client.query_intercept(referenceNo, fo_code)
    logging.info(f"查询订单{fo_code}拦截结果: %s", query_response)
    assert query_response["code"] == 200  # 确保查询请求成功

def test_query_logistics_service_list(api_oms_config, global_oms_client):
    response = global_oms_client.query_logistics_service_list()
    logging.info("查询物流渠道派送结果: %s", response)
    assert response["code"] == 200
