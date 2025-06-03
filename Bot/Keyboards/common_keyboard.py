from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Студент', callback_data='role_student'), InlineKeyboardButton(text='Преподаватель', callback_data='role_teacher')],
    [InlineKeyboardButton(text='Декан', callback_data='role_dean')]
])

