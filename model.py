
#import pytesseract 

import requests
from PIL import Image, ImageDraw
import numpy as np 
import os
import time

from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier


class Model(object):
    def __init__(self):
       pass
    
    def newModel(self):
        self.model = KNeighborsClassifier()
        print("Created a new model")
    def loadModel(self,path):
        if os.path.exists(path):
            self.model = joblib.load(path)
        else:
            print("Model not exit")
            exit(-1)
    def saveModel(self,path):
        if self.model :
            joblib.dump(self.model,path)
            print("model Save at",path)
        else:
            print("saveMode failed, model not exit")

    def predict_imgs(self,imgs,sz):
        result_list = []
        pre_list = []
        imgsLen = len(imgs)
        for i in range(imgsLen):
            pix = np.asarray(imgs[i].convert('L'))
            pix = pix.reshape(sz)
            pre_list.append(pix)

        pre_list = np.asarray(pre_list)
        result_list = self.model.predict(pre_list)
        
        return ''.join(result_list)

    # train
    def trainModel(self,path,items,sz):
        X = []
        y = []
        print("Starting training model...")
        for i in items:
            target_path = os.path.join(path,i)
            print(target_path)
            for name in os.listdir(target_path):
                img = Image.open(os.path.join(target_path,name))
                pix = np.asarray(img.convert('L'))
                X.append(pix.reshape(sz))
                y.append(target_path.split('\\')[-1])

        X = np.asarray(X)
        y = np.asarray(y)
        self.model.fit(X,y)
        print("Train finished")

    #check train result
    def checkModel(self,path,items,sz):
        pre_list = []
        y_list = []
        print("Starting prediction")
        for i in items:
            part_path = os.path.join(path,i)
            for name in os.listdir(part_path):
                img = Image.open(os.path.join(part_path,name))
                pix =  np.asarray(img.convert('L'))
                pix = pix.reshape(sz)
                pre_list.append(pix)
                y_list.append(part_path.split('\\')[-1])

        pre_list = np.asarray(pre_list)
        
        y_list = np.asarray(y_list)
        result_list = self.model.predict(pre_list)
        
        print(result_list,y_list)
        acc = 0
        for i in result_list == y_list:
            if i == np.bool(True):
                acc += 1

        print("Predict result: ")
        print(acc,acc/len(result_list))


