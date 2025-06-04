from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from Bot.Filters.role_filters import RoleFilter

from Bot.FSM.student_states import Student_Wish
from Bot.Filters.role_filters import RoleFilter

import Bot.Keyboards.student_keyboard as kb
from Bot.Utils.constants import schedule, count_of_lessons, all_lessons, translate, days
from Bot.Utils.validators import check_time_for_lesson
from Bot.Utils.schedule_utils import add_lesson, check_lesson_count, lesson_count, day_schedule
from Bot.services import send_schedule_for_review
from Bot.messages import *
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
    await call.message.edit_text(f'{choose_day}{day_schedule(schedule, days[0])}', reply_markup=kb.days)
    await state.update_data(data=0)
    await state.update_data(suggested_schedule = schedule)
    await state.set_state(Student_Wish.day)

async def day_selection(call: CallbackQuery, state: FSMContext, day_index):
    await state.set_state(Student_Wish.day)
    await state.update_data(current_day_index=day_index)
    data = await state.get_data()
    await call.message.edit_text(
        f'{choose_day}{day_schedule(data['suggested_schedule'], days[day_index])}',
        reply_markup=kb.days
    )
    
@student_router.callback_query(RoleFilter('student'), Student_Wish.day)
async def day_navigation(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_day_index = data.get('current_day_index', 0)
    if call.data == 'right':
        if current_day_index < len(days) - 1:
            await day_selection(call, state, current_day_index + 1)
            return
    elif call.data == 'left':
        if current_day_index > 0:
            await day_selection(call, state, current_day_index - 1)
            return
    elif call.data == 'here':
        await state.update_data(day = current_day_index)
        await call.message.edit_text(f'''{choose_lesson}
{day_schedule(data['suggested_schedule'], days[current_day_index])}''', reply_markup=kb.lessons)
        await state.set_state(Student_Wish.lesson)
        return
    elif call.data == 'send':
        send = await send_schedule_for_review(call.from_user.id, data["suggested_schedule"])
        await state.clear()
        if send:
            await call.message.edit_text(schedule_send_for_review, reply_markup=kb.student)
            return
        elif not send:
            await call.message.edit_text("Вы уже отправили расписание.", reply_markup=kb.student)
            return
        
    elif call.data == 'back':
        await state.clear()
        await call.message.edit_text(student_options, reply_markup=kb.student)
        return
    

@student_router.callback_query(RoleFilter('student'), Student_Wish.lesson)
async def wish_student_step_third(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_day_index = data.get('current_day_index', 0)
    if call.data == 'back':
        await state.set_state(Student_Wish.day)
        await call.message.edit_text(f'{choose_day}{day_schedule(data["suggested_schedule"], days[current_day_index])}', reply_markup=kb.days)
        return
    lesson_name = translate[call.data]
    count = check_lesson_count(data["suggested_schedule"], lesson_name)
    if count < count_of_lessons[lesson_name]:
        await state.update_data(lesson = lesson_name)
        await call.message.edit_text(choose_time, reply_markup=kb.time)
        await state.set_state(Student_Wish.time)
        return
    elif count >= count_of_lessons[lesson_name]:
        await call.message.answer(limit_lessons)
        return
    
@student_router.callback_query(RoleFilter('student'), Student_Wish.time)
async def wish_student_step_third(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data == 'back':
            await state.set_state(Student_Wish.lesson)
            await call.message.edit_text(f'{choose_lesson}\n{day_schedule(data["suggested_schedule"], days[0])}', reply_markup=kb.lessons)
            return
    check_time= check_time_for_lesson(data["suggested_schedule"], data['lesson'], call.data, data['day'])
    if check_time[0] == True:
        await state.update_data(time = call.data)
        data = await state.get_data()
        if lesson_count(data["suggested_schedule"]) == 50:
            await state.clear()
            send = await send_schedule_for_review(call.from_user.id, data["suggested_schedule"])
            if send:
                await call.message.edit_text(schedule_send_for_review, reply_markup=kb.student)
                return
            elif not send:
                await call.message.edit_text("Вы уже отправили расписание.", reply_markup=kb.student)
                return
        else:
            await state.set_state(Student_Wish.day)
            await state.update_data(current_day_index=0)
            await add_lesson(data['day'], data['time'], data['lesson'])
            text = f'''
{all_lessons[0]}: {check_lesson_count(data["suggested_schedule"], all_lessons[0])} (Минимум - 1)
{all_lessons[1]}: {check_lesson_count(data["suggested_schedule"], all_lessons[1])//4} (Минимум - 4)
{all_lessons[2]}: {check_lesson_count(data["suggested_schedule"], all_lessons[2])//4} (Минимум - 4)
{all_lessons[3]}: {check_lesson_count(data["suggested_schedule"], all_lessons[3])//4} (Минимум - 4)
{all_lessons[4]}: {check_lesson_count(data["suggested_schedule"], all_lessons[4])//6} (Минимум - 1)
'''
            await call.message.edit_text(f'Отлично, но еще не все!\n{text}\n{day_schedule(data["suggested_schedule"], days[0])}', reply_markup=kb.days)
    else:
        await call.message.answer(f'''{check_time[1]}
{choose_day}''')
        return
