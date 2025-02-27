from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.postgres.models.base import Base


class TaskInfoDB(Base):
    __tablename__ = "tasks_info"

    id = Column(Integer, primary_key=True, index=True)
    task_id: Mapped[str] = mapped_column(String(25), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    comments: Mapped[list["CommentDB"]] = relationship(
        "CommentDB",
        back_populates="task",
        cascade="all, delete-orphan"
    )


class CommentDB(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String(), nullable=True)

    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tasks_info.id", ondelete="CASCADE"),
        nullable=False
    )

    task: Mapped["TaskInfoDB"] = relationship(
        "TaskInfoDB",
        back_populates="comments"
    )
