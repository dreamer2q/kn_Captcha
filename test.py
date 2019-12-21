
from PIL import Image

import captcha
import model
import os

import time
import requests
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import numpy as np 
import random

md = model.Model()
md.loadModel('test1.model')
#md.newModel()
#md.trainModel("cap","123456789",20*25)
#md.checkModel("category","123456789",20*25)
#md.saveModel("test2.model")

#test_dir = "code"
#for title in os.listdir(test_dir):
#    filename = os.path.join(test_dir,title)
#    print(filename)
#    imgs = captcha.Captcha(filename).getImgs(4,(20,25))
#    md.predict_imgs(imgs,20*25)
#    time.sleep(5)

#imgs = []
#imgs.append(Image.open('0.jpg'))
#imgs.append(Image.open('1.jpg'))
#imgs.append(Image.open('2.jpg'))
#imgs.append(Image.open('3.jpg'))

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36',
    'X-Auth-Token': '1abb0d33-7d46-433e-b5e1-ced9690d3b74'
}

url = "https://skl.hdu.edu.cn/api/checkIn/create-code-img"

#plt.ion()
#plt.figure()
#plt.axis('off')

for i in range(20000):

    ret = requests.get(url=url,headers=headers)
    tmpfile = "c.jpg"
    target_path = "predict1"
    if not os.path.exists(target_path) :
        os.mkdir(target_path)
    with open(tmpfile,'wb') as f:
        f.write(ret.content)
        f.close()
    imgs = captcha.Captcha(tmpfile).getImgs(4,(20,25))
    code = md.predict_imgs(imgs,20*25)
    filename = ""
    for c in code:
        filename += str(c)
    filename += "_"+str(random.randint(100000,999999)) + ".jpg"
    Image.open(tmpfile).save(os.path.join(target_path,filename))
    print(i,filename)
    #img = mpimg.imread(tmpfile)
    #plt.imshow(img)
    #plt.pause(2)
    #plt.show()
    #time.sleep(0.1)
    if i % 10 == 0:
        print("take a break")
        #time.sleep(1)



