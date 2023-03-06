import os

def remove_empty_file(img_dir,txt_dir):
    for root,dirs,files in os.walk(img_dir):
        count=0
        for file in files:
            file_base_name = os.path.basename(file)[:-4]
            img_path = os.path.join(img_dir,file)
            txt_path = os.path.join(txt_dir,file_base_name+'.txt')
            # if not os.path.exists(txt_path):
            #     os.remove(img_path)
            #     print("删除文件：%s:%d" % (file_base_name,count))
            size = os.path.getsize(txt_path)
            if size == 0:
                print("空文件：%s:%d" % (file_base_name,count))
                os.remove(img_path)
                os.remove(txt_path)
            count+=1

if __name__ == '__main__':
    img_dir = r"D:\tower_data\new_hook\test_2classes\images_rotated"
    txt_dir = r"D:\tower_data\new_hook\test_2classes\labels_rotated"

    remove_empty_file(img_dir,txt_dir)