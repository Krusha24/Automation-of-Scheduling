from aiogram.fsm.state import StatesGroup, State
class Student_Wish(StatesGroup):
    day = State()
    current_day_index = State()
    lesson = State()
    time = State()
    suggested_schedule = State()