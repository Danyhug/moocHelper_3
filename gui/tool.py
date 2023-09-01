import threading
import webbrowser


def rgb(rgb: tuple):
    # 计算rgb值
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def positionCenter(box: str, windowW: int, windowH: int) -> str:
    """
    通过计算窗口宽高，返回字符串使该窗口居中
    :param box: str
    :param windowW: int
    :param windowH: int
    :return: str
    """
    # 将宽高分开
    boxInfo = box.split('x')
    width = int(boxInfo[0])
    height = int(boxInfo[1])

    x = (windowW - width) // 2
    y = (windowH - height) // 2

    return '{0}+{1}+{2}'.format(box, x, y)


def openWebSite(url):
    # 打开指定网页
    webbrowser.open(url)


# 打包进线程（耗时的操作）
def thread_it(func, *args, **kwargs):
    t = threading.Thread(target=func, args=args, kwargs=kwargs)
    t.setDaemon(True)   # 守护线程
    t.start()  # 启动
