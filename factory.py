import cv2
import numpy as np
import os
import time
import random
import argparse


class factory:

    work = {}
    path = ""
    def __init__(self,work,path):
        self.work = work
        self.path = path

    def go(self):
        if self.work['op'] == 'maintain':
            #go shuffle
            pass
        else:
            pass

    def random_rotate(img):
        rows, cols, c = img.shape
        rad = random.randint(30, 45)
        M = cv2.getRotationMatrix2D((rows / 2, cols / 2), - rad, 1)
        new = cv2.warpAffine(img, M, (cols, rows))
        return new

    def flip(img):
        pass
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

    factory = factory()