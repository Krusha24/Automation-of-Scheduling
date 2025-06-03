from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from Bot.services import get_role
from DataBase.models.users import RoleEnum

class RoleFilter(BaseFilter):
    def __init__(self, role: str):
        self.role = RoleEnum(role)

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        user = await get_role(event.from_user.id)
        return user and user.role == self.role