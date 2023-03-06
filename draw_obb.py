import os
import cv2

def draw_obb(objects,img,save_dir,file_save_name):
    for object in objects:
        w = img.shape[1]
        h = img.shape[0]
        cls = object[0]
        cx = object[1]*w
        cy = object[2]*h
        long_side = object[3]*w
        short_side = object[4]*h
        obb_angle = int(object[5])
        rect = ((cx, cy), (long_side, short_side), obb_angle-90)
        box = cv2.boxPoints(rect).astype(int)
        print(box)
        thickness = round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
        cv2.line(img, box[0], box[1], [255,255,0], thickness)
        cv2.line(img, box[1], box[2], [255,255,0], thickness)
        cv2.line(img, box[2], box[3], [255,255,0], thickness)
        cv2.line(img, box[3], box[0], [255,255,0], thickness)
    save_name = os.path.join(save_dir,file_save_name)
    cv2.imwrite(save_name,img)


def Test_draw_obb(imgs_dir,labels_dir,dst_dir):
    for root, dirs, files in os.walk(imgs_dir):
        for file in files:
            print("processing: %s" % file)
            img_path = os.path.join(root,file)
            txt_name = file.replace('.jpg','.txt')
            label_path = os.path.join(labels_dir,txt_name)
            img = cv2.imread(img_path)
            
            data_list = []
            with open(label_path, encoding='utf-8') as fp:
                all_data = fp.readlines()
                for i in range(len(all_data)):
                    tmp_list = []
                    for object in all_data[i].split():
                        tmp_list.append(float(object))
                    data_list.append(tmp_list)
            draw_obb(data_list,img,dst_dir,file)
                

if __name__ == '__main__':
    img_dir = r'D:\projects\python_simple_script\hook\train\images_symmetry'
    label_dir = r'D:\projects\python_simple_script\hook\train\labels_symmetry'
    img_save_path = r'D:\projects\python_simple_script\hook\train\test'

    Test_draw_obb(img_dir,label_dir,img_save_path)