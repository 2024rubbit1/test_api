import pandas as pd

# 创建一个测试用例执行结果的 DataFrame（模拟真实场景）
df = pd.DataFrame({
    '用例ID': ['TC001', 'TC002', 'TC003', 'TC004', 'TC005', 'TC006', 'TC007'],
    '模块': ['登录', '登录', '订单', '订单', '订单', '支付', '支付'],
    '优先级': ['高', '中', '高', '中', '低', '高', '中'],
    '实际结果': ['通过', '失败', '通过', '通过', '失败', '通过', '未执行'],
    '执行人': ['张三', '李四', '张三', '王五', '李四', '张三', '王五']
})
print(df)
# print(df.groupby("模块").sum())
# 按“模块”分组，然后对每组计数（默认对非空值计数）
print(df.groupby("模块").count())
# 如果只想看“用例ID”的计数
print(df.groupby("用例ID").count())
# 更常用的方式：直接用 size() 统计每组行数
print(df.groupby("模块").size())
# 按多列分组
print(df.groupby(["模块", "用例ID"]).size())
# 映射优先级为数值
priority_map = {'高': 3, '中': 2, '低': 1}
df['优先级数值'] = df['优先级'].map(priority_map)
# 计算每个模块的平均优先级
print(df.groupby('模块')['优先级数值'].mean())
print(df.groupby('模块')['优先级数值'].std())
# 对同一列应用多个聚合函数——用 agg
# 统计每个模块的用例总数、平均优先级、优先级最大值
print(df.groupby("模块").agg({"优先级数值": ["count", "mean", "max"]}))

# 方法1：先创建一个布尔列，再分组求均值
df['是否通过'] = df['实际结果'] == '通过'
print(df)
pass_rate = df.groupby('模块')['是否通过'].mean()
print(pass_rate)

# 方法2：直接用 agg 自定义函数
def pass_rate_func(x):
    return (x == '通过').mean()

print(df.groupby('模块')['实际结果'].agg(pass_rate_func))

'''
分组后对多列用不同聚合函数
统计每个模块的用例数（用 size）和通过率（用 mean）
'''

result = df.groupby('模块').agg(
    用例数=('用例ID', 'count'),
    通过率=('是否通过', 'mean')
)
print(result)

print(df.groupby("模块").size())
print(df.groupby("模块")["用例ID"].count())
print(df.groupby("执行人")["用例ID"].count())
print(df.groupby(["模块", "优先级"])["用例ID"].count())
df["是否通过"] = df["实际结果"] == "通过"
print(df.groupby("模块")["是否通过"].mean())
# 找出通过率低于50%的模块
pass_rate = df.groupby("模块")["是否通过"].mean()

low_pass_modules = pass_rate[pass_rate < 0.5]
print(low_pass_modules)
print(df.groupby("模块").agge(
    用例总数=('用例ID', 'count'),
    通过数=('是否通过', 'count'),
    # 失败数=('')
))

# 计算每个模块的通过率
df["是否通过"] = df["实际结果"] == "通过"
print(df.groupby("模块")["是否通过"].mean())
# 找出通过率低于50 % 的模块
pass_rate = df.groupby("模块")["是否通过"].mean()
print(pass_rate[pass_rate<0.5])
# 用agg统计每个模块的用例总数、通过数、失败数、未执行数
def count_pass(x):
    return (x == '通过').sum()

def count_fail(x):
    return (x == '失败').sum()

def count_pending(x):
    return (x == '未执行').sum()

result = df.groupby('模块').agg(
    用例总数=('用例ID', 'count'),
    通过数=('实际结果', count_pass),
    失败数=('实际结果', count_fail),
    未执行数=('实际结果', count_pending)
)
print(result)
# 按模块和执行人分组统计通过数/总数
result1 = df.groupby(["模块", "执行人"]).agg(
    通过数=('实际结果', count_pass),
    总数=('用例ID', 'count'),
)
result1["通过率"] = result1["通过数"]/result1["总数"]
print(result1)

# 按模块和执行人分组，统计通过数和总数
grouped = df.groupby(['模块', '执行人'])['实际结果'].agg(['count', lambda x: (x=='通过').sum()])
grouped.columns = ['总数', '通过数']
grouped['通过率'] = grouped['通过数'] / grouped['总数']
print(grouped)