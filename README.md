# Cardinal System 
Athletic Meeting Management System. Improve the ecfficency and get rig of annoying work.


## Discription
陸上競技会運営を支援するwebアプリケーション. 当面はプログラムの編成,当日エントリーの受付と流し用スタートリストの自動作成を目指す.Djangoをdocker上で動作させHTTP経由でサーバPCにアクセスすることでスケーラビリティ-を持たせ、複数台のPCで業務を捌けるようにする.


## Requirement
+ Host PC
  + docker
  + docker-compose
  
+ Client PC
  + nothing spetial

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
[1] dockerコンテナを起動させます



## Licence


## Author
+ T.A.F. Data
  + Yoshimura Naoya
  
