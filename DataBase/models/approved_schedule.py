from sqlalchemy.orm import Mapped, mapped_column

from DataBase.base import Base

class Approved_Schedule(Base):
    __tablename__ = 'Approved_Schedule'

    id: Mapped[int] = mapped_column(primary_key=True)
    monday: Mapped[str] = mapped_column()
    tuesday: Mapped[str] = mapped_column()
    wednesday: Mapped[str] = mapped_column()
    thursday: Mapped[str] = mapped_column()
    friday: Mapped[str] = mapped_column()