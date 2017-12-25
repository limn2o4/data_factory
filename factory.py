import cv2
import numpy as np
import os
import shutil
import time
import csv
import random
import argparse


class Worker:

    work = {}
    img_path = "./img"
    label_path = "label.csv"
    def __init__(self,work,img_path,label_path):
        self.work = work
        self.img_path = img_path
        self.label_path = label_path
        print("you have a worker now")

    def do(self):

        if 'num' not in self.work.keys():
            print("go check the list!")
            return
        total = self.work['num']

        with open(self.label_path, "r", newline='') as csv_file:
            old_label = dict(csv.reader(csv_file))
        if len(old_label) == 0:
            print("no such file -_-||")
        print(old_label)

        if self.work['op'] == 'shuffle':

            old_idx = list(old_label.keys())
            new_idx = old_idx.copy()
            np.random.shuffle(new_idx)
            print("old:",old_idx,"new:",new_idx)
            new_label = {}
            new_path = "./img_new"
            if os.path.exists(new_path) == False:
                os.makedirs(new_path)
            for i in range(len(old_label)):
                new_label[new_idx[i]] = old_label[old_idx[i]]
                new_name = new_idx[i]+'.jpg'
                old_name = old_idx[i]+'.jpg'
                shutil.copy(os.path.join(os.path.abspath(self.img_path),old_name),
                            os.path.join(os.path.abspath(new_path),new_name))
            with open("./new.csv","w",newline='') as newcsv:
                writer = csv.writer(newcsv)
                for k in new_label.keys():
                    writer.writerow([k,new_label[k]])
            print("you have screwed up your data set 0_0")


        elif self.work['op'] == 'add':

            img_list = os.listdir(self.img_path)
            img_tot = len(img_list)
            if img_tot == 0:
                print("no such file!")
                return
            new_idx = np.arange(img_tot+1,img_tot+total+1)
            np.random.shuffle(new_idx)
            new_path = "./new_img"
            if os.path.exists(new_path) == False:
                os.makedirs(new_path)
            print(img_tot)
            add_label = {}
            for i in range(total):
                idx = np.random.randint(0,img_tot)
                old_img = cv2.imread(os.path.join(self.img_path,img_list[idx]))
                new_img = self.process(old_img)
                cv2.imwrite(os.path.join(new_path,str(new_idx[idx-1])+".jpg"),new_img )

                add_label[new_idx[i]] = old_label[img_list[idx-1].split(".")[0]]
            with open(self.label_path,"a",newline='') as newfile:
                writer = csv.writer(newfile)
                for k in add_label.keys():
                    writer.writerow([k,add_label[k]])
            print("done! you have add {} to the data set".format(total))
            # random find a img
            # get it's label
            # pro it and save

        elif self.work['op'] == 'new':
            img_list = os.listdir(self.img_path)

            print("you have:{}".format(img_list))

            img_tot = len(img_list)

            if img_tot == 0:
                print("no such image!")
                return

            new_path = "./img_new"
            if os.path.exists(new_path) == False:
                os.makedirs(new_path)
            new_idx = np.random.choice(total,total,replace=False)
            new_label = {}
            for i in range(0, total):
                old_idx = random.randint(1, img_tot)

                org_img = cv2.imread(os.path.join(self.img_path, img_list[old_idx-1]))

                new_label[str(new_idx[i])] = old_label[img_list[old_idx-1].split('.')[0]]

                new_img = self.process(org_img)
                cv2.imwrite(os.path.join(new_path, str(new_idx[i]))+".jpg", new_img)

                print("{} -> :{}.jpg".format(img_list[old_idx-1],new_idx[i]))

            with open("./new.csv","w", newline="") as new_csv:
                writer = csv.writer(new_csv)
                for key in new_label.keys():
                    writer.writerow([key, new_label[key]])
            print("done! total number = {}".format(total))
        else:
            print("you're totally blind...")
            return

    def process(self,img):
        mass = self.work['mass']
        pro = np.random.choice(mass,mass,replace=False)
        dst = img.copy()
        for i in pro:
            if i == 1:
                dst = self.random_blur(dst)
            if i == 2:
                dst = self.random_rotate(dst)
            if i == 3:
                dst = self.flip(dst)
            if i == 4:
                dst = self.random_noise(dst)
            if i == 5:
                dst = self.random_clip(dst)
            if i == 6:
                dst = self.random_distor(dst)
        if self.work['size'] != None:
            dst = cv2.resize(dst,self.work['size'])
        return dst

    def random_rotate(self,img):
        rows, cols, c = img.shape
        rad = random.randint(30, 45)
        M = cv2.getRotationMatrix2D((rows / 2, cols / 2), - rad, 1)
        new = cv2.warpAffine(img, M, (cols, rows))
        return new

    def flip(self,img):
        new  = cv2.flip(img,0)
        return new;
    def random_noise(self,img):
        h, w ,c= img.shape
        new = img.copy()
        dense = random.randint(self.work['mass']*100, self.work['mass']*300)
        for i in range(dense):
            x = random.randint(0, h - 1)
            y = random.randint(0, w - 1)
            new[x][y] = 255
        return new

    def random_clip(self,img):
        mass = self.work['mass']
        h,w,c = img.shape
        pt1 = np.float32([0,0],[0,w],[h,0])
        pt2 = np.float32([10,10],[10,w],[h,10])
        M = cv2.getAffineTransform(pt1,pt2)
        new = cv2.warpAffine(img,M,(h,w))
        return new
    def random_blur(self,img):
        mass = self.work['mass']
        new = cv2.medianBlur(img,3)
        new = cv2.blur(new,(3,3))
        return new
    def random_change(self,img):
        mass = self.work['mass']
        dx = random.randint(1,mass*10)
        dy = random.randint(1,mass*10)
        h, w, c = img.shape
        pt1 = np.float32([0, 0], [0, w], [h, 0])
        pt2 = np.float32([dx, 0], [0, w], [h, dy])
        M = cv2.getAffineTransform(pt1, pt2)
        new = cv2.warpAffine(img, M, (h, w))
        return new
    def random_distor(self,img):
        return img

    def get_count(self):
        with open(self.label_path,"r",newline='') as csvfile:
            labels = dict(csv.reader(csvfile))
        print('total:',len(labels.keys()))


if __name__ == "__main__":

    work_list = {'op':"add",'num': 12,'mass':2,'is_norm_size':False,'size':None}
    worker = Worker(work_list,"./test_img","./label.csv")
    worker.do()
