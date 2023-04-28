from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database():
    def __init__(self, engine: AsyncEngine, recreate_db: bool) -> None:
        self.__engine = engine
        self.__recreate_db = recreate_db
        self.Session: AsyncSession = sessionmaker(  # pylint: disable=invalid-name
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            bind=self.__engine,
            future=True,
            class_=AsyncSession)
        self.Base = declarative_base()  # pylint: disable=invalid-name

    async def __drop_database(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.drop_all)

    async def init_database(self):
        if self.__recreate_db:
            await self.__drop_database()
        async with self.__engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)
