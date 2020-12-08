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
            config = yaml.load(fp, Loader=yaml.FullLoader)
        return config

class live_chat_reader():
    def __init__(self, config):
        YouTubeURL = config['YouTubeURL']
        self.sleep_time = config['sleep_time']
        self.api_key    = config['API_KEY']
        self.live_id = YouTubeURL.replace('https://www.youtube.com/watch?v=', '')
        self.superchat_log_file = 'log/' + self.live_id + '.log'
        self.textchat_log_file = 'log/text_' + self.live_id + '.log'
        print(self.superchat_log_file)
        self.chat_id  = self._get_chat_id()
        self.pageToken = None

    def _get_chat_id(self):
        """チャット基本情報の取得"""
        url    = 'https://www.googleapis.com/youtube/v3/videos'
        params = {'key': self.api_key, 'id': self.live_id, 'part': 'liveStreamingDetails'}
        data   = requests.get(url, params=params).json()

        liveStreamingDetails = data['items'][0]['liveStreamingDetails']

        if 'activeLiveChatId' in liveStreamingDetails.keys():
            chat_id = liveStreamingDetails['activeLiveChatId']
            print('get_chat_id done!')
        else:
            chat_id = None
            print('NOT live')

        return chat_id


    def get_chat(self):
        """チャットの内容取得"""
        url    = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
        params = {'key': self.api_key, 'liveChatId': self.chat_id, 'part': 'id,snippet,authorDetails'}
        
        if type(self.pageToken) == str:
            params['pageToken'] = self.pageToken

        _data = requests.get(url, params=params).json()

        try:
            superchat_list = []
            textchat_list = []
            for item in _data['items']:
                if item['snippet']['type'] == 'superChatEvent':
                    superchat_list.append(item['snippet'])
                elif item['snippet']['type'] == 'textMessageEvent':
                    textchat_list.append(item['snippet'])

            superchat_list.sort(key=lambda x: x['publishedAt'])
            with open(self.superchat_log_file, 'a') as fp:
                for item in superchat_list:
                    usr = item['displayName']
                    msg = item['displayMessage']
                    print('[by {}]\n  {}'.format(usr, msg))
                    item_str = json.dumps(item)
                    print(item_str, file=fp)
            with open(self.textchat_log_file, 'a') as fpt:
                for item in textchat_list:
                    fpt.write("{}\n".format(item['publishedAt']))                    
        except:
            pass

        self.pageToken = _data['nextPageToken']
        time.sleep(self.sleep_time)
        return superchat_list

def main(config):
    liveChat = live_chat_reader(config)
    while True:
        try:
            liveChat.get_chat()
        except:
            print("time out or next token error")
            break


if __name__ == '__main__':
    config = read_yaml("config.yaml")
    main(config)