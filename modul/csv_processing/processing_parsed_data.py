from datetime import datetime

def processing_data_portal(parsed_data: list):
    data = {}
    print(parsed_data)
    for elem in parsed_data:
        if data.get(elem[0], 0) == 0:
            data[elem[0]] = int(elem[2])
        else:
            count = data.get(elem[0])
            data[elem[0]] = count + int(elem[2])
    print(data)
    return data
    # data = {}
    # for elem in parsed_data:
    #     date_action = datetime.strptime(elem.get('date'), "%Y-%m-%d")
    #     if data.get(date_action, 0) == 0:
    #         if 'Шоппер' in elem.get('action'):
    #             verif, check = 1, 0
    #         else:
    #             verif, check = 0, 1
    #         data[date_action] = {elem.get('name'): [verif, check]}
    #     else:
    #         dict_values = data.get(date_action)
    #         if dict_values.get(elem.get('name'), 0) == 0:
    #             if 'Шоппер' in elem.get('action'):
    #                 verif, check = 1, 0
    #             else:
    #                 verif, check = 0, 1
    #             dict_values[elem.get('name')] = [verif, check]
    #             data[date_action] = dict_values
    #         else:
    #             list_values = dict_values.get(elem.get('name'))
    #             if 'Шоппер' in elem.get('action'):
    #                 verif, check = list_values[0]+1, list_values[1]
    #             else:
    #                 verif, check = list_values[0], list_values[1]+1
    #             dict_values[elem.get('name')] = [verif, check]
    #             data[date_action] = dict_values
    # return data

def processing_time_jira(parsed_data: list):
    data = {}
    for i in range(2, len(parsed_data)):
        date_line = datetime.strptime(parsed_data[i][0], "%b %d %Y")
        dict_line = {}
        for indication in range(1, len(parsed_data[i])):
            if parsed_data[i][indication]:
                time_in_seconds = round(float(parsed_data[i][indication]) * 60)
                minutes, seconds = divmod(time_in_seconds, 60)
                dict_line[parsed_data[0][indication]] = f'{minutes}:{seconds}'
        data[date_line] = dict_line
    # print(f'time jirs {data}')
    return(data)

def processing_SLA_jira(parsed_data: list):
    data = {}
    for i in range(1, len(parsed_data)):
        date_line = datetime.strptime(parsed_data[i][0], "%d %b %Y %I%p")
        rounding = date_line.replace(hour=0, minute=0, second=0, microsecond=0)
        dict_line = {}
        for indication in range(1, len(parsed_data[i])):
            if float(parsed_data[i][indication]) != 0:
                dict_line[parsed_data[0][indication]] = float(parsed_data[i][indication])
        data[rounding] = dict_line
    return data

def processing_count_jira(parsed_data: list):
    data = {}
    # print(parsed_data)
    for i in range(1, len(parsed_data)):
        date_line = datetime.strptime(parsed_data[i][0], "%d %b %Y %I%p")
        rounding = date_line.replace(hour=0, minute=0, second=0, microsecond=0)
        dict_line = {}
        if data.get(rounding, 0) == 0:
            for indication in range(1, len(parsed_data[i])):
                if int(parsed_data[i][indication]) != 0:
                    dict_line[parsed_data[0][indication]] = parsed_data[i][indication]
            data[rounding] = dict_line
        else:
            dict_line = data.get(rounding)
            for indication in range(1, len(parsed_data[i])):
                if int(parsed_data[i][indication]) != 0:
                    if dict_line.get(parsed_data[0][indication], 0) == 0:
                        dict_line[parsed_data[0][indication]] = parsed_data[i][indication]
                    else:
                        temp_count = int(data.get(rounding).get(parsed_data[0][indication])) + int(parsed_data[i][indication])
                        dict_line[parsed_data[0][indication]] = temp_count
            data[rounding] = dict_line
    # print(f'count jirs {data}')
    return (data)

def processing_call(parsed_data: list):
    data = {}
    dict_line = {}
    date_line = datetime.strptime(parsed_data[0][0].replace('"', ''), "%d.%m.%Y")
    for elem in parsed_data:
        if int(elem[2]) + int(elem[3]) != 0:
            dict_line[elem[1].replace('"', '')] = int(elem[2]) + int(elem[3])
    data[date_line] = dict_line
    return (data)