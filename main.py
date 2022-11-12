"""
date: 2022/11/12
author: amoxuk
from: 52pojie

用于监测长时间未移动鼠标，自动关闭指定的程序。
"""

import logging
import os
import time
import configparser

import win32api

logging.basicConfig(level=logging.INFO)

FREEZE_DIST = 3


def auto_close(freq, wait, process):
    x1, y1 = win32api.GetCursorPos()
    freeze = time.time()
    while 1:
        try:
            time.sleep(freq)
            x2, y2 = win32api.GetCursorPos()
            if abs(x2 - x1) > FREEZE_DIST and abs(y2 - y1) > FREEZE_DIST:
                # 鼠标挪动，更新时间及初始位置
                freeze = time.time()
                x1, y1 = x2, y2
            if time.time() - freeze > wait:
                for each in process:
                    task_kill(each)
        except Exception as e:
            logging.error('error', exc_info=e, stack_info=True)


def task_kill(process):
    with os.popen(f'tasklist /nh|find /c /i "{process}"') as pid:
        res = pid.read().strip()
        if f"{res}" != '0':
            logging.info(f'long time to move mouse, close process: {process}')
            find_kill = f'TaskKill /F /T /IM "{process}"'
            with os.popen(find_kill) as fp:
                _ = fp.read()


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('config.ini', encoding="utf-8")
    check_freq = float(conf.get('CONFIG', 'CheckFreq'))
    wait_time = float(conf.get('CONFIG', 'WaitTime'))
    processes = conf.get('CONFIG', 'Process').split(',')
    logging.info(f'config: {check_freq}, {wait_time}, {processes}')
    auto_close(check_freq, wait_time, processes)
