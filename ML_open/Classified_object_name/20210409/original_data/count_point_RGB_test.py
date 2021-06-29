# -*- coding: utf-8 -*-
# このプログラムは破壊的処理ではない＝＞もとの画像は残ります
# python .\count_point_RGB_test.py > countBWtest.csv

from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
import random 
from natsort import natsorted
import cv2
import matplotlib.pyplot as plt
import pandas

# ●●●●●●●●●●●●↓ここを指定↓●●●●●●●●●●●●
choose_list = ["final"]
choose_list2=["test"]

#print("起動")
#2600*2900

#このプログラムが置いてあるディレクトリをコピー(1)
current_d = os.getcwd()
for foldername in choose_list:
    for foldername2 in choose_list2:
        os.chdir(os.path.join(current_d,foldername,foldername2))
        #(1)にchoose_list,"2021_02_15","JPG"をつけたディレクトリ
        #ここにはクロップ後の画像が保存されている
        #Hue_araay_c = []
        #Value_araay_c = []
        #Chroma_araay_c = []

        #横2600,縦2900
        #そのフォルダ内のすべての画像をループ
        for filename in os.listdir("."):
            #.jpg,.JPGで終わらないファイルは、以下の処理を行わない
            if not (filename.endswith(".jpg") or filename.endswith(".JPG")):
                continue
            img = cv2.imread(filename)
            img_array = np.asarray(img)
            img_array2 = cv2.cvtColor((img_array), cv2.COLOR_RGB2BGR)
            #cv2の下に赤波線が出るのは問題なし
            #VScodeで実行しなければ問題なし
            #print(filename)

            #取得された三次元配列は画像の高さ、幅、RGBの順に格納されています。
            #そのため1920×1080の画像のx座標1500、y座標700のRGBカラーを取り出す。
            # RGBの配列 [87 60 43]
            #print(img_array2[699][1499])
            # Rの値 87
            #print(img_array2[699][1499][0])
            # Gの値 60
            #print(img_array2[699][1499][1])
            # Bの値 43
            #print(img_array2[699][1499][2])
            
            #横2600,縦2900
            #これを10点決める
            #白飛びの無い内側から6*289=1734 点の平均を取る
            RGB = []
            for y in range(10,298,2):
                for x in range(10,298,2):
                    RGB.append(img_array2[x][y])
            #常にFalseなので実行されない
            if False:
                RGB = [img_array2[325][725],img_array2[325][1450],img_array2[325][2175],
                    img_array2[975][1035],img_array2[975][1760],img_array2[1625][1035],
                    img_array2[1625][1760],img_array2[2275][725],img_array2[2275][1450],
                    img_array2[2275][2175]
                ]
            #print(RGB)

            #print(max(1,2,3))   3
            #Hue_araay_a = []
            #Value_array_a = []
            #Chroma_array_a = []
            #Hue_b =0
            #Value_b =0
            #Chroma_b =0
            R_array=[]
            G_array=[]
            B_array=[]
            #count point 0,0,0 255,255,255
            count_000=0
            count_255255255=0


            for R,G,B in RGB:
                #R,G,Bをintに直さないと、Hの計算が上手くいかない
                #<=なんで・・・。
                R = int(R)
                G = int(G)
                B = int(B)
                """
                maax = max(R,G,B)
                if maax==0:
                    maax+=1
                miin = min(R,G,B)
                #print(maax,miin)
                #彩度C
                C = ((maax-miin)/maax)*100
                #明度V
                V = (maax/255)*100
                #色彩H
                diff = int(maax - miin)
                #print(diff)
                H=0
                if maax == miin:
                    H = 0
                elif maax == R:
                    H = int(60 * ((G-B)/diff)     )
                elif maax == G:
                    H = int(60 * ((B-R)/diff) + 120  )
                elif maax == B:
                    H = int(60 * ((R-G)/diff) + 240)
                if H < 0: 
                    H = H + 360
                #Hue_araay_a.append(H)
                """
                
                """
                #次でも上と同じ色相Hが求められる
                import colorsys
                R = float(R)
                G = float(G)
                B = float(B)
                h,s,v=colorsys.rgb_to_hsv(R,G,B)
                h = int(h*360)
                #print(h)
                #print(h,H)
                """
                #print(H)
                #print("H:",H,R,G,B)
                if (R==0):
                    if (G==0):
                        if (B==0):
                            count_000 +=1
                if (R==255):
                    if (G==255):
                        if (B==255):
                            count_255255255 +=1
               # Hue_araay_a.append(H)
               # Value_array_a.append(V)
                #Chroma_array_a.append(C)
                #R_array.append(R)
                #G_array.append(G)
                #B_array.append(B)


            #Hue_b+=sum(Hue_araay_a)/len(Hue_araay_a)
            #Value_b+=sum(Value_array_a)/len(Value_array_a)
            #Chroma_b+=sum(Chroma_array_a)/len(Chroma_array_a)
            #av_R = sum(R_array)/len(R_array)
            #av_G = sum(G_array)/len(G_array)
            #av_B = sum(B_array)/len(B_array)


            #等級と色相の値を,を隔てて表示
            # python .\RGB2HSV.py > 20210326.csv でエクセルで散布図を作るため
            # python .\RGB2HSV.py > h-jpg-wb有.csv
            if foldername2 == "1":
                tk = 1
            elif foldername2 == "2":
                tk = 2
            elif foldername2 == "3":
                tk = 3
            elif foldername2 == "4":
                tk = 4
            elif foldername2 == "5":
                tk = 5
            elif foldername2 == "test":
                tk = 6
            
            #print(foldername,",",tk,",",Hue_b,",",Value_b,",",Chroma_b,",",av_R,",",av_G,",",av_B)
            #print("色相H10点平均",Hue_b)
            #print("明度V10点平均",Value_b)
            #print("彩度S10点平均",Chroma_b)
            #Hue_araay_c.append(Hue_b)
            #Value_araay_c.append(Value_b)
            #Chroma_araay_c.append(Chroma_b)
            #エクセル用
            print(tk,",",count_000,",",count_255255255)
            #print(Hue_araay_c)
