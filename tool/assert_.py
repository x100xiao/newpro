
from jsonpath import jsonpath
from tool.sql import mysql_db
from tool.allure_ import allure_step_no
from tool.log import logger


class Assert:
    @classmethod
    def assert_response(cls, api_response: dict, assert_list: list):
        """
        :param api_response{}
        :param assert_list
        """
        new_assert_list = []
        logger.info(f'初始断言列表{new_assert_list}')
        for i in assert_list:
            if '$.' in i:
                wz = i.find('$')
                assert_json_path = i[wz:len(i) - 1]
                value = jsonpath(api_response, assert_json_path)
                if not value:
                    logger.error(f'断言表达式提取失败，请检查，接口返回结果{api_response}，表达式{assert_json_path}')
                    return False
                # value = value[0]  replace接收的是str，接口返回信息可能是int，需要转换为str
                value = str(value[0])
                # 用值把表达式替换（注意这个需要用变量接住这个替换的新值）
                i = i.replace(assert_json_path, value)
            if 'sql-' in i:
                wz = i.find('-')
                sql = i[wz+1:len(i) - 1]
                i = i.replace('sql-'+sql, mysql_db.select_db(sql))
            new_assert_list.append(i)
        allure_step_no(f'断言列表：{new_assert_list}')
        logger.info(f'断言表达式新列表：{new_assert_list}')
        assert_result_list = []
        for i in new_assert_list:
            assert_result = eval(i)
            assert_result_list.append(assert_result)
        if False in assert_result_list:
            return False
        return True


if __name__ == '__main__':
    api_response = {'errorCode': 0, 'P20': ['-', '-', '-', '-', '-', '-', '-'], 'v95': [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], 'ODI': '0.0', 'P1': ['-', '-', '-', '-', '-', '-', '-'], 'vMedian': [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], 'P2': ['-', '-', '-', '-', '-', '-', '-'], 'P3': ['-', '-', '-', '-', '-', '-', '-'], 'P4': ['-', '-', '-', '-', '-', '-', '-'], 'P5': ['-', '-', '-', '-', '-', '-', '-'], 'P6': ['-', '-', '-', '-', '-', '-', '-'], 'P7': ['-', '-', '-', '-', '-', '-', '-'], 'P8': ['-', '-', '-', '-', '-', '-', '-'], 'P9': ['-', '-', '-', '-', '-', '-', '-'], 'P10': ['-', '-', '-', '-', '-', '-', '-'], 'P12': ['-', '-', '-', '-', '-', '-', '-'], 'P11': ['-', '-', '-', '-', '-', '-', '-'], 'P14': ['-', '-', '-', '-', '-', '-', '-'], 'P13': ['-', '-', '-', '-', '-', '-', '-'], 'P16': ['-', '-', '-', '-', '-', '-', '-'], 'P15': ['-', '-', '-', '-', '-', '-', '-'], 'P18': ['-', '-', '-', '-', '-', '-', '-'], 'P17': ['-', '-', '-', '-', '-', '-', '-'], 'vMax': [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0], 'P19': ['-', '-', '-', '-', '-', '-', '-'], 'time': ['2022-09-22', '2022-09-23', '2022-09-24', '2022-09-25', '2022-09-26', '2022-09-27', '2022-09-28']}
    print(type(api_response))
    # assert_list = ["'请求\'成功' == '$.ms'", '"值" == "$.提取"']
    # api_response = {'status': 'A0210', 'msg': "User's password is wrong", 'data': {'serialVersionUID': 1, 'userName': 'shiyan', 'firstErrorTime': 1664249396981, 'errorCount': 2, 'lastErrorTime': 1664248798058, 'lockToTime': None, 'serverTime': 1664248798058}}
    # assert_list = [""""User's password is wrong" in "$.msg" ""","'A0210' in '$.status' "]
    # assert_list = ['"User\'s password is wrong" in "$.msg"', "'A0210' in '$.status'"]
    # assert_list = ['"Users password is wrong" in "$.msg"',"'A0210' in '$.status'"]
    assert_list = ['"0" in "$.errorCode"']
    # assert_list = ["'0' in '$.errorCode'"]
    print(Assert.assert_response(api_response, assert_list))
    # i = 'aa'bb' == 'aa'bb'
    # i =  """ "1'2" == "1'2" """
    # d = "'as'as' == 'as'as'"
    # # c = eval(i)
    # # print(c)
    # # print(len(a))
    # b = a[32:len(a)]
    # print(len(b))
    # print(b)
    a = '\'User\'s password is wrong\' in \'User\'s password is wrong\''
    # print(a)