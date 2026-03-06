import pandas as pd
print(pd.__version__)
# 从列表创建（默认索引 0,1,2）
s1 = pd.Series([1, 2, 3])
print(s1)
# 指定索引
s2 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
print(s2)

# 从字典创建，键变成索引
s3 = pd.Series({"语文": 90, "数学": 95, "英语": 80})
print(s3)

# 通过位置访问（类似列表）
print(s1[0])
print(s2[2])
print(s2.iloc[2])

# 通过索引访问
print(s2['a'])
print(s2.loc["a"]) # 推荐用 loc 访问标签

# 切片
print(s2[0:2])
print(s2['a': 'c']) # 标签切片（包含两端）

print(s2.values)
print(s2.index)
print(s2.size)

s4 = pd.Series([1, 2, 3, 4])
print(s4 * 2)
print(s4 + 5)
print(s4 > 2)

s5 = pd.Series([2, 3, 4, 5])
s6 = pd.Series([2, 3, 4, 5], index=["星期一", "星期二", "星期三", "星期四"])
s7 = pd.Series({"第一天最低气温": 8, "第二天最低气温": 7, "第三天最低气温": 9})
print(s5.iloc[1])
print(s6.loc["星期二"])
print(s5.values)
print(s7.size)
print(s6.index)
print(s7 * 1.8 + 32)

s8 = pd.Series([120, 60, 30, 60, 60, 60, 30], index=['周一', '周二', '周三', '周四', '周五', '周六', '周日'])
print(s8.loc['周三'])
print(s8.iloc[5:7])
print(s8.mean())
print(s8.max())
print(s8.idxmax())
print(s8[s8 > 60])

s9 = pd.Series(["pass", "fail", "pass"], index=["testcase1", "testcase2", "testcase3"])
print((s9 == "pass").sum()/len(s9))
# print(s9[s9 == "pass"].sum()/len(s9))
# print(s9[s9 == "fail"])
print(s9[s9 == "fail"].index.tolist())