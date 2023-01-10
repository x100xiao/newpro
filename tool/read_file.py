import os
import yaml
from pathlib import Path
from config.config import Environment, exclude_file, exclude_dir, r_case_path
from tool.sql import mysql_db
from tool.log import logger


class ReadFile:
    # 获取当前项目的绝对路径
    project_directory = str(Path(__file__).parent.parent) + '/'

    @classmethod
    def read_yaml(cls, path):
        """读取yaml文件，以字典格式返回{'yon':{'path':'/test','data': {'id':1}}}"""
        path = cls.project_directory + path
        file = open(path, 'r', encoding='utf-8')
        with file as doc:
            content = yaml.load(doc, Loader=yaml.Loader)
            return content

    @classmethod
    def read_case(cls):
        '''读取case下需要执行的用例文件并返回用例数据'''
        # 这是多个用例文件 ['case/fastapi_test/bill.yaml', 'case/waybill.yaml']
        path_list = cls.file_execute_list()
        # 用例文件的情况 {"用例标题1":{"data":{},"path":'/ff'},"用例标题2":{"data":{},"path":'/ff'}}
        case_data = {}
        ylwj = 0
        yl = 0
        for i in path_list:
            case_data.update(cls.read_yaml(i))
            ylwj = ylwj+1
        print("yongl", ylwj)
        logger.info(f'读取的用例文件数量:{ylwj}')
        logger.info(f'读取的用例数据:{case_data}')
        for k, v in case_data.items():
            # k为用例名称，v为用例数据
            case_name = k
            # 如果用例需要执行
            if v['is_run'] == True:
                # 把用例标题写进最终请求数据中
                v['case_title'] = case_name
                yl = yl+1
                if v['precondition_sql'] != None:
                    for i in v['precondition_sql']:
                        mysql_db.execute_db(i)
                        pass
                if v['data'] != None and type(v['data']) != list:
                    sql_k_list = []
                    sql_v_list = []
                    for data_k, data_v in v['data'].items():
                        if 'sql-' in str(data_v):
                            sql_k_list.append(data_k)
                            sql_result = mysql_db.select_db(data_v[4:])
                            sql_v_list.append(sql_result)
                    new_v = dict(zip(sql_k_list, sql_v_list))
                    v['data'].update(new_v)
                logger.info(f'最终执行的用例数据:{v}')
                yield v
        logger.info(f'执行的用例数量:{yl}')

    @classmethod
    def file_execute_list(cls, exclude_file=exclude_file, exclude_dir=exclude_dir, r_case_path=r_case_path):
        '''
        :param r_case_path: 用例存放根目录     case/
        :param exclude_dir: 要排除的目录（二级目录）例子：ctms  list格式
        :param exclude_file: 要排除的文件（case目录下所有文件）例子：case/ctms/1dl/testdl.yaml   case/waybill.yaml list格式
        :return: 获取case下的所有用例文件列表,最多支持二级目录,通用排除文件返回最终要执行的用例文件
        '''
        file_list = []
        case_path = cls.project_directory + r_case_path
        # case目录下的所有文件
        for filename in os.listdir(case_path):
            if '.yaml' in filename:
                # 要储存为case开头的目录，方便读取用例使用
                file_list.append(r_case_path + filename)
            else:
                # 遍历case下面的二级目录
                for i in os.listdir(case_path + filename):
                    # 检查这个二级目录是否需要被排除
                    if filename in exclude_dir:
                        continue
                    # 要储存为case开头的目录，方便读取用例使用，这是二级目录得把二级目录拼接上
                    file_list.append(r_case_path + filename + '/' + i)
        # 文件列表不为空的话一个一个的排除掉这些文件
        if exclude_file != []:
            for i in exclude_file:
                file_list.remove(i)
        return file_list

    @classmethod
    def case_file_location(cls, case_title):
        path_list = cls.file_execute_list()
        for i in path_list:
            if case_title in cls.read_yaml(i).keys():
                return i

    # 写入token信息至环境配置yaml
    @classmethod
    def yaml_write_token(cls, token):
        if Environment == 'uat':
            test_or_pro = 'uat'
        elif Environment == 'yufa':
            test_or_pro = 'yufa'
        elif Environment == 'S4':
            test_or_pro = 'S4'
        elif Environment == 'S3':
            test_or_pro = 'S3'
        else:
            test_or_pro = 'USA'
        environment_path = 'config/environment.yaml'
        environment = cls.read_yaml(environment_path)
        environment[test_or_pro]['headers']['authentication-info'] = token
        with open(cls.project_directory+environment_path, "w", encoding="utf-8") as f:
            yaml.dump(environment, f)

    @classmethod
    def check_case_title_is_sole(cls):
        '''
        :return: 检查是否有重复的用例名称，放到全局前置,True就是有重复的，False就是没有
        '''
        from collections import Counter
        execute_list = cls.file_execute_list()
        case_title_list = []
        for i in execute_list:
            case_dict = cls.read_yaml(i)
            case_key_list = [i for i in case_dict.keys()]
            case_title_list += case_key_list
        b = dict(Counter(case_title_list))
        repetition = {key: value for key, value in b.items() if value > 1}
        if bool(repetition):
            logger.error(f'有重复的用例标题，请检查所有要执行的用例文件，重复标题和重复次数{repetition}')
            return True
        else:
            return False


if __name__ == '__main__':
    # print(ReadFile.project_directory)
    # print(ReadFile.read_yaml('config/environment.yaml'))
    # print(ReadFile.read_yaml('case/1dl/testdl.yaml'))
    case_data = ReadFile.read_case()
    for i in case_data:
        print(case_data)
    # env_info = ReadFile.read_yaml('config/environment.yaml')
    # request_info = env_info[Environment]
    # print(request_info)
    # print(ReadFile.read_case())
