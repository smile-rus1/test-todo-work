from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from keyboards import main_keyboard, create_task_inline_keyboard, inline_keyboard_to_task, inline_keyboard_to_message, \
    inline_keyboard_user_categories
from api import register_user, get_categories, create_categories, create_tasks, get_user_tasks, get_user_task_by_id, \
    delete_user_task, create_comment_to_task, show_all_comments_to_task_by_id, delete_message_by_id, edit_message_by_id, \
    edit_task_by_id, show_user_categories, show_detail_user_category, delete_user_category, edit_category_
from states import AddTaskSG, AddCommentsToTask, EditMessage, EditTask, EditCategory

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    data_user = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
        "first_name": message.from_user.first_name or None,
        "last_name": message.from_user.last_name or None,
        "telegram_id": message.from_user.id
    }

    if await register_user(data_user) == 200:
        await message.answer("👋 Привет! Вы еще не зарегистрированы.\nДавайте исправим это... ⏳")

        await message.answer(
            "✅ Регистрация успешна!\nТеперь вы можете работать с задачами.",
            reply_markup=main_keyboard
        )
        return
    await message.answer(
        f"👋 С возвращением, {message.from_user.first_name}!\nВыберите действие из меню ниже:",
        reply_markup=main_keyboard
    )


@router.message(Command("add_task"))
@router.message(lambda message: message.text == "➕ Добавить задачу")
async def add_task_start(message: types.Message, state: FSMContext):
    await message.answer("Введите название задачи:")
    await state.set_state(AddTaskSG.title)


@router.message(AddTaskSG.title)
async def add_task_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Теперь введите описание задачи:")
    await state.set_state(AddTaskSG.description)


@router.message(AddTaskSG.description)
async def add_task_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

    categories = await get_categories(
        {
            "username": message.from_user.username,
            "password": f"{message.from_user.username}{message.from_user.id}",
        }
    )

    buttons = [KeyboardButton(text=cat["name"]) for cat in categories]
    buttons.append(KeyboardButton(text="➕ Создать новую категорию"))

    keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await message.answer("Выберите категорию или создайте новую:", reply_markup=keyboard)
    await state.set_state(AddTaskSG.categories)


@router.message(AddTaskSG.categories)
async def add_task_category(message: types.Message, state: FSMContext):
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }
    categories = await get_categories(user_data)
    category_names = [cat["name"] for cat in categories]

    if message.text == "➕ Создать новую категорию":
        await message.answer("Введите название новой категории:")
        await state.set_state(AddTaskSG.new_category)
        return

    if message.text not in category_names:
        await message.answer("❌ Такой категории нет. Выберите из списка или создайте новую.")
        return

    category_id = next(cat["id"] for cat in categories if cat["name"] == message.text)

    await finish_task_creation(message, state, category_id)


@router.message(AddTaskSG.new_category)
async def create_new_category(message: types.Message, state: FSMContext):
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }

    category = await create_categories(user_data, message.text)

    if isinstance(category, dict) and "id" in category:
        category_id = category["id"]
    else:
        await message.answer("❌ Ошибка при создании категории. Попробуйте ещё раз.")
        return

    await message.answer(f"✅ Категория '{message.text}' создана и выбрана!")

    await finish_task_creation(message, state, category_id)


async def finish_task_creation(message: types.Message, state: FSMContext, category_id: str):
    task_data = await state.get_data()
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }

    task_data_save = {
        "title": task_data["title"],
        "description": task_data["description"],
        "category_ids": [category_id],
    }
    result = await create_tasks(user_data, task_data_save)

    if result is None:
        await message.answer(
            "Не удалось создать задачу, попробуйте еще раз",
            reply_markup=main_keyboard
        )

    await message.answer(
        f"✅ Задача успешно добавлена!\n"
        f"Заголовок задачи: {result.get("title")}\n"
        f"Описание задачи: {result.get("description")}\n"
        f"Когда создана: {result.get("created_at")}",
        reply_markup=main_keyboard)
    await state.clear()


