# 參考網址：https://www.delftstack.com/zh-tw/howto/python/python-countdown-timer/

import time

def countdown(num_of_secs):
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = s
        print(min_sec_format)
        time.sleep(1)
        num_of_secs -= 1

    print(0)

inp = int(input('輸入要倒數的秒數：'))
countdown(inp)