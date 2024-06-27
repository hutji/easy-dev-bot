from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Video


async def save_videos(db: AsyncSession, videos):
    for video in videos:
        db_video = Video(
            title=video[0], description=video[1], views=video[2], link=video[3]
        )
        db.add(db_video)
    await db.commit()
