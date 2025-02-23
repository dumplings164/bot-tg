from app.database.db import async_session
from app.database.db import User, Rkeeper, Task
from sqlalchemy import select, delete


async def set_user(tg_id: int, name: str, inn: int, soft: str, soft_id: int, number: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, name=name, inn=inn, soft=soft, soft_id=soft_id, number=number))
            await session.commit()


async def check_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            return True


async def user(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user_info(tg_id: int):
    async with async_session() as session:
        return await session.scalars(select(User).where(User.tg_id == tg_id))


async def set_codeRk(tg_id: int, codeRk: int):
    async with async_session() as session:
        user = await session.scalar(select(Rkeeper).where(Rkeeper.user == tg_id, Rkeeper.codeRk == codeRk))
        
        if not user:
            session.add(Rkeeper(codeRk=codeRk, user=tg_id))
            await session.commit()
            return True


async def len_users(tg_id: int):
    async with async_session() as session:
        users = await session.scalars(select(Rkeeper).where(Rkeeper.user == tg_id))

        u = []
        for user in users:
            u.append(user.codeRk)
        return u


async def get_codeRk(tg_id: int):
    async with async_session() as session:
        return await session.scalars(select(Rkeeper).where(Rkeeper.user == tg_id))
        

async def set_task(tg_id: int, taskID: int):
    async with async_session() as session:
        user = await session.scalar(select(Task).where(Task.user == tg_id))
        
        if not user:
            session.add(Task(taskID=taskID, user=tg_id))
            await session.commit()
            return True
   

async def get_task(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(Task).where(Task.user == tg_id))
        
        
async def delet_task(tg_id: int, taskID: int):
    async with async_session() as session:
        await session.execute(delete(Task).where(Task.user == tg_id, Task.taskID == taskID))
        await session.commit()
        
        