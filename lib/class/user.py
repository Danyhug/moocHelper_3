"""
User类
这里定义有关用户的一切
Created by Danyhug on 2021-01-30 20:55
Coding by Danyhug on 2021-02-01 09:00
"""
import time
import utils


class User(utils.Utils):
    # ******URL******
    # 登录验证码
    URL_LOGIN_VERIFY = 'https://mooc-old.icve.com.cn/portal/LoginMooc/getVerifyCode'
    # 登录
    URL_LOGIN = 'https://mooc-old.icve.com.cn/portal/LoginMooc/loginSystem'
    # URL检查登录状态
    URL_CHECK_LOGIN = 'https://mooc-old.icve.com.cn/portal/LoginMooc/getUserInfo'

    def getVerifyCode(self) -> bytes:
        # 验证码图片数据
        codeContent = super().session.get(
            f'{self.URL_LOGIN_VERIFY}?ts={round(time.time() * 1000)}',
            headers=super().headers).content
        return codeContent

    def checkLogin(self) -> bool:
        res = super().session.get(
            url=self.URL_CHECK_LOGIN
        ).json()
        if res['code'] == 1:
            return True
        # 需要重连
        return False

    def login(self, userName: str, passWord: str, verifyCode: str) -> dict:
        """
        智慧职教登录
        参数:
            userName, 用户名, str
            passWord, 密码, str
            verifyCode, 验证码, str
        :return: 用户信息字典
        """
        data = {
            'userName': userName,
            'password': passWord,
            'verifycode': verifyCode
        }
        res = super().session.post(self.URL_LOGIN, data=data, headers=super().headers).json()

        return res