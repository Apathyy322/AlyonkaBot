import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from others.config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    var1 = InlineKeyboardButton(
        text="Ссылка на наш сайт💻",
        url=f"https://prom.ua/c3306069-poshlaya-alyonka.html"
    )
    var2 = InlineKeyboardButton(
        text="Помощь👋",
        callback_data='help'
    )
    var3 = InlineKeyboardButton(
        text='Часто Задаваемые Вопросы(FAQ)❓',
        callback_data='faq',
        url=f"https://prom.ua/opinions/list/3306069"
    )
    var4 = InlineKeyboardButton(
        text="Ваши данные🥷",
        callback_data='data'
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [var1],
        [var2],
        [var3, var4]
    ])
    await message.answer(
        """<b>Добрый день!</b> 
        \nВас приветствует техподдержка магазина <i>Сексшоп Алёнка!🔞 </i>
        \n\nЧем могу помочь? """,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )
    print(f"User ID: {user_id}")


@dp.message(Command('help'))
async def help_command(message: Message):
    text = '<b>Used:/help  -></b> \n\nЯ - Бот ТехПоддержка магазина <b><i>Сексшоп Алёнка!🤖🔞</i></b> \n\nЯ нужен для связи между клиентом и оператором!✌️ \n\nДля использования бота нажмите нужную кнопку под сообщением после команды <i><b>START</b></i>!🌟🐲'
    await message.answer(text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda c: c.data == 'help')
async def process_help_callback(callback_query: CallbackQuery):
    await help_command(callback_query.message)
    await callback_query.answer()


@dp.message(Command('faq'))
async def faq_comm(message: Message):
    text = '<b>Used: faq</b>'
    await message.answer(text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda c: c.data == 'faq')
async def faq(callback_query: CallbackQuery):
    await faq_comm(callback_query.message)
    await callback_query.answer()


async def fetch_user_data(user: types.User) -> str:
    user_id = user.id
    fsname = user.first_name
    scname = user.last_name
    prem = user.is_premium
    langcode = user.language_code
    botio = user.is_bot

    profile_photos = await bot.get_user_profile_photos(user_id)

    caption_text = f"""
    
<b>Used: /data ->     
    
ID: {user_id} 
Имя: {fsname}
Фамилия: {scname}
Язык Пользователя: {langcode}
isPremium: {prem}
isBot: {botio}
</b>

"""

    if profile_photos.total_count > 0:
        photo = profile_photos.photos[0][-1]
        return photo.file_id, caption_text
    else:
        return None, caption_text


@dp.message(Command('data'))
async def get_user_data_command(message: Message):
    user = message.from_user
    photo_id, caption_text = await fetch_user_data(user)

    if photo_id:
        await message.answer_photo(photo_id, caption=caption_text, parse_mode=ParseMode.HTML)
    else:
        await message.answer(caption_text, parse_mode=ParseMode.HTML)


@dp.callback_query(lambda c: c.data == 'data')
async def get_user_data_callback(callback_query: CallbackQuery):
    user = callback_query.from_user
    photo_id, caption_text = await fetch_user_data(user)

    if photo_id:
        await bot.send_photo(callback_query.message.chat.id, photo_id, caption=caption_text, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(callback_query.message.chat.id, caption_text, parse_mode=ParseMode.HTML)

    await callback_query.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
