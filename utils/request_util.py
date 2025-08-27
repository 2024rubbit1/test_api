# utils/request_util.py
import requests


class RequestUtil:
    def __init__(self, base_url=None, session=None):
        self.session = session if session else requests.Session()  # 允许外部传入 session
        self.base_url = base_url

    def get(self, url, params=None, headers=None, **kwargs):
        return self._request("GET", url, params=params, headers=headers, **kwargs)

    def post_data(self, url, data=None, json=None, headers=None, **kwargs):
        return self._request("POST", url, data=data, json=json, headers=headers, **kwargs)

    def post_json(self, url, data=None, json=None, headers=None, **kwargs):
        return self._request("POST", url, data=data, json=json, headers=headers, **kwargs)

    def _request(self, method, url, **kwargs):
        # 统一处理 URL、请求头、超时、日志等
        full_url = f"{self.base_url}{url}" if self.base_url else url
        headers = kwargs.pop("headers", {})

        # 默认超时时间（避免请求卡死）
        kwargs.setdefault("timeout", 10)

        # 发送请求
        response = self.session.request(method, full_url, headers=headers, **kwargs)

        # 记录日志（可选）
        self._log_request(response, method, full_url)
        return response

    def _log_request(self, response, method, url):
        print(f"[{method}] {url} -> Status: {response.status_code}")