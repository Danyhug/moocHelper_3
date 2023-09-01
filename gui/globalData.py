"""
该文件定义全局数据
"""
import time

import captcha
import user as u
# 用户id
uid = -1

# 连线码
connCode = ''

# 全局用户信息
userInfoRes = ''

# 用户名信息
userName = ''
# 密码信息(用作重连)
userPass = ''

# 验证码
verify = captcha.Captcha()


def reLogin() -> bool:
    global userName
    global userPass
    """
    掉线重连功能
    :return:
    """
    user = u.User()
    print('调用自动重连')

    try:
        # 尝试次数为10次，防止验证码识别出错
        n = 1
        while n < 10:
            n += 1

            # 获取验证码
            verifyCode = user.getVerifyCode()
            # 识别验证码
            verCode = verify.postCaptchaGetCode(verifyCode)

            res = user.login(userName, userPass, verCode)
            if res['code'] == 1:
                return True
            time.sleep(5)
    except:
        return False
    return False


if __name__ == '__main__':
    print(reLogin())