from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Share Phone Number", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Add category'),
            KeyboardButton(text='Add product')
        ]
    ]
)