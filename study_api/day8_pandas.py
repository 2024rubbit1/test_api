import pandas as pd

# 创建一个测试用例表
df1 = pd.DataFrame({
    '用例ID': ['TC001', 'TC002', 'TC003'],
    '模块': ['登录', '订单', '支付'],
    '优先级': ['高', '中', '高'],
    '预期结果': ['登录成功', '创建订单成功', '支付成功']
})
print(df1)

# 适合从 API 返回的 JSON 数据转换
data = [
    {'用例ID': 'TC001', '模块': '登录', '优先级': '高', '预期结果': '登录成功'},
    {'用例ID': 'TC002', '模块': '订单', '优先级': '中', '预期结果': '创建订单成功'},
    {'用例ID': 'TC003', '模块': '支付', '优先级': '高', '预期结果': '支付成功'}
]
df2 = pd.DataFrame(data)
print(df2)

print(df1.head())
print(df1.tail(1))
print(df1.info())
print(df1.shape)
print(df1.columns.tolist())
print(df1.index)
print(df1.describe())
# 保存到当前目录，不包含行索引
df1.to_csv('testcases.csv', index=False, encoding='utf-8-sig')
# 参数说明：
# index=False 表示不把行索引写入文件
# encoding='utf-8-sig' 保证中文在 Excel 中打开不乱码
df_read = pd.read_csv('testcases.csv')
print(df_read.head())
