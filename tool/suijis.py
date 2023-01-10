"""
随机几位数，随机几位字符，时间函数
"""
import datetime
import random


def random_number(places):
    """随机几位数"""

    a = [str(i) for i in range(1, 10)]*10000
    b = random.sample(a, places)
    number = ''
    for i in b:
        number = number+i
    return eval(number)


def random_str(places):
    a = [i for i in 'qwertyuioplkjhgfdsazxcvbnm'] * 10000
    b = random.sample(a, places)
    r_str = ''
    for i in b:
        r_str = r_str + i
    return r_str


def random_time():
    """当前系统时间%Y-%m-%d %H:%M:%S"""
    time = datetime.datetime.now().strftime("%Y-%m-%d")
    return time


if __name__ == '__main__':
    # 6位随机字符设置
    number = random_number(6)
    print(number)
    print(type(number))
    # 88位随机字符设置
    print(random_str(8))
    print(random_time())
