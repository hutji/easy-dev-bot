import httpx
from bs4 import BeautifulSoup


class Parser:
    @staticmethod
    async def parse_channel(channel_url: str, video_count: int):
        async with httpx.AsyncClient() as client:
            channel_response = await client.get(channel_url)
            if channel_response.status_code == 301:
                redirected_url = channel_response.headers["Location"]
                channel_response = await client.get(redirected_url)
            if channel_response.status_code != 200:
                raise Exception(
                    "Ошибка получения данных с канала. "
                    f"Статус ошибки: {channel_response.status_code}"
                )
            channel_soup = BeautifulSoup(channel_response.text, "html.parser")
            channel_videos = channel_soup.select(
                "a.wdp-link-module__link.wdp-card-poster-module__posterWrapper"
            )
            videos = []
            for video in channel_videos[:video_count]:
                video_url = f'https://rutube.ru{video["href"]}'
                video_response = await client.get(video_url)
                video_soup = BeautifulSoup(video_response.text, "html.parser")
                video_title = video_soup.find(
                    "section", class_="video-pageinfo-container-module__videoTitle"
                ).text.strip()
                video_description = (
                    video_soup.find(
                        "div",
                        class_=(
                            "freyja_pen-videopage-description" "__description_x8Lqk"
                        ),
                    ).text.strip()[:97]
                    + "..."
                )
                video_views = video_soup.find(
                    "div",
                    class_=(
                        "wdp-video-options-row-module"
                        "__wdpVideoOptionsRow__views-count"
                    ),
                ).text.strip()
                video_views = int("".join(filter(str.isdigit, video_views)))
                channel_name = video_soup.find(
                    "span",
                    class_=(
                        "freyja_pen-author-options-row"
                        "__pen-author-options-row__author-title_NEF8H"
                    ),
                ).text.strip()
                videos.append(
                    {
                        "title": video_title,
                        "description": video_description,
                        "views": video_views,
                        "video_url": video_url,
                        "channel_name": channel_name,
                    }
                )
            return videos
