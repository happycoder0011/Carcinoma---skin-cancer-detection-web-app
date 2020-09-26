#source c:/Users/user/Desktop/dev/Hackathons/shellhack/shellhack/Scripts/activate
#to activate
import sys
import os
import glob
import re
import numpy as np
from PIL import Image
import json

#tensorflow
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template,jsonify
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# Load your trained model
global model,graph
model = tf.keras.models.load_model('model/my_h5_model.h5', custom_objects={'KerasLayer':hub.KerasLayer})
print(model.get_config())
model.summary()
graph = tf.compat.v1.get_default_graph()
print('Model loaded. Check http://127.0.0.1:12000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.array([img])  # Convert single image to a batch.
    img /=255.
    preds = model.predict(img)
    result = {1:"{:.2f}".format(preds[0][0]*100),
              2:"{:.2f}".format(preds[0][1]*100),
              3:"{:.2f}".format(preds[0][2]*100),
              4:"{:.2f}".format(preds[0][3]*100),
              5:"{:.2f}".format(preds[0][4]*100),
              6:"{:.2f}".format(preds[0][5]*100),
              7:"{:.2f}".format(preds[0][6]*100),
              8:"{:.2f}".format(preds[0][7]*100),
              9:"{:.2f}".format(preds[0][8]*100),
            }  
    json_dump = json.dumps(result)
    final = json.loads(json_dump)                            
    return final

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process to make json
        print(preds)
        return preds
    return None


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=12000,debug=True)