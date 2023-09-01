"""
zyk类
这里定义有关资源库的一切
Created by Danyhug on 2022-4-27 12:49:24
"""
import utils


class Zyk(utils.Utils):
    # ******URL******
    # 获取用户信息
    URL_GET_USER_DETAIL = 'https://www.icve.com.cn/studycenter/PersonalInfo/getUserInfo'
    # 未完成的课程
    URL_GET_NO_DONE_COURSE = 'https://www.icve.com.cn/studycenter/MyCourse/studingCourse'
    # 获取课程目录信息
    URL_GET_DIRECTORY_INFO = 'https://www.icve.com.cn/study/Directory/directoryList?courseId='
    # 获取某课程的项目目录（例如某个课程的PPT和视频）
    URL_GET_COURSE_DIRECTORY = 'https://www.icve.com.cn/study/directory/directory'
    # 更新时间
    URL_POST_STUDY_TIME = 'https://www.icve.com.cn/study/directory/updateStatus'

    def __init__(self):
        # 课程ID
        self.courseId = ''
        # 课程名
        self.courseName = ''

    def __getUserId(self) -> str:
        """
        获取用户ID
        :return:
        """
        res = super().session.post(
            self.URL_GET_USER_DETAIL,
            headers=super().headers
        ).json()
        return res['userInfo']['Id']

    def getCourse(self) -> list:
        """
        获取未完成的课程
        [{"id":"pgy4avqq4rbee9cdneuooa","schedule":"5.63","title":"煤矿开采方法", limit_0","studyhours":"64.0","state":"3"}]
        :return: courseList: list
        """
        data = {
            'userid': self.__getUserId()
        }
        res = super().session.post(
            self.URL_GET_NO_DONE_COURSE,
            data=data,
            headers=super().headers
        ).json()

        # [{"id":"pgy4avqq4rbee9cdneuooa","schedule":"5.63","title":"煤矿开采方法", limit_0","studyhours":"64.0","state":"3"}]
        return res['list']

    def getDirectory(self) -> list:
        """
        获取目录信息
        :return:
        """
        # 拼接链接
        url = self.URL_GET_DIRECTORY_INFO + self.courseId
        res = super().session.get(
            url,
            headers=super().headers
        ).json()

        """
        [{
            section: { Id, CourseId, Title },
            chapters: [{
                chapter: { Id, Title, SectionId, ChapterType },
                cells: [{
                    Id, 
                    Title,
                    ChapterType: video,
                    Status
                }]
            }]
        }]
        """
        return res['directory']

    def getNowCourseDirectory(self, chapterId) -> list:
        """
        获取当前课程的目录详情（点进去展示PPT、视频这些的）
        :return:
        """
        data = {
            'courseId': self.courseId,
            'chapterId': chapterId,
            'sort': 0.003
        }

        res = super().session.post(
            self.URL_GET_COURSE_DIRECTORY,
            data=data,
            headers=super().headers
        ).json()
        # [] {Id: "m0t3agiqclhkc5usfixqg", Title: "煤田划分井田", CellType: "video"}
        return res['cells']

    def postStudy(self, cellId: str):
        """
        提交学习情况
        :return:
        """
        data = {
            'cellId': cellId,
            'learntime': 199,
            'status': 1
        }
        res = super().session.post(
            self.URL_POST_STUDY_TIME,
            data=data,
            headers=super().headers
        ).json()

        if res['code'] == 1:
            pass
            #print('进度更新成功')
