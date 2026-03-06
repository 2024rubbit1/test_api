import requests
url = "https://httpbin.org/status/404"
try:
    r = requests.get(url)
    r.raise_for_status()  # 这行是关键！如果状态码不是 200，会抛出 HTTPError
except requests.exceptions.HTTPError:
    print(f"捕获到 HTTPError，状态码是：{r.status_code}")
except requests.exceptions.RequestException as e:
    # 处理其他所有 requests 可能抛出的异常（如连接错误、超时等）
    print(f"捕获到 RequestException：{e}")