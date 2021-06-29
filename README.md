# ML_open

## 環境
* `python 3.6`

[](
```shell
$ python --version
Python 3.6.9
```
)

### 仮想環境

* [pyenv](https://github.com/pyenv/pyenv):
  python 仮想環境には pyenv を用いています。
  システムの python と切り離す目的や、python のバージョンを好きに変更できるために使っています、
* [venv](https://docs.python.org/3.8/library/venv.html):
  python package の仮想環境には venv を用いています。
  python 標準で用意されている仮想環境です。

* (パッケージ) 仮想環境の作成

```shell
$ python -m venv venv
```

* 仮想環境のアクティベート (有効化)

```shell
# MacOS or Linux
$ source venv/bin/activate

# Windows (?)
> .\[newenvname]\Scripts\activate
```

* ライブラリのインストール

```shell
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


* [日本語 help - venv: Python 仮想環境管理](https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e)


## 主要なライブラリのバージョン

```
tensorflow(-gpu)==1.14
keras==2.3
```

## ディレクトリとその役割

### 主要なディレクトリ
* models    : AI のモデル
* outputs   : 学習後のモデルやログなどの結果・出力を保存する (実行時に作成されたり、したりする)
	- logs
	- models
* utils     : ユーティリティ

## ディレクトリ構成

```
.nori_project/
├── README.md
├── models
└── utils
```
