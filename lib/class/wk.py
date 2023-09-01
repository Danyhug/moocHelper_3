"""
wk类
这里定义有关微课的一切
Created by Danyhug on 2022-4-27 09:33:30
"""
import time

import utils


class Wk(utils.Utils):
    # ******URL******
    # 获取微课未完成课程
    URL_GET_NOT_DONE_COURSE = 'https://www.icve.com.cn/studycenter/mySmallCourse/studingSmallCourse'
    # 获取该课程信息
    URL_GET_COURSE_INFO = 'https://www.icve.com.cn/Portal/microstudy/getHeadInfo'
    # 提交课程数据
    URL_POST_COURSE = 'https://www.icve.com.cn/portal/microstudy/updateStatus'

    def __init__(self):
        # 课程ID
        self.courseId = ''
        self.Zyk = None

    def getAllNotDoneCourse(self):
        """
        获取所有未完成的微课
        :return:
        """
        res = super().session.post(
            self.URL_GET_NOT_DONE_COURSE,
            headers=super().headers
        ).json()

        # 把未完成的课程列表赋值
        return res['list']

    def getCourseInfo(self, courseId):
        """
        获取某课程信息
        {"code":1,"courseInfo":{"Title":"计算机应用基础－说课","StudyScore":0.02,"Cover":"https://file.icve.com.cn/doc_public4/807/137/C9F226D76681FCDB8247A013F21815AA.jpg?x-oss-process=image/resize,m_fixed,w_128,h_72,limit_0"},"courseClassfication":"电子与信息大类 \u003e 计算机类 \u003e 软件与信息服务","knowleadgeNode":"说课","cells":[{"Id":"piczafonrztc5ufg7gc4jw","Title":"说课视频","CellType":"video"}],"cellsCount":1}
        :param courseId:
        :return:
        """
        data = {
            'courseId': courseId
        }
        res = super().session.post(
            self.URL_GET_COURSE_INFO,
            data=data,
            headers=super().headers
        ).json()

        # [{Id: "piczafonrztc5ufg7gc4jw", Title: "说课视频", CellType: "video"}]
        return res['cells']

    def postCourse(self, cellId: str):
        """
        提交课程信息，什么rz东西，一点验证都不做的，害我找半天
        cellId=piczafonrztc5ufg7gc4jw&learntime=212.9&status=1
        :return:
        """
        data = {
            'cellId': cellId,
            'learntime': 1000.9,
            'status': 1
        }
        super().session.post(
            self.URL_POST_COURSE,
            data=data,
            headers=super().headers
        )
        self.Zyk.zykWorkLog('[ 微课观看成功 ]')

    def postAllCourse(self, cells: list):
        """
        完成所有微课任务
        :return:
        """
        for cell in cells:
            # 提交课程
            self.postCourse(cell['Id'])
            self.Zyk.zykWorkLog(cell['Title'] + '已完成')
            time.sleep(5)

    # 将self.moocBox绑定主界面的moocBox，可以使用主界面的函数
    def setZykBox(self, Zyk):
        self.Zyk = Zyk
        self.Zyk.zykWorkLog('资源库配置已就绪')
