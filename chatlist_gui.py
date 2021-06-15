##
# coding:utf-8
##

import os
import sys
import json
import yaml
import reader
import tkinter as tk
from threading import Thread
from datetime import datetime

class App:
    def __init__(self):
        """
         ウィンドウを初期化
        """

        if not os.path.isdir("log"):
            os.makedirs("log")

        self.master = tk.Tk()
        self.master.title('SuperChatList')
        self.master.geometry('1000x600')
        self.master.configure(padx=16, pady=16)

        self.setting_area = SettingArea(self.master)
        self.setting_area.pack(side='bottom', expand=True, fill='both')

        # リストの表示エリアを作成
        self.list_area = ListArea(self.master)
        self.list_area.pack(side='bottom', expand=True, fill='both')

    def mainloop(self):
        """
         masterに処理を委譲
        """
        self.master.mainloop()


class SettingArea(tk.Frame):
    def __init__(self, master):
        super(SettingArea, self).__init__(master)

        # 各種ウィジェットの作成
        self.url_label = tk.Label(self, text="YouTubeURL：")
        self.api_label = tk.Label(self, text="YouTubeAPI KEY：")
        self.err_label = tk.Label(self, text="----")
        self.url_entry = tk.Entry(self)
        self.api_entry = tk.Entry(self)
        self.button = tk.Button(self, text="start", command=self._click_read_btn)

        # 各種ウィジェットの設置
        self.url_label.grid(row=0, column=0)
        self.api_label.grid(row=1, column=0)
        self.url_entry.grid(row=0, column=1)
        self.api_entry.grid(row=1, column=1)
        self.err_label.grid(row=2, column=1)
        self.button.grid(row=1, column=2)

        if os.path.isfile("config.yaml"):
            config = reader.read_yaml("config.yaml")    
            self.url_entry.insert(0, config["YouTubeURL"])
            self.api_entry.insert(0, config["API_KEY"])

        # APIキーの文字数
        self.api_key_length = 39

        # 取得パラメータ格納
        self.liveChat = None
        self.readFlg = False

    def _read_check(self, url_str, api_str):
        """
        入力情報のチェック
        """
        
        if "" == url_str or "" == api_str:
            # URLかAPIキーが入力されていない
            self.err_label["text"] = "URLかAPIキーが入力されていません"
            return False
        
        if not "https://www.youtube.com/watch?v=" in url_str:
            # URLか入力されていない
            self.err_label["text"] = "URLが入力されていません"
            return False

        if not len(api_str) == self.api_key_length:
            # APIキーの長さがおかしい
            self.err_label["text"] = "APIキーの文字数がおかしいです"
            return False
        return True
    
    def _click_read_btn(self):
        """
        コメントのロギングを開始する
        """
        yurl = self.url_entry.get()
        apikey = self.api_entry.get()
        
        read_flg = self._read_check(yurl, apikey)

        #print(yurl)
        #print(apikey)
        #print(read_flg)

        if not read_flg:
            return
    
        config = {"API_KEY": apikey,
                    "YouTubeURL": yurl,
                    "sleep_time": 7 }
        with open("config.yaml", 'w') as fp:
            yaml.dump(config, fp)

        liveChat = reader.live_chat_reader(config)
        thread = Thread(target=liveChat.main_loop, name="SubThread", daemon=True)
        if not thread.ident:
            thread.start()
            dt = str(datetime.now()).split('.')[0]
            self.err_label["text"] = "スパチャ取得開始：{}".format(dt)


class ListArea(tk.Frame):
    def __init__(self, master):
        super(ListArea, self).__init__(master)

        # リストの作成
        self.listbox = tk.Listbox(self, height=10, font=("MSゴシック", "12", "bold"))
        self.listbox.pack(side='top', expand=True, fill='both')

        # 読込みボタンの作成
        self.read_btn = tk.Button(self, text='リッロード！', command=self._click_read_btn)
        self.read_btn.pack(side='bottom', fill='x')

        # 削除ボタンの作成
        self.del_btn = tk.Button(self, text='読んだ！', command=self._click_del_btn)
        self.del_btn.pack(side='bottom', fill='x')
        self.counter = 0
        self.read_time = None

    def _click_del_btn(self):
        """
        先頭行を削除する
        """
        self.counter += 1
        self.listbox.delete(0)

    def _split_comment(self, u_name, comment):
        """
        コメントの切り出し
        ToDo: 絵文字コード対応
        """
        sp_comment = comment.replace("{}:".format(u_name), "").split(" ")
        #print(sp_comment)
        if len(sp_comment) <= 3:
            return "_"
        
        #print(sp_comment)
        joint_com = [sp_comment[s] for s in range(3, len(sp_comment), 1)]
        return " ".join(joint_com)

    def _str2datetime(self, chat_time):
        # format 2020-12-08T14:04:32.249000Z
        chat_time = chat_time.replace('+00:00', '')
        _date, _time = chat_time.split('T')
        y, m, d = _date.split('-')
        hh, mm, _ss = _time.split(':')
        if '.' in _ss:
            ss, _ms = _ss.split('.')
            ms = _ms.replace('Z', '')
        else:
            ss = _ss.replace('Z', '')
            ms = '0'
        return datetime(year=int(y), month=int(m), day=int(d),
                        hour=int(hh), minute=int(mm), second=int(ss),
                        microsecond=int(ms))

    def _loader(self, file):
        """
        ログテキストの読み込み
        """

        #print("loader: {}".format(file))
        dtime = None
        with open(file, 'r') as fp:
            for i, _line in enumerate(fp):
                json_dict = json.loads(_line.replace('\n', ''))
                chat_time = json_dict["publishedAt"]
                dtime = self._str2datetime(chat_time)
                user_name = json_dict['displayName']
                comment = self._split_comment(user_name, json_dict['displayMessage'])
                view = "{:<33s} {}".format(user_name, comment)
                #print(view)
                if self.read_time is None or dtime > self.read_time:
                    self.listbox.insert('end', view)
                    if self.counter % 2 == 0:
                        self.listbox.itemconfig(self.counter, {'bg': 'pink'})
                    self.counter += 1
        if dtime != None:
            self.read_time = dtime

    def _click_read_btn(self):
        """
        logファイルからデータを読み込む
        """
        read_time = datetime.now()
        #print(read_time)

        config = reader.read_yaml("config.yaml")

        YouTubeURL = config['YouTubeURL']
        live_id = YouTubeURL.replace('https://www.youtube.com/watch?v=', '')
        superchat_log_file = 'log/' + live_id + '.log'
        #textchat_log_file = 'log/text_' + self.live_id + '.log'
        self._loader(superchat_log_file)

"""
class ImageArea(tk.Frame):
    def __init__(self, master):
        super(ImageArea, self).__init__(master)

        # 画像表示
        canvas = tk.Canvas(bg="black", width=796, height=816)
        canvas.place(x=0, y=0)
        #canvas.create_image(0, 0, image=haruna, anchor=tk.NW)

        # リストの作成
        #self.listbox = tk.Listbox(self, height=5)
        #self.listbox.pack(side='top', expand=True, fill='both')

        # 削除ボタンの作成
        #self.del_btn = tk.Button(self, text='削除', command=self._click_del_btn)
        #self.del_btn.pack(side='bottom', fill='x')
        #self.counter = 0

    def _click_image_btn(self):
        #グラフ画像を表示する
        haruna = tk.PhotoImage(file="haruna_kankore.png")
"""

def main():
    app = App()
    app.mainloop()
    sys.exit()

if __name__ == '__main__':
    main()