# -*- coding: utf-8 -*-
# このプログラムは破壊的処理ではない＝＞もとの画像は残ります

from PIL import Image
import os
import matplotlib.pyplot as plt
import random 
from natsort import natsorted

# k:背景を切り取る範囲 k*k分のピクセルを左上から切り取る
# N:何枚に水平分割するか
# M:水平分割した画像を縦に何分割するか
# split:分割方法 "cross","horizontal"
#左上に背景を付けたいクラスを指定する
# ●●●●●●●●●●●●↓ここを指定↓●●●●●●●●●●●●
choose_list = ["final"]
choose_list2=["1","2","3","4","5"]
#"3","4","5","C6","3wb3000","4wb3000","5wb3000","C6wb3000" 

print("起動")

#このプログラムが置いてあるディレクトリをコピー(1)
current_d = os.getcwd()
for foldername in choose_list:
    for foldername2 in choose_list2:
        #(1)にchoose_list,"2021_02_15","JPG"をつけたディレクトリ
        os.chdir(os.path.join(current_d,foldername,foldername2))

        #(1)にchoose_list,"2021_02_15","CR3"をつけたディレクトリ
        #os.chdir(os.path.join(current_d,foldername,"2021_02_15","CR3"))

        # フォルダを新たに作る
        os.makedirs("cropped",exist_ok=True)
        #os.makedirs("none",exist_ok=True)
        #os.makedirs("Green",exist_ok=True)
        #os.makedirs("Amber",exist_ok=True)


        #そのフォルダ内のすべての画像をループ
        i=1
        a=[]
        for filename in os.listdir("."):
            #.jpg,.JPGで終わらないファイルは、以下の処理を行わない
            if not (filename.endswith(".jpg") or filename.endswith(".JPG")):
                continue
            a.append(filename)
            

        for filename in natsorted(a):
            #その画像の読み込み
            MONO_im = Image.open(filename)
            #MONO部分だけを切り抜く
            cropped_im = MONO_im.crop((850,350,4250,3600))  # 横1000,縦2250
            cropped_im.save(os.path.join("cropped",filename))

            """
            if (i%3) == 1:
                cropped_im.save(os.path.join("none",filename))
                i=i+1
                print(i,"none",filename)
            elif (i%3) == 2:
                cropped_im.save(os.path.join("Green",filename))
                i=i+1
                print(i,"Green",filename)
            else:
                cropped_im.save(os.path.join("Amber",filename))
                i=i+1
                print(i,"Amber",filename)
            """

    """
            #背景を(0,0)から(k,k)、まで切り抜く
            #cropped_back = MONO_im.crop((0,0,k,k))
            #保存
            #cropped_back.save(os.path.join("BACK",filename))


            #切り抜いたMONOを水平分割
            #cr_w,cr_h = cropped_im.size
            #print(cr_w,cr_h) #(980 2350)

            im_h_divided_N = int(cr_h / N) 
            #2350 / 7
            for i in range(N):
                #分割
                height = i*(im_h_divided_N)
                nnn = cropped_im.crop((0, height, cr_w, height + im_h_divided_N))
                xx,yy = nnn.size
                for j in range(M):
                    mmm = nnn.crop((cr_w * j/3,0,cr_w * (j+1) /3,yy))
                    #保存:背景なし4分割画像
                    mmm.save(os.path.join("limit_withoutBACK","lim"+str(i)+"_"+str(j)+"_"+filename))
                    #背景の貼り付け
                    mmm.paste(cropped_back,(0,0))
                    #保存:背景あり4分割画像
                    mmm.save(os.path.join("limit_withBACK","lim"+str(i)+"_"+str(j)+"_"+filename))

            #表示
            #plt.imshow(MONO_im)
            #plt.show()
    """