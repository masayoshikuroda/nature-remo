# nature-remo

Nature RemoのAPIを発行し、家電を制御する。

## 説明

家電リモコンであるNaure Remo上に登録されたリモコンボタンを、コマンドラインから実行するツールです。

## 特徴

- コマンドライン上で実行可能(CUI)
- Nature Remo APIの知識は不要
- Remote APIを利用しているので、外からも実行可能
- リモコンボボタンの実行を、ボタン名称で指定可能

## 事前準備

- python3

以下のファイルを作成する。

- token.txt: 作成したトークン文字列が格納されているテキストファイル
- appliances.json: get_appliancesコマンドで取得した情報を保存したJSONファイル

## 利用方法

### デバイス一覧

$ python3 remo.py get_devices

`引数`
なし

`戻り値`
CSV形式

複数のデバイスを利用している場合に指定するデバイスの番号を確認する。

### 家電情報の取得

$ python3 remo.py get_appliances

`引数`
なし

`戻り値`
JSON形式

ファイルに保存する場合、リダイレクトを利用する。 例) ... > appliances.json

### 温度、湿度の取得

$ python3 remo.py get_events --dev_no 1

`引数`
- dev_no: 温度、湿度を取得するデバイスの番号

`戻り値`
JSON形式

フォーマットした方がわかりやすい。 例) ... | jq .
値のみ取得したい場合、jqコマンドを利用する。 例) ... | jq '.te.val'

### 赤外線の送信

$ python3 remo.py post_signal --nickname nickname --name name

`引数`
- nickname: いわゆる家電の名前
- name: いわゆるボタンの名前

`戻り値`
JSON形式

### エアコンの設定

エアコン自動運転開始
$ python3 remo.py post_aircon --nickname nickname -t 0 -m auto -v auto -i auto

エアコン停止
$ python3 remo.py post_aircon --nickname aircon_nickname -b power-off

`引数`
- nickname: エアコンの名前
- -t temp: 設定温度
- -m mode: エアコンモード
- -v vol: エアコン風量
- -i dir: エアコン風向き
- -b button: 停止時に指定

`戻り値`
JSON形式

### 電力量消費の取得

$ python3 remo.py get_smart_meter --dev_no 0

`引数`
- dev_no: 電力量消費を取得する Nature Remo Eの番号

`戻り値`
JSON形式

フォーマットした方がわかりやすい。 例) ... | jq .
値のみ取得したい場合、jqコマンドを利用する。 例) ... |jq -r '.[] | select(.name == "normal_direction_cumulative_electric_energy") | .val'

## Local APIの利用

lremo.pyを利用します。

### メッセージの取得

$ python lremo.py Remo-xxxxx.local -get > signal.json

### メッセージの送信

$ python lremo.py Remo-xxxxx.local -post -f signal.json
