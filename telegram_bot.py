import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import bot_token, database_url_async
from database.models import Channel, Video
from services.parser import Parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

async_engine = create_async_engine(database_url_async)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Введите ссылку на канал и количество видео для парсинга:")


@dp.message_handler(commands=["view_videos"])
async def view_videos(message: types.Message):
    async with async_session() as db:
        try:
            channels = await db.execute(select(Channel))
            channels = channels.scalars().all()
            if not channels:
                await message.reply("Нет доступных каналов для просмотра.")
                return

            markup = InlineKeyboardMarkup()
            for channel in channels:
                markup.add(
                    InlineKeyboardButton(
                        channel.name, callback_data=f"channel_{channel.id}"
                    )
                )

            await message.reply("Выберите канал:", reply_markup=markup)
        except Exception as e:
            logger.error(f"Ошибка при попытке просмотреть каналы: {str(e)}")
            await message.reply(
                f"Произошла ошибка при попытке просмотреть каналы: {str(e)}"
            )


@dp.callback_query_handler(lambda c: c.data.startswith("channel_"))
async def process_callback_channel(callback_query: types.CallbackQuery):
    channel_id = int(callback_query.data.split("_")[1])
    async with async_session() as db:
        try:
            videos = await db.execute(
                select(Video).where(Video.channel_id == channel_id)
            )
            videos = videos.scalars().all()
            if not videos:
                await bot.answer_callback_query(
                    callback_query.id, "Нет доступных видео для этого канала."
                )
                return

            markup = InlineKeyboardMarkup()
            for video in videos:
                markup.add(
                    InlineKeyboardButton(video.title, callback_data=f"video_{video.id}")
                )

            await bot.send_message(
                callback_query.from_user.id, "Выберите видео:", reply_markup=markup
            )
        except Exception as e:
            logger.error(f"Ошибка при попытке просмотреть видео: {str(e)}")
            await bot.answer_callback_query(
                callback_query.id, "Ошибка при просмотре видео."
            )


@dp.callback_query_handler(lambda c: c.data.startswith("video_"))
async def process_callback_video(callback_query: types.CallbackQuery):
    video_id = int(callback_query.data.split("_")[1])
    async with async_session() as db:
        try:
            video = await db.get(Video, video_id)
            if not video:
                await bot.answer_callback_query(callback_query.id, "Видео не найдено.")
                return

            await bot.send_message(
                callback_query.from_user.id,
                f"{video.title}\n{video.description[:100]}\nПросмотров: {video.views}\nСсылка: {video.link}",
            )
        except Exception as e:
            logger.error(f"Ошибка при попытке просмотреть видео: {str(e)}")
            await bot.answer_callback_query(
                callback_query.id, "Ошибка при просмотре видео."
            )


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
            channel = Channel(name=channel_url, url=channel_url)
            db.add(channel)
            await db.commit()
            await db.refresh(channel)

            for video in videos:
                db_video = Video(
                    title=video["title"],
                    description=video["description"],
                    views=video["views"],
                    link=video["video_url"],
                    channel_id=channel.id,
                )
                db.add(db_video)
            await db.commit()

            await message.reply(f"Видео сохранено для канала {channel_url}")
        except Exception as e:
            await message.reply(
                f"Произошла ошибка при обработке вашего запроса: {str(e)}"
            )


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp)
