from aiogram.fsm.state import StatesGroup, State
class Student_Wish(StatesGroup):
    day = State()
    monday = State()
    tuesday = State()
    wednesday = State()
    thursday = State()
    friday = State()
    lesson = State()
    time = State()