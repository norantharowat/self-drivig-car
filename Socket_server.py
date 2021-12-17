from flask import Flask, jsonify;
from flask_socketio import SocketIO, send ,emit
import numpy as np
import cv2
# from urllib.request import urlopen
import base64
import matplotlib.pyplot as plt
import matplotlib
import random
def base64_to_cv2_img(data):
#    encoded_data = data.split(',')[1]
   encoded_data = data
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'

@socketIo.on('connect')
def test_connect2():
    print('someone connected to websocket!')


@socketIo.on("mode")
def handleMessage(msg):
    print(msg)
    # send(msg, broadcast=True)
    emit('mode', msg ,broadcast=True)
    return None

@socketIo.on("test")
def handleMessage(msg):
    print(msg)
    # send(msg, broadcast=True)
    # emit('mode', msg ,broadcast=True)
    return None


@socketIo.on("picture")
def handlepicture(pic):
    img = base64_to_cv2_img(pic)
    # cv2.imshow('result', img)
    # plt.imshow(img)
    # plt.show()
    
    matplotlib.image.imsave(str(random.random())+'.png', img)
    # print(img)
    # send(msg, broadcast=True)
    # emit('mode', msg ,broadcast=True)
    return None

if __name__ == '__main__':
    socketIo.run(app , host='192.168.1.2')