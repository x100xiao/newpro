import json

import requests

#假设以下为导出文件接口，与列表查询参数
from jsonpath import jsonpath

from tool.suijis import random_time

def jk():
    urls = "https://uat.resvent.com/web-server/api/follow/complianceList"
    heard = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,fr-FR;q=0.8,fr;q=0.7,pt-PT;q=0.6,pt;q=0.5,en-US;q=0.4,en;q=0.3,es;q=0.2",
        "authentication-info": "8710e9c2-50b1-44f6-8d93-c8f6696c4099",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "language": "en",
        "pragma": "no-cache",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "timefmt": "MM-dd-yyyy HH:mm:ss",
        "timezone": "Asia/Shanghai",
        "referrer": "https://uat.resvent.com/web/dataUpload",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "mode": "cors",
        "credentials": "include"
    }
    # data = {"dayNum":7,"dayTime":random_time(),"page":{"currentPage":1,"showCount":15},"sqlNames":["userName","patientName"]}
    data = {'dayNum': '30', 'dayTime': '2022-11-24', 'page': {'currentPage': 1, 'showCount': 15}, 'sqlNames': ['userName', 'patientName', 'deviceId', 'latelTime', 'dayNum']}
    print("数据类型为：%s" % type(data))
    print(data)
    result = requests.session().post(urls, headers=heard, data=json.dumps(data)).json()
    # result = requests.post(urls, headers=heard, data=json.dumps(data)).json()
    #先将响应结果的编码格式设置为“utf-8"；
    # result.encoding = "utf-8"
    #再用with open的方式打开并新建一个excel表格，并写入response返回的数据流
    #'D:/xx/files/export_data.xlsx文件路劲
    # with open(r'E:\aaa.xlsx', 'wb') as f:
    # #利用Respose对象的iter_content()方法循环；
    #  #并调用write()将每次遍历取回的内容写入该文件
    #     for chunk in result.iter_content():
    #         f.write(chunk)
    # res = result.json()
    print(result)
def cs():
    data = {"dayNum":"30","dayTime":'random_time()',"page":{"currentPage":1,"showCount":15},"sqlNames":["userName","patientName","deviceId","latelTime","dayNum"]}
    for k, v in data.items():
        print(k, v)
        if '^' in str(v):
            print('vvvv')
        data[k] = v
        if '$.' in str(v):
            try:
                print('$$$$')
                data[k] = v
            except Exception as e:
                print(f'jsonpath未读取到值，请检查{e}')
        # 验证码获取
        if 'code' in str(k):
            try:
                print('ccccoide')
            except Exception as e:
                print(f'验证码获取失败{e}')
        if 'random' in v:
            data[k] = eval(v)
    return data
# data  = {'success':True,'data':{'page':{'showCount':15,'totalPage':0,'totalResult':0,'currentPage':0,'currentResult':0,'entityOrField':False,'orderby':None,'keyword':None},'data':[]},'errCode':200}


access_value = {'scs': 'ture22', 'tt': '168', 'err': '666'}

def toself(data):
    for k,v in data.items():
        # 嵌套字典处理
        if type(v) is dict:
            toself(v)
        # 嵌套列表处理
        elif type(v) is list:
            for i in v:
                toself(i)
        else:
            if '$.' in str(v):
                try:
                    v = jsonpath(access_value, v)[0]
                    data[k] = v
                except Exception as e:
                    print(f'jsonpath未读取到值，请检查{e}')
            if 'random' in str(v):
                data[k] = eval(v)

    # print(f'替换完后', data)
    return data

if __name__ == '__main__':
    # print(jk())
    data = {
                'success': '$.scs',
                'data': {
                    'page': {
                        'showCount': 15,
                        'totalPage': '$.tt',
                        'time': 'random_time()',
                        'entityOrField': False,
                        'keyword': 'None'
                            },
                    'data': []
                        },
                'errCode': '$.err'
            }
    # data = {
    #         "isSeng": 0,
    #         "followType": '$.scs',
    #         "followManageVo": [{
    #             "followPatientId": "31668735319",
    #             "followPatientName": '$.tt'
    #         }, {
    #             "followPatientId": "31667200904",
    #             "followPatientName": "2B4544052B454405"
    #         }, {
    #             "followPatientId": "31660974691",
    #             "followPatientName": "不满30天B-2B317703cenhong"
    #         }]
    #     }
    #
    print(toself(data))
