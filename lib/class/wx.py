"""
微信小程序
Created by Danyhug on 2021-02-25 16:22
Coding by Danyhug on 2021-02-25 16:22
"""
import json
import random
import time

import requests
import globalData as glo
from bs4 import BeautifulSoup


class WxApp:
    VERSION = 'VERSION_OVER'
    VERSION_NUM = 446

    def update(self) -> bool:
        return False

    def fbi(self):
        return False

    # 登录获取uid
    def getUid(self, code) -> bool:
        return True

    # 获取用户积分
    def getUserPoint(self, uid):
        return '999'

    # 做题扣除积分
    def doWork(self):
        return True

    # 看视频扣除积分
    def watchRadio(self):
        return True

    # 全部完成
    def doAllWork(self):
        return True

    # 职教云
    def doZjy(self):
        return True

    # 资源库
    def doZyk(self):
        return True

    # 处理答案
    def dealAnswer(self, answerText, answer):
        answerText = json.loads(answerText)['questions']
        # 遍历答案文件
        for ans in answerText:
            # 答案的总文本
            ansText = ''
            # 正确的答案
            rightAns = ''

            # 单选题 或 多选
            # print('测试ans', ans)
            if ans['questionType'] == 1 or ans['questionType'] == 2:
                # 索引 √
                index = 0
                # 遍历答案文本
                for ansList in ans['answerList']:
                    # print('ansList测试', ansList)
                    # 选项ABCD
                    # abcd = ord('A') + index
                    # 将文本加上序号添加
                    # ansTemp = chr(abcd) + '、' + ansList['Content'] + '\n'
                    ansTemp = ansList['Content'] + '\0'
                    ansText += ansTemp
                    if ansList['IsAnswer'] == 'true':
                        rightAns += ansTemp

                    index += 1
            elif ans['questionType'] == 3:
                # 判断题 1 or 0
                rightAns = ans['Answer']
            elif ans['questionType'] == 4 or ans['questionType'] == 5:
                # 填空题 √
                rightAns = ans['Answer']
            elif ans['questionType'] == 6:
                # 客观题 √
                rightAns = ans['Answer']
            elif ans['questionType'] == 7:
                # 匹配题
                rightAns = ans['Answer']
            elif ans['questionType'] == 8:
                return
                # 阅读理解题
                rightAns = ans['Answer']
            else:
                return

            try:
                self.postAnswer(ans['Title'], ansText, rightAns, ans['questionType'])
            except UnboundLocalError:
                self.postAnswer(ans['Title'], '', rightAns, ans['questionType'])

    @staticmethod
    def postAnswer(title, answer, rightAns, type):
        pass
