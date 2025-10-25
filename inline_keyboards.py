from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
db = Database()

def get_categories_keyboard():
    categories = db.get_categories()
    print(categories)

    if categories:
        builder = InlineKeyboardBuilder()
        for category in categories:
            builder.button(
                text=category[1],
                callback_data=f"category_{category[0]}"
            )
        builder.adjust(3)  # Har bir qatorda 2 ta tugma
        return builder.as_markup()
    
def get_products_keyboard(category_id):
    products = db.get_products_by_category(category_id)
    # print(products)

    if products:
        builder = InlineKeyboardBuilder()
        for product in products:
            builder.button(
                text=product[2],
                callback_data=f"product_{product[0]}"
            )
        builder.adjust(2)  # Har bir qatorda 2 ta tugma
        return builder.as_markup()
    
def build_qty_keyboard(pid: int, q: int):
    builder = InlineKeyboardBuilder()
    builder.row(
            InlineKeyboardButton(text="➖", callback_data=f"qty_dec_{pid}_{q}"),
            InlineKeyboardButton(text="➕", callback_data=f"qty_inc_{pid}_{q}\n")
    )
    builder.add(InlineKeyboardButton(text="Buyurtma berish", callback_data=f"order_{pid}_{q}"))
    return builder.as_markup()


def add_to_cart_btn(product_id):
    add_to_cart = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='-', callback_data=f"minus_{product_id}"),
                InlineKeyboardButton(text='1', callback_data=f"count_{product_id}"),
                InlineKeyboardButton(text='+', callback_data=f"plus_{product_id}"),
            ],
            [
                InlineKeyboardButton(text="Savatchaga qo'shish", callback_data=f"add_to_cart_{product_id}"),
            ]
        ]
    )
    return add_to_cart