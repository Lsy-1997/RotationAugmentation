import os

from cv2 import split
from pexpect import split_command_line
def add_angle(file,img_size):
    """
    将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
    :param file: 文件路径
    :param old_str: 需要替换的字符串
    :param new_str: 替换的字符串
    :return: None
    """
    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            split_line = line.strip().split(" ")
            w = float(split_line[3])*img_size[0]
            h = float(split_line[4])*img_size[1]
            if w>h:
                line = line[:-1] + ' ' + '90' + '\n'
            else:
                line = line[:-1] + ' ' + '0' + '\n'
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)

def main():
    txt_dir = './label/val'
    img_size = [1920,1080]
    for root, dirs, files in os.walk(txt_dir):
        for file in files:
            file_abs_path = os.path.join(root,file)
            print(file_abs_path)
            add_angle(file_abs_path,img_size)

if __name__ == '__main__':
    main()

