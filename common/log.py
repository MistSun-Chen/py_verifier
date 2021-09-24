import threading
import time
import sys
import traceback
class Color:
    Black = 0
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4
    Magenta = 5
    Cyan = 6
    White = 7

class Mode:
    Foreground = 30
    Background = 40
    ForegroundBright = 90
    BackgroundBright = 100

def tcolor(c, m=Mode.Foreground):
    return '\033[{}m'.format(m + c)

def treset():
    return '\033[0m'

class log:
    def __init__(self,level):
        self.level = level
        #日志等级
        #error > warning > info > debug
        #level error : 1
        #level warning : 3
        #level info : 7
        #level debug:15
        self.error_level = 1
        self.warning_level = 2
        self.info_level = 3
        self.debug_level = 4




    def error(self,msg):
        currentTreadname = threading.currentThread()

        print("\033[{}m{} [{}]  {}\033[0m".format(str(Mode.Foreground+Color.Red),time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),str(currentTreadname),str(msg)))

        sys.stdout.flush()
        pass

    def info(self,msg):
        if self.level <self.info_level:
            pass
        else:
            currentTreadname = threading.currentThread()

            print("\033[{}m{} [{}]  {}\033[0m".format(str(Mode.Foreground + Color.White),
                                                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                                   str(currentTreadname),str(msg)))

            sys.stdout.flush()

    def debug(self,msg):
        if self.level <self.debug_level:
            pass
        else:
            currentTreadname = threading.currentThread()

            print("\033[{}m{} [{}]  {}\033[0m".format(str(Mode.Foreground + Color.Green),
                                                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                                   str(currentTreadname),msg))

            sys.stdout.flush()

    def warning(self,msg):
        if self.level <self.warning_level:
            pass
        else:
            currentTreadname = threading.currentThread()
            print("\033[{}m{} [{}]  {}\033[0m".format(str(Mode.Foreground + Color.Yellow),
                                                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                                   str(currentTreadname),msg))
            sys.stdout.flush()
        pass






# if __name__ == '__main__':
#     # import os
#     # os.system('')
#
#     # usage
#     mylog = log(1)
#
#     mylog.error("test")

    # print(tcolor(Color.Red) + 'hello' + treset())
    # print(tcolor(Color.Green, Mode.Background) + 'color' + treset())
    # print()
    #
    # COLOR_NAMES = ['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White']
    # MODE_NAMES = ['Foreground', 'Background', 'ForegroundBright', 'BackgroundBright']
    #
    # fmt = '{:11}' * len(COLOR_NAMES)
    # print(' ' * 20 + fmt.format(*COLOR_NAMES))
    #
    # for mode_name in MODE_NAMES:
    #     print('{:20}'.format(mode_name), end='')
    #     for color_name in COLOR_NAMES:
    #         mode = getattr(Mode, mode_name)
    #         color = getattr(Color, color_name)
    #         print(tcolor(color, mode) + 'HelloColor' + treset(), end=' ')
    #     print()
    #

