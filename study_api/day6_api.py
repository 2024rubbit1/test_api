import requests
from requests.exceptions import RequestException, Timeout, HTTPError

def get_user_posts(user_id, timeout=5):
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"user_id": user_id}
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        titles = [item["title"] for item in data]
        return titles
    except Timeout:
        print(f"请求超时（{timeout}秒）")
        return []
    except HTTPError as e:
        print(f"HTTP错误：{e}，状态码：{r.status_code}")
        return []
    except RequestException as er:
        print(er)
        return []
    except requests.exceptions.ConnectionError as ec:
        print(ec)
        return []


# 测试代码
if __name__ == "__main__":
    # 测试1：正常获取用户1的文章
    print("测试用户1：")
    titles = get_user_posts(1)
    print(f"找到 {len(titles)} 篇文章")
    for i, title in enumerate(titles[:3]):  # 只打印前3个
        print(f"  {i + 1}. {title}")

    # 测试2：超时测试（用极短的时间）
    print("\n测试超时：")
    titles = get_user_posts(1, timeout=0.001)
    print(f"返回 {len(titles)} 篇文章")