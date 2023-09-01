"""
Mooc类
这里定义有关智慧职教课程的一切
Created by Danyhug on 2021-01-30 21:00
Coding by Danyhug on 2021-02-01 09:00
"""
import time
import random
import json
import re
import globalData as glo

import utils


class Mooc(utils.Utils):
    # ******URL******
    # 首页
    URL = 'https://mooc-old.icve.com.cn'
    # 用户详情
    URL_GET_USER_INFO = 'https://mooc-old.icve.com.cn/portal/LoginMooc/getUserInfo'

    # 获取课程列表
    URL_GET_LESSON = 'https://mooc-old.icve.com.cn/portal/Course/getMyCourse'
    # 获取正在进行的课程
    URL_GET_LESSON_ING = 'https://mooc-old.icve.com.cn/portal/Course/getMyCourse?isFinished=0&page=1&pageSize=999'
    # 课程详情
    URL_GET_LESSON_DETAIL = 'https://mooc-old.icve.com.cn/study/learn/courseIndex'
    # 获取作业列表
    URL_GET_WORK = 'https://mooc-old.icve.com.cn/study/workExam/getWorkExamList'
    # 获取作业信息
    URL_GET_WORK_INFO = 'https://mooc-old.icve.com.cn/study/workExam/getWorkExamData'
    # 测验界面
    URL_PAGE = 'https://mooc-old.icve.com.cn/study/workExam/workExamPreview'
    # 提交答案
    URL_POST_ANSWER = 'https://mooc-old.icve.com.cn/study/workExam/onlineHomeworkAnswer'
    # 提交答案(考试)
    URL_POST_EXAM_ANSWER = 'https://mooc-old.icve.com.cn/study/workExam/onlineExamAnswer'
    # 提交答案(填空)
    URL_POST_ANSWER_FILL = 'https://mooc-old.icve.com.cn/study/workExam/onlineHomeworkCheckSpace'
    # 提交答案(考试填空)
    URL_POST_EXAM_ANSWER_FILL = 'https://mooc-old.icve.com.cn/study/workExam/onlineExamCheckSpace'
    # 提交答案(匹配)
    URL_POST_ANSWER_Match = 'https://mooc-old.icve.com.cn/study/workExam/onlineHomeworkMatch'
    # 提交答案(阅读理解、完形填空)
    URL_POST_ANSWER_Sub = 'https://mooc-old.icve.com.cn/study/workExam/onlineHomeworkSubAnswer'
    # 考试提交答案(阅读理解)
    URL_POST_EXAM_ANSWER_Sub = 'https://mooc-old.icve.com.cn/study/workExam/onlineExamSubAnswer'
    # 让服务器保存答案
    URL_POST_ANSWER_SAVE = 'https://mooc-old.icve.com.cn/study/workExam/workExamSave'
    # 让服务器保存考试答案
    URL_POST_EXAM_SAVE = 'https://mooc-old.icve.com.cn/study/workExam/onlineExamSave'
    # 获取测验细节
    URL_GET_EXAM_DETAIL = 'https://mooc-old.icve.com.cn/study/workExam/detail'
    # 获取答案
    URL_GET_ANSWER = 'https://mooc-old.icve.com.cn/study/workExam/history'

    # 获取课程模块ID
    URL_GET_MODULE_ID = 'https://mooc-old.icve.com.cn/study/learn/getProcessList'
    # 获取缩放ID
    URL_GET_TOPIC = 'https://mooc-old.icve.com.cn/study/learn/getTopicByModuleId'
    # 获取模块详情
    URL_GET_MODULE_DETAIL = 'https://mooc-old.icve.com.cn/study/learn/getCellByTopicId'
    # 获取视频长度
    URL_GET_VIEW_LENGTH = 'https://mooc-old.icve.com.cn/study/learn/viewDirectory'
    # 提交学习时长
    URL_POST_STUDY_TIME = 'https://mooc-old.icve.com.cn/study/learn/statStuProcessCellLogAndTimeLong'

    # 讨论任务
    URL_GET_TALKTASK = 'https://mooc-old.icve.com.cn/study/discussion/addStuViewTopicRemember'

    # 退出课程
    URL_POST_QUIT_LESSON = 'https://mooc-old.icve.com.cn/portal/Course/withdrawCourse'
    # 加入课程
    URL_POST_JOIN_LESSON = 'https://mooc-old.icve.com.cn/study/Learn/addMyMoocCourse'

    def __init__(self):
        # 课程名
        self._courseName = ''
        # 课程ID
        self._courseOpenId = ''
        # 测验类型
        self._workExamType = 0

    # 将self.moocBox绑定主界面的moocBox，可以使用主界面的函数
    def setMoocBox(self, moocBox):
        self.moocBox = moocBox
        self.moocBox.moocWorkLog('MOOC配置已就绪')

    @property
    def courseName(self):
        # 文件名中可能有\/:*?"><|
        # 更改文件名
        self._courseName = re.sub(r'[/:*?"><|\\]', 'YY', self._courseName)
        return self._courseName

    @property
    def courseOpenId(self):
        return self._courseOpenId

    @property
    def workExamType(self):
        return self._workExamType

    @workExamType.setter
    def workExamType(self, workExamType):
        self._workExamType = workExamType

    # 所用时间
    @property
    def useTime(self):
        return random.randint(220, 520)

    def getLessoning(self) -> dict:
        """
        获取正在进行的课程
        :return: 进行中的课程字典
        """
        res = super().session.get(
            self.URL_GET_LESSON_ING,
            headers=super().headers
        ).json()

        # print('正在进行的课程', res)
        return res['list']


    # 展示课程详情
    def showCourseDetail(self):
        courseOpenId = self.courseOpenId
        try:
            res = super().session.post(
                self.URL_GET_LESSON_DETAIL,
                {'courseOpenId': courseOpenId},
                headers=super().headers
            ).json()
            info = res['learnInfo']

            return {
                'code': res['code'],
                'process': info['process']
            }
        except:
            self.moocBox.moocWorkLog('>> 获取课程详情失败，将尝试自动重连，请等待两分钟！')
            if glo.reLogin():
                self.moocBox.moocWorkLog('重连成功！')
                print('自动重连成功')

    def getWorkList(self) -> list:
        """
        获取作业列表
        :return: 所有课程列表
        """
        data = {
            'pageSize': 5000,
            'page': 1,
            'workExamType': self._workExamType,
            'courseOpenId': self._courseOpenId
        }

        n = 0
        while True:
            try:
                res = super().session.post(
                    self.URL_GET_WORK,
                    data=data,
                    headers=super().headers
                ).json()
                break
            except json.decoder.JSONDecodeError:
                print('mooc模块 line 174')
                print('getWorkList函数执行有误')
                time.sleep(.2)
                n += 1
                if n > 10:
                    print('getWorkList函数执行有误，程序奔溃')
                    break
                continue
            except requests.exceptions.ConnectionError:
                print('网络出错')
                self.moocBox.moocWorkLog('网络出错！请重新打开本软件')

        # 课程列表
        courseList = list()
        for infoList in res['list']:
            courseList.append(
                {
                    'Title': infoList['Title'],
                    'courseOpenId': self._courseOpenId,
                    'workExamId': infoList['Id'],
                    'workExamType': self._workExamType,
                    'Score': infoList['getScore'],
                    # 是否可做
                    'canDo': self.getWorkInfo(
                        self._courseOpenId,
                        infoList['Id'],
                        self._workExamType
                    ),
                    'isOver': infoList['isOver']
                }
            )
        return courseList

    def checkHaveOver(self):
        """
        检查是否有已截止的测验
        :return:
        """
        for i in range(0, 3):
            time.sleep(.8)
            if i == 0:
                self.moocBox.moocWorkLog('正在检查作业是否有已截止测验')
            elif i == 1:
                self.moocBox.moocWorkLog('正在检查测验是否有已截止测验')
            elif i == 2:
                self.moocBox.moocWorkLog('正在检查考试是否有已截止测验')

            # 依次遍历 作业，测验，考试
            data = {
                'pageSize': 5000,
                'page': 1,
                'workExamType': i,
                'courseOpenId': self._courseOpenId
            }
            res = super().session.post(
                self.URL_GET_WORK,
                data=data,
                headers=super().headers
            ).json()

            for infoList in res['list']:
                # 如果有已截止的
                if infoList['isOver']:
                    # 说明有已截止的课程，全部完成时需要弹出警告
                    return True
        return False


    def getWorkInfo(self, courseOpenId: str, workExamId: str, workExamType: int) -> bool:
        """
        获取测验详细信息，没有什么大用处
        :param courseOpenId: 课程ID, str
        :param workExamId: 测验ID, str
        :param workExamType: 测验类型, int
        :return: ReplyCount和stuWorkCount比较的结果，为T时可做，F时说明两值相等
        """
        res = ''
        data = {
            'courseOpenId': courseOpenId,
            'workExamId': workExamId,
            'workExamType': workExamType
        }

        n = 0
        while True:
            try:
                res = super().session.post(
                    self.URL_GET_WORK_INFO,
                    data=data,
                    headers=super().headers
                ).json()
                break
            except json.decoder.JSONDecodeError:
                print('mooc模块 line 211')
                print('getWorkInfo函数执行有误')
                time.sleep(.2)
                n += 1
                if n > 10:
                    print('getWorkInfo函数执行有误，程序奔溃')
                    break
                continue

        return res['workExam']['ReplyCount'] != res['workExam']['stuWorkCount']

    def examPreview(self, workExamId: str, agreeHomeWork: str, workExamType: int) -> dict:
        """
        测验界面
        :param workExamId: 测验ID, str
        :param agreeHomeWork: 测验是否可做, str
        :param workExamType: 测验类型, int
        :return: 保存答案需要的一切
        """
        data = {
            'courseOpenId': self._courseOpenId,
            'workExamId': workExamId,
            'agreeHomeWork': agreeHomeWork,
            'workExamType': workExamType
        }
        while True:
            try:
                res = super().session.post(
                    self.URL_PAGE,
                    data=data,
                    headers=super().headers
                ).json()
                break
            except:
                time.sleep(.5)
                continue

        return {
            'uniqueId': res['uniqueId'],
            'workExamId': workExamId,
            'workExamType': workExamType,
            'title': res['homework']['Title']
        }

    def saveAnswer(self, uniqueId: str, workExamId: str, workExamType: int, title: str):
        """
        保存答案
        :param uniqueId: str
        :param workExamId: str
        :param workExamType: str
        :param title: 该测验的标题
        :return:
        """
        res = dict()
        # 如果是考试
        if workExamType == 2:
            data = {
                'uniqueId': uniqueId,
                'examId': workExamId,
                'workExamType': workExamType,
                'courseOpenId': self._courseOpenId,
                'examStudentId': 0,
                'useTime': self.useTime
            }
            res = super().session.post(
                self.URL_POST_EXAM_SAVE,
                data=data,
                headers=super().headers
            ).json()
        else:
            data = {
                'uniqueId': uniqueId,
                'workExamId': workExamId,
                'workExamType': workExamType,
                'courseOpenId': self._courseOpenId,
                'paperStructUnique': 0,
                'useTime': self.useTime
            }

            n = 0
            while True:
                try:
                    res = super().session.post(
                        self.URL_POST_ANSWER_SAVE,
                        data=data,
                        headers=super().headers
                    ).json()
                    break
                except json.decoder.JSONDecodeError:
                    print('mooc模块 line 321')
                    print('saveAnswer函数执行有误')
                    time.sleep(.2)
                    n += 1
                    if n > 10:
                        print('saveAnswer函数执行有误，程序奔溃')
                        break
                    continue

        try:
            if res['code'] == -2:
                exit(res['msg'])
            elif res['code'] == 1:
                self.moocBox.moocWorkLog('>>' + title + '已提交答案')
        except TypeError:
            self.moocBox.moocWorkLog('>>' + title + '已提交答案')
        except KeyError:
            self.moocBox.moocWorkLog('连接智慧职教失败，请检查网络或智慧职教能否正常访问！')
            return

    def getExamDetail(self, workExamId: str) -> str:
        """
        获取测验细节，该函数只为获取答案的参数studentWorkId
        :param workExamId: 测验ID, str
        :return: studentWorkId
        """
        data = {
            'courseOpenId': self._courseOpenId,
            'workExamId': workExamId,
            'workExamType': self._workExamType
        }
        res = super().session.post(
            self.URL_GET_EXAM_DETAIL,
            data=data,
            headers=super().headers
        ).json()

        return res['list'][0]['Id']

    def getAnswer(self, workExamId: str, workExamType: int, studentWorkId: str) -> dict:
        """
        获取答案
        :param workExamId:
        :param workExamType:
        :param studentWorkId:
        :return: 保存答案需要的值
        """
        data = {
            'courseOpenId': self._courseOpenId,
            'workExamId': workExamId,
            'studentWorkId': studentWorkId,
            'workExamType': workExamType
        }
        res = super().session.post(
            self.URL_GET_ANSWER,
            data=data,
            headers=super().headers
        ).json()
        return {
            'fileName': res['homework']['Title'],
            'answerType': workExamType,
            'answerText': res['workExamData'],
            'courseOpenId': self._courseOpenId,
            'courseName': self._courseName,
            'workExamId': workExamId
        }

    def postAnswer(self, question: dict, uniqueId: str, workExamType: int) -> bool:
        """
        提交答案
        :param question:
        :param uniqueId:
        :param workExamType:
        :return:
        """
        i = 1
        isHaveFileQuestion = False
        # print('测试', question)
        for questionId in question:
            time.sleep(.5)

            def online():
                if question[questionId]['questionType'] == 4 or question[questionId]['questionType'] == 6\
                        or question[questionId]['questionType'] == 5:
                    return 0
                return 1

            def answer(d: dict) -> dict:
                """
                还是为了填空写的一个函数
                如果此题不为填空题,直接添加一个answer，值为
                向data添加一个answerJson参数,传入答案
                循环答案，根据答案的长度，添加若干answer参数，值为对应索引的content
                =============================================================
                匹配题
                """
                # print('进入answer')
                if question[questionId]['questionType'] != 4 and question[questionId]['questionType'] != 5:
                    d['answer'] = question[questionId]['answer']
                    return d
                # 下面为填空题
                d['answer'] = ''
                d['answerJson'] = json.dumps(question[questionId]['answer'])
                # print("question[questionId]['answer']", json.dumps(question[questionId]['answer']))
                d['workExamType'] = workExamType
                # print('转为', json.dumps(question[questionId]['answer']))
                return d

            # 当前模块为考试
            if workExamType == 2:
                # 阅读理解
                if questionId == 'subQuestions' and question['subQuestions'] != '':
                    # print('测试question[subQuestions]', question['subQuestions'])
                    for subIndex in range(len(question['subQuestions'])):
                        subQuestion = question['subQuestions'][subIndex]
                        data = {
                            'answer': subQuestion['answer'],
                            'questionId': subQuestion['questionId'],
                            'subQuestionId': subQuestion['subQuestionId'],
                            'subScore': subQuestion['subScore'],
                            'uniqueId': uniqueId
                        }
                        super().session.post(
                            self.URL_POST_EXAM_ANSWER_Sub,
                            data=data,
                            headers=super().headers
                        )
                else:
                    data = {
                        'studentWorkId': '',
                        'questionId': questionId,
                        'answer': question[questionId]['answer'],
                        'paperStuQuestionId': '',
                        'questionType': question[questionId]['questionType'],
                        'online': online(),
                        'userId': '',
                        'uniqueId': uniqueId
                    }
                    data = answer(d=data)
                    # print('测试workExam data', data)
                    if question[questionId]['questionType'] != 5:
                        # 一般题
                        super().session.post(
                            self.URL_POST_EXAM_ANSWER,
                            data=data,
                            headers=super().headers
                        )
                    else:
                        # 填空题
                        super().session.post(
                            self.URL_POST_EXAM_ANSWER_FILL,
                            data=data,
                            headers=super().headers
                        )
            # 当前模块为作业或测验
            else:
                if questionId == 'subQuestions':
                    continue
                data = {
                    'questionId': questionId,
                    'online': online(),
                    'questionType': question[questionId]['questionType'],
                    'uniqueId': uniqueId
                }
                data = answer(d=data)
                res = ...
                if question[questionId]['questionType'] != 4 and question[questionId]['questionType'] != 5\
                        and question[questionId]['questionType'] != 7 and question[questionId]['questionType'] != 8\
                        and question[questionId]['questionType'] != 9 and question[questionId]['questionType'] != 10:
                    n = 0
                    while True:
                        try:
                            res = super().session.post(
                                self.URL_POST_ANSWER,
                                data=data,
                                headers=super().headers,
                            ).json()
                            break
                        except json.decoder.JSONDecodeError:
                            print('mooc模块 line 491')
                            print('postAnswer函数执行有误')
                            time.sleep(.2)
                            n += 1
                            if n > 10:
                                print('postAnswer函数执行有误，程序奔溃')
                                break
                            continue
                # 匹配题
                elif question[questionId]['questionType'] == 7:
                    res = super().session.post(
                        self.URL_POST_ANSWER_Match,
                        data=data,
                        headers=super().headers,
                    ).json()
                # 阅读理解题
                elif question[questionId]['questionType'] == 8:
                    answer = data['answer']
                    # 'answer': [{'Id': 'bkq4av2s57zd2r3yk8tzwa', 'answer': 0},
                    for subList in answer:
                        data['subQuestionId'] = subList['Id']
                        data['answer'] = subList['answer']
                        res = super().session.post(
                            self.URL_POST_ANSWER_Sub,
                            data=data,
                            headers=super().headers,
                        ).json()
                # 完形填空题
                elif question[questionId]['questionType'] == 9:
                    answer = data['answer']
                    # 'answer': [{'Id': 'bkq4av2s57zd2r3yk8tzwa', 'answer': 0},
                    # print('这里是完形填空', answer)
                    for subList in answer:
                        data['subQuestionId'] = subList['Id']
                        data['answer'] = subList['answer']
                        data['workExamType'] = workExamType
                        data['uniqueId'] = uniqueId
                        time.sleep(.2)
                        res = super().session.post(
                            self.URL_POST_ANSWER_Sub,
                            data=data,
                            headers=super().headers,
                        ).json()
                elif question[questionId]['questionType'] == 10:
                    self.moocBox.moocWorkLog('>> ****** 文件做答题无法完成！请自行完成 ******')
                    isHaveFileQuestion = True
                    i = i + 1
                    continue
                else:
                    # 填空题
                    # print(question[questionId]['questionType'], '填空填空填空填空填空填空填空填空', data)
                    n = 0
                    while True:
                        try:
                            res = super().session.post(
                                self.URL_POST_ANSWER_FILL,
                                data=data,
                                headers=super().headers,
                            ).json()
                            break
                        except json.decoder.JSONDecodeError:
                            print('mooc模块 line 511')
                            print('getProcessList函数执行有误')
                            time.sleep(.2)
                            n += 1
                            if n > 10:
                                print('getProcessList函数执行有误，程序奔溃')
                                break
                            continue
                    # print(data)
                # utils.checkCode(res)

            self.moocBox.moocWorkLog(f'> 已完成第 {i} 题')
            i = i + 1
        return isHaveFileQuestion

    # ****** 观看视频部分 ******
    # 获取课程模块ID
    def getProcessList(self) -> list:
        data = {
            'courseOpenId': self.courseOpenId
        }

        n = 0
        while True:
            try:
                res = super().session.post(
                    self.URL_GET_MODULE_ID,
                    data=data,
                    headers=super().headers
                ).json()
                break
            except json.decoder.JSONDecodeError:
                print('mooc模块 line 541')
                print('getProcessList函数执行有误')
                time.sleep(.2)
                n += 1
                if n > 10:
                    print('getProcessList函数执行有误，程序奔溃')
                    break
                continue

        # self.moocBox.moocWorkLog(res)
        return res['proces']['moduleList']

    # 获取缩放ID
    def getTopicByModuleId(self, moduleId: str) -> list:
        data = {
            'courseOpenId': self.courseOpenId,
            'moduleId': moduleId
        }

        n = 0
        while True:
            try:
                res = super().session.post(
                    self.URL_GET_TOPIC,
                    data=data,
                    headers=super().headers
                ).json()
                break
            except json.decoder.JSONDecodeError:
                print('mooc模块 line 568')
                print('getTopicByModuleId函数执行有误')
                time.sleep(.2)
                n += 1
                if n > 10:
                    print('getTopicByModuleId函数执行有误，程序奔溃')
                    break
                continue
        # print('缩放ID', res['topicList'])
        return res['topicList']

    # 获取模块详情
    def getCellByTopicId(self, topicId: str) -> list:
        data = {
            'courseOpenId': self.courseOpenId,
            'topicId': topicId
        }

        n = 0
        while True:
            try:
                res = super().session.post(
                    self.URL_GET_MODULE_DETAIL,
                    data=data,
                    headers=super().headers
                ).json()
                break
            except json.decoder.JSONDecodeError:
                print('mooc模块 line 622')
                print('getCellByTopicId函数执行有误')
                time.sleep(.2)
                n += 1
                if n > 10:
                    print('getCellByTopicId函数执行有误，程序奔溃')
                    break
                continue
        return res['cellList']

    # 获取视频长度
    def getViewTime(self, moduleId, cellId):
        # return 9999
        # print(moduleId, cellId)
        # print('执行到获取视频长度')
        data = {
            'courseOpenId': self.courseOpenId,
            'cellId': cellId,
            'fromType': 'stu',
            'moduleId': moduleId
        }
        # print(data)
        try:
            res = super().session.post(
                self.URL_GET_VIEW_LENGTH,
                data=data,
                headers=super().headers
            ).json()
            # print('视频长度', res)
        except json.decoder.JSONDecodeError:
            self.moocBox.moocWorkLog('获取视频长度失败！使用默认时间设置，请自行检查课程是否完成')
            return 1200
        return res['courseCell']['VideoTimeLong']

    # 提交学习时长
    def postStudentTime(self, moduleId, cellId, moculeName):
        videoTimeTotalLong = self.getViewTime(moduleId, cellId)
        auvideoLength = videoTimeTotalLong + 100
        # if auvideoLength <= videoTimeTotalLong:
        #     auvideoLength = 9999
        # print('使用时间', auvideoLength)
        # 携带参数获取视频长度
        data = {
            'courseOpenId': self.courseOpenId,
            'moduleId': moduleId,
            'cellId': cellId,
            'auvideoLength': auvideoLength,
            'videoTimeTotalLong': self.getViewTime(moduleId, cellId),
            # 'sourceForm': sourceForm
        }
        # print('学习时长', data)
        while True:
            try:
                res = super().session.post(
                    self.URL_POST_STUDY_TIME,
                    data=data,
                    headers=super().headers
                ).json()
                break
            except:
                time.sleep(.5)
                print('提交学习时长出错')
                continue

        if res['code'] != 1:
            super().session.post(
                self.URL_POST_STUDY_TIME,
                data=data,
                headers=super().headers
            )
        return {
            'code': res['code'],
            'name': moculeName
        }

    # 讨论任务
    def talkTask(self, topicId: str):
        data = {
            'courseOpenId': self.courseOpenId,
            'topicId': topicId
        }
        super().session.post(
            self.URL_GET_TALKTASK,
            data=data,
            headers=super().headers
        )

    # 获取用户信息
    def getUser(self):
        res = super().session.get(
            self.URL_GET_USER_INFO,
            headers=super().headers
        ).json()

        return {
            'userId': res['id'],
            'userName': res['userName'],
            'displayName': res['displayName']
        }

    # 退出加入课程
    def quitAndJoin(self):
        # 获取用户ID
        userId = self.getUser()['userId']

        # 退出课程
        quitData = {
            'courseOpenId': self.courseOpenId,
            'userId': userId
        }
        res = super().session.post(
            self.URL_POST_QUIT_LESSON,
            data=quitData,
            headers=super().headers
        ).json()

        if res['code'] != 1:
            return

        joinData = {
            'courseOpenId': self.courseOpenId,
            'courseId': '',
            'verifycode': ''
        }
        res = super().session.post(
            self.URL_POST_JOIN_LESSON,
            data=joinData,
            headers=super().headers
        ).json()

        n = 1
        # 选课人数过多的情况
        if res['code'] == -2:
            try:
                while n < 10:
                    # 如果服务器禁止使用验证码识别
                    if not glo.verify.joinCourse:
                        return False

                    # 获取验证码图片数据
                    imgData = super().session.get(
                        url='https://mooc-old.icve.com.cn/portal/LoginMooc/getVerifyCode?ts=1652073790246',
                        headers=super().headers
                    ).content

                    # 获取验证码
                    verifycode = self.ocrVerify(imgData)

                    joinData = {
                        'courseOpenId': self.courseOpenId,
                        'courseId': '',
                        'verifycode': verifycode
                    }
                    # 申请加入课程
                    res = super().session.post(
                        self.URL_POST_JOIN_LESSON,
                        data=joinData,
                        headers=super().headers
                    ).json()

                    time.sleep(1)
                    n += 1
                    if res['code'] == 1:
                        break
            except:
                return False

        # {'code': -2, 'msg': '当前课程今日选课人数较多，请输入验证码后进行选课', 'need_verifycode': True}
        if res['code'] != 1:
            return False
        return True

    # 识别验证码
    def ocrVerify(self, imgData: bytes) -> str:
        # 如果加入课程
        if glo.verify.joinCourse:
            code = glo.verify.postCaptchaGetCode(imgData)
            print('课程加入验证码为', code)
            self.moocBox.moocWorkLog('识别到验证码为' + code)
            return code
        return ''
