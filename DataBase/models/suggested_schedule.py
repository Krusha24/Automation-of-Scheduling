from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String

from DataBase.base import Base

class Suggested_Schedule(Base):
    __tablename__ = 'Suggested_Schedule'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, nullable=False)
    role: Mapped[str] = mapped_column()
    monday: Mapped[str] = mapped_column()
    tuesday: Mapped[str] = mapped_column()
    wednesday: Mapped[str] = mapped_column()
    thursday: Mapped[str] = mapped_column()
    friday: Mapped[str] = mapped_column()
    