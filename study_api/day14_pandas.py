import pandas as pd

# 用例信息表
cases = pd.DataFrame({
    '用例ID': ['TC001', 'TC002', 'TC003', 'TC004'],
    '模块': ['登录', '订单', '支付', '用户'],
    '优先级': ['高', '中', '高', '低'],
    '创建人': ['张三', '李四', '王五', '赵六']
})
print("用例信息表：")
print(cases)

# 执行结果表
results = pd.DataFrame({
    '用例ID': ['TC001', 'TC002', 'TC002', 'TC003', 'TC005'],
    '执行时间': ['2025-03-01', '2025-03-01', '2025-03-02', '2025-03-02', '2025-03-03'],
    '实际结果': ['通过', '失败', '通过', '通过', '失败'],
    '执行人': ['张三', '李四', '张三', '王五', '钱七']
})
print("\n执行结果表：")
print(results)

# 假设还有另一份结果表 results2
results2 = pd.DataFrame({
    '用例ID': ['TC006', 'TC007'],
    '执行时间': ['2025-03-04', '2025-03-04'],
    '实际结果': ['通过', '未执行'],
    '执行人': ['李四', '王五']
})

# 纵向合并
all_results = pd.concat([results, results2], ignore_index=True)
print("所有执行结果合并：")
print(all_results)

# 默认 inner join（只保留两边都有的键）
merged_inner = pd.merge(cases, results, on='用例ID')
print("Inner Join 结果：")
print(merged_inner)
# Left Join（左连接）：保留左表所有行，右表匹配不上就填 NaN。
merged_left = pd.merge(cases, results, on='用例ID', how='left')
print("Left Join 结果：")
print(merged_left)
# Right Join（右连接）：保留右表所有行。
merged_right = pd.merge(cases, results, on='用例ID', how='right')
print("Right Join 结果：")
print(merged_right)

# Outer Join（全连接）：保留两边所有行。
merged_outer = pd.merge(cases, results, on='用例ID', how='outer')
print("Outer Join 结果：")
print(merged_outer)

# 如果两张表的关联列名不一样，可以用 left_on 和 right_on 指定。
# 假设 results 表中的用例ID列名叫 'case_id'
results_renamed = results.rename(columns={'用例ID': 'case_id'})
merged_diff = pd.merge(cases, results_renamed, left_on='用例ID', right_on='case_id', how='left')
print(merged_diff)

# 合并后常常需要进一步处理，比如保留最新的一次执行记录：
# 对合并后的表按用例ID排序，保留最后一次执行（假设执行时间可排序）
merged = pd.merge(cases, results, on='用例ID', how='left')
merged['执行时间'] = pd.to_datetime(merged['执行时间'])
latest = merged.sort_values('执行时间').drop_duplicates(subset='用例ID', keep='last')
print("每个用例的最新执行记录：")
print(latest)

result5 = pd.concat([results, results2], ignore_index=True)
print(result5)

result_inner_join = pd.merge(cases, results, on="用例ID")
print(result_inner_join)

result_left = pd.merge(cases, results, on='用例ID', how="left")
print(result_left)

result_outer = pd.merge(cases, results, on='用例ID', how="outer")
print(result_outer)

# 找出所有执行过但不在用例信息表中的用例（提示：用 right join 或 outer join 后筛选）
# result_du = pd.merge(results, cases, on='用例ID', how="left")
result_du = pd.merge(cases, results, on='用例ID', how="right")
print(result_du)
print(result_du[result_du["创建人"].isna()][['用例ID', '执行时间', '实际结果', '执行人']])
results["实际结果"] != "未执行"

# 找出所有未执行的用例（即在用例信息表中但不在执行结果表中的用例，用 left join 筛选实际结果为空的行）
result_no = pd.merge(cases, results, on='用例ID', how="left")
filter_result = result_no[result_no["执行人"].isna()]
print(filter_result[["用例ID", "模块", "优先级", "创建人"]])

# （挑战）把合并后的表按模块统计执行次数、通过率。
result_inner1 = pd.merge(cases, results, on="用例ID", how="inner")
print(result_inner1)
def count_pass(x):
    return (x == '通过').sum()

result3 = result_inner1.groupby("模块").agg(
    执行次数=("用例ID", "count"),
    通过数=('实际结果', count_pass)
)
result3["通过率"] = result3["通过数"]/result3["执行次数"]
print(result3[["执行次数", "通过率"]])