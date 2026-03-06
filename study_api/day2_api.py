import requests
import os
from dotenv import load_dotenv
load_dotenv("../configs/oms/test.env")
url = "http://omst200.newouda.com/prod-api/oms/v1/inventory/order/detail"
inventory_order_code = "GD260227 0001"
params = {"inventoryOrderCode": inventory_order_code}
headers = {"Authorization": os.getenv("Authorization")}
r = requests.get(url, params=params, headers=headers)
print("请求的完整URL：", r.url)
print("服务器返回的请求参数：", r.json())
print(r.json())
# GD2602270001-NODIT