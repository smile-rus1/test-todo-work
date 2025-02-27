import logging

from sqlalchemy import insert, update, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from src.infrastructure.postgres.models.models import CommentDB, TaskInfoDB
from src.infrastructure.postgres.repo.base_repo import SQLAlchemyRepo


class CommentsRepo(SQLAlchemyRepo):
    async def create_comments(self, comments_data: dict) -> int:
        task_info_id = (
            await self._session.execute(
                select(TaskInfoDB.id).where(TaskInfoDB.task_id == comments_data.get("task_id"))
            )
        ).scalar_one_or_none()

        if task_info_id is None:
            sql_insert_task_info = insert(TaskInfoDB).values(
                task_id=comments_data.get("task_id"),
                title=comments_data.get("title")
            ).returning(TaskInfoDB.id)
            try:
                task_info_id = (await self._session.execute(sql_insert_task_info)).scalar_one()

            except IntegrityError:
                logging.error(f"Error in create comments with data={comments_data}")
                await self._session.rollback()
                raise

        sql = insert(CommentDB).values(
            content=comments_data.get("content"),
            task_id=task_info_id
        ).returning(CommentDB.id)

        try:
            result = (await self._session.execute(sql)).scalar()
            await self._session.commit()
            return result

        except IntegrityError:
            logging.error(f"Error in create comments with data={comments_data}")
            await self._session.rollback()
            raise

    async def get_all_comments_to_task(self, task_id: str):
        sql = (
            select(CommentDB)
            .join(TaskInfoDB, TaskInfoDB.id == CommentDB.task_id)
            .where(TaskInfoDB.task_id == task_id)
        )
        results = (await self._session.execute(sql)).scalars().all()
        comments = [{"id": c.id, "content": c.content, "task_id": c.task_id} for c in results]

        return comments

    async def update_comment(self, comment_id: int, comment_data: dict):
        sql = (
            update(CommentDB)
            .where(CommentDB.id == comment_id)
            .values(**comment_data)
            .execution_options(synchronize_session="fetch")
        ).returning(CommentDB.content)
        try:
            result = (await self._session.execute(sql)).scalar()
            await self._session.commit()

            return result

        except IntegrityError as e:
            logging.error(f"Error {e} in update comments with id={comment_id} and data={comment_data}")
            await self._session.rollback()
            raise

    async def delete_comment(self, comment_id: int):
        sql = delete(CommentDB).where(CommentDB.id == comment_id)

        try:
            await self._session.execute(sql)
            await self._session.commit()

        except IntegrityError as e:
            logging.error(f"Error {e} in delete comments with id={comment_id}")
            await self._session.rollback()
            raise
