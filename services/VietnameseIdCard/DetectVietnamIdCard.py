import cv2
from PIL import Image
from services.VietnameseIdCard.Transformer_OCR import vietOCR
from services.VietnameseIdCard.DetectText import DetectTextVnIdCard

def sort_box(coord):
	line1 = []
	line2 = []
	center = (max(coord , key=lambda k: [k[0]])[0]+min(coord , key=lambda k: [k[0]])[0])/2

	for l in coord:
		if l[0] < center:
			line1.append(l)
		else:
			line2.append(l)

	return sorted(line1 , key=lambda k: [k[1]])+sorted(line2 , key=lambda k: [k[1]])

def cropImg(img, coord):
	height, width = img.shape
	space = 5
	return img[int(coord[0]*height-space):int(coord[2]*height+space), int(coord[1]*width-space):int(coord[3]*width+space)]

def vietnam_id_card(img):
	# get box
	original_image, box = DetectTextVnIdCard.detecTextVnIdCard(img)

	# Img to text
	text_box = [[], [], [], [], []]
	count = 0
	gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	for infos in box:
		infos = sort_box(infos)
		for info in infos:
			text_img = Image.fromarray(cropImg(gray, info))
			text_box[count].append(vietOCR.convert_img_to_text(text_img))
		count += 1

	#option 1: return string like gg api
	# return " ".join(map(str, [r for result in text_box for r in result]))
	#option 2: return one of json
	# result_list = [" ".join(map(str, result)) for result in text_box]
	# return {
	# 	"ID": result_list[0],
	# 	"HoTen": result_list[1],
	# 	"NgaySinh": result_list[2],
	# 	"DiaChi": result_list[3],
	# 	"QueQuan": result_list[4]
	# }
	#option 3: return box_json
	result_list = [" ".join(map(str, result)) for result in text_box]
	return {
	"boxs":[{"box": result_list[0]},
		{"box": result_list[1]},
		{"box": result_list[2]},
		{"box": result_list[3]},
		{"box": result_list[4]}]	
	}