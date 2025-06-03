from DataBase.base import async_session
from DataBase.models.users import User
from DataBase.models.suggested_schedule import Suggested_Schedule
from sqlalchemy import select

from Bot.Utils.schedule_utils import day_schedule
from Bot.Utils.constants import days

async def set_user(tg_id_user, role_user):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id_user)) 
        if user:
            user.role = role_user  # обновляем роль
            print('Роль обновлена')
        elif not user:
            session.add(User(tg_id = tg_id_user, role = role_user))
            await session.commit()
            print('Данные внесены')
            return True

async def get_role(tg_id_user):
    async with async_session() as session:
        result = await session.scalars(select(User).where(User.tg_id == tg_id_user))
        user = result.one_or_none()
        return user
    
async def send_schedule_for_review(tg_id_user, schedule):
    role = (await get_role(tg_id_user)).role
    print('Вносит данные')
    try:
        async with async_session() as session:
            user = await session.scalar(select(Suggested_Schedule).where(Suggested_Schedule.tg_id == tg_id_user))
            if user:
                text = 'Вы уже отправили расписание на рассмотрение'
                return False, text
            elif not user:
                monday = day_schedule(schedule, days[0])
                print(monday)
                tuesday = day_schedule(schedule, days[1])
                wednesday = day_schedule(schedule, days[2])
                thursday = day_schedule(schedule, days[3])
                friday = day_schedule(schedule, days[4])
                session.add(Suggested_Schedule(tg_id = tg_id_user, role = str(role),
                                            monday = monday, tuesday = tuesday,
                                            wednesday = wednesday, thursday = thursday,
                                            friday = friday))
                await session.commit()
                return True
    except Exception as e:
        print(f"Ошибка при сохранении расписания: {e}")
        return False