# 进入项目测试根目录
cd D:/PycharmProjects/pythonProject1/WMS/test_api

# 仅运行订单测试用例（可选，如需全量测试可省略路径）
pytest testcases/order/test_common_order.py --alluredir=allure-results
