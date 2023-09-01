"""
这里书写总体框架
"""
import tkinter.messagebox
from datetime import datetime
from tkinter import *
from tkinter import ttk
import time
import logging
import json
from tkinter.messagebox import *

import tool as tool
import wx as wechat
import file as f
import os
import globalData as glo
import conf as c

import zjy as z
import mooc as m
import wk
import zyk

zjy = z.Zjy()
wx = wechat.WxApp()
wk = wk.Wk()
zyk = zyk.Zyk()
file = f.File()
mooc = m.Mooc()
resPath = os.getcwd()
conf = c.Conf()
conf.initConf()

# logging.basicConfig(
#     filename='log/running.log',
#     format='%(asctime)s - %(levelname)s - %(funcName)s|%(lineno)d -> %(message)s',
#     datefmt='%Y-%d-%m %H:%M:%S',
#     level=logging.INFO
# )
class TabPages(ttk.Notebook):
    """
    主体标签页
    """
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        ttk.Style().configure(
            'TNotebook',
            background=tool.rgb((245, 245, 245))
        )
        self.place(x=10, y=10, width=560, height=540)

        # 创建智慧职教窗体
        self.createMoocWidget()
        # 创建职教云窗体
        self.createZjyWidget()
        # 创建资源库窗体
        self.createZykWidget()

        # 默认选中智慧职教
        self.select(self.mooc)

        # 是否为空课程（是否需要守护程序）
        self.emptyCourse = False

        # 智慧职教是否已守护线程
        self.isDaemon = False

        # 已完成扣费的课程
        self.paidCourse = list()

        # 职教云已完成扣费的课程
        self.paidZjyCourse = list()


    def createMoocWidget(self):
        self.mooc = Frame(self, bg=tool.rgb((250, 250, 250)))
        self.add(self.mooc, text='智慧职教')

        # 左上角选择课程
        selectCourse = Frame(self.mooc, bg='white')
        selectCourse.place(x=10, y=10, width=150, height=160)

        Label(selectCourse, text='选择你的课程', bg='white').pack(pady=14)
        ttk.Style().configure(
            'TCombobox',
            background='green',
            width=10
        )
        self.moocCourse = ttk.Combobox(selectCourse, state='readonly')
        self.moocCourse.place(y=40, x=15, width=120)
        # 获取课程列表
        tool.thread_it(self.moocGetCourse)

        # 开始按钮
        start = ttk.Button(selectCourse, text='冲冲冲', command=self.moocSelectCourse)
        start.pack(pady=40)

        # 功能区
        funcBox = Frame(self.mooc, bg='white')
        funcBox.place(x=10, y=180, width=150, height=138)

        # 各个选项
        ttk.Style().configure(
            'TRadiobutton',
            background='white'
        )
        self.doWorkWhat = IntVar()  # 完成什么模块 0 全部 1 课件 2 答题
        ttk.Radiobutton(funcBox, text='全部完成', variable=self.doWorkWhat, value=0).grid(row=0, column=1, pady=8)
        ttk.Radiobutton(funcBox, text='获取答案', variable=self.doWorkWhat, value=1).grid(row=0, column=2, pady=8)
        ttk.Radiobutton(funcBox, text='完成课件', variable=self.doWorkWhat, value=2).grid(row=1, column=1)
        ttk.Radiobutton(funcBox, text='完成答题', variable=self.doWorkWhat, value=3).grid(row=1, column=2)

        # 需要过滤什么模块 作业 测验 考试
        ttk.Style().configure(
            'TCheckbutton',
            background='white'
        )
        self.skipWork = IntVar()
        self.skipTest = IntVar()
        self.skipExam = IntVar()
        ttk.Checkbutton(funcBox, text='跳过作业', variable=self.skipWork).grid(row=2, column=1, pady=8)
        ttk.Checkbutton(funcBox, text='跳过测验', variable=self.skipTest).grid(row=2, column=2)
        ttk.Checkbutton(funcBox, text='跳过考试', variable=self.skipExam).grid(row=3, column=1, columnspan=2)

        # 模块列表区
        self.moocMainBox = ttk.Treeview(self.mooc, show='headings')
        self.moocMainBox['columns'] = ('序号', '章节', '类型', '状态')
        self.moocMainBox.column("序号", width=40, anchor="center")  # #设置列
        self.moocMainBox.column("章节", width=202, anchor="center")
        self.moocMainBox.column("类型", width=60, anchor="center")
        self.moocMainBox.column("状态", width=60, anchor="center")
        self.moocMainBox.heading("序号", text="序号")  # #设置显示的表头名
        self.moocMainBox.heading("章节", text="章节")
        self.moocMainBox.heading("类型", text="类型")
        self.moocMainBox.heading("状态", text="状态")
        self.moocMainBox.place(x=180, y=10, width=364, height=270)

        # 进度条
        self.moocProgressBar = ttk.Progressbar(self.mooc)
        self.moocProgressBar.place(x=180, y=296, width=364, height=20)
        self.moocProgress = Label(self.mooc, text='0%', fg=tool.rgb((4,191,191)), bg=tool.rgb((250,250,250)), font=('微软雅黑', 12, 'bold'))
        self.moocProgress.place(x=350, y=296, height=20)

        # 运行日志区
        self.runLogBox = Text(self.mooc, bg='white')
        self.runLogBox.place(x=10, y=335, width=250, height=170)

        # 任务执行日志
        self.moocWorkLogBox = Text(self.mooc, bg='white')
        # self.moocWorkLogBox.place(x=275, y=335, width=270, height=170)
        self.moocWorkLogBox.place(x=10, y=335, width=535, height=170)
        mooc.setMoocBox(self)
        file.setMoocBox(self)

        # 守护程序启动！
        tool.thread_it(self.daemon)

    # 获取课程列表
    def moocGetCourse(self):
        # 课程的列表，包含所有信息
        self.moocCourseList = mooc.getLessoning()

        # 如果课程列表为空
        if not self.moocCourseList:
            # 表示该用户无课程，无须守护
            self.emptyCourse = True

        self.moocCourseNames = []
        for item in self.moocCourseList:
            # 将课程名从里面选出来 格式为 老师名 + 课程名
            self.moocCourseNames.append(item['courseName'])
        print(self.moocCourseNames)
        try:
            self.moocCourse['values'] = self.moocCourseNames
        except RuntimeError:
            self.moocCourse['values'] = self.moocCourseNames

    # 守护程序
    def daemon(self):
        while(True):
            # 三秒一执行
            time.sleep(3)

            # 该用户无课程
            try:
                if self.emptyCourse:
                    return
            except AttributeError:
                try:
                    if not self.isDaemon:
                        self.isDaemon = True
                        # 守护程序启动！
                        tool.thread_it(self.daemon)
                except:
                    self.isDaemon = True
                    # 守护程序启动！
                    tool.thread_it(self.daemon)

            try:
                # 如果是空的
                if not self.moocCourse['values']:
                    self.moocGetCourse()
                    self.moocWorkLog('守护程序已启动')
                    print('守护程序已启动')
                else:
                    # 退出死循环
                    break
            except:
                print('守护程序出错')
                continue

    # 选择课程
    def moocSelectCourse(self):
        self.master.title('智慧职教助手')

        # 获取当前选中课程的索引值
        try:
            index = self.moocCourseNames.index(self.moocCourse.get())
        except ValueError:
            showerror('警告', '选择课程不能为空')
            return

        # 判断需要的积分
        paint = '0'
        # 判断当前功能
        func = ''

        # 判断当前选择功能
        if self.doWorkWhat.get() == 0:
            # 全部完成
            paint = '50'
        elif self.doWorkWhat.get() == 2:
            # 完成课件
            paint = '30'
        elif self.doWorkWhat.get() == 3:
            # 开始答题
            paint = '30'
            func = 'doWork'

        # 是否为已付费课程
        isPaid = False
        for course in self.paidCourse:
            # 如果当前选中的课程是已付费的课程
            if course == self.moocCourseList[index]['courseName']:
                isPaid = True
                paint = '0'
                break

        # 单击确定按钮
        if tkinter.messagebox.askokcancel('提示', '执行此操作需要花费' + paint + '积分，确定执行吗？'):
            # 扣除积分
            if paint == '50':
                # 全部完成
                if not wx.doAllWork():
                    showerror('警告', '积分不足！无法完成任务')
                    return
            elif paint == '30' and func == 'doWork':
                if not wx.doWork():
                    showerror('警告', '积分不足！无法完成任务')
                    return
            elif paint == '30':
                if not wx.watchRadio():
                    showerror('警告', '积分不足！无法完成任务')
                    return
            elif paint == '0' and isPaid:
                showinfo('提示', '本次使用中该课程已使用过积分，此次使用不消耗积分')

            # 更新积分
            detailWrap.getPoint()
        else:
            # 单击取消按钮
            return

        # 将该课程的courseOpenId和openClassId传入
        mooc._courseName = self.moocCourseList[index]['courseName']
        mooc._courseOpenId = self.moocCourseList[index]['courseOpenId']

        # 如果是获取答案功能，则正常扣除积分
        if paint == '50':
            # 将课程名添加至已付费过的课程
            self.paidCourse.append(mooc._courseName)

        # 中间展示
        tool.thread_it(self.moocShowModule)
        # 更新进度
        tool.thread_it(self.moocShowProcess)

        # 判断当前选择功能
        if self.doWorkWhat.get() == 0:
            # 全部完成
            tool.thread_it(self.moocDoAllWork)
        elif self.doWorkWhat.get() == 1:
            # 获取答案
            self.moocWorkLog('选择功能：获取答案')
            if askokcancel('警告', '使用该功能会导致该账号的测验考试0分，建议使用小号获取答案！'):
                try:
                    tool.thread_it(self.getAnswer)
                except:
                    time.sleep(63)
                    tool.thread_it(self.getAnswer)
                    self.moocWorkLog('任务奔溃，自动重新任务')
        elif self.doWorkWhat.get() == 2:
            # 完成课件
            self.moocWorkLog('选择功能：完成课件')
            try:
                tool.thread_it(self.moocWatchWork)
            except:
                time.sleep(63)
                tool.thread_it(self.moocWatchWork)
                self.moocWorkLog('任务奔溃，自动重新任务')
        elif self.doWorkWhat.get() == 3:
            # 开始答题
            self.moocWorkLog('选择功能：开始答题')
            try:
                tool.thread_it(self.doWork)
            except:
                time.sleep(63)
                tool.thread_it(self.doWork)
                self.moocWorkLog('任务奔溃，自动重新任务')

    # 智慧职教完成所有任务
    def moocDoAllWork(self):
        # 已完成的任务序号
        # 1 获取答案
        # 2 完成课件
        # 3 完成答题
        # 完成的工作序号
        self.doWorkNum = 0
        # 正在完成的工作序号
        self.doingWorkNum = 0

        self.moocWorkLog('智慧职教任务开始')

        # 使用死循环,不断检测是否完成
        while True:
            time.sleep(.5)

            try:
                # 自动获取答案为false还是true
                autoGetAnswer = conf.moocConf['doAllWorkAutoGetAnswer'] == 'True'
            except KeyError:
                showerror('错误', '权限不足，请以管理员权限运行程序！教程在使用手册')
                self.moocWorkLog('权限不足，请以管理员权限运行程序！教程在使用手册')
                return

            # 刚刚准备完成任务
            if self.doWorkNum == 0 and self.doingWorkNum == self.doWorkNum:
                # 如果自动获取答案
                if autoGetAnswer:
                    print('自动获取答案', conf.moocConf['doAllWorkAutoGetAnswer'])
                    self.moocWorkLog('自动获取答案' + conf.moocConf['doAllWorkAutoGetAnswer'])

                    try:
                        # 检查是否有已结束的测验
                        if mooc.checkHaveOver():
                            # 如果有已结束的测验，不获取答案
                            self.doWorkNum = 1
                            self.doingWorkNum = 1
                            showwarning('警告', '有已截止的测验，已跳过自动获取答案，请使用小号获取答案后才能进行答题')
                            showinfo('提示', '您也可以先使用获取答案功能，然后退出课程再使用全部完成功能')
                            self.moocWorkLog('有已截止的测验，已跳过自动获取答案')
                            self.moocWorkLog('原因：已截止测验课程获取答案后，会导致成绩为0分，请使用小号获取答案后进行答题')
                            if askyesno('询问', '您需要继续任务吗（将无法完成答题）'):
                                continue
                            else:
                                # 不继续任务
                                self.moocWorkLog('已终止任务，您可以获取答案后退出课程继续完成任务')
                                return
                    except:
                        print('未能检测是否有已结束测验')

                    tool.thread_it(self.getAnswer)
                else:
                    print('不自动获取')
                    self.doWorkNum = 1
                # 正在完成第一个任务
                self.doingWorkNum = 1
            # 已经完成获取答案任务，准备完成课件
            elif self.doWorkNum == 1 and self.doingWorkNum == self.doWorkNum:
                # 如果确认自动退出课程
                if conf.moocConf['doAllWorkAutoGetAnswer'] == 'True':
                    # 退出课程再加入课程
                    try:
                        if self.isGetAnswer and not mooc.quitAndJoin():
                            # 说明需要输入验证码
                            showerror('警告', '程序出错，需要自行再加入一次本课程！')
                            while not tkinter.messagebox.askokcancel('提示', '是否已加入课程'):
                                pass
                    except json.decoder.JSONDecodeError:
                        self.moocWorkLog('警告：程序出错，需要自行退出课程后再加入一次！')
                        showerror('警告', '程序出错，需要自行退出课程后再加入一次！')
                        return
                    except AttributeError:
                        print('有已截止课程！')

                time.sleep(2)

                tool.thread_it(self.moocWatchWork)
                self.doingWorkNum = 2
            # 已经完成课件任务，准备完成答题任务
            elif self.doWorkNum == 2 and self.doingWorkNum == self.doWorkNum:
                tool.thread_it(self.doWork)
                self.doingWorkNum = 3
            # 已经完成答题任务，准备退出死循环
            elif self.doWorkNum == 3 and self.doingWorkNum == self.doWorkNum:
                self.master.title(f'智慧职教助手 {glo.userName}智慧职教任务完成')
                showinfo('提示', f'{glo.userName} 全部任务已完成！')
                break

    # 智慧职教获取答案
    def getAnswer(self):
        global file
        # 是否获取答案，如果所有答案都有，则为未获取答案，也就是不用退出课程，否则反之
        self.isGetAnswer = 0

        skipWork = False
        skipTest = False
        skipExam = False
        # 判断要跳过哪个项目
        if self.skipWork.get():
            skipWork = True
        if self.skipTest.get():
            skipTest = True
        if self.skipExam.get():
            skipExam = True

        allCourse = list()
        print('当前课程的所有作业信息：')
        for i in range(0, 3):
            mooc.workExamType = i
            # 获取模块需要完成的课程
            allCourse.append(mooc.getWorkList())

            if skipWork and i == 0:
                self.moocWorkLog('已自动跳过作业')
                continue
            if skipTest and i == 1:
                self.moocWorkLog('已自动跳过测验')
                continue
            if skipExam and i == 2:
                self.moocWorkLog('已自动跳过考试')
                continue

            # 从所有课程中遍历指定模块的课程
            for course in allCourse[i]:
                try:
                    file.createNeedFile(mooc.courseOpenId, mooc.courseName)
                except:
                    # 无创建目录权限
                    showerror('错误', '权限不足！软件无法创建文件，请使用管理员权限运行或将软件放在非C盘')
                    return

                # 本地是否有该测验答案
                if file.haveQuestionskip(courseOpenId=mooc.courseOpenId, courseName=mooc.courseName,
                                         workExamId=course['workExamId']):
                    self.moocWorkLog('>> 已有该测验答案，自动跳过')
                    continue
                if course['isOver']:
                    self.moocWorkLog('>> 已过答题时间，下次请及时答题！')
                    continue

                examPreview = mooc.examPreview(
                    workExamId=course['workExamId'],
                    agreeHomeWork='agree',
                    workExamType=course['workExamType']
                )
                self.isGetAnswer = 1
                time.sleep(4)
                mooc.saveAnswer(
                    uniqueId=examPreview['uniqueId'],
                    workExamId=examPreview['workExamId'],
                    workExamType=examPreview['workExamType'],
                    title=examPreview['title']
                )
                # 获取答案
                try:
                    answer = mooc.getAnswer(
                        workExamId=examPreview['workExamId'],
                        workExamType=examPreview['workExamType'],
                        studentWorkId=mooc.getExamDetail(
                            workExamId=examPreview['workExamId']
                        )
                    )
                except IndexError:
                    print('获取答案出错')
                    self.moocWorkLog('答案保存出错，请自行检查该课程能否正常答题！')
                    return

                # 服务器保存答案
                tool.thread_it(wx.postAnswerToServer, answer['answerText'])

                # 保存答案
                self.moocWorkLog(file.saveFile(
                    fileName=answer['fileName'],
                    answerType=answer['answerType'],
                    answerText=answer['answerText'],
                    courseName=answer['courseName'],
                    courseOpenId=answer['courseOpenId'],
                    workExamId=answer['workExamId']
                ))

            if i == 0:
                self.moocWorkLog('******作业模块任务完成******')
            elif i == 1:
                self.moocWorkLog('******测验模块任务完成******')
            elif i == 2:
                self.moocWorkLog('******考试模块任务完成******')

        self.doWorkNum = 1
        # 不是全部完成选项
        if self.doWorkWhat.get() != 0:
            showinfo('提示', '答案已全部获取')

    # 智慧职教完成课件
    def moocWatchWork(self):
        # 模块ID列表
        processList = mooc.getProcessList()
        for item in processList:
            # 是否完成 本次未完成，则不更新模块列表和进度条
            isWatch = False

            self.moocWorkLog('-' * 8 + item['name'] + '-' * 8)
            topicList = mooc.getTopicByModuleId(item['id'])
            # 循环缩放列表
            for topItem in topicList:
                # print('执行到缩放列表')
                self.moocWorkLog('进入模块节点：' + topItem['name'])
                # 没有学过的缩放列表
                cellList = mooc.getCellByTopicId(topItem['id'])
                for cellItem in cellList:
                    if cellItem['cellType'] == 5:
                        self.moocWorkLog(cellItem['cellName'] + '为测验，自动跳过')
                        continue
                    elif cellItem['cellType'] == 6:
                        self.moocWorkLog(cellItem['cellName'] + '为作业，自动跳过')
                        continue
                    elif cellItem['cellType'] == 8:
                        self.moocWorkLog(cellItem['cellName'] + '为讨论任务，正在尝试完成')
                        mooc.talkTask(cellItem['resId'])
                        continue
                    elif cellItem['cellType'] == 9:
                        self.moocWorkLog(cellItem['cellName'] + '为问卷调查，无法完成!!!')
                        continue
                    # print('缩放列表', cellItem['cellType'])
                    # 已经完成了，可以跳过
                    if cellItem['isStudyFinish']:
                        # print(cellItem)
                        self.moocWorkLog(cellItem['cellName'] + '完成，已自动跳过')
                        continue

                    # 已完成的课程不更新列表和进度
                    isWatch = True

                    # 如果没有子节点
                    if not cellItem['childNodeList']:
                        # print('cellItem', cellItem)
                        # print(cellItem['cellName'], '执行到提交时间')
                        # print(cellItem['cellName'])
                        data = mooc.postStudentTime(
                            cellId=cellItem['Id'],
                            moduleId=item['id'],
                            moculeName=cellItem['cellName']
                        )
                        # 时间提交成功
                        if data['code'] == 1:
                            self.moocWorkLog(data['name'] + '已完成')
                        else:
                            self.moocWorkLog(data['name'] + '可能未完成，请自行检查')

                        time.sleep(4)
                    else:
                        # 循环子节点元素
                        for childCellItemList in cellItem['childNodeList']:
                            if childCellItemList['cellType'] == 5:
                                self.moocWorkLog(childCellItemList['cellName'] + '为测验，自动跳过')
                            elif childCellItemList['cellType'] == 6:
                                self.moocWorkLog(childCellItemList['cellName'] + '为作业，自动跳过')
                                continue
                            elif childCellItemList['cellType'] == 8:
                                self.moocWorkLog(childCellItemList['cellName'] + '为讨论任务，尝试完成')
                            elif childCellItemList['cellType'] == 9:
                                self.moocWorkLog(childCellItemList['cellName'] + '为问卷调查，无法完成!!!')
                            # print('子节点', childCellItemList['cellType'])
                            # 已经完成了，可以跳过
                            if childCellItemList['isStudyFinish']:
                                self.moocWorkLog(childCellItemList['cellName'] + '完成，已自动跳过')
                            else:
                                try:
                                    res = mooc.postStudentTime(
                                        cellId=childCellItemList['Id'],
                                        moduleId=item['id'],
                                        moculeName=childCellItemList['cellName']
                                    )
                                except requests.exceptions.ConnectionError:
                                    self.moocWorkLog('网络出错')
                                    return
                                # 已提交时间
                                if res['code'] == 1:
                                    self.moocWorkLog(res['name'] + '已完成')
                                else:
                                    self.moocWorkLog(res['name'] + '可能未完成')
                                time.sleep(4)

                if isWatch:
                    # 更新进度
                    tool.thread_it(self.moocShowProcess)
            if isWatch:
                # 展示模块
                tool.thread_it(self.moocShowModule)

        self.doWorkNum = 2
        # 不是全部完成选项
        if self.doWorkWhat.get() != 0:
            showinfo('提示', '课件已全部完成！')

    # 智慧职教答题
    def doWork(self):
        # 是否有未完成的课程 默认没有
        notSuccess = False

        print('当前课程的所有作业信息：')
        allCourse = list()
        for i in range(0, 3):
            if i == 0:
                print('-' * 8, ' 作业 ', '-' * 8)
            elif i == 1:
                print('-' * 8, ' 测验 ', '-' * 8)
            else:
                print('-' * 8, ' 考试 ', '-' * 8)

            mooc.workExamType = i
            allCourse.append(mooc.getWorkList())
            for v in allCourse[i]:
                print('|', '=' * 4, '>>', v['Title'])

        # 默认所有答案都有
        notSuccess = False

        for i in range(0, 3):
            file.createNeedFile(mooc.courseOpenId, mooc.courseName)
            mooc.workExamType = i
            # 查看本地某课程的答案
            try:
                answer = file.readAnswer(
                    courseOpenId=mooc.courseOpenId,
                    courseName=mooc.courseName,
                    workExamType=mooc.workExamType,
                    allCourse=allCourse[i]
                )
            except json.decoder.JSONDecodeError:
                # 答案文件可能有误
                print('mainUI line 565出错')
                self.moocWorkLog('答案文件有误，请删除answerFile文件夹并重新获取')
                self.moocWorkLog('如果还是有误，请联系作者修复BUG')
                self.moocWorkLog('软件异常退出！！！')
                return

            # 如果该目录下有文件
            if answer['state']:
                # print('answer', answer)
                # 从所有课程中遍历指定模块的课程
                for course in allCourse[i]:
                    # 遍历某模块的所有课程
                    if course['Score'] == 100:
                        self.moocWorkLog('>>' + course['Title'] + '满分测验已自动跳过')
                        continue
                    if not course['canDo']:
                        self.moocWorkLog('>>' + course['Title'] + '可做次数不足，已自动跳过')
                        continue
                    if course['isOver']:
                        self.moocWorkLog('>> 已过答题时间，下次请及时答题！')
                        continue

                    time.sleep(4)

                    examPreview = mooc.examPreview(
                        workExamId=course['workExamId'],
                        agreeHomeWork='agree',
                        workExamType=course['workExamType']
                    )

                    try:
                        isHaveFileQuestion = mooc.postAnswer(
                            question=answer[course['workExamId']],
                            uniqueId=examPreview['uniqueId'],
                            workExamType=mooc.workExamType
                        )
                    except KeyError:
                        self.moocWorkLog('>>' + course['Title'] + '无答案，已自动跳过')
                        notSuccess = True
                        continue

                    # 提交答案
                    if isHaveFileQuestion:
                        self.moocWorkLog('>> 未提交答案')
                        self.moocWorkLog('>> 原因：有文件做答题未能完成')
                        self.moocWorkLog('>> 请自行提交答案')
                        continue
                    mooc.saveAnswer(
                        uniqueId=examPreview['uniqueId'],
                        workExamId=examPreview['workExamId'],
                        workExamType=examPreview['workExamType'],
                        title=examPreview['title']
                    )

                # 展示模块
                tool.thread_it(self.moocShowModule)
                # 更新进度
                tool.thread_it(self.moocShowProcess)

                if i == 0:
                    self.moocWorkLog('******作业模块任务完成******')
                elif i == 1:
                    self.moocWorkLog('******测验模块任务完成******')
                elif i == 2:
                    self.moocWorkLog('******考试模块任务完成******')
        if notSuccess:
            self.moocWorkLog('\n!!! 有无答案的课程，请获取答案后重新答题 !!!\n')

        self.doWorkNum = 3
        # 不是全部完成选项
        if self.doWorkWhat.get() != 0:
            showinfo('提示', '答题任务已全部完成！')

    # 中间展示
    def moocShowModule(self):
        # 清空
        x = self.moocMainBox.get_children()
        for item in x:
            self.moocMainBox.delete(item)

        moduleList = mooc.getProcessList()
        moduleIndex = 0
        for moduleItem in moduleList:
            moduleIndex += 1
            self.moocMainBox.insert("", 0, values=(moduleIndex, moduleItem['name'], "模块", moduleItem['percent']))

    # 展示进度
    def moocShowProcess(self):
        data = mooc.showCourseDetail()
        if data['code'] == 1:
            # 进度获取成功，更新
            self.moocProgressBar['value'] = data['process']
            self.moocProgressBar.update()
            # 更新进度文字
            self.moocProgress['text'] = str(data['process']) + '%'
        else:
            self.moocWorkLog('进度获取失败')
            logging.warning('进度获取失败')

    # 输出工作时日志
    def moocWorkLog(self, msg):
        current = datetime.now()
        date = current.strftime('%Y-%m-%d %H:%M:%S')
        # 在智慧职教窗口输出
        # self.moocWorkLogBox.insert(1.0, '{0} -> {1}\n======================================'.format(date, msg))
        self.moocWorkLogBox.insert(1.0, '{0} -> {1}\n'.format(date, msg))

    """
    上面为智慧职教处理函数
    ====================
    下面为职教云处理函数
    """

    def createZjyWidget(self):
        self.zjy = Frame(self, bg=tool.rgb((250, 250, 250)))
        self.add(self.zjy, text='职教云')

        self.workLogBox = Text(self.zjy, bg='white')

        # 左上角选择课程
        selectCourse = Frame(self.zjy, bg='white')
        selectCourse.place(x=10, y=10, width=150, height=160)

        Label(selectCourse, text='选择你的课程', bg='white').pack(pady=14)
        ttk.Style().configure(
            'TCombobox',
            background='green',
            width=10
        )
        self.zjyCourse = ttk.Combobox(selectCourse, state='readonly')
        self.zjyCourse.place(y=40, x=15, width=120)

        # 开始按钮
        start = ttk.Button(selectCourse, text='冲冲冲', command=self.selectCourse)
        start.pack(pady=40)

        # 功能区
        funcBox = Frame(self.zjy, bg='red')
        funcBox.place(x=10, y=180, width=150, height=138)

        # 提示信息
        tip = Text(funcBox)
        tip.insert(1.0, '职教云目前只支持课件(视频、PPT之类的)\n\n以后有充足的题库后才会更新答题功能')
        tip.pack()
        tip['state'] = DISABLED

        # 模块列表区
        self.zjyMainBox = ttk.Treeview(self.zjy, show='headings')
        self.zjyMainBox['columns'] = ('序号', '章节', '类型', '状态')
        self.zjyMainBox.column("序号", width=40, anchor="center")  # #设置列
        self.zjyMainBox.column("章节", width=202, anchor="center")
        self.zjyMainBox.column("类型", width=60, anchor="center")
        self.zjyMainBox.column("状态", width=60, anchor="center")
        self.zjyMainBox.heading("序号", text="序号")  # #设置显示的表头名
        self.zjyMainBox.heading("章节", text="章节")
        self.zjyMainBox.heading("类型", text="类型")
        self.zjyMainBox.heading("状态", text="进度")
        self.zjyMainBox.place(x=180, y=10, width=364, height=270)

        # self.mainBox.insert("", 0, values=("111", " 专题一 马克思主义中国化有哪些理论成果？", "PPT", "未完成"))  # #给第0行添加数据，索引值可重复
        # self.mainBox.insert("", 1, values=("2", " 专题一", "PPT", "未完成"))  # #给第0行添加数据，索引值可重复
        # self.mainBox.insert("", 2, values=("3", " 马克思主义中国化", "PPT", "未完成"))  # #给第0行添加数据，索引值可重复
        # self.mainBox.insert("", 3, values=("4", " 专题一些理论成果？", "PPT", "未完成"))  # #给第0行添加数据，索引值可重复
        # self.mainBox.insert("", 4, values=("5", " 专题一 马克思主义中国化有哪些理论成果？", "PPT", "未完成"))  # #给第0行添加数据，索引值可重复

        # 进度条
        self.zjyProgressBar = ttk.Progressbar(self.zjy)
        self.zjyProgressBar.place(x=180, y=296, width=364, height=20)
        # 进度条文字
        self.zjyProgress = Label(self.zjy, text='0%', fg=tool.rgb((4,191,191)), bg=tool.rgb((250,250,250)), font=('微软雅黑', 12, 'bold'))
        self.zjyProgress.place(x=350, y=296, height=20)

        # 运行日志区
        # self.runLogBox = Text(self.zjy, bg='white')
        # self.runLogBox.place(x=10, y=335, width=250, height=170)
        # self.runLogBox.insert(0.0, '666')

        # 任务执行日志
        # self.workLogBox.place(x=275, y=335, width=270, height=170)
        self.workLogBox.place(x=10, y=335, width=535, height=170)
        zjy.setZjyBox(self)

        # 获取课程
        tool.thread_it(self.zjyGetCourse)

    # 输出工作时日志
    def workLog(self, msg):
        current = datetime.now()
        date = current.strftime('%Y-%m-%d %H:%M:%S')
        # 在职教云
        self.workLogBox.insert(1.0, '{0} -> {1}\n'.format(date, msg))

    # 获取课程列表
    def zjyGetCourse(self):
        # 课程的列表，包含所有信息
        self.zjyCourseList = zjy.getLessoning()
        self.courseNames = []
        for item in self.zjyCourseList:
            # 将课程名从里面选出来
            self.courseNames.append(item['courseName'])

        n = 1
        while n < 10:
            try:
                self.zjyCourse['values'] = self.courseNames
                break
            except:
                time.sleep(1)
                n += 1
                self.zjyCourse['values'] = self.courseNames

    # 选中课程
    def selectCourse(self):
        self.master.title('智慧职教助手')

        # 获取当前选中课程的索引值
        try:
            index = self.courseNames.index(self.zjyCourse.get())
        except ValueError:
            showerror('警告', '选择的课程不能为空')
            logging.warning('选择课程为空')
            return

        # 判断需要的积分
        paint = '50'

        # 是否为已付费课程
        isZjyPaid = False
        for course in self.paidZjyCourse:
            # 如果当前选中的课程是已付费的课程
            if course == self.zjyCourseList[index]['courseName']:
                isZjyPaid = True
                paint = '0'
                break

        # 单击确定按钮
        if tkinter.messagebox.askokcancel('提示', '执行此操作需要花费' + paint + '积分，确定执行吗？'):
            if paint == '50':
                if not wx.doZjy():
                    showerror('警告', '积分不足！无法完成任务')
                    return
            elif isZjyPaid:
                showinfo('提示', '本次使用中该课程已使用过积分，此次使用不消耗积分')

            # 更新积分
            detailWrap.getPoint()
        else:
            # 单击取消按钮
            return

        # 将该课程的courseOpenId和openClassId传入
        zjy.courseName = self.zjyCourseList[index]['courseName']
        zjy.courseOpenId = self.zjyCourseList[index]['courseOpenId']
        zjy.openClassId = self.zjyCourseList[index]['openClassId']

        # 将课程名添加至已付费过的课程
        self.paidZjyCourse.append(zjy.courseName)
        self.workLog('全部完成任务开始')

        # 中间展示
        tool.thread_it(self.zjyShowModule)
        # 更新进度
        tool.thread_it(self.zjyShowProcess)

        # 视频任务
        try:
            tool.thread_it(self.zjyDoWork)
        except:
            time.sleep(63)
            self.workLog('任务奔溃，自动重连')
            tool.thread_it(self.zjyDoWork)

    # 完成任务
    def zjyDoWork(self):
        self.workLog('任务开始')
        # 模块列表
        moduleList = zjy.getProcessList()

        # 是否完成 本次未完成，则不更新模块列表和进度条
        isWatch = False
        # 遍历模块列表
        for moduleItem in moduleList:
            if moduleItem['percent'] == 100:
                self.workLog(moduleItem['name'] + '完成，已自动跳过')
                continue
            topicList = zjy.getTopicByModuleId(moduleItem['id'])

            time.sleep(2)

            # 循环缩放列表
            for topItem in topicList:
                # 子模块节点
                # 没有学过的缩放列表
                cellList = zjy.getCellByTopicId(topItem['id'])
                for cellItem in cellList:
                    # self.workLog(moduleItem['name'] + '进入该缩放列表')
                    if not cellItem['childNodeList']:
                        if cellItem['stuCellCount'] == 1:
                            self.workLog(cellItem['cellName'] + '已完成，自动跳过')
                            # 已完成 跳过
                            continue

                        isWatch = True

                        res = zjy.postStudentTime(
                            cellId=cellItem['Id'],
                            moduleId=moduleItem['id'],
                            categoryType=cellItem['categoryName']
                            # moculeName=cellItem['cellName']
                        )
                        if res['code'] == 1:
                            # 时长提交成功
                            self.workLog(cellItem['cellName'] + '已完成')
                            try:
                                # 提交评价
                                if conf.zjyConf['zjyAddActivity'] == 'True':
                                    if zjy.addCellActivity(cellId=cellItem['Id'],
                                                           content=conf.zjyConf['zjyAddActivityContent']):
                                        self.workLog('~ 评论成功')
                                    else:
                                        self.workLog('! 评论失败')
                            except:
                                self.workLog('! 评论功能出错')
                        elif res['code'] == -101:
                            self.master.title(f'智慧职教助手 {glo.userName}有被检测出刷课的可能，软件已停止任务，请等待15分钟后再执行任务！')
                            showerror('警告', f'{glo.userName}有被检测出刷课的可能，软件已停止任务，请等待15分钟后再执行任务！')
                            self.workLog('有被检测出刷课的可能，软件已停止任务，请等待15分钟后再执行任务！')
                            return
                        else:
                            self.workLog(cellItem['cellName'] + '可能未完成，请自行检查')
                            logging.warning('职教云提交时长失败')
                        time.sleep(2)
                    else:
                        # 有子节点
                        for childNode in cellItem['childNodeList']:
                            # self.workLog(childNode['cellName'] + '进入该子节点')
                            if childNode['stuCellFourCount'] == 1:
                                self.workLog(childNode['cellName'] + '已完成，自动跳过')
                                # 已完成 跳过
                                continue

                            isWatch = True

                            res = zjy.postStudentTime(
                                cellId=childNode['Id'],
                                moduleId=moduleItem['id'],
                                categoryType=childNode['categoryName']
                                # moculeName=cellItem['cellName']
                            )
                            if res['code'] == 1:
                                # 时长提交成功
                                self.workLog(childNode['cellName'] + '已完成')
                            elif res['code'] == -101:
                                showerror('警告', '有被检测出刷课的可能，软件已停止任务，请等待15分钟后再执行任务！')
                                self.workLog('有被检测出刷课的可能，软件已停止任务，请等待15分钟后再执行任务！')
                                return
                            else:
                                self.workLog(childNode['cellName'] + '可能未完成，请自行检查')
                                logging.warning('职教云提交时长失败')
                            time.sleep(2)

                    if isWatch:
                        # 更新进度条
                        tool.thread_it(self.zjyShowProcess)
                    time.sleep(2)

                if isWatch:
                    # 更新模块信息
                    tool.thread_it(self.zjyShowModule)

        self.master.title(f'智慧职教助手 {glo.userName}职教云任务完成')
        showinfo('提示', f'{glo.userName}《{zjy.courseName}》 已完成')

    # 显示进度信息
    def zjyShowProcess(self):
        data = zjy.getProcess()
        if data['code'] == 1:
            # 进度获取成功，更新
            self.zjyProgressBar['value'] = data['process']
            self.zjyProgressBar.update()
            # 更新进度文字
            self.zjyProgress['text'] = str(data['process']) + '%'
        else:
            self.workLog('进度获取失败')
            logging.warning('进度获取失败')

    # 显示模块信息
    def zjyShowModule(self):
        # 清空
        x = self.zjyMainBox.get_children()
        for item in x:
            self.zjyMainBox.delete(item)

        moduleList = zjy.getProcessList()
        moduleIndex = 0
        for moduleItem in moduleList:
            moduleIndex += 1
            self.zjyMainBox.insert("", 0, values=(moduleIndex, moduleItem['name'], "模块", moduleItem['percent']))

    # 输出工作时日志
    def workLog(self, msg):
        current = datetime.now()
        date = current.strftime('%Y-%m-%d %H:%M:%S')
        # 在职教云
        self.workLogBox.insert(1.0, '{0} -> {1}\n'.format(date, msg))

    """
    上面为职教云处理函数
    ====================
    下面为资源库处理函数
    """

    def createZykWidget(self):
        self.zyk = Frame(self, bg=tool.rgb((250, 250, 250)))
        self.add(self.zyk, text='资源库')

        self.zykWorkLogBox = Text(self.zyk, bg='white')

        # 左上角选择课程
        selectCourse = Frame(self.zyk, bg='white')
        selectCourse.place(x=10, y=10, width=150, height=160)

        Label(selectCourse, text='选择你的课程', bg='white').pack(pady=14)
        ttk.Style().configure(
            'TCombobox',
            background='green',
            width=10
        )
        self.zykCourse = ttk.Combobox(selectCourse, state='readonly')
        self.zykCourse.place(y=40, x=15, width=120)
        # 获取课程列表
        tool.thread_it(self.zykGetCourse)

        # 开始按钮
        start = ttk.Button(selectCourse, text='冲冲冲', command=self.zjkSelectCourse)
        start.place(y=95, x=15, width=55)

        # 微课按钮
        wkStart = ttk.Button(selectCourse, text='完成微课', command=self.doWk)
        wkStart.place(y=95, x=75, width=60)

        # 功能区
        funcBox = Frame(self.zyk, bg='red')
        funcBox.place(x=10, y=180, width=150, height=138)

        # 提示信息
        tip = Text(funcBox)
        tip.insert(1.0, '资源库目前只支持课件(视频、PPT之类的)\n\n以后有充足的题库后才会更新答题功能\n\n完成微课即会完成全部资源库微课')
        tip.pack()
        tip['state'] = DISABLED

        # 模块列表区
        self.zykMainBox = ttk.Treeview(self.zyk, show='headings')
        self.zykMainBox['columns'] = ('序号', '章节', '类型', '状态')
        self.zykMainBox.column("序号", width=40, anchor="center")  # #设置列
        self.zykMainBox.column("章节", width=202, anchor="center")
        self.zykMainBox.column("类型", width=60, anchor="center")
        self.zykMainBox.column("状态", width=60, anchor="center")
        self.zykMainBox.heading("序号", text="序号")  # #设置显示的表头名
        self.zykMainBox.heading("章节", text="章节")
        self.zykMainBox.heading("类型", text="类型")
        self.zykMainBox.heading("状态", text="进度")
        self.zykMainBox.place(x=180, y=10, width=364, height=270)

        # 进度条
        self.zykProgressBar = ttk.Progressbar(self.zyk)
        self.zykProgressBar.place(x=180, y=296, width=364, height=20)
        # 进度条文字
        self.zykProgress = Label(self.zyk, text='α%', fg=tool.rgb((4,191,191)), bg=tool.rgb((250,250,250)), font=('微软雅黑', 12, 'bold'))
        self.zykProgress.place(x=350, y=296, height=20)

        self.zykWorkLogBox.place(x=10, y=335, width=535, height=170)
        wk.setZykBox(self)

    # 微课任务
    def doWk(self):
        # 判断需要的积分
        paint = '30'
        # 单击确定按钮
        if tkinter.messagebox.askokcancel('提示', '执行此操作需要花费' + paint + '积分，确定执行吗？'):
            if paint == '30':
                if not wx.watchRadio():
                    showerror('警告', '积分不足！无法完成任务')
                    return

            # 更新积分
            detailWrap.getPoint()
        else:
            # 单击取消按钮
            return

        tool.thread_it(self.doAllWkWork)

    # 完成所有微课任务
    def doAllWkWork(self):
        # 获取所有未完成的课程
        wkList = wk.getAllNotDoneCourse()
        # 遍历所有课程
        for course in wkList:
            # 获取课程的视频
            cells = wk.getCourseInfo(course['id'])
            # 完成所有课程的微课
            tool.thread_it(wk.postAllCourse, cells)
            time.sleep(2)
        # 完成所有微课任务
        showinfo('提示', '微课任务已完成')

    # 获取资源库课程列表
    def zykGetCourse(self):
        # self.workLog('获取课程列表')
        # 课程的列表，包含所有信息
        self.zykCourseList = zyk.getCourse()

        self.zykCourseNames = []
        for item in self.zykCourseList:
            # 将课程名从里面选出来
            self.zykCourseNames.append(item['title'])
        print(self.zykCourseNames)
        try:
            self.zykCourse['values'] = self.zykCourseNames
        except RuntimeError:
            self.zykCourse['values'] = self.zykCourseNames

    # 资源库选择课程
    def zjkSelectCourse(self):
        self.master.title('智慧职教助手')

        # 获取当前选中课程的索引值
        try:
            index = self.zykCourseNames.index(self.zykCourse.get())
        except ValueError:
            showerror('警告', '选择课程不能为空')
            return

        # 课程ID
        zyk.courseId = self.zykCourseList[index]['id']
        # 课程名
        zyk.courseName = self.zykCourseList[index]['title']

        # 判断需要的积分
        paint = '50'
        # 单击确定按钮
        if tkinter.messagebox.askokcancel('提示', '执行此操作需要花费' + paint + '积分，确定执行吗？'):
            if paint == '50':
                if not wx.doZyk():
                    showerror('警告', '积分不足！无法完成任务')
                    return

            # 更新积分
            detailWrap.getPoint()
        else:
            # 单击取消按钮
            return

        self.zykWorkLog('资源库任务开始')
        tool.thread_it(self.zykDoAllWork)

    # 资源库完成课件
    def zykDoAllWork(self):
        # 获取课程目录信息
        directory = zyk.getDirectory()
        for dir in directory:
            # 目录标签
            """
            mxgavqqvivkzxa8jhzraa 模块四采煤工作面生产组织管理
            q5d9agiqqiphspbhlkbeng 绪论
            """
            section = dir['section']
            id = section['Id']
            title = section['Title']

            # 目录里的项目
            chapters = dir['chapters']
            self.zykWorkLog('当前目录为' + title)
            """
            eaomawiqmlhpcr1r9rml6g 绪论 1
            """
            for item in chapters:
                knowleges = item['knowleges']
                # 如果有子目录
                if knowleges != []:
                    for knowlege in knowleges:
                        subCells = knowlege['cells']
                        for subCell in subCells:
                            subCellId = subCell['Id']
                            subCellTitle = subCell['Title']
                            zyk.postStudy(subCellId)
                            self.zykWorkLog(subCellTitle + '已完成')
                            time.sleep(1)
                        time.sleep(2)

                # 如果knowleges旁的cells不为空
                knowCells = item['cells']
                if knowCells != []:
                    for knowCell in knowCells:
                        knowCellId = knowCell['Id']
                        knowCellTitle = knowCell['Title']
                        zyk.postStudy(knowCellId)
                        self.zykWorkLog(knowCellTitle + '已完成')
                        time.sleep(2)

                chapter = item['chapter']

                # 子项目名称
                chapterTitle = chapter['Title']
                # 子项目ID
                chapterId = chapter['Id']
                # 子项目类型
                chapterType = chapter['ChapterType']
                self.zykWorkLog('进入课程列表 ' + chapterTitle)

                # 子项目列表
                try:
                    subList = zyk.getNowCourseDirectory(chapterId)
                except KeyError:
                    self.zykWorkLog('作业无法完成，自动跳过')
                    continue

                for sub in subList:
                    # {'Id': 'bbsnawiqtprhxmmzyemi8g', 'Title': '绪论01', 'CellType': 'text'}
                    cellId = sub['Id']
                    cellTitle = sub['Title']
                    zyk.postStudy(cellId)
                    self.zykWorkLog(cellTitle + '已完成')
                    time.sleep(1)
                time.sleep(2)
        self.master.title(f'智慧职教助手 {glo.userName}资源库任务完成')
        showinfo('提示', f'{glo.userName} 资源库任务已完成')

    # 输出工作时日志
    def zykWorkLog(self, msg):
        current = datetime.now()
        date = current.strftime('%Y-%m-%d %H:%M:%S')
        # 在职教云
        self.zykWorkLogBox.insert(1.0, '{0} -> {1}\n'.format(date, msg))


