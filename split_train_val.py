# coding:utf-8

import os
import random
import argparse
import shutil

root = './dataset/new_dataset'
files = os.listdir(root)
output_path = os.path.join(root,'yolo_dataset')
img_path = os.path.join(output_path,'images')
ImageSets_Main_path = os.path.join(output_path,'ImageSets','Main')
anno_path = os.path.join(output_path,'Annotations')
if not os.path.exists(img_path):
    os.makedirs(img_path)
if not os.path.exists(ImageSets_Main_path):
    os.makedirs(ImageSets_Main_path)
if not os.path.exists(anno_path):
    os.makedirs(anno_path)

for file in files:
    if file.endswith('.jpg'):
        file_abs_path = os.path.join(root,file)
        file_output_path = os.path.join(img_path,file)
        shutil.copy(file_abs_path, file_output_path)
    if file.endswith('.xml'):
        file_abs_path = os.path.join(root,file)
        file_output_path = os.path.join(anno_path,file)
        shutil.copy(file_abs_path, file_output_path)
        


parser = argparse.ArgumentParser()
#xml文件的地址，根据自己的数据进行修改 xml一般存放在Annotations下
parser.add_argument('--xml_path', default=anno_path, type=str, help='input xml label path')
#数据集的划分，地址选择自己数据下的ImageSets/Main
parser.add_argument('--txt_path', default=ImageSets_Main_path, type=str, help='output txt label path')
opt = parser.parse_args()

trainval_percent = 1.0
train_percent = 0.9
xmlfilepath = opt.xml_path
txtsavepath = opt.txt_path
total_xml = os.listdir(xmlfilepath)
if not os.path.exists(txtsavepath):
    os.makedirs(txtsavepath)

num = len(total_xml)
list_index = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list_index, tv)
train = random.sample(trainval, tr)

file_trainval = open(txtsavepath + '/trainval.txt', 'w')
file_test = open(txtsavepath + '/test.txt', 'w')
file_train = open(txtsavepath + '/train.txt', 'w')
file_val = open(txtsavepath + '/val.txt', 'w')

for i in list_index:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        file_trainval.write(name)
        if i in train:
            file_train.write(name)
        else:
            file_val.write(name)
    else:
        file_test.write(name)

file_trainval.close()
file_train.close()
file_val.close()
file_test.close()
