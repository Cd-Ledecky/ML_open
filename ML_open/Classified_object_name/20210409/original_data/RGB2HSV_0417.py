# -*- coding: utf-8 -*-
# このプログラムは破壊的処理ではない＝＞もとの画像は残ります
# python .\RGB2HSV_0417.py > aaa.csv

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
choose_list2=["1","2","3","4","5"]

#print("起動")
#2600*2900

print("a")


#このプログラムが置いてあるディレクトリをコピー(1)
current_d = os.getcwd()
for foldername in choose_list:
    for foldername2 in choose_list2:
        #(1)にchoose_list,"2021_02_15","JPG"をつけたディレクトリ
        os.chdir(os.path.join(current_d,foldername,foldername2,"cropped"))
        #ここにはクロップ後の画像が保存されている

        Hue_araay_c = []
        Value_araay_c = []
        Chroma_araay_c = []

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
            for y in range(10,3200,10):
                for x in range(10,3200,10):
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
            Hue_araay_a = []
            Value_array_a = []
            Chroma_array_a = []
            Hue_b =0
            Value_b =0
            Chroma_b =0
            R_array=[]
            G_array=[]
            B_array=[]


            for R,G,B in RGB:
                #R,G,Bをintに直さないと、Hの計算が上手くいかない
                #<=なんで・・・。
                R = int(R)
                G = int(G)
                B = int(B)
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
                Hue_araay_a.append(H)
                Value_array_a.append(V)
                Chroma_array_a.append(C)
                R_array.append(R)
                G_array.append(G)
                B_array.append(B)


            Hue_b+=sum(Hue_araay_a)/len(Hue_araay_a)
            Value_b+=sum(Value_array_a)/len(Value_array_a)
            Chroma_b+=sum(Chroma_array_a)/len(Chroma_array_a)
            av_R = sum(R_array)/len(R_array)
            av_G = sum(G_array)/len(G_array)
            av_B = sum(B_array)/len(B_array)


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
            elif foldername2 == "C":
                tk = 6
            
            
            #print("色相H10点平均",Hue_b)
            #print("明度V10点平均",Value_b)
            #print("彩度S10点平均",Chroma_b)
            Hue_araay_c.append(Hue_b)
            Value_araay_c.append(Value_b)
            Chroma_araay_c.append(Chroma_b)
            #エクセル用
            print(foldername,",",tk,",",Hue_b,",",Value_b,",",Chroma_b,",",av_R,",",av_G,",",av_B)


            #print(Hue_araay_c)
        """
        #3,4,5,C6の4回表示される
        #等級分の数のデータ Sx,Sy
        toukyu = [3,4,5]            # Sy
        H_siki = Hue_araay_c[0:3]   # Sx
        V_mei  = Value_araay_c[0:3] # Sx
        C_sai  = Chroma_araay_c[0:3]# Sx
        #データの平均
        t_av = sum(toukyu)/len(toukyu)
        H_av = sum(H_siki)/len(H_siki)
        V_av = sum(V_mei)/len(V_mei)
        C_av = sum(C_sai)/len(C_sai)
        #dataframeのための行列と、転置
        df=pandas.DataFrame([toukyu,H_siki,V_mei,C_sai])
        #df=pandas.DataFrame([toukyu,H_siki,V_mei,C_sai],index=["3","4","5"],columns=["等級","色相H","明度V","彩度C"])
        #print(df)
        df = df.T
        print(foldername)
        print(df)
        res=df.corr()   # pandasのDataFrameに格納される
        print(res)
        #print(np.cov(toukyu,H_siki,bias=True))
        #共分散Cxy
        kyoubunsan1 = np.cov(toukyu,H_siki,bias=True)[0,1]
        kyoubunsan2 = np.cov(toukyu,V_mei,bias=True)[0,1]
        kyoubunsan3 = np.cov(toukyu,C_sai,bias=True)[0,1]
        #print("共分散",kyoubunsan1)
        # Sy^2 Syの分散
        Sy_2_H=np.var(H_siki)
        Sy_2_V=np.var(V_mei)
        Sy_2_C=np.var(C_sai)
        #print(Sx_2)

        #y = ax + b のa
        aaaaa1 = kyoubunsan1 / Sy_2_H
        aaaaa2 = kyoubunsan2 / Sy_2_V
        aaaaa3 = kyoubunsan3 / Sy_2_C

        #y = ax + b のb
        bbbbb1 = t_av - (aaaaa1*H_av)   #xには色相Hを代入
        bbbbb2 = t_av - (aaaaa2*V_av)   #xには明度Vを代入
        bbbbb3 = t_av - (aaaaa3*C_av)   #xには彩度Cを代入

        print("等級と色相の回帰直線","y = ",aaaaa1,"x +",bbbbb1)
        print("等級と明度の回帰直線","y = ",aaaaa2,"x +",bbbbb2)
        print("等級と彩度の回帰直線","y = ",aaaaa3,"x +",bbbbb3)
        """
        
        #print("色相H等級平均",sum(Hue_araay_c)/len(Hue_araay_c))
        #print("明度V等級平均",sum(Value_araay_c)/len(Value_araay_c))
        #print("彩度S等級平均",sum(Chroma_araay_c)/len(Chroma_araay_c))



    #相関係数
