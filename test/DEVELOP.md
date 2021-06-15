# 開発用のREADME

## ■インストール

python3.6.9 >=

### Ubuntu

※特殊文字コード（絵文字）に未対応

```bash
$ sudo apt update
$ sudo apt install python3-dev python3-tk
$ sudo pip3 install -r requirements.txt
$ git clone https://github.com/wakaba130/SuperChatReader.git
```

### Windows(code)

+ [python install link](https://www.python.jp/install/windows/install.html)
+ [python setting](https://www.javadrive.jp/python/install/index3.html)

リンクの設定後、pipで関連ライブラリをインストールする。
コマンドプロンプトで以下を実行する。

```
$ sudo pip3 install -r requirements.txt
$ git clone https://github.com/wakaba130/SuperChatReader.git
```

### EXE化する方法

```
$ pip3 install pyinstaller
$ pyinstaller chatlist_gui.py
```

## reader

配信準備中、配信中のスパチャログと通常チャットの投稿時間ログを保存する。

### 設定ファイルの準備

以下のconfig.yamlファイルを作成して、同じフォルダに保存する。
API_KEYの`XXXXXX`部分には、先程取得したAPIキーを書き込みます。
YouTubeURLは、Live配信のURLをコピペで貼ってください。

config.yaml

```yaml
API_KEY:     XXXXXXXXXXXXXXXXXXXXXXXX
YouTubeURL: https://www.youtube.com/watch?v=XXXXXXXXXX
sleep_time:  10 #sec
```

### 実行

```bash
$ cd SuperChatReader
$ python3 reader.py
```

## create_hist

チャットの投稿頻度を分単位で可視化する。
reader.pyで取得したログファイルを指定する。

```bash
$ python create_hist.py --logfile [text_XXXXXXXXXXX.log] --top 5
```

下図のように分単位のチャットの盛り上がりがわかります。

![image](chat_hist.png)

また、ターミナルには、`--top`で指定した上位のチャット時間が表示されます。

```
=== top 5 ===
('0:52', 812.0)
('0:22', 800.0)
('0:50', 774.0)
('0:27', 738.0)
('0:25', 730.0)
```
