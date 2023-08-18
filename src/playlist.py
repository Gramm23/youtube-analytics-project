import datetime
import os
from googleapiclient.discovery import build
import isodate

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self.playlist()
        self.get_video_response()

    def playlist(self):
        playlist_videos = youtube.playlists().list(
            id=self.playlist_id,
            part='snippet',
            maxResults=50
        ).execute()

        playlist_info = playlist_videos['items'][0]
        self.title = str(playlist_info['snippet']['title'])
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_video_response(self):
        """
        Получаем информацию по видео из плейлиста
        """
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        return video_response

    @property
    def total_duration(self):

        total_duration = datetime.timedelta()

        for video in self.get_video_response()['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def show_best_video(self):

        best_video = None
        best_like_count = 0

        for video in self.get_video_response()['items']:
            like_count = int(video['statistics']['likeCount'])
            if like_count > best_like_count:
                best_like_count = like_count
                best_video = video
        return f"https://youtu.be/{best_video['id']}"



