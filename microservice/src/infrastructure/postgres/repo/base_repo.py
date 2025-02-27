from sqlalchemy.ext.asyncio import AsyncSession

from src.interfaces.repo import IRepo


class SQLAlchemyRepo(IRepo):
    def __init__(self, session: AsyncSession):
        self._session = session
