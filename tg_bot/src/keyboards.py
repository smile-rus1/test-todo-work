from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Мои задачи")],
        [KeyboardButton(text="➕ Добавить задачу")],
        [KeyboardButton(text="📝 Мои категории")]
    ],
    resize_keyboard=True,
)


def create_task_inline_keyboard(tasks: list[dict]):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"📌 {task['title']}", callback_data=f"task_{task['id']}")]
            for task in tasks
        ]
    )
    return keyboard


def inline_keyboard_to_task(task_id: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit-task_{task_id}")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{task_id}")],
        [InlineKeyboardButton(text="💬 Добавить комментарий", callback_data=f"comment_{task_id}")],
        [InlineKeyboardButton(text="🔎 Посмотреть все комментарии к задаче", callback_data=f"show-comment_{task_id}")]
    ])

    return keyboard


def inline_keyboard_to_message(messages: list[dict]):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{message['content']}",
                    callback_data=f"message_{message['id']}")
            ]
            for message in messages
        ]
    )
    return keyboard


def inline_keyboard_user_categories(categories: list[dict]):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{category['name']}",
                    callback_data=f"category_{category['id']}")
            ]
            for category in categories
        ]
    )
    return keyboard
