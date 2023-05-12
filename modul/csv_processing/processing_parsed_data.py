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
    for i in range(1, len(parsed_data)):
        try:
            date_line = datetime.strptime(parsed_data[i][0], "%d %b %Y %I%p")
        except:
            date_line = datetime.strptime(parsed_data[i][0], "%d %b %Y")
        rounding = date_line.replace(hour=0, minute=0, second=0, microsecond=0)
        dict_line = data.get(rounding, {})
        for indication in range(1, len(parsed_data[i])):
            if float(parsed_data[i][indication]) != 0:
                if dict_line.get(parsed_data[0][indication]):
                    dict_line[parsed_data[0][indication]] = (float(dict_line.get(parsed_data[0][indication]))
                                                             + float(parsed_data[i][indication])) / 2
                else:
                    dict_line[parsed_data[0][indication]] = float(parsed_data[i][indication])
        data[rounding] = dict_line
    return data

def processing_count_jira(parsed_data: list):
    data = {}
    # print(parsed_data)
    for i in range(1, len(parsed_data)):
        try:
            date_line = datetime.strptime(parsed_data[i][0], "%d %b %Y %I%p")
        except:
            date_line = datetime.strptime(parsed_data[i][0], "%d %b %Y")
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