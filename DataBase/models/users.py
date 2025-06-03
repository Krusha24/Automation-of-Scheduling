from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger
from sqlalchemy import Enum
import enum
from DataBase.base import Base

class RoleEnum(enum.Enum):
    student = "student"
    teacher = "teacher"
    decan = "dean"

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)