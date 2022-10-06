from io import BytesIO
import socketio # 4.2.1 only
import eventlet
from flask import Flask
from keras.models import load_model
import base64
from PIL import Image
import numpy as np
import cv2

sio = socketio.Server()

app = Flask(__name__)

speed_limit = 10

def img_preprocess(img):
    img = img[60:135, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3,3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img


# Telemetry listenes the updates from the simulator
# It provides the image of the car on the track on which the prediction is done
@sio.on('telemetry')
def telemetry(sid, data):
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = img_preprocess(image)
    # model expects 4d array while our img is 3d
    image = np.array([image])
    steering_angle = float(model.predict(image))
    speed = float(data['speed'])
    throttle = 1.0 - speed/speed_limit
    send_control(steering_angle, throttle)


# register an event handeler
@sio.on('connect')
def connect(sid, environ):
    print('Connected')
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit('steer', data = {
        'steering_angle': steering_angle.__str__(),
        'throttle': throttle.__str__()
    })


if(__name__ == '__main__'):
    model = load_model('model.h5')
    app = socketio.Middleware(sio, app)
    # weserver gateway interface to direct requests to web server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)



# conda create --name selfddrive
# conda activate selfdrive
# conda install -c anaconda flask
# conda install -c conda-forge eventlet tensorflow keras
# pip install python-socketio==4.2.1
# pip install opencv-python
# pip install Pillow