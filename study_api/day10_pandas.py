import pandas as pd
df = pd.read_csv("my_testcases.csv")
print(df["用例ID"])
print(df.模块)
print(df[["用例ID", "模块", "优先级"]])
print(df.iloc[0])
print(df.iloc[0:3])
print(df.iloc[[0, 2, 3]])
print(df.iloc[-1])

# 按索引
print(df.loc[0])
print(df.loc[0:2])
# 如果索引是自定义的（比如用用例ID做索引），loc 的优势就出来了
# df_custom = df.set_index('用例ID')  # 把用例ID设为索引
# print(df_custom)
# print(df_custom.loc[1])       # 直接用用例ID取行
# print(df_custom.loc[1:2])
# 选择索引0到2的行，以及'模块'和'实际结果'列
print(df.loc[0:2, ["模块", "预期结果"]])
# 选择所有行，只取'模块'列
print(df.loc[:, ["模块"]])
# 选择索引为0和2的行，取所有列
print(df.loc[0:2, :])
# 选择前3行（位置0,1,2），以及第1列和第4列（位置1和4）
print(df.iloc[0:3, [0, 3]])
# 选择所有行，只取第0列和第2列
print(df.iloc[:, [0, 2]])
# 选择第2到第4行，以及第0到第2列
print(df.iloc[1:4, 0:3])

print(df.用例ID)
print(df["用例ID"])
print(df[["模块", "预期结果"]])
print(df.iloc[2])
print(df.iloc[1:4])
print(df.iloc[[0, 3]])
print(df.loc[2])
print(df.loc[1:3])
df2 = df.set_index('用例ID')
print(df2.loc[3])
print(df2.loc[2:4])
print(df2.loc[2:4, ["模块", "预期结果"]])
print(df2)
print(df.iloc[0:3, [0, 3]])