class DetailWrap(ttk.Frame):
    """
    右侧详情部分
    """
    def __init__(self, master):
        super().__init__(master, borderwidth=6)
        self.master = master
        ttk.Style().configure(
            'TFrame',
            background='white',
        )
        self.place(x=590, y=10, width=200, height=540)

        # 头像
        try:
            self.photo = PhotoImage(file='res/photo.png', width=99, height=80)
        except:
            showerror('错误', '缺少res文件夹，请将软件压缩包内所有文件解压！')

        # vip图标
        # 不同级别使用图标不同
        # 普通用户
        self.vipImg = PhotoImage(file='res/vip4.png', width=20, height=20)
        if glo.uid == 1 or glo.uid == 27 or glo.uid == 8 or glo.uid == 108:
            # 为元老用户
            self.vipImg = PhotoImage(file='res/vip1.png', width=20, height=20)
        elif glo.uid <= 1000:
            # 为内测用户
            self.vipImg = PhotoImage(file='res/vip2.png', width=20, height=20)
        elif wx.getUserPoint(glo.uid) >= 500:
            # 为会员用户
            self.vipImg = PhotoImage(file='res/vip3.png', width=20, height=20)

        self.createWidget()

    def createWidget(self):
        # 头像
        photo = ttk.Label(self, image=self.photo)
        photo.pack()
        photo.bind('<Button-1>', self.reLogin)

        # 个人软件信息
        ttk.Style().configure(
            'info.Frame',
            padding=(0, 10, 0, 10)
        )
        info = ttk.Frame(self)
        info.pack(padx=10, pady=14)
        ttk.Style().configure(
            'infoL.TLabel',
            width=10,
            height=10,
            background='white'
        )
        # 显示的uid
        uid = str(10000 + glo.uid)
        ttk.Label(info, text='UID:' + uid, style='infoL.TLabel').pack()
        # 积分
        self.point = ttk.Label(info, text='积分: 0', style='infoL.TLabel')
        # 更新积分
        self.getPoint()
        self.point.pack()

        # vip图标
        ttk.Style().configure(
            'img.TLabel',
            background='white'
        )
        Label(self, image=self.vipImg, bd=0).place(relx=0.6, x=14, y=98)

        # 刷新图标
        self.refresh = PhotoImage(file='res/refresh.png')
        refreshBtn = Label(self, image=self.refresh, bd=0)
        refreshBtn.place(relx=0.6, x=16, y=124)
        # 绑定单击事件
        refreshBtn.bind('<Button-1>', self.getPoint)

        # 充值图标
        self.pay = PhotoImage(file='res/love.png')
        payBtn = Label(self, image=self.pay, bd=0)
        payBtn.place(relx=0.6, x=38, y=121)
        # 绑定单击事件
        print(resPath)
        payBtn.bind('<Button-1>', lambda url: tool.openWebSite(resPath + '/res/thanks.png'))

        # 智慧职教信息
        ttk.Style().configure(
            'moocInfo.TLabelframe',
            padding=5,
            background='white'
        )
        moocInfo = LabelFrame(self, text='平台信息', background='white', bd=1, labelanchor='n')
        moocInfo.pack(fill='x')
        ttk.Style().configure(
            'moocInfoLabel.TLabel',
            width=30,
            background='white',
            padding=6
        )
        self.moocName = ttk.Label(moocInfo, style='moocInfoLabel.TLabel')
        self.moocName.pack()
        self.moocUser = ttk.Label(moocInfo, style='moocInfoLabel.TLabel')
        self.moocUser.pack()
        self.moocSchool = ttk.Label(moocInfo, style='moocInfoLabel.TLabel')
        self.moocSchool.pack()
        # 获取信息
        tool.thread_it(self.getMoocUserInfo)

        # 公告
        self.notice = Text(self, height=10)

        self.notice.pack(pady=14)
        self.notice.insert(1.0, 'MOOC全部完成需要50积分\n'
                                '职教云需要50积分\n'
                                '资源库需要50积分\n'
                                '**************************'
                                '获取积分通过小程序智慧mooc助手签到获取\n'
                                '或者捐赠我支持软件\n'
                                '有问题请联系\ndanyhug@qq.com\n')
        # tool.thread_it(self.getNotice)

        # 软件介绍
        softDetail = ttk.Frame(self)
        softDetail.pack()
        ttk.Style().configure(
            'softDetail.TLabel',
            width=15,
            background='white',
            # 左 上 右 下
            padding=(0, 6, 0, 0),
            anchor=CENTER
        )
        # 官网
        ttk.Style().configure(
            'a.TLabel',
            foreground='#2440b3',
            font='微软雅黑 10 underline',
            background='white',
            anchor=CENTER,
            padding=(0, 5, 0, 0)
        )
        officialWebSite = ttk.Label(softDetail, text='软件官网: mooc.zzf4.top', style='a.TLabel', cursor='dotbox')
        officialWebSite.bind('<Button-1>', lambda url: tool.openWebSite('mooc.zzf4.top'))
        officialWebSite.pack()

        ttk.Label(softDetail, text='By ZZF4工作室', style='softDetail.TLabel').pack()
        version = ttk.Label(softDetail, style='softDetail.TLabel')
        version['text'] = '版本: ' + wx.VERSION
        version.pack()

        # 更新
        self.update = PhotoImage(file='res/update.png')
        self.updateLab = Label(self, image=self.update, bd=0)
        self.updateLab.bind('<Button-1>', self.checkUpdate)
        self.updateLab.place(relx=0.7, rely=0.9, y=20)

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

    def reLogin(self, event=None):
        if askokcancel('提示', '要进行断线重连吗？（登录状态失效时请使用）'):
            if glo.reLogin():
                showinfo('提示', '重连成功，请重新开始任务')
            else:
                showinfo('提示', '重连失败，请重新登录')

    # 获取用户积分
    def getPoint(self, event=None):
        uid = str(glo.uid)
        self.point['text'] = '积分:' + str(wx.getUserPoint(uid))

    # 获取用户平台信息
    def getMoocUserInfo(self):
        try:
            info = zjy.getUserInfo()
            self.moocName['text'] = '姓名：' + info['name']
            self.moocUser['text'] = '学号：' + info['stu']
            self.moocSchool['text'] = '学校：' + info['school']
        except:
            print('职教云信息获取失败')
            self.moocName['text'] = '姓名：获取失败'
            self.moocUser['text'] = '学号：获取失败'
            self.moocSchool['text'] = '学习使我快乐'
            showerror('提示', '职教云登录失败，请检查职教云能否正常登录！')

    # 获取公告
    def getNotice(self):
        notice = wx.getNotice()
        allNotice = ''
        for item in notice:
            allNotice += '{0}\n  {1}\n**************************\n'.format(item['time'][:10], item['content'])
        # 更新公告
        self.notice.insert(1.0, allNotice)


root = Tk()
root['bg'] = tool.rgb((254, 254, 254))
root.title('智慧职教助手')

root.geometry(tool.positionCenter(
    '800x560',
    root.winfo_screenwidth(),
    root.winfo_screenheight()
))
#禁止用户调整窗口大小
root.resizable(False,False)

# 标签页
tabPages = TabPages(root)
# 详情页
detailWrap = DetailWrap(root)
tool.thread_it(detailWrap.checkUpdate, auto=True)
# notice = wx.getNotice()
wx.uid = glo.uid

def checkLogin():
    try:
        while True:
            time.sleep(25)
            if not user.checkLogin():
                print('登录状态失效，自动重连')
                glo.reLogin()
    except:
        return
tool.thread_it(checkLogin)

# 保留日志
# logging.info('程序运行成功')
root.mainloop()
