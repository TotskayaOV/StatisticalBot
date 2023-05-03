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


def update_wdb_general(data: dict):
    temp_tuple = db.get_general(date=data.get('date'))
    if temp_tuple:
        if data.get('new') != temp_tuple[0][1] or data.get('fast') != temp_tuple[0][2]:
            db.update_portal(data)
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
                    db.add_jira_count(new_entry)
        else:
            list_name = dict_count.get(elem).keys()
            for name_key in list_name:
                name = name_key.split(" ")[0]
                print(name)
                tg_id = db.get_the_user(name=name)[0]
                if tg_id:
                    new_entry = {'date': elem,
                                 'user': tg_id,
                                 'count': dict_count.get(elem).get(name_key)}
                    db.add_jira_count(new_entry)


def update_wdb_sla_jira():
    dict_count = processing_SLA_jira(read_SLA_jira_file('./cred/SLA_jira.csv'))
    list_date = dict_count.keys()
    for elem in list_date:
        data_portal = db.get_jira_sla(date=elem)
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
                                 'sla': dict_count.get(elem).get(name_key)}
                    db.add_jira_sla(new_entry)
        else:
            list_name = dict_count.get(elem).keys()
            for name_key in list_name:
                name = name_key.split(" ")[0]
                tg_id = db.get_the_user(name=name)[0]
                if tg_id:
                    new_entry = {'date': elem,
                                 'user': tg_id,
                                 'sla': dict_count.get(elem).get(name_key)}
                    db.add_jira_sla(new_entry)

def update_wdb_time_jira():
    dict_count = processing_time_jira(read_time_jira_file('./cred/time_jira.csv'))
    list_date = dict_count.keys()
    for elem in list_date:
        data_portal = db.get_jira_time(date=elem)
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
                                 'time': dict_count.get(elem).get(name_key)}
                    db.add_jira_time(new_entry)
        else:
            list_name = dict_count.get(elem).keys()
            for name_key in list_name:
                name = name_key.split(" ")[0]
                tg_id = db.get_the_user(name=name)[0]
                if tg_id:
                    new_entry = {'date': elem,
                                 'user': tg_id,
                                 'time': dict_count.get(elem).get(name_key)}
                    db.add_jira_time(new_entry)


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


# print(dict.get(datetime(2023, 4, 29, 0, 0)))
# print(jira_dict.get(datetime(2023, 4, 29, 0, 0)))
# print(sla_dict.get(datetime(2023, 4, 29, 0, 0)))
# print(count_dict.get(datetime(2023, 4, 29, 0, 0)))
# print(call_dict.get(datetime(2023, 4, 29, 0, 0)))

    # list_date = dict_portal.keys()
    # for elem in list_date:
    #     data_portal = db.get_date_portal(date=elem)
    #     if data_portal:
    #         list_name = dict_portal.get(elem).keys()
    #         for name_key in list_name:
    #             name = name_key.split(" ")[0]
    #             tg_id = db.get_the_user(name=name)[0]
    #             corrector = True
    #             for i_tuple in data_portal:
    #                 if i_tuple[2] == tg_id:
    #                     rewrite_dict = {'verif': dict_portal.get(elem).get(name_key)[0],
    #                                    'other_act': dict_portal.get(elem).get(name_key)[1],
    #                                    'id': i_tuple[0]}
    #                     db.update_portal(rewrite_dict)
    #                     corrector = False
    #             if corrector:
    #                 new_entry = {'date': elem,
    #                              'user': tg_id,
    #                              'verif': dict_portal.get(elem).get(name_key)[0],
    #                              'other_act': dict_portal.get(elem).get(name_key)[1]}
    #                 db.add_portal(new_entry)
    #     else:
    #         list_name = dict_portal.get(elem).keys()
    #         for name_key in list_name:
    #             name = name_key.split(" ")[0]
    #             tg_id = db.get_the_user(name=name)[0]
    #             if tg_id:
    #                 new_entry = {'date': elem,
    #                              'user': tg_id,
    #                              'verif': dict_portal.get(elem).get(name_key)[0],
    #                              'other_act': dict_portal.get(elem).get(name_key)[1]}
    #                 db.add_portal(new_entry)
