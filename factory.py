import cv2
import numpy as np
import os
import time
import csv
import random
import argparse


###
# work : op,sub_op,num,mass
###
class Worker:

    work = {}
    img_path = "./img"
    label_path = "label.csv"
    def __init__(self,work,img_path,label_path):
        self.work = work
        self.img_path = img_path
        self.label_path = label_path

    def work(self):
        if self.work['op'] == 'maintain':
            #go shuffle or addition
            pass
        else:
        # read file
            with open(self.label_path,newline='') as csv_file:
                old_label =dict(csv.DictReader(csv_file))
                if len(old_label) == 0:
                    print("no such file!")
                    return
            img_list = os.listdir(self.img_path)
            img_tot = len(img_list)
            if img_tot == 0:
                print("no such image!")
                return
            total = self.work['num']

            new_path = "./img_new"
            new_idx = np.random.choice(total,replace=False)
            new_label = {}
            for i in range(0,total):
                old_idx = random.randint(1,img_tot)

                org_img = cv2.imread(os.path.join(self.img_path,img_list[old_idx]))

                new_label[str(new_idx[i])] = old_label[str(old_idx)]

                new_img = self.flip(org_img)
                cv2.imwrite(os.path.join(new_path,str(new_idx[i])))

            with open("./new.csv",newline = "") as new_csv:
                writer = csv.writer(new_csv)
                for key in new_label.keys():
                    writer.writerow([key,new_label[key]])
            print("done! total number = {}".format(total))


    def random_rotate(img):
        rows, cols, c = img.shape
        rad = random.randint(30, 45)
        M = cv2.getRotationMatrix2D((rows / 2, cols / 2), - rad, 1)
        new = cv2.warpAffine(img, M, (cols, rows))
        return new

    def flip(img):
        new  = cv2.flip(img,0)
        return new;
    def random_noise(img,mass):
        h, w ,c= img.shape
        new = img.copy()
        dense = random.randint(100, 300)
        for i in range(dense):
            x = random.randint(0, h - 1)
            y = random.randint(0, w - 1)
            new[x][y] = 255
        return new
    def random_clip(img):
        pass
    def random_blur(img):
        pass
    def random_change(img):
        pass
    def random_distor(img):
        pass

    def shuffle(path):
        pass



if __name__ == "__main__":

    work_list = {'op' : "new",'num': 1000}
    worker = Worker(work_list)
    worker.work()
