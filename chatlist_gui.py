##
# coding:utf-8
##

import json
import tkinter as tk

class App:
    def __init__(self):
        # ウィンドウを初期化
        self.master = tk.Tk()
        self.master.title('SuperChatList')
        self.master.geometry('800x600')
        self.master.configure(padx=16, pady=16)

        # リストの表示エリアを作成
        self.list_area = ListArea(self.master)
        self.list_area.pack(side='bottom', expand=True, fill='both')
        # 表示リストの読み込み
        self.loader("log/FGhIbI9AJr0.log")

    def mainloop(self):
        # masterに処理を委譲
        self.master.mainloop()

    def loader(self, file):
        name_num = 0
        counter = 0
        with open(file, 'r') as fp:
            for i, _line in enumerate(fp):
                json_dict = json.loads(_line.replace('\n', ''))
                user_name = json_dict['displayName']
                coment = json_dict['displayMessage']
                #print("{} : {}".format(user_name, coment))
                view = "{}:{}".format(user_name, coment)
                print(view)
                self.list_area.listbox.insert('end', user_name)
                counter += 1
                if user_name == "seta130":
                    name_num = i
        self.user_num = name_num
        self.user_max = counter

class ListArea(tk.Frame):
    def __init__(self, master):
        super(ListArea, self).__init__(master)

        # リストの作成
        self.listbox = tk.Listbox(self, height=5)
        self.listbox.pack(side='top', expand=True, fill='both')

        # 削除ボタンの作成
        self.del_btn = tk.Button(self, text='削除', command=self._click_del_btn)
        self.del_btn.pack(side='bottom', fill='x')
        self.counter = 0

    def _click_del_btn(self):
        """
        先頭行を削除する
        """
        self.counter += 1
        self.listbox.delete(0)
    
def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()