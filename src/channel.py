import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.id = None
        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None
        self.update_channel_info()

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    @classmethod
    def get_service(cls):
        return youtube

    def update_channel_info(self):
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_info = channel['items'][0]

        self.id = channel_info['id']
        self.title = channel_info["snippet"]["title"]
        self.description = channel_info["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(channel_info['statistics']['subscriberCount'])
        self.video_count = int(channel_info['statistics']['videoCount'])
        self.view_count = int(channel_info['statistics']['viewCount'])

    def to_json(self, file_path: str) -> None:
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        print(f"ID: {self.id}")
        print(f"Название: {self.title}")
        print(f"Описание: {self.description}")
        print(f"Ссылка: {self.url}")
        print(f"Подписчики: {self.subscriber_count}")
        print(f"Видео: {self.video_count}")
        print(f"Просмотры: {self.view_count}")
