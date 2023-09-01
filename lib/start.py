import user as u

user = u.User()

user.info = user.login(
    userName=input('请输入账号：'),
    passWord=input('请输入密码：'),
    verifyCode=user.verifyCode()
)