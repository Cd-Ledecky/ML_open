# # -*- coding: utf-8 -*-
# 各クラスの画像を {train / validaiton / test} フォルダにわける

import os, shutil
import numpy as np
np.random.seed(seed=1000)

# get project root path ----------
cwd = os.getcwd()
datasets_dir = os.path.dirname(cwd)
print(datasets_dir)
# このプログラムが置いてあるフォルダの1つ前のディレクトリになっている
#/home/NAME/MONO_project/datasets

sep_char = os.sep  
rsep_dirpath = cwd.split(sep_char)

""" get project root (MONO_project directory) """
prj_root = sep_char
for fold in rsep_dirpath:
    prj_root = os.path.join(prj_root, fold)
    # print(prj_root, os.path.exists(prj_root))
    
    if "MONO_project" in fold:
        break


""" dataset attributes """
all_cls_list = ["1","2","3","4","5"]
division_list = ["train", "validation", "test"]



def dlist_sieve(dlist):
    """ remove systemfiles utility
        # Args:
            dlist (list): list of files
        # Returns:
            dlist (list): sieved and sorted list
    """

    ignore_list = [".DS_Store", "__pycache__"]

    for igfile in ignore_list:
        if igfile in dlist:
            dlist.remove(igfile)

    return sorted(dlist)



def search(origin_data_src, cls_list=all_cls_list):
    """ fetch all class's file list
        # Args:
            origin_data_src (str): directory path where data-source exists
            cls_list (list): list of classes name
        # Returns:
            None (print each class's files and amount)
    """

    print("\nSearching ... \n")

    for kanri in ["1","2","3","4","5"]:
        for tokyu in chosen_cls_list:
            # set target_path 
            target_path = os.path.join(origin_data_src, kanri,tokyu)
            print("set target_path:", target_path)
            #tokyuの下にBACK30,,,170とかがある

            #★★★★★★
            for pname in percentage_list:
                cls_dir = os.path.join(target_path, pname)
                #print(cls_dir)

                data_list = os.listdir(cls_dir)
                # cls_dir下にあるファイルやフォルダ一覧
                data_list = dlist_sieve(data_list)
                #print(data_list)

                print("  amount: ", len(data_list))
                # assert (len(data_list) % 20) == 0




def separate(origin_data_src, chosen_cls_list, dataset_name, sep_rate, par_dir=None):
    #dataset_name は8:1:1をまとめたフォルダの名前（新しく作成する）
    """ make dataset with the classes you specify

        # Args:
            origin_data_src (str): directory path where data-source exists
            chosen_cls_list (list): list of classes name that you want to specify
            dataset_name (str): dataset name
            sep_rate (dict): dictionary that have {train, validation, test} rate
            par_dir (str): directory path that you want to save dataset
                default: None
                    => save under `MONO_project/datasets/nclass/dataset_name`

        # Returns:
            None
                copy each class's images from origin data
                and distribute in train /validation / test
    """

    # process of while specify save directory -----
    if par_dir == None:
        par_dir = datasets_dir
        # #/home/NAME/MONO_project/datasets

        n_cls = len(chosen_cls_list)
        print("\nmake {0}class dataset named `{1}`.".format(n_cls, dataset_name))
        n_cls_dir = os.path.join(datasets_dir, "{}class".format(n_cls))
        os.makedirs(n_cls_dir, exist_ok=True)
        #このプログラムがおかれているフォルダと同じディレクトリに新しいフォルダをつくる

        dataset_dir = os.path.join(n_cls_dir, dataset_name)
        # 4class => sample0809
        os.makedirs(dataset_dir, exist_ok=False)  # 重複して作成は行わない
        #{}classフォルダの下にseparateの3つめの引数の名前のフォルダをつくる
        # 4classの下にdataset_dir = sample0809 フォルダを作る
    else:
        dataset_dir = os.path.join(par_dir, dataset_name)
        os.makedirs(dataset_dir, exist_ok=False)

    # main process ----------
    for kanri in ["1","2","3","4","5"]:
        for tokyu in chosen_cls_list:
            target_path = os.path.join(origin_data_src, kanri,tokyu)
            print("set target_path:", target_path)
            
            
            for pname in percentage_list:
                cls_dir = os.path.join(target_path, pname)
                #print(cls_dir)

                data_list = os.listdir(cls_dir)
                data_list = dlist_sieve(data_list)
                #print(data_list)

                cls_amount = len(data_list)

                print("  amount: ", cls_amount)
                #assert (cls_amount % 20) == 0

                # make datasets -----
                for purpose in division_list:
                    n_pics = int(cls_amount * sep_rate[purpose])
                    print("  {0} picture amount: {1}".format(purpose, n_pics))
                    picture_list = np.random.choice(data_list, n_pics, replace=False)
                    print("picture list", picture_list)

                    purpose_dir = os.path.join(dataset_dir,pname,purpose,kanri)
                    os.makedirs(purpose_dir, exist_ok=True)
                    #dataset_dir = os.path.join(n_cls_dir, dataset_name)
                    # /......4class => sample0809 => p_size_299299withBACK50=>test(train,vali) => MONO_1 

                    for pic in picture_list:
                        #ランダムに選択したMONO2-BACK30の画像を
                        src_file = os.path.join(cls_dir, pic)

                        dist = os.path.join(purpose_dir, pic)
                        shutil.copy(src_file, dist)
                        # print(src_file, os.path.exists(src_file))
                        # /......4class => sample0809 => p_size_299299withBACK50=>test(train,vali) => MONO_2
                        #に保存

                        data_list.remove(pic)
                        #?????

                    print("data_list:", data_list, len(data_list))

        print("    Dataset has correctly made.")


