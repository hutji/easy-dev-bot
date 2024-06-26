from aiogram import Bot, Dispatcher, types
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import bot_token, database_url_async
from services.parser import Parser

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

async_engine = create_async_engine(database_url_async)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Введите ссылку на канал и количество видео для парсинга:")


@dp.message_handler()
async def get_videos(message: types.Message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.reply(
            "Пожалуйста, введите ссылку на канал и количество видео, разделенные пробелом."
        )
        return

    channel_url, count_str = parts
    try:
        count = int(count_str)
    except ValueError:
        await message.reply("Количество видео должно быть целым числом.")
        return

    async with async_session() as db:
        try:
            videos = await Parser.parse_channel(channel_url, count)
            for video in videos:
                await message.reply(
                    f"{video['title']}\n{video['description']}\n{video['views']}\n{video['video_url']}"
                )
        except Exception as e:
            await message.reply(
                f"Произошла ошибка при обработке вашего запроса: {str(e)}"
            )


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp)
