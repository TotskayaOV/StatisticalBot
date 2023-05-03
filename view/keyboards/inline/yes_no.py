from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .call_back import yesno_data

kb_yesno_inline = InlineKeyboardMarkup(row_width=2)

btn_yes = InlineKeyboardButton(text='ДА', callback_data=yesno_data.new(yes_no='yes'))
btn_no = InlineKeyboardButton(text='НЕТ', callback_data=yesno_data.new(yes_no='no'))

kb_yesno_inline.row(btn_yes, btn_no)
