import pandas as pd

data1 = {"用例ID": [1, 2, 3, 4,5], "模块": ["登录", "产品", "入库", "出库", "结算"], "优先级":[1, 2, 3, 4, 4], "预期结果":
    ["登录成功", "新增产品成功", "新增入库单成功", "新建出库单成功", "结算无误"]}
df1 = pd.DataFrame(data1)
data2 = [
    {"用例ID": 1, "模块": "登录", "优先级": 1, "预期结果": "登录成功"},
    {"用例ID": 2, "模块": "产品", "优先级": 2, "预期结果": "新增产品成功"},
    {"用例ID": 3, "模块": "入库", "优先级": 3, "预期结果": "新增入库成功"},
    {"用例ID": 4, "模块": "出库", "优先级": 4, "预期结果": "新增出库成功"},
    {"用例ID": 5, "模块": "结算", "优先级": 4, "预期结果": "结算无误"}

]
df2 = pd.DataFrame(data2)
print(df1)
print(df2)
print(df1.head(3))
print(df1.info())
print(df1.shape)
df1.to_csv("my_testcases.csv", index=False, encoding='utf-8-sig')
cs = pd.read_csv("my_testcases.csv")
print(cs.head(3))