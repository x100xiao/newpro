import json
import importlib_metadata
from tool.suijis import random_time, random_str, random_number
from jsonpath import jsonpath
import urllib.request
from ddddocr import DdddOcr
from tool import ReadFile
# from tool import request_data_nest_replace
from tool.log import logger


class ParameterSetting:
    # 参数池,保存接口的返回参数提取的值，提供给需要的接口请求参数使用
    access_value = {}

    @classmethod
    def get_path(cls, path):
        if '$.' in str(path):
            wz_2 = None
            if '$.' in str(path):
                if '&' in str(path):
                    wz_2 = path.find('&')
                wz = path.find('$')
                if wz_2 == None:
                    bds = path[wz:len(path)]
                else:
                    bds = path[wz:wz_2]
                value = str(jsonpath(cls.access_value, bds)[0])
                path = path.replace(bds, value)
                if '$' in path:
                    # cls.data_is_replace(path)
                    wz = path.find('$')
                    bds = path[wz:len(path)]
                    value = str(jsonpath(cls.access_value, bds)[0])
                    path = path.replace(bds, value)
                return path
        return path

    @classmethod
    def data_is_replace(cls, data):
    # data：请求参数data和提取参数extract_key
    # return：返回参数是否需要被替换
        if data is None:
            return False
        if type(data) == list:
            for i in data:
                if '$.' in str(i) or 'random' in str(i):
                    return 'list_request'
            return False
            # 先检查是否有嵌套参数里面有指定替换格式,然后$.然后random
        for k, v in data.items():
            if type(v) is dict:
                cls.data_is_replace(v)
            if '^' in str(v) or '$.' in str(v) or 'random' in str(v):
                return True
        return False

    @classmethod
    def parameter_setting_list(cls, data: list):
        i_wz = 0
        for i in data:
            if type(i) is dict:
                ParameterSetting.parameter_setting_dict(i)
            if '$.' in str(i):
                data[i_wz] = jsonpath(cls.access_value, i)[0]
            if 'random' in str(i):
                data[i_wz] = eval(i)
            i_wz += 1

        return data

    @classmethod
    def parameter_setting_dict(cls, data: dict, type1 ='get'):
    # data：返回结果提取和参数依赖使用dict
    # type :save把数据存到参数池里面无返回，get读取参数池数据并返回新值
        if type1 == 'get':
            for k, v in data.items():
                '''请求多级嵌套'''
                # if '^' in str(v):
                #     v = request_data_nest_replace(cls.access_value, v)
                #     data[k] = v
                # 嵌套字典处理
                if type(v) is dict:
                    cls.parameter_setting_dict(v)
                # 嵌套列表处理
                elif type(v) is list:
                    for i in v:
                        if type(i) is dict:
                            cls.parameter_setting_dict(i)
                    '''请求参数只有一个层级'''
                else:
                    if '$.' in str(v):
                        try:
                            v = jsonpath(cls.access_value, v)[0]
                            data[k] = v
                        except Exception as e:
                            print(f'jsonpath未读取到值，请检查{e}')
                        logger.info(f'读取前的参数池{cls.access_value}')
                    # 验证码获取
                    if 'code' in str(k):
                        try:
                            urllib.request.urlretrieve(v, 'yzm.png')
                            orc = DdddOcr()
                            with open('yzm.png', 'rb') as f:
                                im = f.read()
                                data[k] = orc.classification(im)
                        except Exception as e:
                            print(f'验证码获取失败{e}')
                    if 'random' in str(v):
                        data[k] = eval(v)
            logger.info(f'最终返回参数：{data}')
            return data
        elif type1 == 'save':
            for k, v in data.items():
                # 写入token
                if 'token' in str(k):
                    ReadFile.yaml_write_token(v)
                cls.access_value[k] = v
            logger.info(f'参数提取完成后的参数池：{cls.access_value}')

    @classmethod
    def extract_value(cls, api_response: dict, extract_key: dict):
        extract_value = {}
        for k, v in extract_key.items():
            extract_value[k] = jsonpath(api_response, v)[0]
        return extract_value


if __name__ == '__main__':
    a = {'zlid': 452, 'fsid': '41608015906', 'sfid': 451, 'sfjyid': '41608015906'}
    b = {"isSeng":0,"followDesc":"2334343","followType":"1",
             "followManageVo":[{"followPatientId":"$.sfjyid","followPatientName":"小小需矮小"}],"id":"$.sfid"}
    # a = {"status":"00000","msg":"一切OK","data":{"image":"data:ima","token":"adsdsd"}}
    # print(ParameterSetting.access_value)
    ParameterSetting.parameter_setting_dict(a, 'save')
    ParameterSetting.parameter_setting_dict(b)
    print(ParameterSetting.data_is_replace(b))
    # ParameterSetting.parameter_setting_dict({'a': 44, 'a1': 144, 'b': 1, 'g': 'wbg'}, 'save')
    # ParameterSetting.parameter_setting_dict({'b': '$.b', 'g': '$.g'})
    # print(f'最终的参数池{ParameterSetting.access_value}')
    # ParameterSetting.get_path("/dfs/dfdf")
    # path = "/df/fd/sd/$.a1"
    # print(f'最终path：{ParameterSetting.get_path(path)}')
    # api_response = {'success':True,'data':{'resultPageVo':{'page':{'showCount':15,'totalPage':5,'totalResult':64,'currentPage':1,'currentResult':0,'entityOrField':False,'orderby':None,'keyword':None},'data':[{'id':448,'followType':2,'followUserId':'41608015906','addTime':'2022-09-30 17:20:56','addTimeMax':None,'followDesc':'发是多少','followPatientId':31663037288,'followPatientName':"SHUJ <FSF>U2SAFSA<>.'2323!#",'followUserName':'shiyan','followGroup':'6561839','isSeng':1,'followInstitutionId':'41608015906','doctorName':None,'newDate':None,'page':None,'orderBy':None,'doctorId':None,'patientId':None,'orderByTwo':None,'deviceId':None,'followManageVo':None}]}},'errCode':200}
    # extract_key = {'sfjyid':'$data.resultPageVo.data[0].followUserId'}
    # ParameterSetting.extract_value(api_response, extract_key)
