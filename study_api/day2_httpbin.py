import requests

# 字典方式
params_dict = {"keyword": "hello world"}
r_dict = requests.get("https://httpbin.org/get", params=params_dict)
print(r_dict.url)  # 空格会被编码成 + 或 %20

# 手动拼接字符串
params_str = "keyword=hello world"
r_str = requests.get("https://httpbin.org/get", params=params_str)
print(r_str.url)  # 空格保留原样，可能不符合URL规范