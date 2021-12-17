import flask
from flask import request
from flask_cors import cross_origin
import numpy as np
import cv2
# from urllib.request import urlopen
import base64
import matplotlib.pyplot as plt

def base64_to_cv2_img(data):
#    encoded_data = uri.split(',')[1]
   encoded_data = data
   nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img




# def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
#     # download the image, convert it to a NumPy array, and then read
#     # it into OpenCV format
#     resp = urlopen(url)
#     print(resp.read())
#     image = np.asarray(bytearray(resp.read()), dtype="uint8")
#     image = cv2.imdecode(image, readFlag)

#     # return the image
#     return image

# img = url_to_image("https://pyimagesearch.com/wp-content/uploads/2014/12/adrian_face_detection_sidebar.png")
    
# cv2.imshow("Image", img)
# cv2.waitKey(0)
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    print("HIIIIIII")
    return ""

@app.route('/photo', methods=['GET', 'POST'])
@cross_origin()
def photo():
    req_data = request.get_json()
    # print(req_data['photo'])
    # img = url_to_image(str(req_data['photo']))

    img = base64_to_cv2_img(req_data['photo'])

    # img = req_data['photo']
    
    # cv2.imshow("Image", img)
    plt.imshow(img)
    plt.show()
    
    return ""

app.run(host='192.168.1.2',port=5000)