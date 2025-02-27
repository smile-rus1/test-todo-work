from aiogram.fsm.state import State, StatesGroup


class CreateCategorySG(StatesGroup):
    name = State()


class AddTaskSG(StatesGroup):
    title = State()
    description = State()
    categories = State()
    new_category = State()


class AddCommentsToTask(StatesGroup):
    task_id = State()
    content = State()


class EditMessage(StatesGroup):
    new_message = State()


class EditTask(StatesGroup):
    title = State()
    description = State()
    categories = State()


class EditCategory(StatesGroup):
    name = State()
