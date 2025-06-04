from DataBase.base import async_session
from DataBase.models.users import User
from DataBase.models.suggested_schedule import Suggested_Schedule
from DataBase.models.approved_schedule import Approved_Schedule
from sqlalchemy import select

from Bot.Utils.schedule_utils import day_schedule
from Bot.Utils.constants import days

async def set_user(tg_id_user, role_user):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id_user)) 
        if user:
            user.role = role_user  # обновляем роль
        elif not user:
            session.add(User(tg_id = tg_id_user, role = role_user))
            await session.commit()
            return True

async def get_role(tg_id_user):
    async with async_session() as session:
        result = await session.scalars(select(User).where(User.tg_id == tg_id_user))
        user = result.one_or_none()
        return user
    
async def send_schedule_for_review(tg_id_user, schedule):
    role = (await get_role(tg_id_user)).role
    try:
        async with async_session() as session:
            user = await session.scalar(select(Suggested_Schedule).where(Suggested_Schedule.tg_id == tg_id_user))
            if user:
                return False
            elif not user:
                monday = day_schedule(schedule, days[0])
                print(monday)
                tuesday = day_schedule(schedule, days[1])
                wednesday = day_schedule(schedule, days[2])
                thursday = day_schedule(schedule, days[3])
                friday = day_schedule(schedule, days[4])
                session.add(Suggested_Schedule(tg_id = tg_id_user, role = role.value,
                                            monday = monday, tuesday = tuesday,
                                            wednesday = wednesday, thursday = thursday,
                                            friday = friday))
                await session.commit()
                return True
    except Exception as e:
        print(f"Ошибка при сохранении расписания: {e}")
        return False

async def view_suggested_schedules(index): # Функция чтобы получить предложенное расписание на неделю по индексу в таблице
    try:
        async with async_session() as session:
            table = await session.scalar(select(Suggested_Schedule).where(Suggested_Schedule.id == index))
            monday = table.monday
            tuesday = table.tuesday
            wednesday = table.wednesday
            thursday = table.thursday
            friday = table.friday
            result = [monday, tuesday, wednesday, thursday, friday]
            return result

    except Exception as e:
        print(f"Ошибка при выводе: {e}")
        return False
    
async def get_all_suggested_schedules_indexes_list(): # Функция получения списка айдишников предложенных расписаний
    async with async_session() as session:
        result = await session.execute(
            select(Suggested_Schedule.id).order_by(Suggested_Schedule.id)
        )
        ids = result.scalars().all()
        return ids

async def approve_schedule(index): # Утверждение расписания
    try:
        async with async_session() as session:
            results = await session.execute(select(Suggested_Schedule).order_by(Suggested_Schedule.id))
            rows = results.scalars().all()
            if index >= len(rows):
                return False
            suggested_schedule = rows[index]
            approved_schedule = await session.scalar(select(Approved_Schedule).where(Approved_Schedule.id == 1))
            if approved_schedule:
                approved_schedule.monday = suggested_schedule.monday
                approved_schedule.tuesday = suggested_schedule.tuesday
                approved_schedule.wednesday = suggested_schedule.wednesday
                approved_schedule.thursday = suggested_schedule.thursday
                approved_schedule.friday = suggested_schedule.friday
            else:
                approved_schedule = Approved_Schedule(
                id=1,  # Явно указать id, если он нужен
                    monday=suggested_schedule.monday,
                    tuesday=suggested_schedule.tuesday,
                    wednesday=suggested_schedule.wednesday,
                    thursday=suggested_schedule.thursday,
                    friday=suggested_schedule.friday
                )
                session.add(approved_schedule)
            await session.delete(suggested_schedule)
            await session.commit()
            return True
    except Exception as e:
        print(f"ERROR KEY: {e}")
        return False

async def rejection_schedule(index): #Отказ в предложенном расписании и удалении его из таблицы
    try:
        async with async_session() as session:
            results = await session.execute(select(Suggested_Schedule).order_by(Suggested_Schedule.id))
            rows = results.scalars().all()
            if index >= len(rows):
                return False
            suggested_schedule = rows[index]
            await session.delete(suggested_schedule)
            await session.commit()
            return True
    
    except Exception as e:
        print(f"ERROR KEY: {e}")
        return False