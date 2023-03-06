import os
import cv2
import numpy as np
import math

#旋转图像的函数
def rotate_image(src, angle, scale=1.):
    w = src.shape[1]
    h = src.shape[0]
    angle = -angle
    # 角度变弧度
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    # 仿射变换
    raw_result = cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
    convert_w = raw_result.shape[1]
    convert_h = raw_result.shape[0]
    if convert_w>convert_h:
        longer_side = convert_w
    else:
        longer_side = convert_h

    squre_mat = np.ones((longer_side, longer_side, 3), dtype="uint8")

    squre_mat[(longer_side-convert_h)//2:(longer_side+convert_h)//2,(longer_side-convert_w)//2:(longer_side+convert_w)//2] = raw_result
    rectify_result = squre_mat[(longer_side-h)//2:(longer_side+h)//2,(longer_side-w)//2:(longer_side+w)//2]
    return rectify_result

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


    # radius_obb = math.sqrt(math.pow(long_side/2,2)+math.pow(short_side/2,2))
    # a = cx + radius_obb
    # b = cx - radius_obb
    # c = cy + radius_obb
    # d = cy - radius_obb
    # if a<w and b>0 and c<h and d>0:
    #     return True
    # else:
    #     return False
    

#中心旋转obb映射
def convert_obb(object,angle,shape):
    w = shape[1]
    h = shape[0]
    cls = object[0]
    cx = object[1]*w
    cy = object[2]*h
    long_side = object[3]
    short_side = object[4]
    obb_angle = object[5]

    rad_angle = angle/180*math.pi

    center = [w/2,h/2]

    rad_angle = -rad_angle
    c_cx = ((cx-w/2)*math.cos(rad_angle)+(cy-h/2)*math.sin(rad_angle)+w/2)/w
    c_cy = (-(cx-w/2)*math.sin(rad_angle)+(cy-h/2)*math.cos(rad_angle)+h/2)/h

    #角度修正
    if obb_angle+angle>=180:
        result_angle = obb_angle+angle-180
    elif obb_angle+angle<0:
        result_angle = obb_angle+angle+180
    else:
        result_angle = obb_angle+angle

    result = [int(cls),c_cx,c_cy,long_side,short_side,int(result_angle)]
    if check_obb(result,shape):
        return result
    else:
        return 0

def img_rot(img_dir,label_dir,num_i):
    img_save_path = os.path.join(os.path.split(img_dir)[0],'images_rotated')
    label_save_path = os.path.join(os.path.split(label_dir)[0],'labels_rotated')
    if not os.path.exists(img_save_path):
        os.mkdir(img_save_path)
    if not os.path.exists(label_save_path):
        os.mkdir(label_save_path)
    
    list_img = os.listdir(img_dir)
    path_img = [os.path.join(img_dir, path) for path in list_img]
    count = 0
    for path in path_img:
        file_name = os.path.basename(path).replace('.jpg', '')  # 返回文件名
        print("processing %s [%d|%d]" % (file_name,count,len(path_img)))
        count+=1

        txt_path = file_name + '.txt'
        annot_path = os.path.join(label_dir, txt_path)

        if os.path.getsize(annot_path)==0:
            print('空文件，跳过\n')
            continue

        data_list = []
        with open(annot_path, encoding='utf-8') as fp:
            all_data = fp.readlines()
            for i in range(len(all_data)):
                tmp_list = []
                for object in all_data[i].split():
                    tmp_list.append(float(object))
                data_list.append(tmp_list)

        img = cv2.imread(path)
        # 图像旋转
        rotate_angles = np.arange(5,180,5)
        for rotate_angle in rotate_angles:
            num_i += 1

            #标注框转换
            convert_data_list = []
            for object in data_list:
                convert_data = convert_obb(object,rotate_angle,img.shape)
                if convert_data!=0:
                    convert_data_list.append(convert_data)

            txt_name = 'rotated_' + str(num_i) + '.txt'

            with open(os.path.join(label_save_path, txt_name), 'w') as fp:
                for obj in convert_data_list:
                    for i in range(6):
                        fp.write(str(obj[i]))
                        if i!=5:
                            fp.write(' ')
                    fp.write('\n')
                fp.close()

            # 只改变txt文件时可以注释掉下面三行
            img_square = rotate_image(img,rotate_angle)
            img_name = 'rotated_' + str(num_i) + '.jpg'
            cv2.imwrite(os.path.join(img_save_path, img_name), img_square)

if __name__ == '__main__':
    img_dir = r'D:\tower_data\new_hook\test_2classes\images_3'
    label_dir = r'D:\tower_data\new_hook\test_2classes\labels_3'
    #输出起始编号,添加类别时记得改
    num_i = 10000000

    # 图像旋转
    img_rot(img_dir, label_dir,num_i)