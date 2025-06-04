from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)

dean_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Посмотреть предложенные расписания', callback_data='check_suggested')]
])

suggest_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<', callback_data='left'), InlineKeyboardButton(text='>', callback_data='right')],
    [InlineKeyboardButton(text='Утвердить', callback_data='approve'), InlineKeyboardButton(text='Полный вариант', callback_data='full_week'), InlineKeyboardButton(text='Отказ', callback_data='rejection')],
    [InlineKeyboardButton(text='Прошлое предложение', callback_data='last'), InlineKeyboardButton(text='Назад', callback_data='back'), InlineKeyboardButton(text='Следующее предложение', callback_data='next')]
])

back_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])