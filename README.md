# SuperChatReader

+ Youtubeのスパチャを読み込んで一覧にするツール
+ ライブ配信中のチャットヒストグラム作成
  + チャットの盛り上がりの可視化

## ■事前準備

下記の準備をしてください。

### YouTubeのAPIKey取得

下記のリンクからYouTubeのAPIキーを取得してください。

[YouTube API Keyの取得](https://qiita.com/iroiro_bot/items/1016a6a439dfb8d21eca)

### インストール

python3.6.9 >=

#### Ubuntu

```bash
$ sudo apt update
$ sudo apt install python3-dev python3-tk
$ sudo pip3 install pyyaml
$ sudo pip3 install numpy
$ sudo pip3 install matplotlib
$ git clone https://github.com/wakaba130/SuperChatReader.git
```

#### Windows

+ [install link](https://www.python.jp/install/windows/install.html)
+ [setting](https://www.javadrive.jp/python/install/index3.html)

リンクの設定後、pipでpyyamlをインストールする。
コマンドプロンプトで以下を実行する。

```
$ python -m pip install pyyaml
$ sudo pip3 install numpy
$ sudo pip3 install matplotlib
$ git clone https://github.com/wakaba130/SuperChatReader.git
```


# 実行方法

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

![image](test/chat_hist.png)

また、ターミナルには、`--top`で指定した上位のチャット時間が表示されます。

```
=== top 5 ===
('0:52', 812.0)
('0:22', 800.0)
('0:50', 774.0)
('0:27', 738.0)
('0:25', 730.0)
```

# ToDo

+ reader
  + 配信前予約機能
    + ライブ配信前の動画URLに対して、ずっとパラメータ取得を行っていると切断されるため
  + スパチャを見やすくする
  + GUI対応
  + ToDoリストのように読んだチャットをチェックする
  + 自分のスパチャのみハイライト表示
+ create_hist
  + 特になし

## できたらいいこと

+ 自動チェック
  + 特定の言葉(〜さん、ありがとう)が入った場合にリストを更新する。
+ ハイライト動画自動作成
  + チャットの盛り上がりから、ハイライト動画を作成