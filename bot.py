from aiogram import Dispatcher, Bot, types, F
import asyncio
from aiogram.fsm.context import FSMContext
from states import AddUserState, AddCategoryState, AddProductState
from keyboards import phone_btn, admin_menu
from inline_keyboards import get_categories_keyboard
from database import Database


bot = Bot(token="8432374022:AAGGJ4wou8QzCycOXNYKJYb9kBeghk7arnE")
dp = Dispatcher()
db = Database()

ADMINS = [726130790, 231515355]

@dp.message(F.text=='/start')
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMINS:
        await message.answer("Assalamu alaykum Admin", reply_markup=admin_menu)
    else:
        user = db.get_user(user_id)
        if user:
            await message.answer("Assalamu alaykum bratiiim")
        else:
            await message.answer("Iltimos telefon raqamingizni ulashing", reply_markup=phone_btn)
            await state.set_state(AddUserState.phone_number)

@dp.message(AddUserState.phone_number)
async def add_user_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username
    db.add_user(user_id, username, phone_number)
    await message.answer("Ro'yxatdan o'tdingiz, rahmat!")
    await state.clear()

@dp.message(F.text=='Add category')
async def add_category_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer("Yangi Category nomini kitiring")
        await state.set_state(AddCategoryState.category_name)
    else:
        print("Qaysidir bot admin panelga kirib oldi")

@dp.message(AddCategoryState.category_name)
async def add_category_handler(message: types.Message, state: FSMContext):
    name = message.text
    db.add_category(name)
    await message.answer(f"Yangi {name} kategoriyasi qo'shildi")
    await state.clear()

@dp.message(F.text == 'Add product')
async def add_product_handler(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        categories = db.get_categories()
        if not categories:
            await message.answer("Iltimos avval kategoriya qo'shing")
            return
        keyboard = get_categories_keyboard()
        await message.answer("Iltimos kategoriyani tanlang", reply_markup=keyboard)
        await state.set_state(AddProductState.category_id)
    else:
        print("Qaysidir bot admin panelga kirib oldi")

@dp.callback_query(AddProductState.category_id)
async def category_chosen_handler(callback_query: types.CallbackQuery, state: FSMContext):
    category_id = int(callback_query.data.split("_")[1])
    await state.update_data(category_id=category_id)
    await callback_query.message.answer("Mahsulot nomini kiriting")
    await state.set_state(AddProductState.product_name)

@dp.message(AddProductState.product_name)
async def product_name_handler(message: types.Message, state: FSMContext):
    product_name = message.text
    await state.update_data(product_name=product_name)
    await message.answer("Mahsulot haqida to'liqroq ma'lumot bering")
    await state.set_state(AddProductState.product_description)

@dp.message(AddProductState.product_description)
async def product_description_handler(message: types.Message, state: FSMContext):
    product_description = message.text
    await state.update_data(product_description=product_description)
    await message.answer("Mahsulot narxini kiriting")
    await state.set_state(AddProductState.product_price)

@dp.message(AddProductState.product_price)
async def product_price_handler(message: types.Message, state: FSMContext):
    product_price = float(message.text)
    await state.update_data(product_price=product_price)
    await message.answer("Mahsulot rasmini yuboring")
    await state.set_state(AddProductState.product_image)

@dp.message(AddProductState.product_image, F.photo)
async def product_image_handler(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    image_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

    data = await state.get_data()
    category_id = data['category_id']
    product_name = data['product_name']
    product_description = data['product_description']
    product_price = data['product_price']

    db.add_product(category_id, product_name, product_description, product_price, image_url)
    await message.answer(f"{product_name} nomli mahsulot qo'shildi")
    await state.clear()




async def main():
    print("Bot ishlayapdi...")
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    db.create_tables()
    asyncio.run(main())