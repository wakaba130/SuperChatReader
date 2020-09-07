##
# cording:utf-8
##

import time
import requests
import json
import yaml

def read_yaml(file_name):
    """設定ファイルの読み込み"""

    with open(file_name, 'r') as fp:
        config = yaml.load(fp)
    return config


def get_chat_id(api_key, live_id):
    """チャット基本情報の取得"""

    print('video_id : ', live_id)
    url    = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': api_key, 'id': live_id, 'part': 'liveStreamingDetails'}
    data   = requests.get(url, params=params).json()

    liveStreamingDetails = data['items'][0]['liveStreamingDetails']

    if 'activeLiveChatId' in liveStreamingDetails.keys():
        chat_id = liveStreamingDetails['activeLiveChatId']
        print('get_chat_id done!')
    else:
        chat_id = None
        print('NOT live')

    return chat_id


def get_chat(api_key, chat_id, pageToken, log_file):
    """チャットの内容取得"""
    url    = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {'key': api_key, 'liveChatId': chat_id, 'part': 'id,snippet,authorDetails'}
    
    if type(pageToken) == str:
        params['pageToken'] = pageToken

    _data = requests.get(url, params=params).json()
    #print("read done!")

    try:
        with open(log_file, 'a') as fp:
            for item in _data['items']:
                if item['snippet']['type'] == 'superChatEvent':
                    usr       = item['authorDetails']['displayName']
                    msg       = item['snippet']['displayMessage']
                    log_text  = '[by {}]\n  {}'.format(usr, msg)
                    print(log_text)
                    print(item, file=fp)
    except:
        pass

    return _data['nextPageToken']


def main(config):
    YouTubeURL = config['YouTubeURL']
    sleep_time = config['sleep_time']
    api_key    = config['API_KEY']

    live_id = YouTubeURL.replace('https://www.youtube.com/watch?v=', '')
    log_file = live_id + '.log'

    chat_id  = get_chat_id(api_key, live_id)

    SuperChatList = []
    nextPageToken = None
    while True:
        try:
            nextPageToken = get_chat(api_key, chat_id, nextPageToken, log_file)
            time.sleep(sleep_time)
        except:
            print("time out or next token error")
            break


if __name__ == '__main__':
    config = read_yaml("config.yaml")
    main(config)