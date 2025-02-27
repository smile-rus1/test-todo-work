from dataclasses import dataclass

from src.dto.base_dto import BaseDTO


@dataclass
class CommentsDTO(BaseDTO):
    ...


@dataclass
class CreateCommentsDTO(CommentsDTO):
    task_id: str
    title: str = None
    content: str = None


@dataclass
class UpdateCommentDTO(CommentsDTO):
    content: str = None


@dataclass
class CommentsToTask(CommentsDTO):
    id: int
    content: str
    task_id: str
