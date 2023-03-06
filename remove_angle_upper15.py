import os 
import cv2

def remove_hook(txt_dir,txt_save_dir):
    for root,dirs,files in os.walk(txt_dir):
        count=0
        for file in files:
            txt_path = os.path.join(txt_dir,file)
            data_list = get_data_list(txt_path)

            convert_result = []
            for object in data_list:
                if object[0] != 2:
                    convert_result.append(object)
                else:
                    print('find %d hook and remove' % count)
            save_path = os.path.join(txt_save_dir,file)
            write_and_save_txt(convert_result,save_path)

def remove_angle_upper15(img_dir,txt_dir):
    for root,dirs,files in os.walk(img_dir):
        count=0
        for file in files:
            file_base_name = os.path.basename(file)[:-4]
            img_path = os.path.join(img_dir,file)
            txt_path = os.path.join(txt_dir,file_base_name+'.txt')

            file_num = int(file_base_name[-4:])
            cls = int(file[8])
            if file_num%35>3 or file_num%35==0 and cls == 3:
                os.remove(img_path)
                os.remove(txt_path)

            count+=1

def get_data_list(txt_abs_path):
    data_list = []
    with open(txt_abs_path, encoding='utf-8') as fp:
        all_data = fp.readlines()
        for i in range(len(all_data)):
            tmp_list = []
            for object in all_data[i].split():
                tmp_list.append(float(object))
            data_list.append(tmp_list)
    return data_list

def write_and_save_txt(data_list, txt_save_path):
    for object in data_list:
        object[0] = int(object[0])
        object[5] = int(object[5])
    with open(txt_save_path, 'w') as f:
        for obj in data_list:
            for i in range(6):
                f.write(str(obj[i]))
                if i!=5:
                    f.write(' ')
            f.write('\n')

def horizontal_symmetry(img_dir,txt_dir,img_save_dir,txt_save_dir):
    for root,dirs,files in os.walk(img_dir):
        count=0
        for file in files:
            file_base_name = os.path.basename(file)[:-4]
            img_path = os.path.join(img_dir,file)
            txt_path = os.path.join(txt_dir,file_base_name+'.txt')

            img = cv2.imread(img_path)
            img_symmetry = cv2.flip(img,1)
            
            img_save_name = 'sym_' + file
            img_save_path = os.path.join(img_save_dir,img_save_name)
            cv2.imwrite(img_save_path,img_symmetry)

            data_list = get_data_list(txt_path)
            
            #标注框转换
            convert_data_list = []
            for object in data_list:
                object[1] = str(1 - float(object[1]))
                if object[5]!=0:
                    object[5] = 180 - object[5]
                convert_data_list.append(object)

            txt_save_name = 'sym_' + file_base_name+'.txt'
            txt_save_path = os.path.join(txt_save_dir, txt_save_name)
            write_and_save_txt(convert_data_list,txt_save_path)
            
                

if __name__ == '__main__':
    img_dir = r"hook\train\images_rotated"
    txt_dir = r"D:\tower_data\new_hook\test_2classes\rebar-3_stick_hook\labels_include_hook\val"
    img_save_dir = r"hook\train\images_symmetry"
    txt_save_dir = r"D:\tower_data\new_hook\test_2classes\rebar-3_stick_hook\labels\val"

    remove_hook(txt_dir,txt_save_dir)
    # horizontal_symmetry(img_dir,txt_dir,img_save_dir,txt_save_dir)
    # remove_angle_upper15(img_dir,txt_dir)