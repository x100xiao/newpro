import os
import shutil
import pytest

if __name__ == '__main__':

    try:
        # 删除之前的文件夹
        shutil.rmtree("report")
        print('清除之前的报告')
    except:
        pass
    pytest.main([])
    # 直接生成报告html文件
    os.system('allure generate  report/allure_raw -o report/html --clean')
    # 编译报告原文件并启动报告服务
    # os.system('allure server report/html/')
    # os.system('allure open report/html/')
