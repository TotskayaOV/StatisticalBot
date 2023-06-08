from datetime import datetime

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
    return(data)

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
    date_line = datetime.strptime(parsed_data[0][0].replace('"', ''), "%d.%m.%Y")
    for elem in parsed_data:
        if int(elem[2]) + int(elem[3]) != 0:
            dict_line[elem[1].replace('"', '')] = int(elem[2]) + int(elem[3])
    data[date_line] = dict_line
    return data