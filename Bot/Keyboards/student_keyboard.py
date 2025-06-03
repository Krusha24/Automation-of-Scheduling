from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)

student = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Оставить пожелания по расписанию', callback_data='wish_shedule_student')],
    [InlineKeyboardButton(text='Посмотреть текущее расписание', callback_data='check_shedule')]
])

days = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<', callback_data='left'),InlineKeyboardButton(text='Cюда!', callback_data='here'), InlineKeyboardButton(text='>', callback_data='right')],
    [InlineKeyboardButton(text='Назад', callback_data='back'), InlineKeyboardButton(text='Отправить на рассмотрение', callback_data='send')]
])

lessons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Командно-лидерские турниры', callback_data='CLT')],
    [InlineKeyboardButton(text='Практические занятие/стажировка', callback_data='PL'), InlineKeyboardButton(text='Теоретическое занятие', callback_data='TL')],
    [InlineKeyboardButton(text='Занятие с инженерами-наставниками', callback_data='LE'), InlineKeyboardButton(text='Смежные компетенции', callback_data='WW')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='8:00', callback_data='8:00')],
    [InlineKeyboardButton(text='9:00', callback_data='9:00'), InlineKeyboardButton(text='10:00', callback_data='10:00'), InlineKeyboardButton(text='11:00', callback_data='11:00')],
    [InlineKeyboardButton(text='12:00', callback_data='12:00'), InlineKeyboardButton(text='13:00', callback_data='13:00'), InlineKeyboardButton(text='14:00', callback_data='14:00')],
    [InlineKeyboardButton(text='15:00', callback_data='15:00'), InlineKeyboardButton(text='16:00', callback_data='16:00'), InlineKeyboardButton(text='17:00', callback_data='17:00')],
    [InlineKeyboardButton(text='18:00', callback_data='18:00'), InlineKeyboardButton(text='19:00', callback_data='19:00'), InlineKeyboardButton(text='20:00', callback_data='20:00')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])