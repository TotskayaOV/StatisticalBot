from datetime import datetime, timedelta

def processing_data_portal(parsed_data: list):
    data = {}
    for elem in parsed_data:
        if len(elem) > 2:
            if data.get(elem[0], 0) == 0:
                data[elem[0]] = int(elem[2])
            else:
                count = data.get(elem[0])
                data[elem[0]] = count + int(elem[2])
        else:
            if data.get(elem[0], 0) == 0:
                data[elem[0]] = int(elem[1])
            else:
                count = data.get(elem[0])
                data[elem[0]] = count + int(elem[1])
    return data


def processing_time_jira(parsed_data: list):
    data = {}
    for i in range(2, len(parsed_data)):
        date_line = datetime.strptime(parsed_data[i][0], "%b %d %Y")
        dict_line = {}
        for indication in range(1, len(parsed_data[i])):
            if parsed_data[i][indication]:
                time_in_seconds = round(float(parsed_data[i][indication]) * 60)
                minutes, seconds = divmod(time_in_seconds, 60)
                if seconds < 10:
                    dict_line[parsed_data[0][indication]] = f'{minutes}:0{seconds}'
                else:
                    dict_line[parsed_data[0][indication]] = f'{minutes}:{seconds}'
        data[date_line] = dict_line
    return data

def processing_SLA_jira(parsed_data: list):
    data = {}
    for i in range(2, len(parsed_data)):
        try:
            date_line = datetime.strptime(parsed_data[i][0], "%b %d %Y %I%p")
        except:
            date_line = datetime.strptime(parsed_data[i][0], "%b %d %Y")
        rounding = date_line.replace(hour=0, minute=0, second=0, microsecond=0)
        dict_line = data.get(rounding, {})
        for indication in range(1, len(parsed_data[i])):
            if parsed_data[i][indication] != '' and float(parsed_data[i][indication]) != 0:
                if dict_line.get(parsed_data[0][indication]):
                    dict_line[parsed_data[0][indication]] = (float(dict_line.get(parsed_data[0][indication]))
                                                             + float(parsed_data[i][indication])) / 2
                else:
                    dict_line[parsed_data[0][indication]] = float(parsed_data[i][indication])
        data[rounding] = dict_line
    return data

def processing_count_jira(parsed_data: list) -> dict:
    """
    Функция проходит по спискам в списке полученных данных начиная с 3 индекса. В 0 индексе содержаться ФИО
    сотрубников (1 - процесс изменения статусов, 2 - сводные данные).
    В функцию заложена проверка формата даты с указанным временем или без него. Формат даты в изначальном файле:
    'месяц 31 1999'.
    :param parsed_data: список строк в формате список из файла
    :return: {datetime: {'str': int}}
    """
    result_data = {}
    for indx_out_list in range(3, len(parsed_data)):
        try:
            date_line = datetime.strptime(parsed_data[indx_out_list][0], "%b %d %Y %I%p")
        except:
            date_line = datetime.strptime(parsed_data[indx_out_list][0], "%b %d %Y")
        rounding = date_line.replace(hour=0, minute=0, second=0, microsecond=0)
        dict_line = {}
        for indx_int_list in range(1, len(parsed_data[indx_out_list])):
            if parsed_data[indx_out_list][indx_int_list].isdigit() and \
                    int(parsed_data[indx_out_list][indx_int_list]) != 0:
                if dict_line is False:
                    dict_line[parsed_data[0][indx_int_list]] = int(parsed_data[indx_out_list][indx_int_list])
                elif dict_line.get(parsed_data[0][indx_int_list], 0) == 0:
                    dict_line[parsed_data[0][indx_int_list]] = int(parsed_data[indx_out_list][indx_int_list])
                else:
                    temp_count = dict_line.get(parsed_data[0][indx_int_list])\
                                 + int(parsed_data[indx_out_list][indx_int_list])
                    dict_line[parsed_data[0][indx_int_list]] = temp_count
        result_data[rounding] = dict_line
    return result_data

def processing_call(parsed_data: list):
    data = {}
    dict_line = {}
    for elem in parsed_data:
        date_line = datetime.strptime(elem[0].replace('"', ''), "%d.%m.%Y %H:%M") \
            .replace(hour=0, minute=0, second=0)
        if not dict_line or dict_line.get(elem[2].replace('"', ''), 0) == 0:
            dict_line[elem[2].replace('"', '')] = 1
        else:
            dict_line[elem[2].replace('"', '')] = dict_line.get(elem[2].replace('"', '')) + 1
    data[date_line] = dict_line
    return data

def processing_between_time(data_list: list) -> list:
    """
    Обратным циклом проходит по данным и собрает в словарь идентификаторы пользователя начиная с первого
    упоминания статуса 'ReviewRequested'. Временные метки добавляются к списку по мере совпадения идентификаторов
    с ключом.
    В цикле по словарю вычисляется разница между ближайшими значениями (исключая values = 1 и значения не имеющие пары).
    Значения timedelta переводятся в показатель количества минут(float).
    Задается ключ, в качестве значения передается список с параметрами: id_партнера, да авхода, дата выхода, дельта
    :return: timedelta_dict
    """
    timestamps_temp_dict = {}
    for elem in range(len(data_list)-1, -1, -1):
        if data_list[elem][2] == 'ReviewRequested':
            if not timestamps_temp_dict or timestamps_temp_dict.get(data_list[elem][0], 0) == 0:
                timestamps_temp_dict[data_list[elem][0]] = [data_list[elem][1]]
            else:
                timestamps_temp_dict[data_list[elem][0]].append(data_list[elem][1])
        else:
            if timestamps_temp_dict and timestamps_temp_dict.get(data_list[elem][0], 0) != 0:
                timestamps_temp_dict[data_list[elem][0]].append(data_list[elem][1])
    timedelta_dict = {}
    key_value = 0
    for ident, time_list in timestamps_temp_dict.items():
        if len(time_list) > 1:
            for i in range(0, len(time_list)-1, 2):
                timedelta_list = []
                time_result = datetime.strptime(time_list[i+1], '%Y-%m-%dT%H:%M:%S.%f')\
                              - datetime.strptime(time_list[i], '%Y-%m-%dT%H:%M:%S.%f')
                total_minuts = time_result.total_seconds() / 60
                timedelta_list.append(ident)
                timedelta_list.append(time_list[i])
                timedelta_list.append(time_list[i+1])
                timedelta_list.append(total_minuts)
                timedelta_dict[key_value] = timedelta_list
                key_value +=1
    return timedelta_dict

def processing_coordinator_evaluations(data_list: list) -> dict:
    evalutions_dict = {}
    for elem in data_list:
        time_mark = datetime.strptime(elem[4].split(' ')[0], '%d.%m.%Y').date()
        if not evalutions_dict or evalutions_dict.get(time_mark, 0) == 0:
            evalutions_dict[time_mark] = {elem[2]: int(elem[0])}
        else:
            if evalutions_dict.get(time_mark).get(elem[2], 0) == 0:
                temp_dict = evalutions_dict.get(time_mark)
                temp_dict[elem[2]] = int(elem[0])
                evalutions_dict[time_mark] = temp_dict
            else:
                temp_dict = evalutions_dict.get(time_mark)
                temp_dict[elem[2]] = (temp_dict.get(elem[2]) +int(elem[0])) / 2
                evalutions_dict[time_mark] = temp_dict
    return evalutions_dict
