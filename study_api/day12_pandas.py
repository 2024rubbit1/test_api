import pandas as pd
import numpy as np  # numpy 用于生成空值 NaN

# 制造一份脏数据
df_dirty = pd.DataFrame({
    '用例ID': ['TC001', 'TC002', 'TC003', 'TC003', 'TC004', 'TC005'],
    '模块': ['登录', '产品', '入库', '入库', None, '结算'],
    '优先级': ['高', '中', '高', '高', '低', None],
    '执行时间': ['2024-03-01', '2024/03/02', '20240303', '2024-03-04', '2024-03-05', '2024-03-06'],
    '实际结果': ['通过', '失败', '通过', '通过', '未执行', None]
})
print("原始脏数据：")
print(df_dirty)
print(df_dirty.isna())
print(df_dirty.isna().sum())
print(df_dirty.info())
# print(df_dirty.dropna(subset=["实际结果"]))
# 删除任何包含空值的行
df_dropna = df_dirty.dropna()
print(df_dropna)

# 用特定值填充
df_fillna = df_dirty.fillna('未知')
print(df_fillna)

# 对不同列用不同值填充
df_fillna2 = df_dirty.fillna({
    '模块': '待定',
    '优先级': '低',
    '实际结果': '未执行'
})
print(df_fillna2)

# 检查重复行
print(df_dirty.duplicated())
print(df_dirty.duplicated(subset=['用例ID']))

# 删除重复行（保留第一次出现的）
df_unique = df_dirty.drop_duplicates(subset=['用例ID'])
print(df_unique)

# 先查看当前各列类型
print(df_dirty.dtypes)

# 把“执行时间”统一转换成日期类型
df_clean = df_dirty.copy()  # 先复制一份，避免修改原数据
df_clean['执行时间'] = pd.to_datetime(df_clean['执行时间'], errors='coerce')
print(df_clean.dtypes)
print(df_clean)

# 如果某列应该是数字，但被读成了字符串，用 astype 转换
# df['优先级数字'] = df['优先级'].astype('int')  # 但这里优先级是文本，不能直接转

# 把列名改成更顺眼的名字
df_renamed = df_clean.rename(columns={
    '用例ID': 'testcase_id',
    '模块': 'module',
    '优先级': 'priority',
    '执行时间': 'execute_time',
    '实际结果': 'actual_result'
})
print(df_renamed.columns)

df_reset = df_unique.reset_index(drop=True)  # drop=True 表示丢弃原来的索引
print(df_reset)

print(df_dirty.info())
print(df_dirty.isna().sum())
print(df_dirty)
df_no_duplicate = df_dirty.drop_duplicates(subset=["用例ID"])
print(df_no_duplicate)
df_filled = df_no_duplicate.fillna({"模块": "待定", "优先级": "低", "实际结果": "未执行"})
print(df_filled)
# df_filled1 = df_filled.copy()

df_test3 = df_filled.copy()

# 第一步：把斜杠替换成横杠
df_test3["执行时间"] = df_test3["执行时间"].str.replace('/', '-')

# 第二步：把纯数字格式（如20240303）转换成 YYYY-MM-DD
# 正则表达式：(\d{4})(\d{2})(\d{2}) 匹配四位数字-两位数字-两位数字，然后用 \1-\2-\3 替换
df_test3["执行时间"] = df_test3["执行时间"].str.replace(
    r'(\d{4})(\d{2})(\d{2})', r'\1-\2-\3', regex=True
)

# 现在所有格式应该都统一为 YYYY-MM-DD 了
df_test3["执行时间"] = pd.to_datetime(df_test3["执行时间"], errors="coerce")
print(df_test3)
df_renamed1 = df_test3.rename(columns={'用例ID': 'testcase_id',
    '模块': 'module',
    '优先级': 'priority',
    '执行时间': 'execute_time',
    '实际结果': 'actual_result'})
print(df_renamed1)
df_renamed2 = df_renamed1.reset_index(drop=True)
print(df_renamed2)
df_renamed2.to_csv("testcases_clean.csv", index=False, encoding='utf-8-sig')