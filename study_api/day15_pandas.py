import pandas as pd
'''
# 1. 用例信息表
cases = pd.DataFrame({
    '用例ID': ['TC001', 'TC002', 'TC003', 'TC004', 'TC005', 'TC006'],
    '模块': ['登录', '登录', '订单', '订单', '支付', '用户中心'],
    '优先级': ['高', '中', '高', '低', '中', '低'],
    '创建人': ['张三', '李四', '王五', '赵六', '张三', '李四'],
    '创建日期': ['2025-02-01', '2025-02-01', '2025-02-02', '2025-02-02', '2025-02-03', '2025-02-03']
})
cases.to_csv('cases.csv', index=False, encoding='utf-8-sig')

# 2. 执行记录表（每个用例可能有多条执行记录）
executions = pd.DataFrame({
    '执行ID': [1, 2, 3, 4, 5, 6, 7, 8],
    '用例ID': ['TC001', 'TC001', 'TC002', 'TC003', 'TC003', 'TC004', 'TC005', 'TC007'],
    '执行时间': ['2025-03-01 10:00', '2025-03-02 09:30', '2025-03-01 11:20', '2025-03-01 14:00',
                '2025-03-03 16:30', '2025-03-02 08:45', '2025-03-03 09:15', '2025-03-03 10:00'],
    '执行结果': ['通过', '失败', '通过', '通过', '失败', '通过', '未执行', '通过'],
    '执行人': ['张三', '李四', '王五', '张三', '李四', '赵六', '王五', '钱七']
})
executions.to_csv('executions.csv', index=False, encoding='utf-8-sig')

# 3. 缺陷表（关联到用例，有些缺陷可能有多个关联用例，这里简化）
bugs = pd.DataFrame({
    '缺陷ID': ['BUG001', 'BUG002', 'BUG003'],
    '关联用例': ['TC001', 'TC003', 'TC005'],  # 假设每个缺陷只关联一个用例
    '缺陷等级': ['严重', '一般', '轻微'],
    '发现时间': ['2025-03-02 09:35', '2025-03-03 16:45', '2025-03-03 09:20'],
    '状态': ['已修复', '打开', '打开']
})
bugs.to_csv('bugs.csv', index=False, encoding='utf-8-sig')

print("数据文件已生成。")


# 任务1：数据读取与初步探索
# 读取三个 CSV 文件，分别命名为 df_cases、df_exec、df_bugs。
#
# 查看每个 DataFrame 的前几行、基本信息（info()）、形状，确保数据正确。
#
# 检查各表有无空值（特别是关联键列）。
df_cases = pd.read_csv("cases.csv")
df_exec = pd.read_csv("executions.csv")
df_bugs = pd.read_csv("bugs.csv")
print(df_cases.head())
print(df_cases.info())
print(df_cases.shape)
print(df_exec.head())
print(df_exec.info())
print(df_exec.shape)
print(df_bugs.head())
print(df_bugs.info())
print(df_bugs.shape)
print(df_cases.isna().sum())
print(df_exec.isna().sum())
print(df_bugs.isna().sum())

任务2：清洗执行记录表
df_exec 中的“执行时间”是字符串，请转换成日期时间类型（pd.to_datetime）。

检查“执行结果”列有无非法值（比如应该只有“通过/失败/未执行”），如有则处理（例如填“未知”或删除）。

删除完全重复的行（如果有）。
'''
df_cases = pd.read_csv("cases.csv")
df_exec = pd.read_csv("executions.csv")
df_bugs = pd.read_csv("bugs.csv")
df_exec_clean = df_exec.copy()
# 2.1 转换执行时间为日期时间类型
df_exec_clean["执行时间"] = pd.to_datetime(df_exec_clean["执行时间"])
# 2.2 检查并处理“执行结果”列的非法值
print("清洗前执行结果唯一值：", df_exec_clean["执行结果"].unique())

df_exec_clean["执行结果"] = df_exec_clean["执行结果"].fillna("未知")
df_exec_clean.drop_duplicates(inplace=True)
print(df_exec_clean)

# 定义合法值集合
valid_results = {"通过", "失败", "未执行"}

# 找出非法值（不在合法集合中的值）
invalid_mask = ~df_exec_clean["执行结果"].isin(valid_results)
if invalid_mask.any():
    print("发现非法值：", df_exec_clean.loc[invalid_mask, "执行结果"].unique())
    # 将非法值替换为“未知”（或根据情况删除）
    df_exec_clean.loc[invalid_mask, "执行结果"] = "未知"

# 2.3 删除完全重复的行
df_exec_clean.drop_duplicates(inplace=True)

print("清洗后执行结果唯一值：", df_exec_clean["执行结果"].unique())
print("清洗后数据形状：", df_exec_clean.shape)
'''
任务3：关联用例与执行记录
用 left join 将 df_cases 和 df_exec 合并，保留所有用例信息，执行记录匹配不上则留空。结果命名为 df_merged。

观察合并后的表，哪些用例没有执行记录？哪些执行记录没有对应用例？
'''
df_merged = pd.merge(df_cases, df_exec, on="用例ID", how="left")
print(df_merged)
# 找出没有执行记录的用例
no_execution = df_merged[df_merged['执行ID'].isna()]
print(no_execution[['用例ID', '模块', '优先级']])  # 只看需要的列