@router.message(Command("tasks"))
@router.message(lambda message: message.text == "📋 Мои задачи")
async def show_my_tasks(message: types.Message):
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }
    user_tasks = await get_user_tasks(user_data)
    if not user_tasks:
        await message.answer("📝 У вас пока нет задач. Добавьте первую задачу с помощью кнопки ➕ Добавить задачу.")
        return

    keyboard = create_task_inline_keyboard(user_tasks)

    await message.answer("🗂 Ваши задачи:", reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("task_"))
async def task_details(callback: types.CallbackQuery):
    user_data = {
        "username": callback.from_user.username,
        "password": f"{callback.from_user.username}{callback.from_user.id}",
    }
    task_id = callback.data.split("_")[1]
    task = await get_user_task_by_id(user_data, task_id)

    if not task:
        await callback.answer("❌ Задача не найдена!", show_alert=True)
        return

    text = (
        f"📌{task.get('title')}\n\n"
        f"📝 {task.get('description')}\n"
        f"Категории: {[category.get('name') for category in task.get('categories')][0]}\n"
        f"📅 Дата создания: {task.get('created_at')[:10]}\n"
    )

    keyboard = inline_keyboard_to_task(task.get("id"))

    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_task(callback: types.CallbackQuery):
    user_data = {
        "username": callback.from_user.username,
        "password": f"{callback.from_user.username}{callback.from_user.id}",
    }
    task_id = callback.data.split("_")[1]
    await delete_user_task(user_data, task_id)
    await callback.message.delete()

    user_tasks = await get_user_tasks(user_data)
    keyboard = create_task_inline_keyboard(user_tasks)

    await callback.message.answer(
        f"Задача была удалена\n"
        f"Оставшиеся задачи:\n",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("comment_"))
async def add_to_task_comment(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("Введите комментарий")

    task_id = callback.data.split("_")[1]

    await state.update_data(task_id=task_id)
    await state.set_state(AddCommentsToTask.content)


@router.message(AddCommentsToTask.content)
async def comment_to_task(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)

    data = await state.get_data()
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }
    comment_data = {
        "task_id": data.get("task_id"),
        "content": data.get("content")
    }
    comment_id = await create_comment_to_task(user_data, comment_data)
    if comment_id is None:
        await message.answer(
            f"❌ Комментарий не был добавлен! Попробуйте еще раз\n",
            reply_markup=main_keyboard)
        await state.clear()
        return

    await message.answer(
        f"✅ Комментарий был добавлен!\n",
        reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("show-comment_"))
async def show_all_comments_to_task(callback: types.CallbackQuery):
    await callback.message.delete()

    task_id = callback.data.split("_")[1]
    comments = await show_all_comments_to_task_by_id(task_id)
    if not comments:
        await callback.message.answer(
            "Комментариев еще нет!",
            reply_markup=main_keyboard
        )
        return

    keyboard = inline_keyboard_to_message(comments)

    await callback.message.answer(
        "Комментарии:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("message_"))
async def show_detail_message(callback: types.CallbackQuery):
    message_id = callback.data.split("_")[1]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit-message_{message_id}")],
            [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete-message_{message_id}")],
        ]
    )

    await callback.message.answer(
        text="Что вы хотите сделать:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("delete-message_"))
async def delete_message(callback: types.CallbackQuery):
    message_id = callback.data.split("_")[1]
    await delete_message_by_id(int(message_id))

    await callback.message.answer(
        text="Сообщение к задаче было удалено",
        reply_markup=main_keyboard
    )


@router.callback_query(lambda c: c.data.startswith("edit-message_"))
async def edit_message(callback: types.CallbackQuery, state: FSMContext):
    message_id = callback.data.split("_")[1]
    await state.update_data(message_id=message_id)
    await callback.message.delete()
    await callback.message.answer("Введите новый комментарий")
    await state.set_state(EditMessage.new_message)


@router.message(EditMessage.new_message)
async def edit_comment_to_task(message: types.Message, state: FSMContext):
    await state.update_data(new_message=message.text)
    data = await state.get_data()

    new_message = await edit_message_by_id(
        message_id=int(data.get("message_id")),
        comment=data.get("new_message")
    )
    if new_message is None:
        await message.answer(
            text=f"Не удалось обновить сообщение, попробуйте еще раз!",
            reply_markup=main_keyboard
        )
        await state.clear()
        return

    await message.answer(
        text=f"Сообщение изменено на:"
             f"{new_message}",
        reply_markup=main_keyboard
    )
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("edit-task_"))
async def edit_task(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название задачи или пропустите:")
    task_id = callback.data.split("_")[1]

    await state.update_data(task_id=task_id)
    await state.set_state(EditTask.title)


@router.message(EditTask.title)
async def add_task_new_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите новое описание задачи или пропустите:")
    await state.set_state(EditTask.description)


@router.message(EditTask.description)
async def add_task_new_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

    categories = await get_categories(
        {
            "username": message.from_user.username,
            "password": f"{message.from_user.username}{message.from_user.id}",
        }
    )

    buttons = [KeyboardButton(text=cat["name"]) for cat in categories]

    keyboard = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await message.answer("Выберите категорию", reply_markup=keyboard)
    await state.set_state(EditTask.categories)


@router.message(EditTask.categories)
async def add_task_new_categories(message: types.Message, state: FSMContext):
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }

    categories = await get_categories(user_data)
    category_id = next(cat["id"] for cat in categories if cat["name"] == message.text)
    category_names = [cat["name"] for cat in categories]

    if message.text not in category_names:
        await message.answer("❌ Такой категории нет. Выберите из списка или создайте новую.")
        return

    await finish_edit_task(message, state, category_id)


