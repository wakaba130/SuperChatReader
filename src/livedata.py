##
# coding:utf-8
##

# ライブ配信状態の取得

import os
import sys
import json
import yaml
import time
import reader
import tkinter as tk
from threading import Thread
from datetime import datetime

from apiclient.discovery import build
from datetime import datetime, timedelta
import os

config_yaml = reader.read_yaml("config.yaml")

DEVELOPER_KEY = os.environ.get('YOUTUBE_API_KEY', config_yaml['API_KEY'])
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

def youtube_search(channel_id: str, max_results: int = 10) -> list:
    # Search: list で channel_id から検索する
    search_response = youtube.search().list(channelId=channel_id, part='id', order='date').execute()
    return search_response.get('items', [])

def youtube_video_details(video_id: str) -> list:
    # Videos: list で video_id から検索する
    video_response = youtube.videos().list(id=video_id, part='liveStreamingDetails').execute()
    return video_response.get('items', [])

def call(youtube_channel_key:str):
    now_time = datetime.now()
    upcoming_list = []
    for item in youtube_search(youtube_channel_key):
        video_id = item['id']['videoId']
        details = youtube_video_details(video_id)
        if len(details) == 0:
            continue

        scheduled_start_time = datetime.strptime(details[0]['liveStreamingDetails']['scheduledStartTime'], '%Y-%m-%dT%H:%M:%SZ')
        scheduled_start_time_jst = scheduled_start_time + timedelta(hours=9)  # 日本時間(JST)にする
        #print(scheduled_start_time_jst)
        # 指定時刻よりも
        if now_time < scheduled_start_time_jst:
            print(scheduled_start_time_jst)
            upcoming_list.append(video_id)

    return upcoming_list

if __name__ == '__main__':
    channelKey = 'UC6eWCld0KwmyHFbAqK3V-Rw'
    upcoming = call(channelKey)
    print(upcoming)

    for live_id in upcoming:
        print(live_id)
        watch_url = 'https://www.youtube.com/watch?v=' + live_id
        config = reader.YouTubeConfig(watch_url, config_yaml['API_KEY'])
        lcr = reader.live_chat_reader(config)
        
        while lcr.get_chat_id() is None:
            print(datetime.now())
            time.sleep(60)

        with open("config.yaml", 'w') as fp:
            yaml.dump(config.dump_dict(), fp)

        # 自動的にロガーを開始する（GUIとの分離）

        
    
