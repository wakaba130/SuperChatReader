##
# cording:utf-8
##

import argparse
import copy
import datetime
import numpy as np
from matplotlib import pyplot as plt

def argparser():
    """
    コマンドライン引数設定。wはWEBカメラ入力でカメラIDを入力、mは動画読み込みで動画パスを設定する。
    :return: コマンドライン引数
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', type=str, default='log/text_8d5M0ZU0H1M.log')
    return parser.parse_args()


def str2datetime(chat_time):
    # format 2020-12-08T14:04:32.249000Z
    _date, _time = chat_time.split('T')
    y, m, d = _date.split('-')
    hh, mm, _ss = _time.split(':')
    if '.' in _ss:
        ss, _ms = _ss.split('.')
        ms = _ms.replace('Z', '')
    else:
        ss = _ss.replace('Z', '')
        ms = '0'
    return datetime.datetime(year=int(y), month=int(m), day=int(d),
                             hour=int(hh), minute=int(mm), second=int(ss),
                             microsecond=int(ms))


def main(args):
    time_line = []
    with open(args.logfile, 'r') as fp:
        for r in fp:
            line = r.replace('\n', '')
            time_line.append(line)

    start_time = str2datetime(time_line[-1])
    print(start_time)
    
    hist = {}
    for tt in time_line:
        now_time = str2datetime(tt)
        if now_time > start_time:
            sub_time = now_time - start_time
            _idx = str(sub_time).split('.')[0]
            hh, mm, _ = _idx.split(':')
            idx = hh + ':' + mm
            if idx in hist:
                hist[idx] += 1.0
            else:
                hist[idx] = 0.0

    left = [m for m in hist]
    height = [hist[m] for m in hist]

    plt.title('chat histgram')
    plt.xlabel('time line')
    plt.ylabel('chat frequency')

    plt.bar(left, height)
    plt.xticks(rotation=90)
    plt.show()

if __name__ == "__main__":
    args = argparser()
    main(args)