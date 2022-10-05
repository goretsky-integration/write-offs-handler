import asyncio

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.engine import engine, Base


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    write_offs = relationship('WriteOff', back_populates='ingredient', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<{self.id=} {self.name=}>'

    __mapper_args__ = {"eager_defaults": True}


class WriteOff(Base):
    __tablename__ = 'write_offs'

    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, nullable=False)
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), nullable=False)
    to_be_write_off_at = Column(DateTime, nullable=False)
    written_off_at = Column(DateTime, nullable=True)

    ingredient = relationship('Ingredient', back_populates='write_offs')

    def __repr__(self):
        return f'<{self.id=} {self.ingredient_id=}>'


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(init_db())
