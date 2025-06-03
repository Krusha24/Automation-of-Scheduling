from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from Bot.Filters.role_filters import RoleFilter

from Bot.FSM.student_states import Student_Wish
from Bot.Filters.role_filters import RoleFilter

import Bot.Keyboards.student_keyboard as kb
from Bot.Utils.constants import schedule, times, count_of_lessons, all_lessons, translate, days
from Bot.Utils.validators import check_time_for_lesson
from Bot.Utils.schedule_utils import add_lesson, check_lesson_count, lesson_count, day_schedule

student_router = Router()

@student_router.callback_query(RoleFilter('student'), F.data == 'check_shedule')
async def show_shedule(call: CallbackQuery):
    schedule_message = ""
    for day in schedule:
        schedule_message += f'\n{day}:\n'
        for time in schedule[day]:
            if schedule[day][time] == 'Командно-лидерские турниры':
                schedule_message += f'8:00-20:00: {schedule[day][time]}\n'
            else:
                schedule_message += f'{time}: {schedule[day][time]}\n'
    
    await call.message.answer(schedule_message) 

@student_router.callback_query(RoleFilter('student'), F.data == 'wish_shedule_student')
async def wish_student_step_first(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[0])}', reply_markup=kb.days)
    await state.set_state(Student_Wish.monday)

@student_router.callback_query(RoleFilter('student'), Student_Wish.monday)
async def wish_student_step_second_monday(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await state.clear()
        await call.message.edit_text('Вот твои возможности.', reply_markup=kb.student)
        return
    elif call.data == 'send':
        await state.clear()
        await call.message.edit_text('Ваше желание отправлено на рассмотрение!', reply_markup=kb.student)
        return
    elif call.data == 'here':
        await state.update_data(day = days[0])
        await call.message.edit_text(f'''Отлично, теперь выберите предмет который желаете видеть в этот день:
{day_schedule(schedule, days[0])}''', reply_markup=kb.lessons)
        await state.set_state(Student_Wish.lesson)
        return
    elif call.data == 'right':
        await state.set_state(Student_Wish.tuesday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[1])}', reply_markup=kb.days)
        return
    elif call.data == 'left':
        return
    
@student_router.callback_query(RoleFilter('student'), Student_Wish.tuesday)
async def wish_student_step_second_tuesday(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await state.clear()
        await call.message.edit_text('Вот твои возможности.', reply_markup=kb.student)
        return
    elif call.data == 'send':
        await state.clear()
        await call.message.edit_text('Ваше желание отправлено на рассмотрение!', reply_markup=kb.student)
        return
    elif call.data == 'here':
        await state.update_data(day = days[1])
        await call.message.edit_text(f'''Отлично, теперь выберите предмет который желаете видеть в этот день:
{day_schedule(schedule, days[1])}''', reply_markup=kb.lessons)
        await state.set_state(Student_Wish.lesson)
        return
    elif call.data == 'right':
        await state.set_state(Student_Wish.wednesday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[2])}', reply_markup=kb.days)
        return
    elif call.data == 'left':
        await state.set_state(Student_Wish.monday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[0])}', reply_markup=kb.days)
        return

@student_router.callback_query(RoleFilter('student'), Student_Wish.wednesday)
async def wish_student_step_second_wednesday(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await state.clear()
        await call.message.edit_text('Вот твои возможности.', reply_markup=kb.student)
        return
    elif call.data == 'send':
        await state.clear()
        await call.message.edit_text('Ваше желание отправлено на рассмотрение!', reply_markup=kb.student)
        return
    elif call.data == 'here':
        await state.update_data(day = days[2])
        await call.message.edit_text(f'''Отлично, теперь выберите предмет который желаете видеть в этот день:
{day_schedule(schedule, days[2])}''', reply_markup=kb.lessons)
        await state.set_state(Student_Wish.lesson)
        return
    elif call.data == 'right':
        await state.set_state(Student_Wish.thursday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[3])}', reply_markup=kb.days)
        return
    elif call.data == 'left':
        await state.set_state(Student_Wish.tuesday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[1])}', reply_markup=kb.days)
        return

