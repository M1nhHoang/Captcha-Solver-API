try:
	import os
	from flask import Flask, render_template, redirect, url_for, request
	from flask_cors import CORS, cross_origin
	from PIL import Image, ImageFile
	import requests
	
except:
	os.system('py -m pip install --upgrade pip')
	os.system('py -m pip install flask')
	os.system('py -m pip install requests')
	os.system('py -m pip install pillow==9.3.0')
	os.system('py -m pip install pandas')
	os.system('py -m pip install numpy==1.22.2')
	os.system('py -m pip install flask_cors')
	os.system('py -m pip install tensorflow')
	os.system('py -m pip install keras==2.10.0')
	os.system('py -m pip install object-detection')
	os.system('py -m pip install opencv-python==4.5.5.64')
	os.system('py -m pip install torch==1.12.0')
	os.system('py -m pip install torchvision==0.13.0')
	os.system('py -m pip install patch-ng')
	os.system('py -m pip install wheel==0.37.1')
	os.system('py -m pip install setuptools==65.5.1')
	os.system('py -m pip install vietocr==0.3.6')                   
	os.system('py -m pip install scikit-learn==1.0.2')
	os.system('py -m pip install pyyaml==5.4.1')
	os.system('py -m pip install tensorflow-object-detection-api==0.1.1')
	os.system('py -m pip install tf_slim')
	os.system('py -m pip install tensorflow.io')

import base64
from io import BytesIO
from xml.dom import minidom
from services.Pred_Capthcha_t1v1 import Pred_Capthcha_t1v1
from services.CSDN import CSDN_Captcha
from services.SubMail import SubMailCaptCha
from services.VietnameseIdCard import DetectVietnamIdCard

UPLOAD_FOLDER = './static/Images/'

# create backend
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# apply flask cors
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# api
@app.route('/', methods=['GET'])
@cross_origin(origin='*')
def Home():
	return render_template('index.html')

@app.route('/trycaptcha', methods=['GET'])
@cross_origin(origin='*')
def captcha_web():
	file = minidom.parse(r'.\App_Data\data.xml')
	captcha      = str(request.args.get('captcha'))
	captcha_type = str(request.args.get('type'))
	url          = [url for url in file.getElementsByTagName(captcha)[0].getElementsByTagName('type') if url.getElementsByTagName('id')[0].childNodes[0].nodeValue == captcha_type]

	return render_template('CaptCha.html', content=[captcha, captcha_type, url[0].getElementsByTagName('imgTestURL')[0].childNodes[0].nodeValue])

@app.route('/Images/<img_name>', methods=['GET'])
@cross_origin(origin='*')
def display_image(img_name):
	return redirect(url_for('static', filename='Images/' + img_name), code=301)

@app.route('/getText', methods=['GET', 'POST'])
@cross_origin(origin='*')
def test_post():
	captcha      = str(request.args.get('captcha'))
	captcha_type = str(request.args.get('type'))
	image        = str(request.args.get('image')).replace(' ','+')
	imgdata 	 = base64.b64decode(image[image.find(',')+1:])
	img 		 = Image.open(BytesIO(imgdata))
	
	if captcha == 'text-captcha':
		if captcha_type == '1':
			return Pred_Capthcha_t1v1.predict(img)
		elif captcha_type == '2':
			return CSDN_Captcha.predict(img)
		elif captcha_type == '3':
			return SubMailCaptCha.predict(img)
		# basic captcha

@app.route('/vietidcard', methods=['POST'])
@cross_origin(origin='*')
def VieIdCard():
	# try:
	# image        = str(request.args.get('image')).replace(' ','+')
	# imgdata 	 = base64.b64decode(image[image.find(',')+1:])
	# img 		 = Image.open(BytesIO(imgdata))
	image        = request.data
	img 		 = Image.open(BytesIO(image))
	
	return DetectVietnamIdCard.vietnam_id_card(img)
	# except:
	# 	return "Không thấy ảnh"

# start backend
if __name__ == '__main__':
	app.run(host='0.0.0.0', port='7777', debug=True)
