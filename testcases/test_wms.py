import logging
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))

from wms.wms_client import WmsClient
from utils.random_number import CustomSnowflake



# 定义多个 SKU 作为测试数据
@pytest.mark.skip("先不测普通订单了")
@pytest.mark.parametrize("fo_no", [
    # ("TEST-IPING0020","JD-1DD"),
    "FO2509250003-NODIT"
    # ("Test-02-04098", "JD-1DD")
    # "NEW-BLACK-YK-LY-2001",
    # "TEST-PICK-00002",
    # "IT-TEST-202402501"
    # "TEST1-Chair-173131859177"
])
def test_create_common_order(api_wms_config, fo_no):
    wms_client = WmsClient()
    response = wms_client.upload_tracking_no_and_waybill(fo_no)
    # order_data = load_order_template("EBAY")
    # logging.info(res)
    # response = oms_client.create_common_order(order_data)
    logging.info("上传跟踪号和面单结果: %s", response)
    assert response["code"] == 200