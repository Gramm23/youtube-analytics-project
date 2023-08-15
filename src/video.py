import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.id = None
        self.video_title = None
        self.url_video = None
        self.view_count = None
        self.like_count = None
        self.video_info()

    def __str__(self):
        return f'{self.video_title}'

    def video_info(self):
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        video_info = video_response['items'][0]
        self.id = video_info['id']
        self.video_title = str(video_info['snippet']['title'])
        self.url_video = f"https://www.youtube.com/watch?v=jTxqXwHY-ig&list={self.id}"
        self.view_count = int(video_info['statistics']['viewCount'])
        self.like_count = int(video_info['statistics']['likeCount'])


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id


