import json
import requests
from tool import requests_environment_info
from tool.log import logger
from tool.allure_ import allure_description, allure_step_no

'''
def res_all(method, path, header, data='', data_type='json'):
    url = 'ip' + path 
    if data == '':
        response = requests.get(url=url, headers=header)
    else:
        if data_type == 'form':
            response = requests.request(method=method, url=url, data=data, headers=header)
        else:
            response = requests.request(method=method, url=url, headers=header, data=json.dumps(data))
    try:
        try:
            res = response.json()
        except:
            res = response.text
        # self.rel.locallcache(caches, bodys=data_random, res=res, cookie=response.cookies)
        return res, response.elapsed.total_seconds(), response.status_code
    except Exception as e:
        raise
    # return result


class Requests:
    @classmethod
    def get(cls, path, data, headers, data_type):
        return res_all('GET', path, data, headers, data_type)

    @classmethod
    def post(cls, path, data, headers, data_type):
        return res_all('POST', path, data, headers, data_type)

    @classmethod
    def put(cls, path, data, headers, data_type):
        return res_all('PUT', path, data, headers, data_type)

    @classmethod
    def delete(cls, path, data, headers, data_type):
        return res_all('DELETE', path, data, headers, data_type)
'''


class Requests:
    rs = requests.request
    # verify=False  安全证书路径配置，false为不配置，主要为了解决fiddler等代理报错
    session = requests.Session()
    
    @classmethod
    def get(cls, path):
        url = requests_environment_info()['ip']+path
        headers = requests_environment_info()['headers']
        allure_step_no(f'最终请求地址 {url}')
        logger.info(f'get请求的最终请求地址:{url}')
        result = Requests.session.get(url=url, headers=headers, verify=False).json()
        allure_step_no(f'返回结果：{result}')
        logger.info(f'{url}返回结果：{result}')
        return result

    @classmethod
    def post(cls, path, data=None):
        url = requests_environment_info()['ip'] + path
        headers = requests_environment_info()['headers']
        allure_step_no(f'最终请求地址 {url}')
        allure_description(f'POST请求参数:{data}')
        logger.info(f'POST请求的最终请求地址:{url}')
        result = requests.Session().post(url=url, headers=headers, data=json.dumps(data), verify=False).json()
        allure_step_no(f'返回结果：{result}')
        logger.info(f'{url}返回结果：{result}')
        return result


if __name__ == '__main__':
    Requests.get('/ds')
    Requests.post('/post', {'data': '123'})
