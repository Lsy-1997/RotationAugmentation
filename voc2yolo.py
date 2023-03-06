# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import getcwd
import shutil

from sqlalchemy import false

sets = ['train', 'val', 'test']
# classes = ["rhatperson","yhatperson","bhatperson","whatperson","nhatperson","car","digger","truck","concreteTruck","waterproof-1","waterproof-2","wood","stick","rebar","rebar-2","steelpipe","steel","steel-2","waterpipe","steelpillar","steelhoop","container","rubbish"]   # 改成自己的类别
classes = []
dataset_path = './test_2classes/rebar-3'
output_path = os.path.join(os.path.split(dataset_path)[0],'convert_result')

abs_path = os.getcwd()
print(abs_path)

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def convert_rotation_box(size, box):
    dw = 1. / (size[2])
    dh = 1. / (size[3])
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    angle = box[4]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    angle = int(angle * 180)
    return x, y, w, h, angle

def convert_annotation(image_set,image_id,rotation_box = false):
    in_file = open(dataset_path + '/Annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open(dataset_path +'/labels/%s.txt' % (image_id), 'w')
    output_label_path = os.path.join(output_path,image_set,'labels')
    

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        # difficult = obj.find('Difficult').text
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    out_file.close()
    shutil.copy(dataset_path +'/labels/%s.txt' % (image_id),output_label_path + '/%s.txt' % (image_id))

def get_classes(xml_path):
    xml_files = os.listdir(xml_path)
    for xml_file in xml_files:
        in_file = os.path.join(xml_path, xml_file)
        tree = ET.parse(in_file)
        root = tree.getroot()
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                classes.append(cls)
    print('classes = ')
    print(classes)
    print('nc = ' + str(classes.__len__()))

def gen_yaml():
    data_yaml = open(os.path.join(output_path,'data.yaml'),'w')
    data_yaml.write('train: ' + os.path.join(output_path, 'train','images')+'\n')
    data_yaml.write('val: ' + os.path.join(output_path, 'val','images')+'\n')
    data_yaml.write('\n')
    data_yaml.write('nc: ' + str(classes.__len__())+'\n')
    data_yaml.write('names: ' + str(classes)+'\n')
    data_yaml.close()

if __name__ == "__main__":

    get_classes(os.path.join(dataset_path,'Annotations'))

    for image_set in sets:
        if not os.path.exists(os.path.join(dataset_path, 'labels')):
            os.makedirs(os.path.join(dataset_path, 'labels'))
        image_ids = open(dataset_path + '/ImageSets/Main/%s.txt' % (image_set)).read().strip().split()
        list_file = open(dataset_path + '/%s.txt' % (image_set), 'w')
        for image_id in image_ids:
            list_file.write(abs_path + '/voc_dataset/images/%s.jpg\n' % (image_id))

            output_img_path = os.path.join(output_path,image_set,'images')
            output_label_path = os.path.join(output_path,image_set,'labels')
            if not os.path.exists(output_img_path):
                os.makedirs(output_img_path)

            if not os.path.exists(output_label_path):
                os.makedirs(output_label_path)

            shutil.copy(os.path.join(dataset_path,'images',image_id+'.jpg'),
                        os.path.join(output_img_path,image_id+'.jpg'))

            convert_annotation(image_set, image_id)
        list_file.close()
    gen_yaml()
    
    
