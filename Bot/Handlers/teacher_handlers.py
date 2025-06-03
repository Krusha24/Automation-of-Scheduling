from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import Bot.Keyboards.teacher_keyboard as kb
from Bot.Utils.constants import schedule, times, count_of_lessons, all_lessons, translate, days
from Bot.Utils.validators import check_time_for_lesson
from Bot.Utils.schedule_utils import add_lesson, check_lesson_count, lesson_count, day_schedule

teacher_router = Router()