from aiogram.filters.state import State, StatesGroup

class AddUserState(StatesGroup):
    phone_number = State()

class AddCategoryState(StatesGroup):
    category_name = State()

class AddProductState(StatesGroup):
    category_id = State()
    product_name = State()
    product_description = State()
    product_price = State()
    product_image = State()

class AddCartState(StatesGroup):
    category = State()
    product = State()
    add_to_cart = State()

class AdState(StatesGroup):
    image = State()
    text = State()

    