def makeMul(origin_data_src, n, chosen_cls_list, dataset_name, sep_rate, seeds):
    """ make some datasets with the classes you specify

        # Args:
            origin_data_src (str): directory path where data-source exists
            n (int): the number of dataset you want to create
            chosen_cls_list (list): list of classes name that you want to specify
            dataset_name (str): dataset name
            sep_rate (dict): dictionary that have {train, validation, test} rate
            seeds (list): list of seed-value
                each seed value will be used chose what image destribute in
                train / validation / test
                default: None
                    => generate 5times random int in [0, 1000]

        # Returns:
            None
                copy each class's images from origin data
                and distribute in train /validation / test
                repeat in `n` times.
    """

    n_cls = len(chosen_cls_list)
    print("\nmake {0}class dataset named `{1}`.".format(n_cls, dataset_name))
    n_cls_dir = os.path.join(datasets_dir, "{}class".format(n_cls))
    os.makedirs(n_cls_dir, exist_ok=True)
    #cwd = os.getcwd()
    #datasets_dir = os.path.dirname(cwd)


    cover_dir = os.path.join(n_cls_dir, "mulSample", dataset_name)
    os.makedirs(cover_dir, exist_ok=False)  # 重複して作成は行わない

    for i in range(n):
        if seeds == None:
            seed_val = np.random.randint(0, 1000)
        else:
            seed_val = seeds[i]
        print("\n{} times: set np.random.seed(seed={})".format(i, seed_val))
        np.random.seed(seed=seed_val)
        separate(origin_data_src, chosen_cls_list, "{0}_{1}".format(dataset_name, i),
                 sep_rate, cover_dir)
    


if __name__ == "__main__":

    #origin4のうちで、学習したいフォルダを選択複数可
    percentage_list = ["299299"]


    # set configuration -----
    date = "final1"  # 20200218 or 20200225

    # define where original data source
    origin_data_src = os.path.join(datasets_dir, "data20210315", date)
    print("original data source: ", origin_data_src)


    # print all pictures list
    # search(origin_data_src)

    
    # set some configuration -----
    #chosen_cls_list = ["MONO_1", "MONO_5"]  # 2class
    chosen_cls_list = ["cropped"]  # 3class
    sep_rate = {"train":0.8, "validation":0.1, "test":0.1}


    # conferm what file devides
    search(origin_data_src, chosen_cls_list)


    # make dataset -----
    #良ければ、以下のコメントを外して分ける
    #１つしか作らない場合のseedは114
    separate(origin_data_src, chosen_cls_list, "97977979", sep_rate)

    # make Multi dataset -----
    # 乱数を変えて、データセットを5個作る
    seeds = [4000, 5000]
    makeMul(origin_data_src, 2, chosen_cls_list, "multi_20210315", sep_rate, seeds)
    #                        ↑seedsのリストの個数と合わせる
