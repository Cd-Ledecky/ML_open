# このプログラムは破壊的処理ではない＝＞もとの画像は残ります

# このプログラムは、各クラスのフォルダがあるディレクトリにおく
#   クラス1,2,3,4,5フォルダが置いてあるディレクトリと一緒のところ

#前提
# くりぬいた画像がクラス1,2,3,4,5フォルダの中の
#「cropped」フォルダにある

from PIL import Image
import os
import matplotlib.pyplot as plt

#★
choose_list = ["1","2","3","4","5",]

current_d = os.getcwd()
for foldername in choose_list:
    os.chdir(os.path.join(current_d,foldername,"cropped"))
    #     print(os.getcwd())
    #C:\Users\NAME\Desktop\2021撮影\分類対象\20210315-17\1照明強度\97lux\1\cropped

    # croppedというフォルダを新たに作り、切り取った背景画像を保存
    os.makedirs("299299",exist_ok=True)

    #そのフォルダ内のすべての画像をループ
    for filename in os.listdir("."):
        #.jpg,.pngで終わらないファイルは、以下の処理を行わない
        if not (filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".JPG")):
            continue

        #画像の読み込み
        # 横3400,縦3300 20210315
        # 299*299を11*11いけそう
        IMAGE_im = Image.open(filename)
        #ori_x,ori_y = IMAGE_im.size
        #print(ori_x,ori_y)  #1451 2808


        #切り抜いた分類対象画像を水平分割
        #横3400,縦3300
        cr_w,cr_h = IMAGE_im.size

        #画像の横サイズを299で割った時の整数部分
        count_x = int(cr_w / 299)    #11
        #print(count_x)
        count_y = int(cr_h / 299)    #11
        #print(count_y)

        #for は 0からrange -1 まで。
        for i in range(count_y):
            #分割
            SIZE = 299
            #overlap = (299 - (cr_h - 299*count_y)) / count_y   #21
            #print(overlap)

            #横に分割したものを、縦に分割
            #今、横長の画像ができている（yの大きさはOK）
            nnn = IMAGE_im.crop((0, i*SIZE, cr_w, (i*SIZE)+SIZE))
            # xxx:横長
            xxx,yyy=nnn.size
            for j in range(count_x):
                mmm = nnn.crop((j*SIZE,0,(j*SIZE)+SIZE,yyy))
                #保存
                mmm.save(os.path.join("299299",str(i)+"_"+str(j)+"_"+filename))
                print("実行中",i,j)