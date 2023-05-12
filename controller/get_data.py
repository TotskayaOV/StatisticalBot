from loader import db
from .combining_data import summation_data_general_portal, summation_data_jira_call


def read_wb_data(data_obj, date):
    genetal_data = db.get_general(date)
    general_string = '\n🤓Общие показатели:\n'
    if genetal_data:
        for elem in genetal_data:
            general_string = general_string + 'Количество новых анкет: ' + str(elem[1])\
                            + '\nКоличество верифицированных за 15 минут: ' + str(elem[2])\
                            + '\n% верификации за 15 минут: ' + str(round((elem[2] * 100) / elem[1], 2)) + '%\n'
    else:
        general_string = general_string + "данных за эту дату нет. 😔\n"
    portal_data = db.get_date_portal(date)
    portal_string = '\n🧑🏻‍💻Результаты портала:\n\n'
    all_portal = 0
    if portal_data:
        for elem in portal_data:
            all_portal = all_portal + elem[3]
        portal_string = portal_string + '▪️Всего анкет проверено: ' + str(all_portal) + '\n'
        for elem in portal_data:
            portal_string = portal_string + (db.get_the_user(id=elem[2]))[1] + ': ' + str(elem[3]) + '\n'
    else:
        portal_string = portal_string + "данных за эту дату нет. 😔\n"
    jira_count_data = db.get_jira_count(date=date)
    jira_count_string = '\n📦Количество выполненных заявок:\n\n'
    if jira_count_data:
        for elem in jira_count_data:
            if int(elem[2]) != 111121:
                jira_count_string = jira_count_string + (db.get_the_user(id=elem[2]))[1] + ': ' + str(elem[3]) + '\n'
    else:
        jira_count_string = jira_count_string + "данных за эту дату нет. 😔\n"
    jira_time_data = db.get_jira_time(date=date)
    jira_time_string = '\n⏳Среднее время выполнения заявки:\n\n'
    if jira_time_data:
        for elem in jira_time_data:
            jira_time_string = jira_time_string + (db.get_the_user(id=elem[2]))[1] + ': ' + str(elem[3]) + '\n'
    else:
        jira_time_string = jira_time_string + "данных за эту дату нет. 😔\n"
    jira_sla_data = db.get_jira_sla(date=date)
    jira_sla_string = '\n📊SLA выполнения заявок:\n\n'
    if jira_sla_data:
        all_sla = 0
        is_Po = False
        for elem in jira_sla_data:
            if int(elem[2]) == 111121:
                is_Po = True
            if int(elem[2]) != 111121:
                jira_sla_string = jira_sla_string + (db.get_the_user(id=elem[2]))[1] + ': ' + str(elem[3] * 100) + '%\n'
                all_sla = all_sla + (elem[3] * 100)
        if is_Po:
            jira_sla_string = jira_sla_string + '\nSLA отдела: ' + str(round(all_sla / (len(jira_sla_data)-1), 1)) + '%\n'
        else:
            jira_sla_string = jira_sla_string + '\nSLA отдела: ' + str(round(all_sla/len(jira_sla_data), 1)) + '%\n'
    else:
        jira_sla_string = jira_sla_string + "данных за эту дату нет. 😔\n"
    call_data = db.get_call(date=date)
    call_string = '\n📞Количество звонков:\n\n'
    if call_data:
        all_call = 0
        for elem in call_data:
            call_string = call_string + (db.get_the_user(id=elem[2]))[1] + ': ' + str(elem[3]) + '\n'
            all_call = all_call + elem[3]
        call_string = call_string + '\nОбщее количество звонков: ' + str(all_call) + '\n'
    else:
        call_string = call_string + "данных за эту дату нет. 😔\n"
    full_string = 'Данные за ' + data_obj + '\n' + general_string + portal_string + jira_count_string\
                  + jira_time_string + jira_sla_string + call_string
    return (full_string)

def read_wb_period(que_dict: dict):
    """

    :param que_dict: {name_beg_date: str, name_end_date: str, beg_date: datetime, end_date: datetime}
    :return:
    """
    finally_string = f"Данные за период {que_dict.get('name_beg_date')} - {que_dict.get('name_end_date')}\n\n"
    portal_data = summation_data_general_portal({'begin_period': que_dict.get('beg_date'),
                                                 'end_period': que_dict.get('end_date')})
    finally_string += f"Пришло на портал новых партнеров: {portal_data.get('new')}\n" \
                      f"из них верифицировано за 15 минут" \
                      f" {round(portal_data.get('fast')*100/portal_data.get('new'), 1)}%\n" \
                      f"Всего выполнено проверок: {portal_data.get('total')}\n"
    jira_count_data = summation_data_jira_call({'begin_period': que_dict.get('beg_date'),
                                                 'end_period': que_dict.get('end_date'),
                                                'get_method': db.get_jira_count})
    jira_sla_data = summation_data_jira_call({'begin_period': que_dict.get('beg_date'),
                                                 'end_period': que_dict.get('end_date'),
                                                'get_method': db.get_jira_sla})
    jira_time_data = summation_data_jira_call({'begin_period': que_dict.get('beg_date'),
                                              'end_period': que_dict.get('end_date'),
                                              'get_method': db.get_jira_time})
    call_data = summation_data_jira_call({'begin_period': que_dict.get('beg_date'),
                                              'end_period': que_dict.get('end_date'),
                                              'get_method': db.get_call})
    time_in_seconds = round(jira_time_data.get('time') / jira_time_data.get('count') * 60)
    minutes, seconds = divmod(time_in_seconds, 60)
    finally_string += f"Заявок в Jira выполнено: {jira_count_data.get('total')}\n" \
                      f"SLA выполнения заявок за период составил" \
                      f" {round((jira_sla_data.get('total')/jira_sla_data.get('count')) * 100, 1)}%\n" \
                      f"Среднее время выполнения заявки сотавило: {minutes} мин. {seconds} сек.\n" \
                      f"Количество звонков: {call_data.get('total')}"
    return finally_string
