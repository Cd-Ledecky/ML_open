#-*- coding: utf-8 -*-

#前提
#教師、検証、テストデータに分けられた学習データがすでにある

#このプログラムの配置場所
#このフォルダ1を開くと、test,validation,testがあるフォルダ2があるような
#フォルダ1と同じディレクトリに配置
#test,validation,test を含むフォルダ1と、同じフォルダに配置
#   もちろんそのtest,validation,test中には1,2,3,4,5というようなクラスフォルダがあり、
#   その中には分割された学習データがある


from __future__ import absolute_import, division, print_function, unicode_literals
import os, time
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.preprocessing.image import img_to_array, load_img
print("TensorFlow version:", tf.__version__)
print("Keras version:", keras.__version__)

#新しいヴァージョンがあるとの警告がされる場合があるが、問題ない
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.compat.v1.Session(config=config)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# 参考 「pythonとkerasによるディープラーニング」


#引数   元データのパス、画像の大きさ
def image_network_train(learn_data_path, image_size):
    #教師、検証、テストデータのパス
    train_dir = os.path.join(learn_data_path, 'train')
    validation_dir = os.path.join(learn_data_path, 'validation')
    test_dir = os.path.join(learn_data_path, 'test')

    # カテゴリー数の計算
    num_category = 0
    for dirpath, dirnames, filenames in os.walk(train_dir):
        for dirname in dirnames:
            num_category += 1

    # 画像の大きさは 299*299 or 598*598、転移学習のモデルに合わせるため固定

    # batch size 
    batch_size = 8

    # すべての画像を1/255でリスケールする
    train_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    validation_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    test_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

    #クラス分類は"categorical"
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical')

    validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical')

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(image_size, image_size),
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False)

    # 事前に学習させた畳み込みNN(転移学習モデル)からベースモデルを作成します。
    IMG_SHAPE = (image_size, image_size, 3)

    # 転移学習のモデルを選択
    # model :xception
    base_model = keras.applications.xception.Xception(input_shape=IMG_SHAPE,
                                                      include_top=False,
                                                      weights='imagenet')

    # 畳み込みNNの凍結(重みの固定)  False=固定しない
    base_model.trainable = False

    # モデル
    # 活性化関数の指定
    model = keras.Sequential([
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(num_category, activation='softmax')
    ])

    # モデルのコンパイル
    # 学習率、損失関数、評価関数、の指定
    model.compile(optimizer=keras.optimizers.Adam(lr=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # early stopping
    # 学習して、5回連続で損失が下がらなかったら、学習を停止する
    es = keras.callbacks.EarlyStopping(monitor='val_loss',
                                       patience=5,
                                       restore_best_weights=True)

    #表示
    print("\ntraining sequence start .....")

    #表示
    print("\nwarm up sequence .....")

    #学習モデルの表示
    model.summary()

    # 更新される重みの数
    print('after', len(model.trainable_weights))

    # Train the model   モデルの学習
    #エポックの設定
    epochs = 40
    steps_per_epoch = train_generator.n // batch_size
    validation_steps = validation_generator.n // batch_size
    test_steps = test_generator.n // batch_size

    start = time.time()
    history = model.fit_generator(train_generator,
                                  steps_per_epoch=steps_per_epoch,
                                  epochs=epochs,
                                  workers=4,
                                  validation_data=validation_generator,
                                  validation_steps=validation_steps,
                                  callbacks=[es],
                                  verbose=2)

    _val_pred = model.evaluate_generator(validation_generator,
                                         steps=validation_steps)
    print('val loss: {}, val acc: {}'.format(_val_pred[0], _val_pred[1]))


    # Fine tuning   ファインチューニング
    print("\nfine tuning.....")
    # モデルのトップ層の凍結解除
    base_model.trainable = True

    # ベースモデル中の層の数
    print("Number of layers in the base model: ", len(base_model.layers))

    # Fine tune from this layer onwards 微調整
    fine_tune_at = 108

    # ファインチューニングの前に層の重みを凍結するか `fine_tune_at` layer
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    # より低い学習率でモデルをコンパイルする
    # lr=learning rate の指定   先ほどよりも小さく
    model.compile(optimizer = keras.optimizers.Adam(lr=2e-5),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.summary()

    # 更新される重みの数
    print('after Fine tune', len(model.trainable_weights))

    # モデルの学習の続行
    history_fine = model.fit_generator(train_generator,
                                       steps_per_epoch=steps_per_epoch,
                                       epochs=epochs,
                                       workers=4,
                                       validation_data=validation_generator,
                                       validation_steps=validation_steps,
                                       callbacks=[es],
                                       verbose=2)
    elapsed_time = time.time() - start
    print( "elapsed time (for train): {} [sec]".format(time.time() - start) )

    # print(history_fine.history)
    model_val_acc = history_fine.history['val_accuracy'][-1]
    print( 'val_acc: ', model_val_acc )

    # モデルを hdf5 ファイルで保存 ----------
    """ mulSampleの目的は検証なので、モデルファイルは通常保存しない
    base_dir, dataset_name = os.path.split(LEARN_PATH)
    base_dir, n_class = os.path.split(base_dir)
    save_file = '{}.h5'.format(dataset_name)
    save_location = os.path.join(os.path.dirname(os.getcwd()), "outputs",
                                 n_class, "models", str(image_size),
                                 save_file)
    model.save(save_location)
    print("\nmodel has saved in", save_location)
    """


    print("\nevaluate messages below ...")
    # val_pred = model.evaluate_generator(validation_generator,
    #                                     steps=validation_steps)
    # print('val loss: {}, val acc: {}'.format(val_pred[0], val_pred[1]))

    test_pred = model.evaluate_generator(test_generator,
                                         steps=test_steps)
    print('Test loss: {}, Test acc: {}'.format(test_pred[0], test_pred[1]))

    # confusion matrix & each class accuracy -----
    #正解率の表示
    print("\nconfusion matrix")
    cm_pred = model.predict_generator(test_generator,
                                      steps=test_steps,
                                      verbose=2)

    test_label = []
    for i in range(test_steps):
        _, tmp_tl = next(test_generator)
        if i == 0:
            test_label = tmp_tl
        else:
            test_label = np.vstack((test_label, tmp_tl))

    idx_label = np.argmax(test_label, axis=-1)  # one_hot => normal
    idx_pred = np.argmax(cm_pred, axis=-1)  # 各 class の確率 => 最も高い値を持つ class

    cm = confusion_matrix(idx_label, idx_pred)
    print(cm)

    # each class accuracy -----
    print("\neach class accuracy")
    bunbo = np.sum(cm, axis=1) 

    for i in range( len(cm) ):
        cls_acc = cm[i][i] / bunbo[i]
        print( "  class {} acc: {}".format(i, cls_acc) )

    # Calculate Precision and Recall
    # print(classification_report(idx_label, idx_pred))

    return test_pred[1], cm



if __name__ == '__main__':
    # if __name__ == '__main__':
    # このプログラムを直接実行した場合のみ以下を実行する
    # 他のプログラムからこのプログラムが実行された場合は、以下を実行しない

    # configuration -----
    # クラス数
    n_class = 5  
    experiment = "bg_experiment"

    # experiment = "protoBG"
    # split = "horizontal"  # horizontal or cross

    dataset_list = ["299299"]
    #このフォルダを開くと、test,validation,testがあるフォルダを指定
    #["withBG","noBG"]として一気に複数の実行することもできる

    #画像の入力サイズ
    IMAGE_SIZE = 299  # 299 or 598


    test_acc_list = np.zeros( len(dataset_list) )
    collect_list = np.zeros( (n_class, len(dataset_list)) )
    # print("test_acc_list shape:", test_acc_list.shape)
    # print("collect_list shape:", collect_list.shape)

    for i, dataset_name in enumerate(dataset_list):
        print("\n>>>>> {} times: use {} <<<<<".format(i+1, dataset_name))

        print(os.getcwd())
        if experiment == "bg_experiment":
            LEARN_PATH = os.path.join(os.path.dirname(os.getcwd()),"data20210315_299299_seed5000","299299")
            # ↑このプログラムを含んでいるフォルダへのパス
            #os.getcwd()) はこのプログラムを含むフォルダ1が含まれているフォルダ2へのパスを得る。
            #   なので続けてフォルダ1,学習データフォルダ[train,vali,test]を指定する
            # dataset_nameは例えばp_size_299299withBACK160のこと
            # LEARN_PATH = r"C:\Users\name\Desktop\learn20200513\hogehoge"
            #os.path.dirname(os.getcwd())は、このプログラムがあるディレクトリ
            print("★★★★★★",LEARN_PATH)
        elif experiment == "prptpBG":
            LEARN_PATH = os.path.join(os.path.dirname(os.getcwd()), "datasets",
                                      experiment, "{}class".format(n_class),
                                      split, dataset_name)
        print(LEARN_PATH, os.path.exists(LEARN_PATH))


        test_acc, cm = image_network_train(LEARN_PATH, IMAGE_SIZE)

        print("-> return test accuracy:", test_acc)
        test_acc_list[i] = test_acc

        for j in range(len(cm)):
            collect_list[j][i] = cm[j][j]
            # print(cm)
            # print(collect_list)
        

    print( "Each condition test accuracy:" )
    print( test_acc_list )

    print( "Each class collect classified pictures:" )
    for i in range(n_class):
        ave_collect_num = sum(collect_list[i])/len(dataset_list)
        print( "class{} collect picture:".format(i) )
        print( collect_list[i] )
