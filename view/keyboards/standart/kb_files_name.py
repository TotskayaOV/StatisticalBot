from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_name_files = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)


btn_portal = KeyboardButton(text='Портал')
btn_call = KeyboardButton(text='Звонки')
btn_count = KeyboardButton(text='Кол-во JIRA')
btn_time = KeyboardButton(text='Time JIRA')
btn_sla = KeyboardButton(text='SLA JIRA')
btn_evo = KeyboardButton(text='Оценки')
btn_exit = KeyboardButton(text='Завершить')

kb_name_files.row(btn_portal, btn_call)
kb_name_files.row(btn_count, btn_time)
kb_name_files.row(btn_sla, btn_evo)
kb_name_files.row(btn_exit)
