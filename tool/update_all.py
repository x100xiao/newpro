"""
@Author: 600490
@Email: xianrong.song@resvent.com
@FileName: update_all.py 为避免data发生变化，多层级嵌套单独处理
@DataTime: 2022/12/23 10:05
"""
from tool.suijis import random_time


class Man:

    @classmethod
    def cs(cls, data: dict):
        for k, v in data.items():
            if type(v) is dict:
                cls.cs(v)
            if '1' in str(v):
                data[k] = 666
            if '15' in str(v):
                data[k] = 555
        return data


if __name__ == '__main__':
    a = {
    "success": 1,
    "data": {
        "page": {
            "showCount": 15,
            "currentResult": 0
        },
        "data": []
    },
    "errCode": 200
}
    data = Man.cs(a)
    print(data)
