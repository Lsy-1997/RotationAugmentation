from importlib.resources import path
from ntpath import join
import os
import random
import shutil
import math

from gevent import joinall

ratio_for_val = 0.1

def randomSplit(file_dir, train_class_dir, valid_class_dir, ratio):

    path_dir = os.listdir(file_dir)
    filenumber = len(path_dir)
    picknumber = math.ceil(filenumber*ratio)
    val_imgs = random.sample(path_dir, picknumber)

    train_imgs = []
    for i in path_dir:
        if i not in val_imgs:
            train_imgs.append(i)

    for name in val_imgs:
        img_path = os.path.join(file_dir, name)
        tar_path = os.path.join(valid_class_dir, name)
        shutil.copy(img_path, tar_path)

    if train_imgs != []:
        for name in train_imgs:
            img_path = os.path.join(file_dir, name)
            tar_path = os.path.join(train_class_dir, name)
            shutil.copy(img_path, tar_path)


def main(root_path):
    dir_list = os.listdir(root_path)
    train_dir = os.path.join(os.path.dirname(root_path), 'train')
    valid_dir = os.path.join(os.path.dirname(root_path), 'val')

    if os.path.exists(train_dir) == False:
        os.mkdir(train_dir)
    if os.path.exists(valid_dir) == False:
        os.mkdir(valid_dir)

    for dir in dir_list:
        dir_path = os.path.join(root_path, dir)
        dir_name = os.path.basename(dir_path)

        train_class_dir = os.path.join(train_dir, dir_name)
        valid_class_dir = os.path.join(valid_dir, dir_name)

        if os.path.exists(train_class_dir) == False:
            os.mkdir(train_class_dir)
        if os.path.exists(valid_class_dir) == False:
            os.mkdir(valid_class_dir)

        randomSplit(dir_path, train_class_dir, valid_class_dir, ratio_for_val)


if __name__ == '__main__':
    root_path = r"D:/20220225/022513/data_set/src"
    main(root_path)
