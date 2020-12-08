# SuperChatReader

Youtubeのスパチャを読み込んで一覧にするツール

## ■事前準備

下記の準備をしてください。

### YouTubeのAPIKey取得

下記のリンクからYouTubeのAPIキーを取得してください。

[YouTube API Keyの取得](https://qiita.com/iroiro_bot/items/1016a6a439dfb8d21eca)

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

### インストール

python3.6.9 >=

#### Ubuntu

```bash
sudo apt update
sudo apt install python3-dev
sudo pip3 install pyyaml
```

#### Windows

+ [install link](https://www.python.jp/install/windows/install.html)
+ [setting](https://www.javadrive.jp/python/install/index3.html)

リンクの設定後、pipでpyyamlをインストールする。
コマンドプロンプトで以下を実行する。

```
python -m pip install pyyaml
```


## 実行方法

```bash
$ git clone https://github.com/wakaba130/SuperChatReader.git
$ cd SuperChatReader
$ python3 reader.py
```

# ToDo

+ スパチャを見やすくする
+ GUI対応
+ ToDoリストのように読んだチャットをチェックする
+ 自分のスパチャのみハイライト表示

## できたらいいこと

+ 自動チェック
  + 特定の言葉(〜さん、ありがとう)が入った場合にリストを更新する。