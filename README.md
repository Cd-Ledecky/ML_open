# ML_open

## 環境
* `python 3.6`

## 主要ライブラリのバージョン

```
tensorflow(-gpu)==1.14
keras==2.3
```
tensorflow(-gpu)は2系でも動くと思われる


## ディレクトリとその役割

### 主要なディレクトリ
* models    : AI のモデル
* outputs   : 学習後のモデルやログなどの結果・出力を保存する (実行時に作成されたり、したりする)
	- logs
	- models
* utils     : ユーティリティ



## ディレクトリ構成

```
ML_open
├── Classified_object_name
│   ├── 299299bunkatu_29299315.py
│   ├── lim_bunkatu20210315.py
│   ├── traing_model.py
│   ├──20210409
│   │   ├── original_data
│   │   |   ├── count_point_RGB.py
│   │   |   ├── count_point_RGB_test.py
│   │   |   ├── lim_bunkatu.py
│   │   |   ├── RGB2HSV_0417.py
│   │   |   ├── final
│   │   |   |   ├── 1
│   │   |   |   |   ├── cropped
│   │   |   |   ├── 2
│   │   |   |   |   ├── cropped
│   │   |   |   ├── 3
│   │   |   |   |   ├── cropped
│   │   |   |   ├── 4
│   │   |   |   |   ├── cropped
│   │   |   |   ├── 5
│   │   |   |   |   ├── cropped

```
