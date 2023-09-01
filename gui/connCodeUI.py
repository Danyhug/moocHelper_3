"""
这里书写连线码的UI界面
"""
import os
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from os import startfile, path

import tool
import tool as t
try:
    import wx as wechat
    import globalData as glo
except:
    showerror('软件奔溃', '服务器连接失败，请检查网络或更新版本')


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
        self.createWidget()

    def createWidget(self):
        ttk.Style().configure(
            'TLabel',
            background='white'
        )
        ttk.Label(self, text="连线码", font='微软雅黑 24', padding=18).pack()

        # 输入内容
        self.code = StringVar()
        self.inp = ttk.Entry(self)
        self.inp.config(
            font='Arial 30 bold',
            width=8,
            textvariable=self.code,
            justify='center',
        )
        self.inp.pack()
        self.inp.bind('<KeyRelease>', self.changeCode)

        # 功能区
        btnBox = ttk.Frame(root)
        btnBox.place(x=40, y=160, width=250)
        # 创建登录按钮样式
        loginCss = ttk.Style()
        loginCss.configure(
            'login.TButton',
            #background=t.rgb((29, 197, 252)),
        )
        btn1 = ttk.Button(btnBox, text='登录软件', style='login.TButton', command=self.login)
        # 绑定回车事件
        root.bind('<Return>', self.login)
        btn1.pack(side='left')
        btn2 = ttk.Button(btnBox, text='获取帮助', command=lambda: tool.openWebSite('mooc.zzf4.top/help.html'))
        btn2.pack(side='right')

        btn3 = ttk.Button(text='控制台', command=lambda: self.openCommand())
        btn3.place(x=40, rely=0.7, y=25, width=250, height=30)

        self.isNewUser()

    # 打开控制台
    def openCommand(self):
        startfile(os.getcwd() + '/控制台.exe')

    # 查看是否为新用户
    def isNewUser(self):
        # 判断是否有answerFile文件夹
        if not os.path.exists(os.getcwd() + '/answerFile'):
            showerror('警告', '请查看软件目录下智慧职教助手使用手册')
            showerror('警告', '请使用管理员权限运行软件！如果您已完成，无视即可')

    # 输入时将输入内容改为大写
    def changeCode(self, event):
        # 显示为大写
        self.code.set(self.code.get().upper())

    # 登录
    def login(self, event=None):
        # 连线码
        code = self.code.get()
        try:
            res = wx.getUid(code)
        except:
            showerror('软件奔溃', '服务器连接失败，请检查网络或更新版本')
            return
        if res['code'] == 1:
            # 保存全局数据
            glo.uid = res['uid']
            glo.connCode = code
            # 显示提示信息
            showinfo('登录成功', res['msg'])
            # 销毁本窗口
            root.destroy()
            # 进入登录界面
            import loginUI
        elif not res:
            showerror('软件奔溃', '服务器出错！')
        else:
            # 登录失败
            showwarning('登录失败', res['msg'])


root = Tk()
root['bg'] = 'white'
root.title('智慧职教助手')
#禁止用户调整窗口大小
root.resizable(False,False)

# 窗口居中显示
root.geometry(t.positionCenter(
    '320x250',
    root.winfo_screenwidth(),
    root.winfo_screenheight()
))


app = Application(root)

fbi = wx.fbi()
if fbi:
    showerror('特别警告！！！', fbi)
    app.inp.focus_force()
else:
    print('FBI Do Not Warring')

root.mainloop()