# 方法1：right join（以执行记录表为主）
right_merged = pd.merge(df_cases, df_exec, on='用例ID', how='right')
orphan_exec = right_merged[right_merged['模块'].isna()]  # 左表字段为空的行
print(orphan_exec[['用例ID', '执行时间', '执行结果', '执行人']])
'''
任务4：关联缺陷信息
将 df_bugs 合并到 df_merged 中，关联键为用例ID（注意：df_bugs 中的关联用例列名可能不同，请先统一）。

因为一个用例可能对应多个缺陷（但本例中每个缺陷只关联一个用例，所以是一对一），选择合适的连接方式（建议 left join 以保留所有用例执行记录）。

合并后，检查没有缺陷的用例对应字段是否为空。
'''

df_bugs_renamed = df_bugs.rename(columns={"关联用例": "用例ID"})
print(df_bugs_renamed)
left_merge = pd.merge(df_merged, df_bugs_renamed, on="用例ID", how="left")
print(left_merge)
print(left_merge[left_merge["缺陷ID"].isna()])
'''
任务5：筛选与分析
找出所有至少执行过一次的用例（即 df_merged 中“执行ID”非空的行）。

找出所有未执行的用例（即“执行ID”为空的行）。

找出所有失败的执行记录，并关联显示用例模块、优先级、执行人等信息。

找出所有关联了缺陷的执行记录（即“缺陷ID”非空的行），并列出用例ID、缺陷等级、执行结果。
'''
print(df_merged[~df_merged["执行ID"].isna()])
print(df_merged[df_merged["执行ID"].isna()])
df_fail = df_merged["执行结果"] == "失败"
print(df_merged[df_fail])
bug_exe = pd.merge(df_exec, df_bugs_renamed, on="用例ID", how="left")
bug_exe_no_null = bug_exe[~bug_exe["缺陷ID"].isna()]
print(bug_exe_no_null[["用例ID", "缺陷等级", "执行结果"]])

# left_merge_value = left_merge[~left_merge["缺陷ID"].isna()]
# print(f"left_merge_value is {left_merge_value}")
'''
任务6：分组统计
按模块统计：用例总数、执行次数、通过次数、失败次数、缺陷数。

通过次数：执行结果 == '通过' 的计数。

失败次数：执行结果 == '失败' 的计数。

缺陷数：缺陷ID 的非空计数（注意一个用例可能有多个缺陷，这里先简单计数）。

计算每个模块的通过率（通过次数/执行次数）和缺陷密度（缺陷数/用例总数）。

按优先级统计：用例分布、执行情况。
'''
by_moudle = left_merge.copy()
def exe_pass(x):
    return (x=="通过").sum()
def exe_fail(x):
    return (x=="失败").sum()
by_moudle = by_moudle.groupby("模块").agg(
    用例总数=("用例ID", "nunique"),
    执行次数=("执行结果", "count"),
    通过次数=("执行结果", exe_pass),
    失败次数=("执行结果", exe_fail),
    缺陷数=("缺陷ID", "count")
)
by_moudle["通过率"] = by_moudle["通过次数"]/by_moudle["执行次数"]
by_moudle["缺陷密度"] = by_moudle["缺陷数"]/by_moudle["用例总数"]
print(by_moudle)
by_priority = left_merge.copy()
by_priority = by_priority.groupby("优先级").agg(
    用例总数=("用例ID", "nunique"),
    执行次数=("执行结果", "count"),
    通过次数=("执行结果", exe_pass),
    失败次数=("执行结果", exe_fail),
    缺陷数=("缺陷ID", "count")
)
'''
任务7：生成分析报告
将上述统计结果整理成一个简洁的 DataFrame 或几个关键表格，并输出为 Excel 文件（包含多个 sheet），例如：

Sheet1：模块质量概览（模块、用例数、执行次数、通过率、缺陷数、缺陷密度）

Sheet2：未执行用例列表

Sheet3：失败用例详情（含关联缺陷）

Sheet4：缺陷列表（含关联用例信息）

可以使用 pd.ExcelWriter 将多个 DataFrame 写入同一个 Excel 文件的不同 sheet。

提示与注意事项
合并时注意键的列名是否一致，必要时用 rename 或 left_on/right_on。

计数时注意空值的处理，可以用 count() 或 sum() 结合条件。

分组聚合时，可以先用 groupby 再 agg，也可以使用 pivot_table。

如果某个用例有多条执行记录，统计“用例总数”时要去重（用 nunique 或先取唯一值）。
'''
# 1. 未执行用例列表（在 left_merge 中筛选执行ID为空的行）
no_execution = left_merge[left_merge["执行ID"].isna()][["用例ID", "模块", "优先级", "创建人"]].drop_duplicates()
# 2. 失败用例详情（执行结果为失败的记录，关联缺陷信息）
failed_cases = left_merge[left_merge["执行结果"] == "失败"][
    ["用例ID", "模块", "执行时间", "执行人", "缺陷ID", "缺陷等级", "状态"]
]
# 3. 缺陷列表（所有缺陷，关联用例信息）
bugs_list = left_merge[left_merge["缺陷ID"].notna()][
    ["缺陷ID", "用例ID", "模块", "缺陷等级", "发现时间", "状态"]
].drop_duplicates()  # 缺陷ID应该唯一，但以防万一
# 4. 使用 ExcelWriter 输出到多个 sheet
with pd.ExcelWriter("测试分析报告.xlsx") as writer:
    by_moudle.to_excel(writer, sheet_name="模块质量概览")
    by_priority.to_excel(writer, sheet_name="优先级分布")
    no_execution.to_excel(writer, sheet_name="未执行用例", index=False)
    failed_cases.to_excel(writer, sheet_name="失败用例详情", index=False)
    bugs_list.to_excel(writer, sheet_name="缺陷列表", index=False)

print("报告已生成：测试分析报告.xlsx")