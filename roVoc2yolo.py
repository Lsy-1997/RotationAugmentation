# -*- coding: utf-8 -*-
from cmath import pi
import xml.etree.ElementTree as ET
import os
import shutil

classes = []
xml_dir = r'D:\tower_data\新吊钩数据\test_2classes\labels_xml'
output_path = os.path.join(os.path.split(xml_dir)[0],'convert_result')

def convert_rotation_box(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    angle = box[4]

    x = x * dw
    y = y * dh

    if w>h:
        long_side = w
        short_side = h
    else:
        long_side = h
        short_side = w
 
    long_side = long_side * dw
    short_side = short_side * dh

    if h>w:
        angle = int(angle/pi * 180)
    else:
        if angle/pi*180<90:
            angle = int(angle/pi*180+90)
        else:
            angle = int(angle/pi*180-90)
    return x, y, long_side, short_side, angle

def convert_robox_annotation(xml_file_path):
    in_file = open(xml_file_path, encoding='UTF-8')
    xml_file_name = os.path.basename(xml_file_path[:-4])
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    out_file = open(output_path +'/%s.txt' % (xml_file_name), 'w')    

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('robndbox')
        b = (float(xmlbox.find('cx').text), float(xmlbox.find('cy').text), float(xmlbox.find('w').text),
             float(xmlbox.find('h').text), float(xmlbox.find('angle').text))
        bb = convert_rotation_box((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    out_file.close()

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

    get_classes(xml_dir)

    for root,dir,files in os.walk(xml_dir):
        for file in files:
            file_abs_path = os.path.join(root,file)
            convert_robox_annotation(file_abs_path)

    gen_yaml()
    
    
