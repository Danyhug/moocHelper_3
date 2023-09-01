"""
工具类
"""
import requests

class Utils:
    # 请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 12.0; COL-AL10 Build/HUAWEICOL-AL10) AppleWebKit/537.36 (KHTML, like '
                             'Gecko) Chrome/103.0.5060.53 Mobile Safari/537.36 Edg/103.0.1264.37'}

    # 会话状态保持
    session = requests.session()
