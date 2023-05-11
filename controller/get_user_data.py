from loader import db


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
    if jira_count_data:
        for elem in jira_count_data:
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
                jira_sla_string = jira_sla_string + str(elem[3] * 100) + '%\n'
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
    full_string = 'Данные за ' + data_obj + ':\n'
    if general_string:
        full_string = full_string + general_string
    if all_portal:
        final_word = 'анкет'
        if all_portal == 1 or (all_portal < 100 and all_portal % 10 == 1)\
                or (all_portal % 100 == 1 and all_portal % 10 != 11):
            final_word = 'анкета'
        elif 1 < all_portal < 5 or (all_portal < 100 and 1 < all_portal % 10 < 5)\
                or (1 < all_portal % 100 < 5 and (all_portal % 100) / 10 != 1):
            final_word = 'анкеты'
        full_string = full_string + 'Всего проверено ' + str(all_portal) + ' ' + final_word + '\n'
    if all_sla:
        if is_Po:
            full_string = full_string + 'SLA выполнения зявок в Jira отдела: ' + str(round(
                all_sla / (len(jira_sla_data) - 1), 1)) + '%\n'
        else:
            full_string = full_string + 'SLA выполнения зявок в Jira отдела: ' + str(round(
                all_sla/len(jira_sla_data), 1)) + '%\n'
    if all_call:
        full_string = full_string + 'Общее количество звонков: ' + str(all_call) + '\n'
    if portal_string or jira_count_string or jira_time_string or jira_sla_string or call_string:
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
    return (full_string)