async def finish_edit_task(message: types.Message, state: FSMContext, category_id: str):
    task_data = await state.get_data()
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }

    task_data_save = {
        "title": task_data["title"],
        "description": task_data["description"],
        "category_ids": [category_id],
    }
    result = await edit_task_by_id(user_data, task_data.get("task_id"), task_data_save)

    if result is None:
        await message.answer(
            "Не удалось обновить задачу, попробуйте еще раз",
            reply_markup=main_keyboard
        )

    await message.answer(
        f"✅ Задача успешно обновлена!\n"
        f"Заголовок задачи: {result.get("title")}\n"
        f"Описание задачи: {result.get("description")}\n"
        f"Когда создана: {result.get("created_at")}",
        reply_markup=main_keyboard)
    await state.clear()


@router.message(Command("show_categories"))
@router.message(lambda message: message.text == "📝 Мои категории")
async def show_my_categories(message: types.Message):
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }
    categories = await show_user_categories(user_data)

    if categories is None:
        await message.answer(
            "У вас пока что нет категорий!",
            reply_markup=main_keyboard
        )
        return

    keyboard = inline_keyboard_user_categories(categories)

    await message.answer(
        "Ваши категории",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("category_"))
async def show_details_category(callback: types.CallbackQuery):
    await callback.message.delete()
    category_id = callback.data.split("_")[1]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit-category_{category_id}")],
            [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete-category_{category_id}")],
        ]
    )

    await callback.message.answer(
        text="Что вы хотите сделать:",
        reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith("edit-category"))
async def edit_category(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split("_")[1]
    await state.update_data(category_id=category_id)
    await callback.message.delete()
    await callback.message.answer("Введите новое название категории")
    await state.set_state(EditCategory.name)


@router.message(EditCategory.name)
async def edit_user_category(message: types.Message, state: FSMContext):
    user_data = {
        "username": message.from_user.username,
        "password": f"{message.from_user.username}{message.from_user.id}",
    }

    await state.update_data(name=message.text)
    data = await state.get_data()

    new_category = await edit_category_(user_data, data.get("category_id"), data.get("name"))
    if new_category is None:
        await message.answer(
            "Не удалось обновить категорию, попробуйте еще раз",
            reply_markup=main_keyboard
        )

    await message.answer(
        f"✅ Категория успешно обновлена!\n"
        f"Новый заголовок: {new_category.get("name")}",
        reply_markup=main_keyboard)
    await state.clear()


@router.callback_query(lambda c: c.data.startswith("delete-category"))
async def delete_category(callback: types.CallbackQuery):
    await callback.message.delete()
    user_data = {
        "username": callback.from_user.username,
        "password": f"{callback.from_user.username}{callback.from_user.id}",
    }
    category_id = callback.data.split("_")[1]

    await delete_user_category(user_data, category_id)

    await callback.message.answer(
        text="Категория была удалена",
        reply_markup=main_keyboard
    )

