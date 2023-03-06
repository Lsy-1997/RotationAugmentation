import os


root = 'd:/20220225/testdata/'
dir_list = os.listdir(root)
for dir in dir_list:
    dir_path = os.path.join(root,dir)
    for img in os.listdir(dir_path):
        img_path = os.path.join(dir_path,img)
        print(img_path)
        img_name = os.path.basename(img_path)
        img_name = img_name[:-3] + 'jpg'
        new_path = os.path.join(dir_path,img_name)
        print(new_path)
        os.rename(img_path,new_path)