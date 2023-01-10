
# 把参数操作、断言操作、请求操作结合最终的用例执行结果
from tool import logger
from tool.allure_ import allure_description
from tool.parameter_setting import ParameterSetting
from tool.requests_ import Requests
from tool.assert_ import Assert


def extract_(api_response, extract_key):
    logger.info(f'提取参数字典{extract_key}')
    if extract_key:
        extract_value = ParameterSetting.extract_value(api_response, extract_key)
        ParameterSetting.parameter_setting_dict(extract_value, 'save')


def case_assert_result(case_data):
    allure_description(case_data['remark'])
    logger.info(f'用例原始数据：{case_data}')
    if case_data['method'] == 'get':
        path = ParameterSetting.get_path(case_data['path'])
        api_response = Requests.get(path)
        # api_response = Requests.get(case_data['path'])
        extract_key = case_data['extract_key']
        extract_(api_response, extract_key)
        assert_r = Assert.assert_response(api_response, case_data['assert_expression'])

    elif case_data['method'] == 'post':
        # 参数替换和参数依赖操作必须在一个页面，不然页面切换参数池也会重置为{}
        if ParameterSetting.data_is_replace(case_data['data']) == True:
            data = ParameterSetting.parameter_setting_dict(case_data['data'], 'get')
        elif ParameterSetting.data_is_replace(case_data['data']) == 'list_request':
            data = ParameterSetting.parameter_setting_list(case_data['data'])
        else:
            data = case_data['data']
        path = ParameterSetting.get_path(case_data['path'])
        api_response = Requests.post(path, data)
        # api_response = Requests.post(case_data['path'], data)
        extract_key = case_data['extract_key']
        extract_(api_response, extract_key)
        assert_r = Assert.assert_response(api_response, case_data['assert_expression'])
    else:
        assert_r = False
    case_title = case_data['case_title']
    logger.info(f'-----"{case_title}"用例运行完成------')
    return assert_r



