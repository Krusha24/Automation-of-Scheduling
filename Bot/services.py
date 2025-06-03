from DataBase.base import async_session
from DataBase.models.users import User
from sqlalchemy import select

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
        print("get_role():", user)  # <--- отладка
        return user