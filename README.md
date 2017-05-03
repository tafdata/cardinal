# Cardinal System 
Athletic Meeting Management System. Improve the ecfficency and get rig of annoying work.


## Discription
陸上競技会運営を支援するwebアプリケーション. 当面はプログラムの編成,当日エントリーの受付と流し用スタートリストの自動作成を目指す.Djangoをdocker上で動作させHTTP経由でサーバPCにアクセスすることでスケーラビリティ-を持たせ、複数台のPCで業務を捌けるようにする.


## Requirement
+ Host PC
  + docker
  + docker-compose
  
+ Client PC
  + (Nothing)

## Instlation
まず、dockerをインストールする。以下のサイトを参考に
+ docker installation[https://docs.docker.com/engine/installation/]
+ docker-compose installation[https://docs.docker.com/compose/install/]

dockerをインストールしたのち、`docker-comose.yml`があるディレクトリで以下のコマンドを実行する。
```bash
# コンテナの作成
$ docker-compose build 
# コンテナ同士のリンク関係を構築
$ docker-compose up -d
# コンテナの実行
$ docker-compose up
# コンテナの停止
$ docker-compose down
```
この時点ではコンテナが動かない可能性が高いので、以下のコマンドでデータベースの初期化を行う。
```bash
$ docker-compose run web
$ docker-compose exec web python3 manage.py migrate
# 管理者アカウントの追加
$ docker-compose exec web python3 manage.py createsuperuser
```
ex. `user='root', email='cardinal.sysyem@tafdata.com', PW='password1234'`




djangoのコマンドを実行したい場合は以下のコマンドでコンテナの中に入るか、
```
$ docker-compose exec web bash
```
以下のコマンドで直接コマンドを実行することができる.
```
$ docker-compose exec web python3 manage.py migrate
```


## Usage
### システムの起動
セキュリティーについては無視して、プライベートなLAN環境内でのみ動作させることを想定.
1. dockerコンテナを`docker-compose up`で起動する
1. ブラウザを開き`localhost:7000`にアクセスする
   
もしブラウザでページが開けない場合は、`docker-compose up`をサイド実行する.

### 大会基本情報の管理
#### 大会と実施種目の登録
大会と種目の登録は管理ページ(admin)から行う.管理者権限が必要.以下の手順をadminページで行う.
1. 大会を登録
1. 競技種目を登録(すでに登録されている場合は不要)
1. 大会と競技種目を結び付けるため、EventStatusを追加.

登録した情報は`http://localhost:7000/comp/`から確認できる.また、実施種目の**Status**と**Entry**は実施種目一覧ページから変更可能.

#### エントリー
エントリー情報の登録は、個別にやる方法とcsvファイルから一括して行う方法がある。
##### Entry File [Cardinal Format]
エントリー情報をcsv形式で登録する場合、CSVファイルは以下のカラムを持つ必要がある。
1. 部門: VS(=対校), OP(=オープン), TT(=記録会), XX=その他
1. 性別: [男/女]
1. 種目名: ex. 100m
1. レース区分: [Heats, Qualification, Semifinal, Final]
1. 組: 空欄でもOK
1. レーン/試技順: 空欄でもOK
1. ゼッケン番号:
1. 氏名: 漢字, 姓と名の間は**全角スペース**を入れる
1. フリガナ: 入力フォーマットは以下を確認
   + 全角カナ:  セイとメイの間は**全角スペース**
   + 半角ｶﾅ:  ｾｲとﾒｲの間は**半角スペース**
1. 学年: 
1. 所属: 
1. 登録陸協: 
1. 参考記録: 入力フォーマットは以下を参考に
   + Static Format: 数字6桁で入力。(ex. 12"34==>001234, 6m54==>000654, 1h23m45s==>012345)
   + Readable format: 分=>', 秒=", 距離==>mのみ使用可 (ex. 12"34, 6m54)


## Licence


## Author
+ T.A.F. Data
  + Yoshimura Naoya
  
