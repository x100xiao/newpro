import time
import calendar
import datetime
import pytz

"当天" "[('create_date','&gt;=', time.strftime('%Y-%m-%d 00:00:00')),('create_date', '&lt;', context_today().strftime('%Y-%m-%d 23:59:59'))]"
"本周" "[('create_date','&gt;', (context_today() - datetime.timedelta(weeks=1)).strftime('%%Y-%%m-%%d 00:00:00'))]"
"本月" "[('create_date','&gt;=', time.strftime('%Y-%m-01 00:00:00')),('create_date','&lt;',  (context_today() + relativedelta(months=1)).strftime('%Y-%m-01 00:00:00'))]"
"上月""[('create_date','&lt;', time.strftime('%Y-%m-01 00:00:00')),('create_date','&gt;=',  (context_today() - relativedelta(months=1)).strftime('%Y-%m-01 00:00:00'))]"
"本年" "[('create_date','&lt;=', time.strftime('%Y-12-31 23:59:59')),('create_date','&gt;=', time.strftime('%Y-01-01 00:00:00'))]"


def recent_date_domain(days=0, weeks=0):
    date = (datetime.datetime.utcnow() - datetime.timedelta(days=days) - datetime.timedelta(weeks=weeks)).strftime(
        '%Y-%m-%d 00:00:00')
    return [('create_date', '>=', date)]


def custom_date_domain(args):
    domain = []
    start_date = args.get('start_date', False)
    end_date = args.get('end_date', False)
    if start_date:
        domain.append(('create_date', '>=', start_date))
    if end_date:
        domain.append(('create_date', '<=', end_date))
    return domain


def birthday_to_age(birthday):
    now = (datetime.datetime.now() + datetime.timedelta(days=1))
    year = now.year
    month = now.month
    day = now.day
    if year == birthday.year:
        return 0
    else:
        if birthday.month > month or (birthday.month == month and birthday.day > day):
            return year - birthday.year - 1
        else:
            return year - birthday.year


def get_birthday_by_id_card(id_card):
    """通过身份证号获取出生日期"""
    if len(id_card) == 15:
        birth_year = int(id_card[6:8]) + 1900
        birth_month = int(id_card[8:10])
        birth_day = int(id_card[10:12])
    else:
        birth_year = int(id_card[6:10])
        birth_month = int(id_card[10:12])
        birth_day = int(id_card[12:14])
    return datetime.date(birth_year, birth_month, birth_day)


def get_age_by_id_card(id_card):
    """通过身份证号获取年龄"""
    now = (datetime.datetime.now() + datetime.timedelta(days=1))
    year = now.year
    month = now.month
    day = now.day
    birthday = get_birthday_by_id_card(id_card)

    if year == birthday.year:
        return 0
    else:
        if birthday.month > month or (birthday.month == month and birthday.day > day):
            return year - birthday.year - 1
        else:
            return year - birthday.year


def stamp_to_utc(stamp, utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.000Z'):
    if not stamp:
        return False
    dateArray = datetime.datetime.utcfromtimestamp(stamp)
    utc_to_local(utc_time_str)
    return dateArray.strftime(utc_format)


def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Shanghai')  # 定义本地时区
    local_format = '%Y-%m-%d %H:%M:%S'  # 定义本地时间format

    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)  # 国际时间的格式转化为datetime.datetime格式
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)  # 想将datetime格式添加上世界时区，然后astimezone切换时区：世界时区==>本地时区
    time_str = local_dt.strftime(local_format)  # 将datetime格式转化为str—format格式
    return int(time.mktime(
        time.strptime(time_str, local_format)))  # 运用mktime方法将date—tuple格式的时间转化为时间戳;time.strptime()可以得到tuple的时间格式


def local_to_utc(local_ts, utc_format='%Y-%m-%dT%H:%M:%S.000Z'):
    local_tz = pytz.timezone('Asia/Shanghai')  # 定义本地时区
    local_format = '%Y-%m-%d %H:%M:%S'  # 定义本地时间format

    time_str = time.strftime(local_format, time.localtime(local_ts))  # 首先将本地时间戳转化为时间元组，用strftime格式化成字符串
    dt = datetime.datetime.strptime(time_str, local_format)  # 将字符串用strptime 转为为datetime中 datetime格式
    local_dt = local_tz.localize(dt, is_dst=None)  # 给时间添加时区，等价于 dt.replace(tzinfo=pytz.timezone('Asia/Chongqing'))
    utc_dt = local_dt.astimezone(pytz.utc)  # astimezone切换时区
    return utc_dt.strftime(utc_format)  # 返回世界时间格式


def time_last_day_of_month():
    """
    获取当前月的最后一天
    :return:
    """
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = calendar.monthrange(year, month)[1]
    return datetime.datetime(year, month, day).strftime("%Y-%m-%d")


def add_months(start, months):
    year = start.year + months // 12
    month = (start.month + months % 12) % 12
    if month == 0:
        month = 12
    day = start.day
    max_day = calendar.monthrange(year, month)[1]  # 获取某个月最多多少天
    if day > max_day:
        day = max_day
    return datetime.datetime(year, month, day, hour=start.hour, minute=start.minute, second=start.second,
                             microsecond=start.microsecond)


def stamp_to_str(stamp):
    """
    stamp转换为本地 传入的本地时间戳 1531411200
    :param stamp:
    :return:
    """
    # #时间戳转换为本地时间
    if len(str(stamp)) != 10 and len(str(stamp)) != 13:
        raise Warning('时间格式不正确！')
    if len(str(stamp)) == 13:
        stamp = int(stamp / 1000)
    timeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp))
    return timeStr
# stamp_to_str(1558360093656)
# https://blog.csdn.net/qq_37193537/article/details/78987949

# 使用示例
print(utc_to_local('2018-07-13T16:00:00Z', utc_format='%Y-%m-%dT%H:%M:%SZ'))
print(local_to_utc(1564243200))
# print(local_to_utc(1564243200, local_tz='Asia/Shanghai'))

# 其他
# date_=datetime.datetime(2018,6,19,20,55,00)
# timestamp2=time.mktime(date_.timetuple())   #date_.timetuple() 将datetime格式的转化为time模块的tuple格式
# print(timestamp2)
