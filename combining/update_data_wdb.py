from loader import db

from modul import read_portal_file
from modul import processing_data_portal
from modul import read_time_jira_file
from modul import processing_time_jira
from modul import read_SLA_jira_file
from modul import processing_SLA_jira
from modul import read_count_jira_file
from modul import processing_count_jira
from modul import read_call_file
from modul import processing_call
from modul import reade_coordinator_evaluations
from modul import processing_coordinator_evaluations


def rewriting_data_db_jira(dict_table: dict):
    """
    Записывает данные джиры в БД, если обнаружены какие-либо данные за дату. Перезаписывает или делает новую запись
    :param dict_table: {dict_data: {name: value}, db_data: [tuples], upd_method: , add_method: , col_name: }
    :return:
    """
    updating_method = dict_table.get('upd_method')
    adding_method = dict_table.get('add_method')
    column_name = dict_table.get('col_name')
    list_name = dict_table.get('dict_data').keys()
    for name_key in list_name:
        name = name_key.split(" ")[0]
        tg_id = db.get_the_user(name=name)[0]
        update_status = True
        for elem in dict_table.get('db_data'):
            if elem[2] == tg_id:
                dict_from_db = {'id': elem[0], column_name: dict_table.get('dict_data').get(name_key)}
                updating_method(dict_from_db)
                update_status = False
        if update_status:
            adding_method({'date': dict_table.get('db_data')[0][1], 'user': int(tg_id),
                           column_name: dict_table.get('dict_data').get(name_key)})

def writing_db_jira(dict_table: dict):
    """
    Записывает данные джиры в БД, если записей за дату нет
    :param dict_table: {date_obj: datetime, dict_data: {name: value}, add_method: , col_name: }
    :return:
    """
    adding_method = dict_table.get('add_method')
    column_name = dict_table.get('col_name')
    list_name = dict_table.get('dict_data').keys()
    for name_key in list_name:
        name = name_key.split(" ")[0]
        tg_id = db.get_the_user(name=name)[0]
        adding_method({'date': dict_table.get('date_obj'), 'user': int(tg_id),
                       column_name: dict_table.get('dict_data').get(name_key)})


def update_wdb_general(data: dict):
    temp_tuple = db.get_general(date=data.get('date'))
    if temp_tuple:
        if int(data.get('new')) != temp_tuple[0][1] or int(data.get('fast')) != temp_tuple[0][2]:
            db.update_general(data)
    else:
        db.add_general(data)


def update_wdb_portal(date):
    dict_portal = processing_data_portal(read_portal_file('./cred/portal.csv'))
    db_data = db.get_date_portal(date=date)
    if db_data:
        for key, value in dict_portal.items():
            tg_id = db.get_the_user(name=key.split(" ")[0])[0]
            for i in range(len(db_data)):
                if int(db_data[i][2]) == int(tg_id):
                    if int(db_data[i][3]) != value:
                        db.update_portal({'verif': value, 'id': db_data[i][0]})
    else:
        for key, value in dict_portal.items():
            tg_id = db.get_the_user(name=key.split(" ")[0])[0]
            db.add_portal({'date': date, 'user': tg_id, 'verif': value})


def update_wdb_count_jira():
    dict_count = processing_count_jira(read_count_jira_file('./cred/count_jira.csv'))
    list_date = dict_count.keys()
    for elem in list_date:
        data_portal = db.get_jira_count(date=elem)
        if data_portal:
            rewriting_data_db_jira({'dict_data': dict_count.get(elem), 'db_data': data_portal,
                           'upd_method': db.update_jira_count, 'add_method':  db.add_jira_count, 'col_name': 'count'})
        else:
            writing_db_jira({'date_obj': elem, 'dict_data': dict_count.get(elem),
                             'add_method':  db.add_jira_count, 'col_name': 'count'})


def update_wdb_sla_jira():
    dict_count = processing_SLA_jira(read_SLA_jira_file('./cred/SLA_jira.csv'))
    list_date = dict_count.keys()
    for elem in list_date:
        data_portal = db.get_jira_sla(date=elem)
        if data_portal:
            rewriting_data_db_jira({'dict_data': dict_count.get(elem), 'db_data': data_portal,
                           'upd_method': db.update_jira_sla, 'add_method': db.add_jira_sla, 'col_name': 'sla'})
        else:
            writing_db_jira({'date_obj': elem, 'dict_data': dict_count.get(elem),
                             'add_method': db.add_jira_sla, 'col_name': 'sla'})



def update_wdb_time_jira():
    dict_count = processing_time_jira(read_time_jira_file('./cred/time_jira.csv'))
    list_date = dict_count.keys()
    for elem in list_date:
        data_portal = db.get_jira_time(date=elem)
        if data_portal:
            rewriting_data_db_jira({'dict_data': dict_count.get(elem), 'db_data': data_portal,
                           'upd_method': db.update_jira_time, 'add_method': db.add_jira_time, 'col_name': 'time'})
        else:
            writing_db_jira({'date_obj': elem, 'dict_data': dict_count.get(elem),
                             'add_method': db.add_jira_time, 'col_name': 'time'})


def update_wdb_call():
    dict_count = processing_call(read_call_file('./cred/call.csv'))
    list_date = dict_count.keys()
    for elem in list_date:
        data_portal = db.get_call(date=elem)
        if data_portal:
            list_name = dict_count.get(elem).keys()
            for name_key in list_name:
                name = name_key.split(" ")[0]
                tg_id = db.get_the_user(name=name)[0]
                corrector = True
                for i_tuple in data_portal:
                    if i_tuple[2] == tg_id:
                        corrector = False
                if corrector:
                    new_entry = {'date': elem,
                                 'user': tg_id,
                                 'count': dict_count.get(elem).get(name_key)}
                    db.add_call(new_entry)
        else:
            list_name = dict_count.get(elem).keys()
            for name_key in list_name:
                name = name_key.split(" ")[0]
                tg_id = db.get_the_user(name=name)[0]
                if tg_id:
                    new_entry = {'date': elem,
                                 'user': tg_id,
                                 'count': dict_count.get(elem).get(name_key)}
                    db.add_call(new_entry)

def update_coordinator_evolutions(path: str):
    dict_data = processing_coordinator_evaluations(reade_coordinator_evaluations(path))
    users_list = db.get_user()
    users_dict = {}
    for elem in users_list:
        users_dict[elem[1]] = elem[0]
    for key, value in dict_data.items():
        date_upd = key
        for key_d, value_d in value.items():
            check_db = db.get_the_evolutions({'date_ev': date_upd, 'user_id': users_dict.get(key_d.split(" ")[0])})
            if not check_db:
                db.add_evolutions({'date_ev': date_upd,
                                   'user_id': users_dict.get(key_d.split(" ")[0]),
                                   'mean_evolutions': value_d})
            else:
                db.update_evolutions({'mean_evolutions': value_d, 'id': check_db[0][0]})
