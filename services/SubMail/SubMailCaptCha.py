import numpy as np
from PIL import Image
import cv2
import os

def RemoveNoise(img):
	pixels = img.load()
	step = 50
	NoiseColor = pixels[0, 0]

	new_img = Image.new(img.mode, img.size)
	pixels_new = new_img.load()
	for i in range(new_img.size[0]):
	    for j in range(new_img.size[1]):
	        r, g, b = pixels[i,j]
	        if NoiseColor[0]-step <= r <= NoiseColor[0]+step and NoiseColor[1]-step <= g <= NoiseColor[1]+step and NoiseColor[2]-step <= b <= NoiseColor[2]+step:
	            pixels_new[i,j] = (255, 255, 255, 3)
	        else:
	            pixels_new[i,j] = (r, g, b, 3)

	return new_img

def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    # return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return np.asarray(img)

def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # return Image.fromarray(img)

def predict(img):
	try:
		img_color = convert_from_image_to_cv2(RemoveNoise(img))

		gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
		_, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
		contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

		character_img = []
		for i in range(len(contours)):
			rect = cv2.boundingRect(contours[i])
			y,x,h,w = rect
			y,x,h,w = y-1,x-1,h+2,w+2
			# if w < 5 or h < 5: 
			# 	continue
			# print(rect)
			crop_img = gray[x:x+w, y:y+h]
			character_img.append((y, crop_img, w, h))

		character_img.sort(key=lambda x: (x[0]))

		result = ''

		for character in character_img:
			picture1 = np.array(convert_from_cv2_to_image(character[1]))
			picture1_norm = picture1/np.sqrt(np.sum(picture1**2))

			src = r'C:\Users\HP\Desktop\\captcha-break-master\\captcha-break-master\submail\\cpp\recognizer\dataset\\'
			same_list = []
			Model_list = os.listdir(src)
			for l in Model_list:
				picture2 = Image.open(src+l).convert('L')
				width, height = picture2.size
				if character[2] == height and character[3] == width:
					picture2 = np.array(picture2).reshape(height, width, 1)
					picture2_norm = picture2/np.sqrt(np.sum(picture2**2))

					same_list.append((float(np.sum(picture2_norm*picture1_norm)), l))

			try:
				result += str(max(same_list)[1]).replace('[', '').replace(']', '').replace('.png', '')
			except:
				pass

		return result
	except:
		return 'erorr'

# xac xuat doan trung la 42% thap vcc
