from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(60))
    inn: Mapped[int] = mapped_column(BigInteger)
    soft: Mapped[str] = mapped_column(String(60))
    soft_id: Mapped[int] = mapped_column()
    number: Mapped[str] = mapped_column(String(60))


class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    taskID: Mapped[str] = mapped_column(String(25))
    user = mapped_column(BigInteger)


class Rkeeper(Base):
    __tablename__ = "rkeeper"

    id: Mapped[int] = mapped_column(primary_key=True)
    codeRk = mapped_column(BigInteger)
    user: Mapped[BigInteger] = mapped_column(ForeignKey('users.tg_id'))



async def connect_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)