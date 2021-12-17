import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def canny(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	kernel = 5
	blur=cv2.GaussianBlur(gray,(kernel, kernel),0)
	canny = cv2.Canny(gray, 120, 360)
	return canny


def region_of_interest(image , height,width):
	polygons1=np.array([
		[(0,height),(100 , 180),(1250 , 150),(width,height)]
		])
	mask1=np.zeros_like(image)
	cv2.fillPoly(mask1, polygons1, 255)
	masked_image1 = cv2.bitwise_and(image , mask1)
	return masked_image1


def make_coordinated(image , line):
	try:
		slope, intercept = line
	except TypeError:
		slope, intercept = 0,0
	y1 = int(image.shape[0])
	y2 = int(y1*(3/5))
	x1 = int((y1-intercept) / slope)
	x2 = int((y2-intercept) / slope)
	return np.array([x1,y1,x2,y2])


def average_slop_intercept(image , lines):
	left_fit=[]
	right_fit=[]
	left_line = np.array([])
	right_line = np.array([])
	if lines is None:
		return None

	for line in lines:
		for x1,y1,x2,y2 in line:
			x1,y1,x2,y2 = line.reshape(4)
			parameters= np.polyfit((x1,x2) , (y1,y2) ,1)
			slope = parameters[0]
			intercept = parameters[1]
			if slope < 0:
				left_fit.append((slope , intercept))
			else:
				right_fit.append((slope , intercept))
	if left_fit:
		left_fit_average = np.average(left_fit , axis=0)
		#print(left_fit_average , 'left')
		left_line = make_coordinated(image , left_fit_average)
	if right_fit:
		right_fit_average = np.average(right_fit , axis=0)
		#print(right_fit_average , 'right')
		right_line = make_coordinated(image , right_fit_average)
	averaged_lines = [left_line , right_line]
	return averaged_lines

def display_lines(image , lines):
	line_image = np.zeros_like(image)
	if lines!= None:
		for line in lines:
			#print(line.shape)
			try:
				x1,y1,x2,y2 = line.reshape(4)
			except ValueError:
				x1,y1,x2,y2 = 0,0,0,0

			#print(x1,x2,y1,y2)
			cv2.line(line_image , (x1,y1) , (x2,y2) , (255, 0,0) , 10 )		
	return line_image


def compute_steering_angle(image, line , height,width):
	if len(line) == 0:
		return -90
		# No lane_lines detected
	if len(line) == 1:
		x1,_,x2,_= line[0][0]
		x_offset = x2 -x1
		# Only detected one lane_line
	else:
		try:
			_,_,left_x2,_ = line[0][2]
		except TypeError:
			_,_,left_x2,_ = 0,0,0,0
		try:
			_,_,right_x2,_ = line[1][2]
		except TypeError:
			_,_,right_x2,_ =0,0,0,0
		camera_mid_offset_percent = 0.02
		mid = int(width / 2 * (camera_mid_offset_percent) )
		x_offset = (left_x2 + right_x2) / 2 - mid
	y_offset = int(height / 2)
	angle_to_mid_in_rad = math.atan(x_offset/y_offset)
	angle_to_mid_in_deg = int(angle_to_mid_in_rad* 180.0 / math.pi)
	steering_angle = angle_to_mid_in_deg + 90
	#print(angle_to_mid_in_deg)
	return steering_angle


def display_heading_line(image , line , steering_angle , height , width):
	heading_image = np.zeros_like(image)
	steering_angle_in_rad = steering_angle / 180.0 *math.pi
	x1 = int(width / 2)
	y1 = height
	x2 = int(x1 - height / 2 / math.tan(steering_angle_in_rad))
	y2 = int(height / 2)
	cv2.line(heading_image , (x1,y1) , (x2,y2) , (0, 0,255) , 10 )
	heading_image = cv2.addWeighted(image , 0.8, heading_image , 1 ,1)
	return heading_image




img = cv2.imread('test1.jpg')
height = 704
width = 1279
lane_image=cv2.resize(np.copy(img) , (width , height))
canny_image=canny(lane_image)
cropped_image = region_of_interest(canny_image , height,width)
lines = cv2.HoughLinesP(cropped_image , 2 , np.pi/180 , 100 , np.array([]) , minLineLength=40 , maxLineGap= 5)
averaged_lines = average_slop_intercept(lane_image , lines)
line_image = display_lines(lane_image ,averaged_lines)
combo_image = cv2.addWeighted(lane_image , 0.3, line_image , 1 ,1)
angle = compute_steering_angle(lane_image , averaged_lines , height , width)
combo_heading_image = display_heading_line(combo_image , averaged_lines , angle , height , width)
cv2.imshow("Result", combo_heading_image)
cv2.waitKey(0)
