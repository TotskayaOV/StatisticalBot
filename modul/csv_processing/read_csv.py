import csv

def read_portal_file(path: str)  -> list:
    '''
    Метод работает с файлом с данными с портала. Парсит строки, формирует список со словарями по ключам
    дата, действие, ФИО
    :param path: путь к файлу
    :return: [{'date': '', 'action': '', 'name': ''}]
    '''
    db_list = []
    with open(path, 'r', encoding='UTF-8') as file:
        my_list = file.readlines()
        for line in range(1, len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(','))
        return db_list
    # db_list = []
    # with open(path, 'r', encoding='UTF-8') as file:
    #     my_list = file.readlines()
    #     for line in range(1, len(my_list)):
    #         values = my_list[line].split(',+')
    #         date_action = values[0].split('T')[0]
    #         values = values[1].split(',')
    #         action = values[1]
    #         coord_name = values[2].rstrip("\n")
    #         data_dict = {'date': date_action,
    #                      'action': action,
    #                      'name': coord_name}
    #         db_list.append(data_dict)
    #     return db_list

def read_time_jira_file(path: str)  -> list:
    '''
    Метод работает с файлом с данными с jira. Парсит строки, формирует список со списками
    :param path: путь к файлу
    :return: [[ФИО], [дата, значения]]
    '''
    db_list = []
    with open(path, 'r', encoding='UTF-8') as file:
        my_list = file.readlines()
        for line in range(1, len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(','))
        return db_list

def read_SLA_jira_file(path: str) -> list:
    '''
    Метод работает с файлом с данными с jira. Парсит строки, формирует список со словарями по ключам
    дата, действие, ФИО
    :param path: путь к файлу
    :return: [{'date': '', 'action': '', 'name': ''}]
    '''
    db_list = []
    with open(path, 'r', encoding='UTF-8') as file:
        my_list = file.readlines()
        for line in range(len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(','))
        return db_list

def read_count_jira_file(path: str) -> list:
    '''
    Метод работает с файлом с данными с jira. Парсит строки, формирует список со словарями по ключам
    дата, действие, ФИО
    :param path: путь к файлу
    :return: [{'date': '', 'action': '', 'name': ''}]
    '''
    db_list = []
    with open(path, 'r', encoding='UTF-8') as file:
        my_list = file.readlines()
        for line in range(len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(','))
        return db_list

def read_call_file(path: str) -> list:
    '''
    Метод работает с файлом с данными с jira. Парсит строки, формирует список со словарями по ключам
    дата, действие, ФИО
    :param path: путь к файлу
    :return: [{'date': '', 'action': '', 'name': ''}]
    '''
    db_list = []
    with open(path, 'r', encoding='UTF-8') as file:
        my_list = file.readlines()
        for line in range(2, len(my_list)-1, 2):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(';'))
        return db_list


        #     values = my_list[line].split(',+')
        #     date_action = values[0].split('T')[0]
        #     values = values[1].split(',')
        #     action = values[1]
        #     coord_name = values[2].rstrip("\n")
        #     data_dict = {'date': date_action,
        #                  'action': action,
        #                  'name': coord_name}
        #     db_list.append(data_dict)
        # return db_list
