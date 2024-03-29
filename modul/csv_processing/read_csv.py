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
        for line in range(1, len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(','))
        print(db_list)
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
        for line in range(1, len(my_list)):
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
        for line in range(2, len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(';'))
        return db_list

def reade_between_time(path_file='./cred/difference.csv') -> list:
    db_list = []
    with open(path_file, 'r', encoding='UTF-8') as file:
        csv_reader = csv.reader(file, delimiter=',', quoting=csv.QUOTE_ALL)
        for line_num, row in enumerate(csv_reader):
            if line_num >= 2:  # Пропуск первых двух строк
                db_list.append(row)
        return db_list

def reade_coordinator_evaluations(path_file='./cred/evolutions.csv') -> list:
    db_list = []
    with open(path_file, 'r', encoding='UTF-8') as file:
        my_list = file.readlines()
        for line in range(1, len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            db_list.append(temp_string2.split(';'))
        return db_list