# nature-remo

Nature RemoのAPIを発行し、家電を制御する。

## 説明

家電リモコンであるNaure Remo上に登録されたリモコンボタンを、コマンドラインから実行するツールです。

## 特徴

- コマンドライン上で実行可能(CUI)
- Nature Remo APIの知識は不要
- Remote APIを利用
- リモコンボボタンの事項を、ボタン名称で指定可能

## 事前準備

- python2+

以下のファイルを作成する。

- token.txt: 作成したトークン文字列が格納されているテキストファイル
- appliances.json: RESTで1appliancesコマンドで取得できる設定を保存したJSONファイル

## 利用方法

### 温度、湿度の取得

$ python remo.py get_temp

`引数`
- nickname: いわゆる家電の名前
- name: いわゆるコマンドの名前
`戻り値`
JSON形式

### 家電情報の取得

$ python remo.py get_appliances

`引数`
なし
`戻り値`
JSON形式
### 赤外線の送信

$ python remo.py send_signal --nickname nickname --name name

`引数`
- nickname: いわゆる家電の名前
- name: いわゆるコマンドの名前
`戻り値`
なし


