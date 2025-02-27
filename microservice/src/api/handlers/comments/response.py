from pydantic import BaseModel


class CommentCreateOut(BaseModel):
    comment_id: int


class CommentsToTask(BaseModel):
    id: int
    content: str
    task_id: int
