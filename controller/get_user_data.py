from loader import db
from .combining_data import summation_data_general_portal_user, summation_data_user_jira_call
from .combining_data import summation_data_general_portal, summation_data_jira_call


def read_user_wb_data(data_obj, date, user_id):
    genetal_data = db.get_general(date)
    general_string = ''
    if genetal_data:
        general_string = general_string + '🤓Общие показатели:\n'
        for elem in genetal_data:
            general_string = general_string + 'Количество новых анкет: ' + str(elem[1])\
                            + '\nКоличество верифицированных за 15 минут: ' + str(elem[2])\
                            + '\n\t\t% верификации за 15 минут: ' + str(round((elem[2] * 100) / elem[1], 2)) + '%\n'
    portal_data = db.get_date_portal(date)
    portal_string = ''
    all_portal = 0
    if portal_data:
        for elem in portal_data:
            all_portal = all_portal + elem[3]
        for elem in portal_data:
            if elem[2] == user_id:
                portal_string = portal_string + '\tОбработано анкет: ' + str(elem[3]) + '\n'
                port_result = (elem[3] * 100) / all_portal
                portal_string = portal_string + '\t\t\t\t' + str(round(port_result, 2)) + '% от общего количества\n'
    jira_count_data = db.get_jira_count(date=date)
    jira_count_string = ''
    count_jira = 0
    if jira_count_data:
        for elem in jira_count_data:
            if int(elem[2]) != 111121:
                count_jira += int(elem[3])
            if elem[2] == user_id:
                jira_count_string = jira_count_string + str(elem[3]) + '\n'
    jira_time_data = db.get_jira_time(date=date)
    jira_time_string = ''
    if jira_time_data:
        for elem in jira_time_data:
            if elem[2] == user_id:
                jira_time_string = jira_time_string + str(elem[3]) + '\n'
    jira_sla_data = db.get_jira_sla(date=date)
    jira_sla_string = ''
    all_sla = 0
    if jira_sla_data:
        is_Po = False
        for elem in jira_sla_data:
            if int(elem[2]) == 111121:
                is_Po = True
            if elem[2] == user_id:
                jira_sla_string = jira_sla_string + str(round(elem[3] * 100, 2)) + '%\n'
            if int(elem[2]) != 111121:
                all_sla = all_sla + (elem[3] * 100)
    call_data = db.get_call(date=date)
    call_string = ''
    all_call = 0
    if call_data:
        for elem in call_data:
            if elem[2] == user_id:
                call_string = call_string + str(elem[3]) + '\n'
            all_call = all_call + elem[3]
    evolution_data = db.get_evolutions(date_ev=date.date())
    evol_string = ''
    evo_all = 0
    if evolution_data:
        for elem in evolution_data:
            evo_all = evo_all + elem[3]
            if elem[2] == user_id:
                check_emod = elem[3]
                evol_string = evol_string + str(elem[3]) + '\n'
    full_string = 'Данные за ' + data_obj + ':\n'
    if general_string:
        full_string = full_string + general_string
    if all_portal:
        final_word = 'анкет'
        prefinal_word = 'проверено '
        if all_portal == 1 or (20 < all_portal < 100 and all_portal % 10 == 1)\
                or (all_portal % 10 == 1 and all_portal % 100 != 11):
            final_word = 'анкета'
            prefinal_word = 'проверена '
        elif 1 < all_portal < 5 or (20 < all_portal < 100 and 1 < all_portal % 10 < 5)\
                or (1 < all_portal % 10 < 5 and (all_portal % 100 < 11 or all_portal % 100 > 20)):
            final_word = 'анкеты'
        full_string = full_string + 'Всего ' + prefinal_word + str(all_portal) + ' ' + final_word + '\n'
    if count_jira:
        full_string = full_string + f"Всего заявок в Jira выполнено: {str(count_jira)}\n"
    if all_sla:
        if is_Po:
            full_string = full_string + 'SLA выполнения зявок в Jira отдела: ' + str(round(
                all_sla / (len(jira_sla_data) - 1), 1)) + '%\n'
        else:
            full_string = full_string + 'SLA выполнения зявок в Jira отдела: ' + str(round(
                all_sla/len(jira_sla_data), 1)) + '%\n'
    if all_call:
        full_string = full_string + 'Общее количество звонков: ' + str(all_call) + '\n'
    if evo_all:
        full_string = full_string + 'Оценка отдела за день: ' + str(round(evo_all / len(evolution_data), 2)) + '\n'
    if portal_string or jira_count_string or jira_time_string or jira_sla_string or call_string or evol_string:
        full_string = full_string + '\nТвои показатели:\n'
        if portal_string:
            full_string = full_string + '\n🧑🏻‍💻Результаты по порталу:\n' + portal_string
        if jira_count_string:
            full_string += '📦 Количество выполненных заявок JIRA: ' + jira_count_string
        if jira_time_string:
            full_string += '⏳ Среднее время выполнения заявки:' + jira_time_string
        if jira_sla_string:
            full_string += '📊SLA выполнения заявок: ' + jira_sla_string
        if call_string:
            full_string += '📞 Количество звонков: ' + call_string
        if evol_string:
            if check_emod >= 90:
                full_string += '✅ Оценка за день: ' + evol_string
            else:
                full_string += '⛔️ Оценка за день: ' + evol_string
    return (full_string)

