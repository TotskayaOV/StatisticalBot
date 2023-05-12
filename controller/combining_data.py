from datetime import datetime, timedelta
from loader import db



def summation_data_jira_call(date_dict: dict):
    """
    Формирует численный стек данных из БД
    :param date_dict: {begin_period: datetime, end_period: datetime, get_method: cl.method}
    :return: {'count': count_sum, 'total': total_digit, 'time': decimal_time}
    """
    query_method = date_dict.get('get_method')
    date1 = date_dict.get('begin_period')
    count_sum = 0
    total_digit = 0
    decimal_time = 0
    while date1 <= date_dict.get('end_period'):
        list_data = query_method(date=date1)
        if list_data:
            for elem in list_data:
                if elem[2] != 111121:
                    if type(elem[3]) == str and ':' in elem[3]:
                        hours, minutes = map(int, elem[3].split(":"))
                        decimal_time += hours + minutes / 60
                    elif type(elem[3]) == float:
                        total_digit += elem[3]
                    else:
                        total_digit += int(elem[3])
                    count_sum += 1
        date1 += timedelta(days=1)
    return {'count': count_sum, 'total': total_digit, 'time': decimal_time}

def summation_data_user_jira_call(date_dict: dict):
    """
    Формирует численный стек данных из БД для пользователя
    :param date_dict: {begin_period: datetime, end_period: datetime, get_method: cl.method, user_id: int}
    :return: {'day_count': count_sum, 'total': total_digit, 'time': decimal_time}
    """
    query_method = date_dict.get('get_method')
    date1 = date_dict.get('begin_period')
    count_sum = 0
    total_digit = 0
    decimal_time = 0
    while date1 <= date_dict.get('end_period'):
        list_data = query_method(date=date1)
        if list_data:
            for elem in list_data:
                if elem[2] == date_dict.get('user_id'):
                    if type(elem[3]) == str and ':' in elem[3]:
                        hours, minutes = map(int, elem[3].split(":"))
                        decimal_time += hours + minutes / 60
                    elif type(elem[3]) == float:
                        total_digit += elem[3]
                    else:
                        total_digit += int(elem[3])
                    count_sum += 1
        date1 += timedelta(days=1)
    return {'day_count': count_sum, 'total': total_digit, 'time': decimal_time}


def summation_data_general_portal(date_dict: dict):
    """
    Формирует численный стек данных из БД
    :param date_dict: {begin_period: datetime, end_period: datetime}
    :return: 'count': count_sum, 'total': total_digit, 'new': new_digit, 'fast': fast_digit}
    """
    date1 = date_dict.get('begin_period')
    count_sum = 0
    total_digit = 0
    new_digit = 0
    fast_digit = 0
    while date1 <= date_dict.get('end_period'):
        list_data_portal = db.get_date_portal(date1)
        if list_data_portal:
            for elem in list_data_portal:
                if type(elem[3]) == int:
                    total_digit += elem[3]
                count_sum += 1
        list_data_general = db.get_general(date1)
        if list_data_general:
            for elem in list_data_general:
                if type(elem[1]) == int:
                    new_digit += elem[1]
                    fast_digit += elem[2]
        date1 += timedelta(days=1)
    return {'count': count_sum, 'total': total_digit, 'new': new_digit, 'fast': fast_digit}

def summation_data_general_portal_user(date_dict: dict):
    """
    Формирует численный стек данных из БД для отдельного пользователя
    в возвращаемом словаре:
    day_count - количество записей пользователя = количество дней
    total - количество анкет
    :param date_dict: {begin_period: datetime, end_period: datetime, user_id:int}
    :return: {'day_count': count_sum, 'total': total_digit}
    """
    date1 = date_dict.get('begin_period')
    day_count = 0
    total_digit = 0
    while date1 <= date_dict.get('end_period'):
        list_data_portal = db.get_date_portal(date1)
        if list_data_portal:
            for elem in list_data_portal:
                if type(elem[3]) == int:
                    if elem[2] == date_dict.get('user_id'):
                        total_digit += elem[3]
                        day_count += 1
        date1 += timedelta(days=1)
    return {'day_count': day_count, 'total': total_digit}
