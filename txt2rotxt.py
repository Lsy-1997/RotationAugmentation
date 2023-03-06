#普通yolo数据转旋转框yolo数据 txt格式
import os
from numpy import save

from sympy import im

def txt2rotxt(txt_path,save_path):
    img_shape = [1920,1080]
    for root,dirs,files in os.walk(txt_path):
        for file in files:
            txt_abs_path = os.path.join(txt_path,file)
            data_list = []
            with open(txt_abs_path,'r') as f:
                all_data = f.readlines()
                for object in all_data:
                    tmp_list = []
                    for data in object.split():
                        tmp_list.append(data)
                    w = float(tmp_list[3])*img_shape[0]
                    h = float(tmp_list[4])*img_shape[1]

                    #标注吊钩框的w一定小于h
                    short_side = w/img_shape[1]
                    long_side = h/img_shape[0]
                    
                    #添加角度
                    angle = '0'
                    tmp_list.append(angle)

                    #更改类别和长短边
                    tmp_list[0] = '2'
                    tmp_list[3] = str(long_side)
                    tmp_list[4] = str(short_side)
                    print(tmp_list)
                    data_list.append(tmp_list)
            txt_save_abs_path = os.path.join(save_dir,file)
            with open(txt_save_abs_path,'w') as f:
                for object in data_list:
                    for i in range(6):
                        f.write(object[i])
                        if i!=5:
                            f.write(' ')
                        else:
                            f.write('\n')

if __name__ == '__main__':
    txt_dir = r'hook\train\labels'
    save_dir = r'hook\train\ro_labels'
    
    txt2rotxt(txt_dir,save_dir)
