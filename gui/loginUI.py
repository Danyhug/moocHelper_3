"""
这里书写连线码的UI界面
"""
import time
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *

import tool
import tool as t
import user as u
import globalData as glo
import conf as c
import wx as wechat

user = u.User()
conf = c.Conf()
wx = wechat.WxApp()

class Application(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        # 默认样式
        self.defaultCss = ttk.Style()
        self.defaultCss.configure(
            'TFrame',
            background='white'
        )

        # 登录次数
        self.loginCount = 0

        self.createWidget()

    def createWidget(self):
        ttk.Style().configure(
            'TLabel',
            background='white'
        )
        ttk.Label(self, text="智慧职教助手", font='微软雅黑 20', padding=14).pack()

        # 输入内容
        formBox = Frame(bg='white')
        formBox.place(x=60, y=60, width=200, height=200)
        self.username = StringVar()
        self.password = StringVar()
        self.verCodeChar = StringVar()

        self.username = ttk.Combobox(formBox)
        self.username.bind('<<ComboboxSelected>>', self.changPwd)
        self.appendData()
        # 用户名
        ttk.Label(formBox, text='账号').place(x=5, y=5)
        self.username.place(x=50, y=5, width=130)
        # 密码
        ttk.Label(formBox, text='密码').place(x=5, y=40)
        ttk.Entry(formBox, textvariable=self.password, style='form.TEntry')\
            .place(x=50, y=40, width=130)
        # 验证码
        ttk.Label(formBox, text='验证码').place(x=5, y=75)
        self.verCode = ttk.Entry(formBox, textvariable=self.verCodeChar)
        self.verCode.place(x=50, y=75, width=130)

        # 创建验证码
        self.verCodePhoto = Label(formBox)
        self.verCodePhoto.place(x=20, y=110, width=161, height=41)
        # 刷新验证码图片
        self.refreshVerify()
        # 绑定单击事件
        self.verCodePhoto.bind('<Button-1>', self.refreshVerify)

        btn1 = ttk.Button(formBox, text='登录软件', style='login.TButton', command=self.login)
        # 绑定回车事件
        root.bind('<Return>', self.login)
        btn1.place(x=30, y=170, width=130)
        self.autoChange()
        # 自动更新
        tool.thread_it(self.checkUpdate, auto=True)

    def checkUpdate(self, event=None, auto=False):
        up = wx.update()
        # 有更新的情况
        if up:
            if askokcancel('提示', '有新版本更新，是否前往官网更新？'):
                tool.openWebSite('http://mooc.zzf4.top/index.html#download')
        else:
            # 如果手动点击
            if not auto:
                showinfo('提示', '暂无版本更新')

    # 输入框添加数据
    def appendData(self):
        data = conf.readMoocUser()
        self.userData = []
        self.unames = []
        for u in data:
            # 倒序插入
            self.unames.insert(0, u['uname'])
            self.userData.insert(0, u)
        self.username['values'] = self.unames

    # 更改输入框密码
    def changPwd(self, event=None):
        self.password.set(self.userData[self.username.current()]['passwd'])
        self.verCode.focus_set()

    # 打开软件时自动更改值
    def autoChange(self):
        try:
            self.username.current(0)
            self.changPwd()
        except:
            return

    # 刷新验证码
    def refreshVerify(self, event=None):
        # 验证码数据
        try:
            self.verifyCode = user.getVerifyCode()
        except:
            print('验证码识别失败')

        # 更改图片数据
        try:
            self.verCodeImg = PhotoImage(data=self.verifyCode)
            # 识别验证码
            tool.thread_it(self.ocrVerify)
            # 更改标签中的图片
            self.verCodePhoto['image'] = self.verCodeImg
        except:
            showerror('提示', '请重新启动软件重试，如果还有此提示，请检查能否登录智慧职教，您可能已被智慧职教防火墙屏蔽！')

    # 识别验证码
    def ocrVerify(self):
        try:
            if glo.verify.loginState:
                code = glo.verify.postCaptchaGetCode(self.verifyCode)
                if code != '':
                    self.verCodeChar.set(code)
                print('验证码为', code)
        except:
            print('loginUI 验证码模块有误')
            return

    def login(self, event=None):
        # 获取用户名密码以及验证码
        username = self.username.get()
        passwd = self.password.get()
        verCode = self.verCode.get()
        try:
            res = user.login(username, passwd, verCode)
        except:
            showwarning('提示', '智慧职教平台连接出错，请等待一段时间或切换网络')
            return

        if res['code'] == 1:
            # 登录成功,保存数据
            glo.userInfoRes = res
            # 保存用户名
            glo.userName = username
            # 保存密码
            glo.userPass = passwd

            # 保存到配置文件中
            if not username in self.unames:
                conf.writeMoocUser({
                    'uname': username,
                    'passwd': passwd
                })
            else:
                print('账号信息已存在')
                # 如果密码和已保存密码不一样，再保存一次
                if self.password.get() != self.userData[self.username.current()]['passwd']:
                    conf.writeMoocUser({
                        'uname': username,
                        'passwd': passwd
                    })
            # 提示信息
            showinfo('提示', '登录成功！')
            # 销毁本窗口
            root.destroy()
            # 打开主窗口
            import mainUI
        else:
            # 登录失败, 提示信息
            self.loginCount += 1
            if self.loginCount == 3:
                showwarning('温馨提示', '请输入智慧职教的账号密码，非本软件！')
            else:
                showwarning('登录失败', res['msg'])
                # 刷新验证码图片
                self.refreshVerify()

root = Tk()
root['bg'] = 'white'
root.title('智慧职教助手')
# 窗口居中显示
root.geometry(t.positionCenter(
    '320x276',
    root.winfo_screenwidth(),
    root.winfo_screenheight()
))
#禁止用户调整窗口大小
root.resizable(False,False)

# showwarning('提示', '请输入智慧职教的账号密码，非本软件！')
app = Application(root)

root.mainloop()
