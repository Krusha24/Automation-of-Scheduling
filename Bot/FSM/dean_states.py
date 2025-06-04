from aiogram.fsm.state import StatesGroup, State
class Dean(StatesGroup):
    dean_main = State()
    check_suggested = State()
    check_suggested_day = State()
    current_week = State()
    current_week_in_table = State()
    check_suggested_index = State()