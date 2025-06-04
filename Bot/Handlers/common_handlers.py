from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from Bot.services import set_user

import Bot.Keyboards.common_keyboard as kb_common
import Bot.Keyboards.student_keyboard as kb_student
import Bot.Keyboards.teacher_keyboard as kb_teacher
import Bot.Keyboards.dean_keyboard as kb_dean

common_router = Router()
list_of_users = []

@common_router.message(CommandStart())
async def get_id(message: Message):
    list_of_users.append(str(message.from_user.id))
    await message.answer('Добро пожаловать в бота для составления расписания. Выберите вашу роль:', reply_markup=kb_common.main)

@common_router.callback_query(F.data.startswith('role_'))
async def set_user_role(callback: CallbackQuery, state: FSMContext):
    role = callback.data.replace("role_", "")
    await set_user(callback.from_user.id, role)
    await state.clear()
    if role == 'student':
        keyboard = kb_student.student
    elif role == 'teacher':
        pass
    elif role == 'dean':
        keyboard = kb_dean.dean_menu
    await callback.message.answer(f"Ваша роль — {role.capitalize()} успешно выбрана!", reply_markup=keyboard)

