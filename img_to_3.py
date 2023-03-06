import cv2
import numpy as np
import os
import math
import copy

#检查obb是否越界，（待优化）
def check_obb(object,shape):
    w = shape[1]
    h = shape[0]
    cls = object[0]
    cx = object[1]*w
    cy = object[2]*h
    long_side = object[3]*w
    short_side = object[4]*h
    obb_angle = object[5]

    rect = ((cx, cy), (long_side, short_side), obb_angle-90)
    box = cv2.boxPoints(rect).astype(int)
    
    for i in range(4):
        if box[i][0]<0 or box[i][0]>w or box[i][1]<0 or box[i][1]>h:
            return False
    
    return True

def convert_obb(object,shape,num):
    w = shape[1]
    h = shape[0]
    cls = object[0]
    cx = object[1]*w
    cy = object[2]*h
    long_side = object[3]*w
    short_side = object[4]*h
    obb_angle = object[5]
    object[0] = int(object[0])
    object[5] = int(object[5])

    if num==0:
        object[1] = cx/min(w,h)
        object[3] = long_side/min(w,h)
        object[4] = short_side/min(w,h)
        return object
    elif num==1:
        new_cx = cx - (w//2-h//2)
        new_cx = new_cx/min(w,h)
        object[1] = new_cx
        object[3] = long_side/min(w,h)
        object[4] = short_side/min(w,h)
        return object
    elif num==2:
        new_cx = cx - (w-h)
        new_cx = new_cx/min(w,h)
        object[1] = new_cx
        object[3] = long_side/min(w,h)
        object[4] = short_side/min(w,h)
        return object

def img_to_3(img_dir,txt_dir):
    #创建save文件夹
    img_save_path=os.path.join(os.path.split(img_dir)[0],'images_3')
    label_save_path=os.path.join(os.path.split(txt_dir)[0],'labels_3')
    if not os.path.exists(img_save_path):
        os.mkdir(img_save_path)
    if not os.path.exists(label_save_path):
        os.mkdir(label_save_path)

    for root,dirs,files in os.walk(img_dir):
        for file in files:
            file_no_suffix = file[:-4]
            print('processing ' + file_no_suffix)
            img = cv2.imread(os.path.join(img_dir,file))
            w = img.shape[1]
            h = img.shape[0]

            #将图片一分为三
            square_side = min(w,h)
            square_mat = [[],[]]*3

            square_mat[0] = np.ones((square_side, square_side, 3), dtype="uint8")
            square_mat[1] = np.ones((square_side, square_side, 3), dtype="uint8")
            square_mat[2] = np.ones((square_side, square_side, 3), dtype="uint8")
            square_mat[0][:,:] = img[0:square_side,0:square_side]
            square_mat[1][:,:] = img[0:square_side,w//2-square_side//2:w//2+square_side//2]
            square_mat[2][:,:] = img[0:square_side,-square_side:]

            for i in range(3):
                save_name = file_no_suffix + '_' + str(i) + '.jpg'
                save_name = os.path.join(img_save_path, save_name)
                cv2.imwrite(save_name,square_mat[i])

            #标注框坐标修改
            txt_path = os.path.join(txt_dir,file_no_suffix+'.txt')
            
            data_list = []
            with open(txt_path,'r') as fp:
                data_all=fp.readlines()
                for i in range(len(data_all)):
                    tmp_list = []
                    for object in data_all[i].split():
                        tmp_list.append(float(object))
                    data_list.append(tmp_list)

            convert_data_list = [[],[],[]]

            for i in range(3):
                for object in data_list:
                    #使用深拷贝防止原始数据改变
                    object_copy = copy.deepcopy(object)
                    convert_data = convert_obb(object_copy,img.shape,i)
                    if check_obb(convert_data,[square_side,square_side]):
                        convert_data_list[i].append(convert_data)
            
            for i in range(3):
                with open(os.path.join(label_save_path,file_no_suffix+'_'+str(i)+'.txt'),'w') as fp:
                    for obj in convert_data_list[i]:
                        for i in range(6):
                            fp.write(str(obj[i]))
                            if i!=5:
                                fp.write(' ')
                        fp.write('\n')


if __name__ == '__main__':
    img_dir = r'D:\tower_data\new_hook\test_2classes\images'
    label_dir = r'D:\tower_data\new_hook\test_2classes\labels'

    img_to_3(img_dir,label_dir)
    