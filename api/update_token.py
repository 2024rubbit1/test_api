from oms_client import OmsClient

class UpdateToken:
    def __init__(self, oms_client: OmsClient):
        self.oms_client = oms_client

    def generate_base_url(self):
        """
        生成基础URL
        """
        base_urls = []
        # 循环从'h'到'z'的每个字母，生成三个相同字母的前缀（如hhh、iii、jjj...zzz）
        for char_code in range(ord('i'), ord('z') + 1):
            prefix = chr(char_code) * 3  # 生成hhh、iii、jjj等前缀
            url = f"http://{prefix}oms.test.com/"  # 拼接完整URL
            base_urls.append(url)
        return base_urls  # 返回包含所有URL的列表