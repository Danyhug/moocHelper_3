"""
zjy类
这里定义有关职教云的一切
Created by Danyhug on 2021-07-09 11:05
Coding by Danyhug on 2021-07-11 09:00
Update by Danyhug on 2021-09-05 20.11 - moocHelper 3.0
"""
import json
import time

import requests
import utils

import globalData as glo
import conf

class Zjy(utils.Utils):
    # ******URL******
    # 获取用户信息
    URL_GET_USER_INFO = 'https://zjy2.icve.com.cn/api/student/stuInfo/getStuInfo'
    # 获取正在进行的课程
    URL_GET_LESSON_ING = 'https://zjy2.icve.com.cn/api/student/learning/getLearnningCourseList'
    # 获取课程模块ID
    URL_GET_MODULE_ID = 'https://zjy2.icve.com.cn/api/study/process/getProcessList'
    # 获取缩放ID
    URL_GET_TOPIC = 'https://zjy2.icve.com.cn/api/study/process/getTopicByModuleId'
    # 获取模块详情
    URL_GET_MODULE_DETAIL = 'https://zjy2.icve.com.cn/api/study/process/getCellByTopicId'
    # 获取视频详情
    URL_GET_VIDEO_DETAIL = 'https://zjy2.icve.com.cn/api/common/Directory/viewDirectory'
    # 提交学习时长
    URL_POST_STUDY_TIME = 'https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog'
    # 获取课程进度
    URL_GET_PROCESS = 'https://zjy2.icve.com.cn/api/student/learning/getLearnningCourseList'
    # 更新状态
    URL_POST_CHANGE_DATA = 'https://zjy2.icve.com.cn/api/common/Directory/changeStuStudyProcessCellData'
    # 职教云评价
    URL_POST_ADD_ACTIVITY = 'https://zjy2.icve.com.cn/api/common/Directory/addCellActivity'

    def __init__(self):
        # 课程名
        self.courseName = ''
        # 课程ID
        self.courseOpenId = ''
        # 开放教室ID
        self.openClassId = ''
        # 是否为危险人群(易被封号)
        self.risk = False
        # 职教云提交请求延迟
        self.defaultDelay = 5
        # 已被检测出异常的次数
        self.exceptionNum = 0

    # 将self.moocBox绑定主界面的moocBox，可以使用主界面的函数
    def setZjyBox(self, zjy):
        self.zjy = zjy
        self.zjy.workLog('职教云配置已就绪')

    # 获取用户信息
    def getUserInfo(self) -> dict:
        res = super().session.get(
            self.URL_GET_USER_INFO,
            headers=super().headers
        ).json()
        if res['code'] == 1:
            data = res['stu']
            # 获取成功
            return {
                'name': data['Name'],
                'stu': data['StuNo'],
                'school': data['SchoolName']
            }

        return {
            'name': '社会学习者',
            'stu': '20021008',
            'school': 'Social University'
        }

    def getLessoning(self) -> dict:
        """
        获取正在进行的课程
        :return: 进行中的课程字典
        """
        res = super().session.get(
            self.URL_GET_LESSON_ING,
            headers=super().headers
        ).json()

        courseList = list()
        for course in res['courseList']:
            courseList.append({
                'courseName': course['assistTeacherName'] + '-' + course['courseName'],
                'courseOpenId': course['courseOpenId'],
                'openClassId': course['openClassId']
            })
        # 将课程名变为 老师名-课程名
        # 课程列表
        return courseList

    # 获取课程模块ID
    def getProcessList(self) -> list:
        data = {
            'courseOpenId': self.courseOpenId,
            'openClassId': self.openClassId
        }
        try:
            res = super().session.post(
                self.URL_GET_MODULE_ID,
                data=data,
                headers=super().headers
            ).json()
        except:
            res = super().session.post(
                self.URL_GET_MODULE_ID,
                data=data,
                headers=super().headers
            ).json()
        print(res)
        try:
            return res['progress']['moduleList']
        except KeyError:
            self.zjy.workLog('登录状态失效，将尝试重新登录，请等待两分钟！')
            if glo.reLogin():
                self.zjy.workLog('重连成功！')
                print('自动重连成功')
            else:
                return

    # 获取缩放ID
    def getTopicByModuleId(self, moduleId: str) -> list:
        data = {
            'courseOpenId': self.courseOpenId,
            'moduleId': moduleId
        }
        try:
            res = super().session.post(
                self.URL_GET_TOPIC,
                data=data,
                headers=super().headers
            ).json()
        except json.decoder.JSONDecodeError:
            print('*** 获得小模块出错，尝试修复 ***')
            res = super().session.post(
                self.URL_GET_TOPIC,
                data=data,
                headers=super().headers
            ).json()
        # print('缩放ID', res['topicList'])
        try:
            return res['topicList']
        except KeyError:
            time.sleep(50)
            res = super().session.post(
                self.URL_GET_TOPIC,
                data=data,
                headers=super().headers
            ).json()
            return res['topicList']

    # 获取模块详情
    def getCellByTopicId(self, topicId: str) -> list:
        data = {
            'courseOpenId': self.courseOpenId,
            'openClassId': self.openClassId,
            'topicId': topicId
        }
        try:
            res = super().session.post(
                self.URL_GET_MODULE_DETAIL,
                data=data,
                headers=super().headers
            ).json()
        except json.decoder.JSONDecodeError:
            print('*** 程序出错，尝试修复 ***')
            try:
                res = super().session.post(
                    self.URL_GET_MODULE_DETAIL,
                    data=data,
                    headers=super().headers
                ).json()
            except json.decoder.JSONDecodeError:
                self.zjy.workLog('等待20秒后继续任务······')
                time.sleep(20)
                res = super().session.post(
                    self.URL_GET_MODULE_DETAIL,
                    data=data,
                    headers=super().headers
                ).json()
        try:
            return res['cellList']
        except KeyError:
            res = super().session.post(
                self.URL_GET_MODULE_DETAIL,
                data=data,
                headers=super().headers
            ).json()
            return res['cellList']

    # 获取视频详情
    def getVideoDetail(self, moduleId: str, celld: str) -> dict:
        data = {
            'courseOpenId': self.courseOpenId,
            'openClassId': self.openClassId,
            'cellId': celld,
            'flag': 's',
            'moduleId': moduleId
        }
        try:
            res = super().session.post(
                self.URL_GET_VIDEO_DETAIL,
                data=data,
                headers=super().headers
            ).json()
        except:
            e = 1
            while e < 10:
                try:
                    res = super().session.post(
                        self.URL_GET_MODULE_ID,
                        data=data,
                        headers=super().headers
                    ).json()
                    break
                except requests.exceptions.JSONDecodeError:
                    e += 1
                    self.zjy.workLog('等待20秒后继续任务······')
                    time.sleep(20)
                    res = super().session.post(
                        self.URL_GET_MODULE_ID,
                        data=data,
                        headers=super().headers
                    ).json()
                    break
        print('测试', res)

        # 说明询问了是选择上次课程继续完成还是当前课程完成
        if res['code'] == -100:
            tempData = {
                'courseOpenId': self.courseOpenId,
                'openClassId': self.openClassId,
                'moduleId': moduleId,
                'cellId': celld,
                'cellName': '1.2反函数'
            }
            super().session.post(
                self.URL_POST_CHANGE_DATA,
                data=tempData,
                headers=super().headers
            )

        if res['code'] != 1:
            print('> 程序出错，尝试修复')
            res = super().session.post(
                self.URL_GET_VIDEO_DETAIL,
                data=data,
                headers=super().headers
            ).json()

        # 返回需要的数据
        try:
            return {
                'flag': res['flag'],
                'cellLogId': res['cellLogId'],
                'token': res['guIdToken'],
                'audioVideoLong': res['audioVideoLong'],
                'cellName': res['cellName'],
                'pageCount': res['pageCount']
            }
        except KeyError:
            print('res 错误', res)
            time.sleep(60)
            res = super().session.post(
                self.URL_GET_VIDEO_DETAIL,
                data=data,
                headers=super().headers
            ).json()
            return {
                'flag': res['flag'],
                'cellLogId': res['cellLogId'],
                'token': res['guIdToken'],
                'audioVideoLong': res['audioVideoLong'],
                'cellName': res['cellName'],
                'pageCount': res['pageCount']
            }


    # 提交评价
    def addCellActivity(self, cellId: str, content: str = '好') -> bool:
        data = {
            'courseOpenId': self.courseOpenId,
            'openClassId': self.openClassId,
            'cellId': cellId,
            'content': content,
            'docJson': '',
            'star': 5,
            'activityType': 1
        }
        res = super().session.post(
            self.URL_POST_ADD_ACTIVITY,
            data=data,
            headers=super().headers
        ).json()

        if res['code'] != 1:
            return False
        return True

    # 提交学习时长
    def postStudentTime(self, moduleId: str, cellId: str, categoryType: str):
        # 需要的数据
        needData = self.getVideoDetail(moduleId, cellId)
        # 提交的数据
        data = ''
        finalData = {}

        # 携带参数获取视频长度
        if categoryType == '视频':
            data = {
                'courseOpenId': self.courseOpenId,
                'openClassId': self.openClassId,
                'cellId': cellId,
                'cellLogId': needData['cellLogId'],
                'picNum': 0,
                'studyNewlyTime': needData['audioVideoLong'],
                'studyNewlyPicNum': 0,
                'token': needData['token']
                # 'sourceForm': sourceForm
            }
        elif categoryType == 'ppt' or categoryType == 'swf':
            # PPT有两个重要参数，picNum和studyNewlyPicNum，他们的值为pageCount
            data = {
                'courseOpenId': self.courseOpenId,
                'openClassId': self.openClassId,
                'cellId': cellId,
                'cellLogId': needData['cellLogId'],
                'picNum': needData['pageCount'],
                'studyNewlyTime': needData['audioVideoLong'],
                'studyNewlyPicNum': needData['pageCount'],
                'token': needData['token']
                # 'sourceForm': sourceForm
            }
        elif categoryType == '文档':
            data = {
                'courseOpenId': self.courseOpenId,
                'openClassId': self.openClassId,
                'cellId': cellId,
                'cellLogId': needData['cellLogId'],
                'picNum': needData['pageCount'],
                'studyNewlyTime': needData['audioVideoLong'],
                'studyNewlyPicNum': needData['pageCount'],
                'token': needData['token']
                # 'sourceForm': sourceForm
            }
        elif categoryType == '音频':
            data = {
                'courseOpenId': self.courseOpenId,
                'openClassId': self.openClassId,
                'cellId': cellId,
                'cellLogId': needData['cellLogId'],
                'picNum': needData['pageCount'],
                'studyNewlyTime': needData['audioVideoLong'],
                'studyNewlyPicNum': needData['pageCount'],
                'token': needData['token']
            }

        if data:
            finalData = data.copy()

        # 如果不是危险人群，直接提交数据
        if not self.risk:
            # 提交学习记录
            res = super().session.post(
                self.URL_POST_STUDY_TIME,
                data=data,
                headers=super().headers
            ).json()

            # 已被检测到异常学习，该用户为危险人群
            if res['code'] == -2:
                self.risk = True
                print('该用户为危险人群')
                self.zjy.workLog('警告：您为危险人群，已自动减缓课程完成速度！')

            # 如果提交有误,重新提交
            elif res['code'] != 1:
                res = super().session.post(
                    self.URL_POST_STUDY_TIME,
                    data=data,
                    headers=super().headers
                ).json()

        # 提交时长
        count = 25

        # 如果是危险人群，使用第二种提交办法
        if self.risk:
            # 分次数提交，每次提交10s
            num = needData['audioVideoLong'] / count   # 次数
            nowNum = 0  # 当前次数
            while num > 0:
                if not nowNum:
                    data['studyNewlyTime'] = 0.0
                else:
                    data['studyNewlyTime'] = count * nowNum + 0.871383

                n = 0
                while True:
                    try:
                        res = super().session.post(
                            self.URL_POST_STUDY_TIME,
                            data=data,
                            headers=super().headers
                        ).json()
                        break
                    except json.decoder.JSONDecodeError:
                        print('zjy模块 line 313')
                        print('postStudentTime函数执行有误')
                        time.sleep(.2)
                        n += 1
                        if n > 10:
                            print('postStudentTime函数执行有误，程序奔溃')
                            break
                        continue

                print('提交res', res)
                print('测试修补data', data)

                # 当前进度
                process = round(data['studyNewlyTime'] / needData['audioVideoLong'] * 100, 2)
                if categoryType == '音频':
                    self.zjy.workLog('当前音频完成进度：' + str(process) + '%')
                else:
                    self.zjy.workLog('当前视频完成进度：' + str(process) + '%')

                num -= 1
                nowNum += 1
                time.sleep(self.defaultDelay)

                if res['code'] == -2:
                    # 如果检测出来异常，则让延迟加1
                    self.defaultDelay += 1
                    nowNum -= 1
                    # 异常数+1
                    self.exceptionNum += 1
                    self.zjy.workLog('已被检测出异常，更新延迟为：' + str(self.defaultDelay))

                    # 如果异常数大于等于3，则返回101，软件退出
                    if self.exceptionNum >= 3:
                        return {
                            'code': -101
                        }
                elif res['code'] == -101:
                    print('有被检测出刷课的可能，软件已停止任务，请等待15分钟后再执行任务！')
                    self.zjy.workLog('有被检测出刷课的可能，软件已停止任务，请等待15分钟后再执行任务！')
                    return res
                else:
                    # 正常则重置
                    self.exceptionNum = 0

            try:
                # 最后再发送一次
                res = super().session.post(
                    self.URL_POST_STUDY_TIME,
                    data=finalData,
                    headers=super().headers
                ).json()
            except json.decoder.JSONDecodeError:
                # 最后再发送一次
                res = super().session.post(
                    self.URL_POST_STUDY_TIME,
                    data=finalData,
                    headers=super().headers
                ).json()

        return {
            'code': res['code'],
            'name': needData['cellName']
        }
        # print('***该课程可能未完成，请自行检查***')
        # print('>>', needData['cellName'], '已完成')

    # 获取课程进度
    def getProcess(self):
        courseOpenId = self.courseOpenId
        res = super().session.post(
            self.URL_GET_PROCESS,
            headers=super().headers
        ).json()

        if res['code'] == 1:
            # 获取进度成功
            for item in res['courseList']:
                # 遍历课程列表
                if courseOpenId == item['courseOpenId']:
                    return {
                        'code': res['code'],
                        'process': item['process']
                    }

        # 获取进度失败
        return {
            'code': res['code'],
            'process': None
        }
