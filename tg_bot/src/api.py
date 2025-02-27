import logging

import aiohttp

from src.config import config


async def register_user(user_data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{config.backend_url}/api/accounts/register/",
                json=user_data
        ) as response:
            return response.status


async def auth_user(user_data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{config.backend_url}/api/accounts/token/",
                json=user_data
        ) as response:
            results = await response.json()
            token = results.get("access")

    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers


async def get_categories(user_data: dict):
    headers = await auth_user(user_data)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.backend_url}/api/categories/",
                headers=headers
        ) as response:
            logging.info(f"INFO: {response.status}")
            logging.info(f"INFO: {await response.json()}")
            if response.status == 200:
                return await response.json()
            return []


async def create_categories(user_data: dict, name_category: str):
    headers = await auth_user(user_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{config.backend_url}/api/categories/",
                headers=headers,
                json={"name": name_category}
        ) as response:
            logging.info(f"INFO: {response.status}")
            # logging.info(f"INFO: {await response.json()}")
            if response.status == 201:
                return await response.json()


async def create_tasks(user_data: dict, task_data: dict):
    headers = await auth_user(user_data)
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{config.backend_url}/api/tasks/",
                headers=headers,
                json=task_data
        ) as response:
            logging.info(f"INFO: {response.status}")
            logging.info(f"INFO: {await response.json()}")
            if response.status == 201:
                return await response.json()
            return []


async def get_user_tasks(user_data: dict):
    headers = await auth_user(user_data)
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.backend_url}/api/tasks/",
                headers=headers,
        ) as response:
            logging.info(f"INFO: {response.status}")
            logging.info(f"INFO: {await response.json()}")
            if response.status == 200:
                return await response.json()
            return []


async def get_user_task_by_id(user_data: dict, task_id: str):
    headers = await auth_user(user_data)
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.backend_url}/api/tasks/{task_id}",
                headers=headers,
        ) as response:
            logging.info(f"INFO: {response.status}")
            logging.info(f"INFO: {await response.json()}")
            if response.status == 200:
                return await response.json()
            return []


async def edit_task_by_id(user_data: dict, task_id: str, task_data: dict):
    headers = await auth_user(user_data)
    async with aiohttp.ClientSession() as session:
        async with session.patch(
                f"{config.backend_url}/api/tasks/{task_id}/",
                headers=headers,
                json=task_data
        ) as response:
            logging.info(f"INFO: {response.status}")
            logging.info(f"INFO: {await response.json()}")
            if response.status == 200:
                return await response.json()


async def delete_user_task(user_data: dict, task_id: str):
    headers = await auth_user(user_data)
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                f"{config.backend_url}/api/tasks/{task_id}/",
                headers=headers,
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 204:
                return


async def create_comment_to_task(user_data: dict, comments_data: dict):
    headers = await auth_user(user_data)

    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{config.microservice_url}/comments",
                json=comments_data,
                headers=headers
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 201:
                return await response.json()


async def show_all_comments_to_task_by_id(task_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.microservice_url}/comments/{task_id}",
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 200:
                return await response.json()


async def delete_message_by_id(message_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                f"{config.microservice_url}/comments/{message_id}",
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 204:
                return await response.json()


async def edit_message_by_id(message_id: int, comment: str):
    async with aiohttp.ClientSession() as session:
        async with session.patch(
                f"{config.microservice_url}/comments/{message_id}",
                json={"new_comment": comment}
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 202:
                return await response.json()


async def show_user_categories(user_data: dict):
    headers = await auth_user(user_data)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.backend_url}/api/categories/",
                headers=headers
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 200:
                return await response.json()


async def show_detail_user_category(user_data: dict, category_id: str):
    headers = await auth_user(user_data)

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{config.backend_url}/api/categories/{category_id}",
                headers=headers
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 200:
                return await response.json()


async def edit_category_(user_data: dict, category_id: str, name_category: str):
    headers = await auth_user(user_data)

    async with aiohttp.ClientSession() as session:
        async with session.patch(
                f"{config.backend_url}/api/categories/{category_id}/",
                headers=headers,
                json={"name": name_category}
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 200:
                return await response.json()


async def delete_user_category(user_data: dict, category_id: str):
    headers = await auth_user(user_data)

    async with aiohttp.ClientSession() as session:
        async with session.delete(
                f"{config.backend_url}/api/categories/{category_id}/",
                headers=headers
        ) as response:
            logging.info(f"INFO: {response.status}")
            if response.status == 204:
                return
