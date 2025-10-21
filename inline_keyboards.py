from aiogram.utils.keyboard import InlineKeyboardBuilder
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