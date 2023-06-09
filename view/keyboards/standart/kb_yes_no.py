from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .kb_cancel_fsm import btn_cancel

kb_yesno = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_yes = KeyboardButton(text='Да')
btn_no = KeyboardButton(text='Нет')

kb_yesno.add(btn_yes, btn_no)
kb_yesno.add(btn_cancel)
