from fastapi import APIRouter, status, Depends, Request, HTTPException, Body

from src.api.handlers.comments.requests import CommentCreateIn
from src.api.handlers.comments.response import CommentCreateOut, CommentsToTask
from src.api.providers.abstract.services import comments_service_provider
from src.dto.comments_dto import CreateCommentsDTO, UpdateCommentDTO
from src.services.comments.comments import CommentService


comments_router = APIRouter(prefix="/comments", tags=["Comments"])


@comments_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentCreateOut
)
async def create_comment(
        request: Request,
        comment_data: CommentCreateIn,
        comments_service: CommentService = Depends(comments_service_provider)
):
    dto = CreateCommentsDTO(
        task_id=comment_data.task_id,
        content=comment_data.content
    )
    access = request.cookies.get("access_token")

    if access is None:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing Authorization header"
            )

        access = auth_header.split("Bearer ")[1].strip()
    comment = await comments_service.create_comments(access, dto)

    return CommentCreateOut(comment_id=comment)


@comments_router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[CommentsToTask]
)
async def get_comments_to_task(
        task_id: str,
        comments_service: CommentService = Depends(comments_service_provider)
):
    comments = await comments_service.get_all_comments_to_task(task_id)

    return [CommentsToTask(**comment.__dict__) for comment in comments]


@comments_router.patch(
    "/{comment_id}",
    status_code=status.HTTP_202_ACCEPTED
)
async def update_comment(
        comment_id: int,
        new_comment: str | None = Body(None, embed=True),
        comments_service: CommentService = Depends(comments_service_provider)
):
    dto = UpdateCommentDTO(content=new_comment)
    updated_comment = await comments_service.update_comment(comment_id, dto)

    return updated_comment


@comments_router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
        comment_id: int,
        comments_service: CommentService = Depends(comments_service_provider)
):
    await comments_service.delete_comment(comment_id)
