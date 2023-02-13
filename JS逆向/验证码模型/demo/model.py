# import tensorflow as tf
from tensorflow.keras import Sequential,layers,models
from tensorflow import keras
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import img_to_array,load_img

def captcha_cnn():
    if os.path.exists('cnn_model.h5'):
        print(f'已存在model,加载model中..........')
        model = models.load_model('cnn_model.h5')
    else:
        model = Sequential()
        model.add(layers.Conv2D(32, kernel_size=(3, 3),activation='relu'))
        model.add(layers.MaxPool2D(pool_size=(2, 2)))
        model.add(layers.Conv2D(64, (3, 3),activation='relu'))
        model.add(layers.MaxPool2D())
        model.add(layers.Dropout(rate=0.25))
        model.add(layers.Conv2D(64, (3, 3),activation='relu'))
        model.add(layers.MaxPool2D())
        model.add(layers.Flatten())
        model.add(layers.Dense(128))
        model.add(layers.Dropout(rate=0.5))
        model.add(layers.Dense(36,activation='softmax'))
    model.compile(optimizer='Adam',
                  metrics=['accuracy'],
                  loss='categorical_crossentropy')
    return model

def split_img(train_image, img_nums):
    """
        返回数组形式的数据集x和数据集y
    """
    img_filenames = os.listdir(train_image)
    x_list = []
    y_list = []
    for img_filename in img_filenames:
        img = load_img(train_image+img_filename, color_mode='grayscale')
        img_array = img_to_array(img)
        x_list.append(img_array)
        temp = []
        for i in range(img_nums):    
            if img_filename[i].isdigit():
                temp.append(img_filename[i])
            elif img_filename[i].islower():
                num = int(ord(img_filename[i])) - int(ord('a')) + 10  # 10 是10个数字的长度
                temp.append(str(num))
            else:
                num = int(ord(img_filename[i])) - int(ord('A')) + 10  # 10 是10个数字的长度
                temp.append(str(num))
        temp = keras.utils.to_categorical(temp, num_classes=36)
        y_list.append(temp)
        # img_rows, img_cols, _ = img_array.shape
        # step = img_cols // img_nums
        # for i in range(img_nums):    
        #     x_list.append(img_array[:, i * step:(i + 1) * step] / 255)
        #     if img_filename[i].isdigit():
        #         y_list.append(img_filename[i])
        #     elif img_filename[i].islower():
        #         num = int(ord(img_filename[i])) - int(ord('a')) + 10  # 10 是10个数字的长度
        #         y_list.append(str(num))
        #     else:
        #         num = int(ord(img_filename[i])) - int(ord('A')) + 10  # 10 是10个数字的长度
        #         y_list.append(str(num))
        # print(img_filename)
        # break
    # y_list = keras.utils.to_categorical(y_list, num_classes=36)
    return x_list, y_list

    
def train_model():
    img_nums = 5        #验证码个数
    train_image="./train_pic/"  #训练图片的路径
    x_list, y_list = split_img(train_image, img_nums)  #切分数据集 
    x_train, x_val, y_train, y_val = train_test_split(x_list, y_list)   #训练集分为train和val
    model = captcha_cnn()     #训练模型
    model.fit(np.array(x_train), np.array(y_train), batch_size=32, epochs=10, verbose=1, validation_data=(np.array(x_val), np.array(y_val)))
    model.save('cnn_model.h5')      #保存模型


def predit_model():
    img_nums = 5        #验证码个数
    train_image="./test_pic/"  #训练图片的路径
    x_list, y_list = split_img(train_image, img_nums)  #切分数据集 
    # x_list = np.expand_dims(np.array(x_list), axis=0)
    model = captcha_cnn()     #训练模型
    pre_list = model.predict(np.array(x_list))
    y_pre = np.argmax(pre_list, axis=-1)
    y_true = np.argmax(y_list, axis=-1)
    print(y_pre,y_true)
    print()

train_model()