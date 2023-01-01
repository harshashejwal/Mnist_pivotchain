import pickle
from flask import Flask,request,app
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
import sys
import os


app=Flask(__name__)
modl=pickle.load(open('model5.pkl','rb'))

@app.route('/')
def home():
    return "hello"


@app.route('/predict',methods=['POST'])
def predict_digit():
    f=request.files['file']
    basepath= os.path.dirname(__file__)
    file_path = os.path.join(basepath,'upload',secure_filename(f.filename))
    f.save(file_path)

    img = image.load_img(file_path,target_size=(28,28,1),grayscale=True)
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    image_nor=tf.keras.utils.normalize(img_batch,axis=1)
    img_res=np.array(image_nor).reshape(-1,28,28,1)
    preds=modl.predict([img_res])
    answer=np.argmax(preds)
    
    return "The digit present at above image is "+ str(answer)

if __name__=='__main__':
    app.run(debug=True)