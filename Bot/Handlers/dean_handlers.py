from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from Bot.FSM.dean_states import Dean

import Bot.Keyboards.dean_keyboard as kb
from Bot.Utils.constants import days
from Bot.Filters.role_filters import RoleFilter
from Bot.services import view_suggested_schedules, approve_schedule, get_all_suggested_schedules_indexes_list, rejection_schedule
dean_router = Router()

@dean_router.callback_query(RoleFilter('dean'), F.data == 'check_suggested')
async def check_suggested_schedule(call: CallbackQuery, state: FSMContext):
    list_of_ids = await get_all_suggested_schedules_indexes_list()
    if len(list_of_ids) > 0:
        await state.set_state(Dean.check_suggested)
        await state.update_data(check_suggested_day = 0)
        await state.update_data(current_week = 0)
        data = await state.get_data()
        current_week_index = data.get('current_week', 0)
        current_week_in_table = data.get('current_week_in_table', list_of_ids[current_week_index])
        current_week_schedule = await view_suggested_schedules(current_week_in_table)
        await call.message.edit_text(f'Вот вариант:\n{current_week_schedule[data["check_suggested_day"]]}', reply_markup=kb.suggest_menu)
        return
    elif len(list_of_ids) < 1:
        await state.set_state(Dean.dean_main)
        await call.message.edit_text("В данный момент нет расписаний на рассмотрение.", reply_markup=kb.back_menu)

async def day_selection(call: CallbackQuery, state: FSMContext, day_index, schedule_week):
    await state.set_state(Dean.check_suggested)
    await state.update_data(check_suggested_day=day_index)
    await call.message.edit_text(f'Предложенный вариант расписания:\n{schedule_week[day_index]}', reply_markup=kb.suggest_menu)

async def week_selection(call: CallbackQuery, state: FSMContext, week_index, current_week_in_table):
    await state.set_state(Dean.check_suggested)
    await state.update_data(current_week = week_index)
    await state.update_data(current_week_in_table = current_week_in_table)
    await state.update_data(check_suggested_day = 0)
    data = await state.get_data()
    current_week_schedule = await view_suggested_schedules(current_week_in_table)
    await call.message.edit_text(f'Предложенный вариант расписания:\n{current_week_schedule[data['check_suggested_day']]}', reply_markup=kb.suggest_menu)

@dean_router.callback_query(RoleFilter('dean'), Dean.check_suggested)
async def suggested_menu(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_day_index = data.get('check_suggested_day', 0)
    await state.set_state(Dean.check_suggested)

    list_of_ids = await get_all_suggested_schedules_indexes_list()
    current_week_index = data.get('current_week', 0)
    current_week_in_table_index = data.get('current_week_in_table', list_of_ids[current_week_index])
    current_week_schedule = await view_suggested_schedules(current_week_in_table_index)
    if call.data == 'last':
        if current_week_index > 0:
            await week_selection(call, state, current_week_index - 1, list_of_ids[current_week_index-1])
    elif call.data == 'next':
        if current_week_index < len(list_of_ids) - 1:   
            await week_selection(call, state, current_week_index + 1, list_of_ids[current_week_index+1])
    elif call.data == 'approve':
        approved_schedule = await approve_schedule(current_week_index)
        if approved_schedule:
            await state.clear()
            await call.message.edit_text('Расписание утверждено.', reply_markup=kb.dean_menu)
        else:
            await call.message.edit_text('Расписание утверждено по неизвестной причине.', reply_markup=kb.dean_menu)
    elif call.data == 'rejection':
        rejectioned_schedule = await rejection_schedule(current_week_index)
        if rejectioned_schedule:
            await state.clear()
            await call.message.edit_text('Отказано', reply_markup=kb.dean_menu)
        else:
            await call.message.edit_text('Не отказано по неизвестной причине', reply_markup=kb.dean_menu)
    elif call.data == 'right':
        if current_day_index < len(days) - 1:
            await day_selection(call, state, current_day_index + 1, current_week_schedule)
            return
    elif call.data == 'left':
        if current_day_index > 0:
            await day_selection(call, state, current_day_index - 1, current_week_schedule)
            return
    elif call.data == 'full_week':
        result = ''
        for i in range(0,5):
            result += current_week_schedule[i] + '\n'
        await call.message.edit_text(result, reply_markup=kb.suggest_menu)
    elif call.data == 'back':
        await state.clear()
        await call.message.edit_text('Добрый день!', reply_markup=kb.dean_menu)
        return

@dean_router.callback_query(RoleFilter('dean'), F.data == 'back' and Dean.dean_main)
async def return_in_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text('Добрый день!', reply_markup=kb.dean_menu)