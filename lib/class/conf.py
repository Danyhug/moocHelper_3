"""
配置文件
Coding By Danyhug 2022-1-27 13:53:05
"""
import os
from configobj import ConfigObj
from functools import wraps


class Conf:
    # 默认配置
    moocDefaultConf = {
        'doAllWorkAutoGetAnswer': True,  # 全部完成功能自动获取答案
    }

    zjyDefaultConf = {
        'zjyAddActivity': False,         # 职教云评论
        'zjyAddActivityContent': '好',  # 职教云评论内容
    }

    def __init__(self):
        # 创建conf目录
        try:
            os.mkdir('conf')
        except FileExistsError:
            print('配置文件夹已存在')

        # 当前目录
        self.path = os.getcwd() + '/conf/'
        # 默认目录
        self.defaultPath = os.getcwd()
        # 读取配置目录文件
        self.conf = ConfigObj(self.path + 'conf.ini', encoding='utf8')

        # 职教云所有配置
        self.zjyConf = dict()
        # 智慧职教所有配置
        self.moocConf = dict()

    # 回到默认目录
    @staticmethod
    def goDefaultPath(func) -> any:
        @wraps(func)
        # 目录切换
        def change(self, *args, **kwargs):
            os.chdir(self.path)
            r = func(self, *args, **kwargs)
            os.chdir(self.defaultPath)
            return r

        return change

    # 读取智慧职教账号密码
    @goDefaultPath
    def readMoocUser(self) -> list:
        moocUsers = []
        try:
            with open('moocUser', 'r') as f:
                # 每次读取一行文本
                for line in f.readlines():
                    if not line:
                        return []

                    # 以空格为分隔符，分隔成两个
                    user = line.split(' ', 1)
                    # print('line', user)
                    moocUsers.append(
                        {
                            'uname': user[0],
                            'passwd': user[1][:-1]
                        }
                    )
                    # print('moocUsers', moocUsers)
        except FileNotFoundError:
            self.writeMoocUser(method=0)
        except IndexError:
            if os.path.exists('moocUser'):
                # 清空文件
                os.remove('moocUser')
                self.writeMoocUser(method=0)
            return []

        return moocUsers

    # 写入智慧职教账号密码
    # method 为方法，1为默认，0为创建文件
    @goDefaultPath
    def writeMoocUser(self, user: dict = None, method: int = 1):
        with open('moocUser', 'a+') as f:
            if not method:
                # 创建文件，你的任务完成了，直接退出
                return

            # 将账号密码换行符去掉
            uname = user['uname'].replace('\n', '')
            passwd = user['passwd'].replace('\n', '')

            f.write(uname + ' ' + passwd + '\n')
            print(uname + ' ' + passwd)
            print('账号信息写入成功', uname + ' ' + passwd)

    # 初始化配置参数
    @goDefaultPath
    def initConf(self):
        # 查看程序是否存在
        if os.path.exists('conf.ini'):
            # 读取配置
            # 检查配置文件
            self.readConf()
            self.checkConf()
        else:
            # 写入默认配置文件
            self.writeConf(
                section='mooc',
                **self.moocDefaultConf
            )
            self.writeConf(
                section='zjy',
                **self.zjyDefaultConf
            )

    # 读取职教云配置文件
    @goDefaultPath
    def readConf(self):
        # 读取配置
        try:
            self.zjyConf = self.conf['zjy']
        except KeyError:
            self.writeConf(
                section='mooc',
                **self.zjyDefaultConf
            )
            self.zjyConf = self.conf['zjy']

        # =================================
        try:
            self.moocConf = self.conf['mooc']
        except KeyError:
            self.writeConf(
                section='mooc',
                **self.moocDefaultConf
            )
            self.moocConf = self.conf['mooc']

    # 写入配置文件
    @goDefaultPath
    def writeConf(self, section, **kwargs):
        # 传入section和相关的k v
        self.conf[section] = dict()
        for option, value in kwargs.items():
            self.conf[section][option] = str(value)
        # 写入
        self.conf.write()

    # 检查默认文件和配置文件的项是否一致
    @goDefaultPath
    def checkConf(self):
        # 是否需要覆盖
        needCover = False

        # 从默认文件中遍历keys
        for k in self.moocDefaultConf.keys():
            # 如果配置文件中没有该项
            if k not in self.moocConf.keys():
                needCover = True
                # 将该项添加到文件中
                self.moocConf[k] = self.moocDefaultConf[k]

        for k in self.zjyDefaultConf.keys():
            # 如果配置文件中没有该项
            if k not in self.zjyConf.keys():
                needCover = True
                self.zjyConf[k] = self.zjyDefaultConf[k]

        if needCover:
            print('已覆盖配置文件')
            self.writeConf(section='mooc', **self.moocConf)
            self.writeConf(section='zjy', **self.zjyConf)
