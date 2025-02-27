from pydantic import BaseModel


class CommentCreateIn(BaseModel):
    task_id: str
    content: str | None = None
