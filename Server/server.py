from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, send ,emit
import numpy as np
import cv2
# from urllib.request import urlopen
import base64
import matplotlib.pyplot as plt
import matplotlib
import random
import time
import base64
from PIL import Image
from io import BytesIO
import algo

import requests
# im.save('image.png', 'PNG')


def base64_to_cv2_img(data):
#    encoded_data = data.split(',')[1]
    
#    img = Image.open(BytesIO(base64.b64decode(data))) ##Not CV2

   encoded_data = data

   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img
#    return np.array(img)



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True
app.host = 'localhost'

@app.route('/')
def index():
    # msg = "static/test1.jpg"
    # msg = "https://i.pinimg.com/originals/e4/a0/0e/e4a00e405edccf0ed87ac4cbeef20364.jpg"
    return render_template('index.html')
	# return '<a href = '+str('https://www.google.com')+'>HIIII</a>'
	


@socketIo.on('connect')
def test_connect2():
    emit('connect',"hello msg" ,broadcast=True)
    print('someone connected to websocket!')


@socketIo.on("mode")
def handleMessage(msg):
    print(msg)
    # send(msg, broadcast=True)
    emit('mode', msg ,broadcast=True)
    return None

@socketIo.on("test")
def handleMessage(msg):
    print(str(msg))
    emit('test', str(msg) ,broadcast=True)
    # send(msg, broadcast=True)
    # emit('mode', msg ,broadcast=True)
    return None
# direction = ''
@socketIo.on("picture")
def handlepicture(pic):
    img = base64_to_cv2_img(pic)
    if ( img.any() == np.NaN):
        print("empty") 
    else:

        img_rotate_90_counterclockwise = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # height = 300
        # width = 300
        # lane_image=cv2.resize(np.copy(img_rotate_90_counterclockwise) , (width , height))
        combo_image , direction , angle = algo.action(img_rotate_90_counterclockwise)
        string = base64.b64encode(cv2.imencode('.jpg', combo_image)[1]).decode()
        emit('picture', string ,broadcast=True)
        requests.post("http://172.28.135.141:80/direction" , direction )
        # requests.post("http://192.168.43.223:80/direction" , direction )
        time.sleep(0.3)

        requests.post("http://172.28.135.141:80/direction" , 'S' )
        # requests.post("http://192.168.43.223:80/direction" , 'S' )

        print(direction , angle)
        

        
        
    return None



# @socketIo.on("auto_direction")
# def handleauto_direction(data):
#     emit('auto_direction', data ,broadcast=True)
#     print(data)
#     return None

if __name__ == '__main__':
    socketIo.run(app , host='172.28.135.133')
    # socketIo.run(app , host='192.168.1.2')
    # socketIo.run(app , host='192.168.43.226')