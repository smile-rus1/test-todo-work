from abc import ABC

import aiohttp

from src.dto.comments_dto import CreateCommentsDTO, UpdateCommentDTO, CommentsToTask
from src.infrastructure.postgres.repo.comments_repo import CommentsRepo
from src.infrastructure.redis_db.redis_repo import RedisRepo


class CommentsUseCase(ABC):
    def __init__(self, comments_repo: CommentsRepo, redis_repo: RedisRepo, backend_api_url: str):
        self._repo = comments_repo
        self._redis = redis_repo
        self._backend_api_url = backend_api_url
        self._headers = {
            "accept": "application/json",
            "Authorization": ""
        }


class CreateComments(CommentsUseCase):
    async def __call__(self, access: str, comments_data: CreateCommentsDTO) -> int:
        self._headers["Authorization"] = f"Bearer {access}"

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"{self._backend_api_url}/api/tasks/{comments_data.task_id}",
                    headers=self._headers
            ) as response:
                result = await response.json()
                comments_data.title = result.get("title")

        return await self._repo.create_comments(comments_data.__dict__)


class GetAllCommentsToTask(CommentsUseCase):
    async def __call__(self, task_id: str) -> list[CommentsToTask]:
        cached_data = await self._redis.get_by_key(task_id)
        if cached_data:
            return [CommentsToTask(**comment) for comment in cached_data]

        comments_data = await self._repo.get_all_comments_to_task(task_id)
        await self._redis.set_in_redis(task_id, comments_data)

        return [CommentsToTask(**comment) for comment in comments_data]


class UpdateComment(CommentsUseCase):
    async def __call__(self, comment_id: int, comment_data: UpdateCommentDTO) -> str:
        return await self._repo.update_comment(comment_id, comment_data.__dict__)


class DeleteComment(CommentsUseCase):
    async def __call__(self, comment_id: int):
        await self._repo.delete_comment(comment_id)


class CommentService:
    def __init__(self, comments_repo: CommentsRepo, redis_repo: RedisRepo, backend_api_url):
        self._repo = comments_repo
        self._redis = redis_repo
        self._backend_api_url = backend_api_url

    async def create_comments(self, access: str, comments_data: CreateCommentsDTO) -> int:
        return await CreateComments(self._repo, self._redis, self._backend_api_url)(access, comments_data)

    async def get_all_comments_to_task(self, task_id: str) -> list:
        return await GetAllCommentsToTask(self._repo, self._redis, self._backend_api_url)(task_id)

    async def update_comment(self, comment_id: int, comment_data: UpdateCommentDTO) -> str:
        return await UpdateComment(self._repo, self._redis, self._backend_api_url)(comment_id, comment_data)

    async def delete_comment(self, comment_id: int):
        await DeleteComment(self._repo, self._redis, self._backend_api_url)(comment_id)
