import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

__all__ = ('Base', 'WriteOff',)


class Base(DeclarativeBase):
    pass


class WriteOff(Base):
    __tablename__ = 'write_offs'

    unit_id: Mapped[int] = mapped_column(primary_key=True)
    ingredient_name: Mapped[str] = mapped_column(primary_key=True)
    to_be_written_off_at: Mapped[datetime.datetime] = mapped_column(nullable=False)

    def __str__(self):
        return f'<Write-off: unit {self.unit_id}, ingredient {self.ingredient_name}>'