def read_user_period(que_dict: dict):
    """

    :param que_dict: {name_beg_date: str, name_end_date: str, beg_date: datetime, end_date: datetime, user_id: int}
    :return: string
    """
    finally_string = f"Данные за период {que_dict.get('name_beg_date')} - {que_dict.get('name_end_date')}\n"
    portal_data = summation_data_general_portal({'begin_period': que_dict.get('beg_date'),
                                                 'end_period': que_dict.get('end_date')})
    users_list = db.get_user()
    portal_string = ''
    jira_string = ''
    call_string = ''
    for elem in users_list:
        if elem[0] == que_dict.get('user_id'):
            finally_string += f'{elem[1]}\n'
            pt_dt = summation_data_general_portal_user({'begin_period': que_dict.get('beg_date'),
                                                        'end_period': que_dict.get('end_date'), 'user_id': elem[0]})
            jc_dt = summation_data_user_jira_call({'begin_period': que_dict.get('beg_date'),
                                                   'end_period': que_dict.get('end_date'),
                                                   'get_method': db.get_jira_count, 'user_id': elem[0]})
            jt_dt = summation_data_user_jira_call({'begin_period': que_dict.get('beg_date'),
                                                  'end_period': que_dict.get('end_date'),
                                                   'get_method': db.get_jira_time, 'user_id': elem[0]})
            js_dt = summation_data_user_jira_call({'begin_period': que_dict.get('beg_date'),
                                                   'end_period': que_dict.get('end_date'),
                                                   'get_method': db.get_jira_sla, 'user_id': elem[0]})
            cl_dt = summation_data_user_jira_call({'begin_period': que_dict.get('beg_date'),
                                                   'end_period': que_dict.get('end_date'),
                                                   'get_method': db.get_call, 'user_id': elem[0]})
            if portal_data.get('total') == 0:
                portal_string = 'нет данных'
            else:
                portal_string += f"▪️ Портал: проверено анкет: {pt_dt.get('total')}, " \
                                f"{round(pt_dt.get('total') * 100 / portal_data.get('total'), 1)}% " \
                                f"от общего количества\n" \
                                f"смен на портале: {pt_dt.get('day_count')}\n"
            if jt_dt.get('day_count') != 0:
                time_in_seconds_us = round(jt_dt.get('time') / jt_dt.get('day_count') * 60)
                minutes_us, seconds_us = divmod(time_in_seconds_us, 60)
            else:
                minutes_us, seconds_us = 0, 0
            if js_dt.get('day_count') != 0:
                sla_user = round(js_dt.get('total') / js_dt.get('day_count') * 100, 2)
            else:
                sla_user = 0
            jira_string += f"▪️ JIRA: выполнено заявок: {jc_dt.get('total')}, SLA = {sla_user}%\n" \
                           f"среднее время выполнения: {minutes_us} мин. {seconds_us} сек.\n"
            call_string += f"▪️ Звонки: количество звонков: {cl_dt.get('total')}\n" \
                           f"количество дней на звонках: {cl_dt.get('day_count')}"
    finally_string = finally_string + portal_string + jira_string + call_string
    return finally_string
