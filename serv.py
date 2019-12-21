
from flask import Flask,request
from PIL import Image
from tempfile import TemporaryFile
import json,base64
import captcha as capt
import model

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello,world"

@app.route('/captcha',methods=['GET','POST'])
def captcha():
    
    if request.method ==  'GET':
        return makeErrJson(1)
    else:
        #global skl_model
        img_base64 = request.form['data']
        img = base64.b64decode(img_base64)

        imgs = []
        with TemporaryFile() as f:
            f.write(img)
            imgs = capt.Captcha(f).getImgs(4,(20,25))

        code = skl_model.predict_imgs(imgs,20*25)
        print(code)

        return makeSuccessJson(code)

def makeErrJson(err):
    msg = {
        1:"payload error"
    }
    return json.dumps({
        'err':err,
        'msg':msg[err],
        'data':None
    })
def makeSuccessJson(data):
    return json.dumps({
        'err':0,
        'msg':'success',
        'data':data
    })

if __name__ == '__main__':
    skl_model  = model.Model()
    skl_model.loadModel("test1.model")
    app.run(threaded=False)