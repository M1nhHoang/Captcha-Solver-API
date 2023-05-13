import cv2
import time
import numpy as np
from services.VietnameseIdCard.LoadModel import LoadCheckPoint
from PIL import Image, ImageTransform

def center_box(coord):
    return (coord[0]+coord[2])/2, (coord[1]+coord[3])/2

def Count_box(output_dict):
	# count = 0
	# for i in range(1,4):
	# 	index = np.where(output_dict['detection_classes'] == i)[0][0]
	# 	if output_dict['detection_scores'][index] >= 0.3:
	# 		print(index, output_dict['detection_scores'][index])
	# 		count += 1
	# return count
	return len([count for count in range(1, 4) if output_dict['detection_scores'][np.where(output_dict['detection_classes'] == count)[0][0]] >= 0.3])

def CropImgae(img, output_dict):
	width, height = img.size
	for i in range(1,4):
		index = np.where(output_dict['detection_classes'] == i)[0][0]
		ymin, xmin, ymax, xmax = float(output_dict['detection_boxes'][index][0])*height, float(output_dict['detection_boxes'][index][1])*width, float(output_dict['detection_boxes'][index][2])*height, float(output_dict['detection_boxes'][index][3])*width
		center_coord = center_box((xmin, ymin, xmax, ymax))
		if (i == 2):
			topRight = center_coord
		elif (i == 1):
			topLeft = center_coord
		else:
			botRight = center_coord

	# print(topRight, topLeft, botRight)
	vector = [topRight[0]-topLeft[0], topRight[1]-topLeft[1]]
	# print(vector)
	bot_left = [botRight[0]-vector[0], botRight[1]-vector[1]]

	import math
	new_width = int(math.sqrt((topRight[0]-topLeft[0])**2+(topRight[1]-topLeft[1])**2))
	new_height = int(math.sqrt((topRight[0]-botRight[0])**2+(topRight[1]-botRight[1])**2))
	transform=[topLeft[0], topLeft[1], bot_left[0], bot_left[1], botRight[0], botRight[1], topRight[0], topRight[1]]
	img = img.transform((new_width,new_height), ImageTransform.QuadTransform(transform))
	return img

def result(img, output_dict):
	return CropImgae(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), output_dict)

def detect4corner(img):
	for i in range(30, 24, -1):
		# load checkpoint
		configs_path = r"./services/VietnameseIdCard/Detect4Corner/pipeline.config"
		checkpoint_path = rf"./services/VietnameseIdCard/Detect4Corner/output_model/ckpt-{i}"
		label_map_path = r"./services/VietnameseIdCard/Detect4Corner/label_map.txt"

		detector = LoadCheckPoint.Detector(configs_path, checkpoint_path, label_map_path)

		# predict
		image, original_image, output_dict = detector.predict(img)

		# count box
		if Count_box(output_dict) >= 3:
			return result(original_image, output_dict)