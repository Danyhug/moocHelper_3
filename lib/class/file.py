"""
文件读写
更改策略：
    单击按钮时，弹出确定框，是否要获取答案
    确定框文本：
        是否要获取答案（确定会使用本账号获取答案，取消会直接使用本地答案）
            确定 取消
        确定 -> 不扣除积分，获取答案
            -> 该答案本地答案已有，跳过获取
            -> 该答案本地答案未有，获取答案
                -> 答案获取完成
                -> 弹出确定框，是否要
Created by Danyhug on 2021-01-30 22:00
Coding by Danyhug on 2021-02-01 15:00
"""
import os
import base64
import json
import re
from bs4 import BeautifulSoup


class File:
    def __init__(self):
        # 进入答案文件夹
        try:
            os.mkdir('answerFile')
        except FileExistsError:
            print('答案文件夹已存在')

        # 当前课程openID
        self.openID = ''

    # 将self.moocBox绑定主界面的moocBox，可以使用主界面的函数
    def setMoocBox(self, moocBox):
        self.moocBox = moocBox
        self.moocBox.moocWorkLog('文件配置已就绪')

    # 创建需要的目录
    # openID
    #   -> work
    #   -> test
    #   -> exam
    def createNeedFile(self, courseOpenId, courseName):
        # 查看当前是否已初始化
        try:
            if self.answerFile:
                # 说明已初始化完成
                if self.openID == courseOpenId:
                    # 说明文件当前ID与课程ID相同
                    # 跳过生成
                    return
        except AttributeError:
            pass
        finally:
            self.openID = courseOpenId

        # 获取到当前路径
        nowPath = os.getcwd() + '/answerFile/'

        # 需要的几个文件
        # 创建openID目录
        try:
            # 尝试创建
            os.mkdir(nowPath + courseOpenId)
            # 创建dhg配置文件
            print(nowPath + courseOpenId + '/' + courseName + '.dhg', 'a')
            open(nowPath + courseOpenId + '/' + courseName + '.dhg', 'a').close()
        except FileExistsError:
            self.moocBox.moocWorkLog('测验目录已存在')
        except:
            self.moocBox.moocWorkLog('权限不足，请以管理员权限运行程序！教程在使用手册')
            return
        finally:
            nowPath += courseOpenId

        # 获取测验目录的文件
        nowPathList = os.listdir('answerFile/' + courseOpenId)
        # 作业 测验 考试
        needFileList = ['work', 'test', 'exam']
        # 查看需要的几个文件是否存在
        for needFile in needFileList:
            # 默认当前目录没有需要的文件
            isHave = False
            # 当前目录的文件
            for nowFile in nowPathList:
                print(needFile, '------------', nowFile)
                # 说明该目录已存在，不需要创建
                if nowFile == needFile:
                    isHave = True
                    continue
            # 如果当前目录没有
            if not isHave:
                # 则进入答案路径新建
                os.mkdir(nowPath + '/' + needFile)
                self.moocBox.moocWorkLog('已新建目录' + needFile)

        self.answerFile = nowPath + '/'
        self.workFile = nowPath + '/work/'
        self.testFile = nowPath + '/test/'
        self.examFile = nowPath + '/exam/'

    def haveQuestionskip(self, courseOpenId, courseName, workExamId):
        # 本地已有该测验答案，跳过
        try:
            fo = open(self.answerFile + courseName + '.dhg', 'r')
        except FileNotFoundError:
            # 无该文件
            self.moocBox.moocWorkLog('无该文件')
            return False

        try:
            data = json.loads(fo.read())  # 获得里面的内容
            fo.close()
        # 里面可能为空
        except json.decoder.JSONDecodeError:
            return False
        # 如果文件中有该id
        if workExamId in data.values():
            return True
        return False

    # 保存文件
    def saveFile(self, fileName: str, answerType, answerText, courseOpenId, courseName, workExamId):
        # 文件名 + 后四位的测验ID
        # 因为有些课程会有同名ID, 为了防止同名测验被覆盖, 所以加上ID后四位
        fileName += workExamId[-4:]
        # 将答案文本进行加密 utf8编码再base64编码 de
        answerText = base64.b64encode(answerText.encode())
        # 判断答案类型进入不同目录 0 作业 1 测验 2 考试
        # 进入答案目录
        if answerType == 0:
            # 作业答案
            dirName = self.workFile
        elif answerType == 1:
            # 测验答案
            dirName = self.testFile
        else:
            # 考试答案
            dirName = self.examFile
        # 写入二进制数据
        fileName = re.sub(r'[/:*?"><|\\]', 'YY', fileName)
        fo = open(dirName + fileName + '.hpc', 'wb')

        fo.write(answerText)
        fo.close()
        # 更改dhg文件
        try:
            fo = open(self.answerFile + courseName + '.dhg', 'r')  # 打开课程文件
        except FileNotFoundError:
            # 可能是因为文件名被正则修改了
            # 将文件名正则匹配后再使用
            courseName = re.sub(r'[/:*?"><|\\]', 'YY', courseName)
            fo = open(self.answerFile + courseName + '.dhg', 'r')  # 打开课程文件

        try:
            data = json.loads(fo.read())  # 获得里面的内容
        # 里面可能为空
        except json.decoder.JSONDecodeError:
            data = dict()
        fo.close()  # 关闭
        data[fileName] = workExamId  # 添加新字典
        fo = open(self.answerFile + courseName + '.dhg', 'w')
        fo.write(json.dumps(data))  # 将新字典写入
        fo.close()  # 关闭

        return '>>> 保存成功'

    def readAnswer(self, courseOpenId: str, courseName: str, workExamType: int, allCourse: list) -> dict:
        """
        首先将所有课程与本地课程答案对比,将本地目录有答案的课程取出,
        调用useLocalGetAnswer函数,获取相关测验答案
        :param courseOpenId: 课程ID, str
        :param courseName: 课程名, str
        :param workExamType: 测验类型, int
        :param allCourse: 所有课程, list
        :return: 本课程指定模块所有测验答案
        """
        # 获取本地答案
        # 打开目录
        dirName = self.answerFile
        # 加载本地json配置文件
        fo = open(dirName + courseName + '.dhg', 'r')
        print('测试', dirName + courseName + '.dhg')
        try:
            data = json.loads(fo.read())
            print('测试data', data)
        except json.decoder.JSONDecodeError:
            data = dict()
            self.moocBox.moocWorkLog('有错误,当前目录无答案,请认真查看软件使用说明！')
            return {'state': False}
        # print('读取', data)
        tempQuestion = list()  # 需要做的题
        if workExamType == 0:
            doDirName = self.workFile
        elif workExamType == 1:
            doDirName = self.testFile
        elif workExamType == 2:
            doDirName = self.examFile

        # 本测验答案
        allAnswer = {'state': True}
        # 遍历目录下的文件
        for file in os.listdir(doDirName):
            # 遍历配置文件键值
            haveAns = False  # 默认没有答案
            for conf in data:
                print('测试conf', conf)
                # print('conf ', conf, ' file ', file)
                if file == conf + '.hpc':
                    # 本地答案有并且配置文件也有相关数据
                    haveAns = True
                    # 遍历所有课程
                    for index in range(len(allCourse)):
                        # 如果配置文件有本课程
                        if allCourse[index]['workExamId'] == data[conf]:
                            # 此时,本地确定有该测验答案,调用useLocal
                            # allAnswer应当为一个字典 键值为测验ID 值是问题ID: 答案
                            allAnswer[allCourse[index]['workExamId']] = self.useLocalGetAnswer(file=doDirName + file)
                            # 将此文件添加到临时课程
                            break

            # 没有答案直接退出本次循环
            if not haveAns:
                self.moocBox.moocWorkLog('没有', file, '答案,跳过此测验')
                continue

        # 答案列表
        return allAnswer

    @staticmethod
    # 使用本地文件获取答案
    def useLocalGetAnswer(file: str) -> dict:
        """
        使用本地文件获取答案，一次获取一个测验
        :param file:
        :return: answer 题ID: 题答案
        """
        # print('useLocal的tempQuestion', tempQuestion)
        # 只读方式打开
        fileContent = open(file, 'r').read()
        # base64 解码 再 utf8解码
        fileContent = base64.b64decode(fileContent).decode()
        jsonContent = json.loads(fileContent)
        # questionType 2 客观 1 单选
        # print(jsonContent['questions'][2]['questionType'])
        # answer是一个字典, 题ID: 题答案
        answer = dict()
        # answerDetail是一个字典, 类型, 题答案
        answerDetail = dict()
        for questionList in jsonContent['questions']:
            # 判断是否有多个答案 目前用来处理填空题
            def haveAnswers():
                answersList = list()
                # 有多个答案
                if len(questionList['answerList']) >= 1:
                    for answerListItem in questionList['answerList']:
                        # print('有多个答案')
                        content = BeautifulSoup(answerListItem['Content'], features="html.parser").text
                        answersList.append({
                            'SortOrder': answerListItem['SortOrder'],
                            # 去除首尾空格
                            'Content': content.strip()
                        })

                    return answersList
                return ''.join(questionList['Answer'])

            # 单选
            if questionList['questionType'] == 1:
                abcd = 0
                abcdOption = list()
                answerLen = len(questionList['answerList'])
                for answerList in questionList['answerList']:
                    # A B C D E ...
                    if abcd < answerLen:
                        abcdOption.append(answerList['IsAnswer'])
                    abcd = abcd + 1
                # print('单选答案', abcdOption.index('true'))
                try:
                    answer[questionList['questionId']] = abcdOption.index('true')
                except ValueError:
                    print('** 该题可能答案有误，正在使用AI模拟答案')
                    answer[questionList['questionId']] = questionList['Answer']
            # 多选
            elif questionList['questionType'] == 2:
                # print('多选答案', questionList['Answer'])
                answer[questionList['questionId']] = questionList['Answer']
            # 判断
            elif questionList['questionType'] == 3:
                # print('判断答案', questionList['Answer'])
                answer[questionList['questionId']] = questionList['Answer']
            # 填空
            elif questionList['questionType'] == 4 or questionList['questionType'] == 5:
                # print('填空答案', ''.join(questionList['Answer']))
                # answer[questionList['questionId']] = ''.join(questionList['Answer'])
                answer[questionList['questionId']] = haveAnswers()
            # 客观
            elif questionList['questionType'] == 6:
                # print('客观答案', ''.join(questionList['Answer']))
                answer[questionList['questionId']] = ''.join(questionList['Answer'])
            # 匹配
            elif questionList['questionType'] == 7:
                optionList = list()
                for answerList in questionList['answerList']:
                    # [1, 0, 3, 4, 5]
                    optionList.append(int(answerList['OptionSelectContent']))
                # print('单选', abcdOption)
                # print('单选答案', abcdOption.index('true'))
                answer[questionList['questionId']] = optionList
            # 阅读理解
            elif questionList['questionType'] == 8:
                subAnswer = jsonContent['subQuestions']
                subList = list()
                for subAnswerList in subAnswer:
                    # [1, 0, 3, 4, 5]
                    subList.append({
                        'Id': subAnswerList['subQuestion'][0]['Id'],
                        'answer': subAnswerList['subQuestion'][0]['questionAnswer']
                    })
                    answer[questionList['questionId']] = subList
            # 完形填空
            elif questionList['questionType'] == 9:
                subAnswer = jsonContent['subQuestions']
                subList = list()
                for subAnswerList in subAnswer:
                    # [1, 0, 3, 4, 5]
                    subList.append({
                        'questionId':subAnswerList['QuestionId'],
                        'online': 1,
                        'Id': subAnswerList['subQuestion'][0]['Id'],
                        'answer': subAnswerList['subQuestion'][0]['questionAnswer']
                    })
                    answer[questionList['questionId']] = subList
            else:
                # print('未知类型', ''.join(questionList['Answer']))
                answer[questionList['questionId']] = ''.join(questionList['Answer'])
            # html读内容的bug 使用这个临时修补一下
            if answer[questionList['questionId']] == '':
                answer[questionList['questionId']] = questionList['Answer']
                # print('修正答案', questionList['Answer'])

            answerDetail[questionList['questionId']] = {
                'questionType': questionList['questionType'],
                'answer': answer[questionList['questionId']],
            }

        # 小题的答案
        subAnswer = list()
        # 负责处理考试中的阅读理解题
        for questionList in jsonContent['subQuestions']:
            # 该问题ID
            questionID = questionList['QuestionId']
            # 小题的信息
            subAnswerQuestion = dict()
            # 遍历该问题的小题
            for subQuestion in questionList['subQuestion']:
                subAnswerQuestion = {
                    'questionId': questionID,
                    'subQuestionId': subQuestion['Id'],
                    'answer': subQuestion['questionAnswer'],
                    'subScore': subQuestion['subScore'],
                }
            subAnswer.append(subAnswerQuestion)

        if subAnswer:
            answerDetail['subQuestions'] = subAnswer

        # 返回该测验的答案字典
        return answerDetail