@student_router.callback_query(RoleFilter('student'), Student_Wish.thursday)
async def wish_student_step_second_thursday(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await state.clear()
        await call.message.edit_text('Вот твои возможности.', reply_markup=kb.student)
        return
    elif call.data == 'send':
        await state.clear()
        await call.message.edit_text('Ваше желание отправлено на рассмотрение!', reply_markup=kb.student)
        return
    elif call.data == 'here':
        await state.update_data(day = days[3])
        await call.message.edit_text(f'''Отлично, теперь выберите предмет который желаете видеть в этот день:
{day_schedule(schedule, days[3])}''', reply_markup=kb.lessons)
        await state.set_state(Student_Wish.lesson)
        return
    elif call.data == 'right':
        await state.set_state(Student_Wish.friday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[4])}', reply_markup=kb.days)
        return
    elif call.data == 'left':
        await state.set_state(Student_Wish.wednesday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[2])}', reply_markup=kb.days)
        return
    
@student_router.callback_query(RoleFilter('student'), Student_Wish.friday)
async def wish_student_step_second_friday(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await state.clear()
        await call.message.edit_text('Вот твои возможности.', reply_markup=kb.student)
        return
    elif call.data == 'send':
        await state.clear()
        await call.message.edit_text('Ваше желание отправлено на рассмотрение!', reply_markup=kb.student)
        return
    elif call.data == 'here':
        await state.update_data(day = days[4])
        await call.message.edit_text(f'''Отлично, теперь выберите предмет который желаете видеть в этот день:
{day_schedule(schedule, days[4])}''', reply_markup=kb.lessons)
        await state.set_state(Student_Wish.lesson)
        return
    elif call.data == 'right':
        return
    elif call.data == 'left':
        await state.set_state(Student_Wish.thursday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[3])}', reply_markup=kb.days)
        return
    

@student_router.callback_query(RoleFilter('student'), Student_Wish.lesson)
async def wish_student_step_third(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await state.set_state(Student_Wish.monday)
        await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[0])}', reply_markup=kb.days)
        return
    lesson_name = translate[call.data]
    count = check_lesson_count(schedule, lesson_name)
    if count < count_of_lessons[lesson_name]:
        await state.update_data(lesson = lesson_name)
        await call.message.edit_text("Введите время, в которое желаете видеть этот предмет:", reply_markup=kb.time)
        await state.set_state(Student_Wish.time)
        return
    elif count >= count_of_lessons[lesson_name]:
        await call.message.answer(f'Этого предмета ({lesson_name}) уже достаточно на неделю, попробуйте другие предметы.')
        return
    
@student_router.callback_query(RoleFilter('student'), Student_Wish.time)
async def wish_student_step_third(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
            await state.set_state(Student_Wish.lesson)
            await call.message.edit_text(f'На какой день вы хотите добавить свое пожелание?\n{day_schedule(schedule, days[0])}', reply_markup=kb.lessons)
            return
    data = await state.get_data()
    check_time= check_time_for_lesson(schedule, data['lesson'], call.data, data['day'])
    if check_time[0] == True:
        await state.update_data(time = call.data)
        data = await state.get_data()
        if lesson_count(schedule) == 50:
            await state.clear()
            await call.message.edit_text('Ваше желание отправлено на рассмотрение!', reply_markup=kb.main)
            return
        else:
            await state.set_state(Student_Wish.monday)
            await add_lesson(data['day'], data['time'], data['lesson'])
            text = f'''
{all_lessons[0]}: {check_lesson_count(schedule, all_lessons[0])} (Минимум - 1)
{all_lessons[1]}: {check_lesson_count(schedule, all_lessons[1])//4} (Минимум - 4)
{all_lessons[2]}: {check_lesson_count(schedule, all_lessons[2])//4} (Минимум - 4)
{all_lessons[3]}: {check_lesson_count(schedule, all_lessons[3])//4} (Минимум - 4)
{all_lessons[4]}: {check_lesson_count(schedule, all_lessons[4])//6} (Минимум - 1)
'''
            await call.message.edit_text(f'Отлично, но еще не все!\n{text}\n{day_schedule(schedule, days[0])}', reply_markup=kb.days)
    else:
        await call.message.answer(f'''{check_time[1]}
На какой день вы хотите добавить свое пожелание:''')
        return
