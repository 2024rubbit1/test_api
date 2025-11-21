import logging
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))

from oms.oms_client import OmsClient
from utils.random_number import CustomSnowflake

@pytest.mark.skip("1")
def test_create_inbound(api_oms_config):
    oms_client = OmsClient()
    response = oms_client.create_inbound()
    logging.info("新增入库单: %s", response)
    # assert response["code"] == 200

@pytest.mark.skip("1")
def test_query_inbound(api_oms_config):
    oms_client = OmsClient()
    response = oms_client.query_inbound_order(["WE2510160005-NODIT", "WE2510160004-NODIT", "WE2510160003-NODIT", "WE2510160002-NODIT", "WE2510160001-NODIT"])
    logging.info("查询入库单: %s", response)