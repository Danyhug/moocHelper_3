"""
captcha类
这里定义有关验证码的一切
Created by Danyhug on 2022-5-9 09:56:27
"""
import requests


class Captcha:
    # ******URL******
    # 获取验证码状态
    URL_GET_STATE = 'https://baidu.com'
    # 提交验证码图片
    URL_POST_CAPTCHA_GET_CODE = 'https://baidu.com'

    def __init__(self):
        self.loginState = None
        self.joinCourse = None

        # 更新内部状态
        self.queryNeedUse()

    def queryNeedUse(self):
        """
        查询是否需要使用服务器的验证码功能
        :return:
        """
        # res = requests.get(self.URL_GET_STATE).json()

        # {'login': True, 'joinCourse': True}
        self.loginState = True
        self.joinCourse = True

    def postCaptchaGetCode(self, imgData: bytes) -> str:
        """
        提交验证码图片获取验证码
        :param imgData: 图片数据
        :return:
        """

        return ''
