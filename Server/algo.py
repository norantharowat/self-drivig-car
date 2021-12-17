import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.pyplot as plt
#from PIL import Image

def detect_edges(image):
    # print("1")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([60, 40, 40])
    upper_blue = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    edges = cv2.Canny(mask, 200, 400)

    return edges

def region_of_interest(edges):
    # print("2")
    height, width = edges.shape
    mask = np.zeros_like(edges)

    # only focus bottom half of the screen
    polygon = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, height),
        (0, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)
    return cropped_edges


def detect_line_segments(cropped_edges):
    # print("3")
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, 
                                    np.array([]), minLineLength=8, maxLineGap=4)

    return line_segments



def make_points(frame, line):
    # print("4")
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]


def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        
        return lane_lines

    height, width, _ = frame.shape
    # print("5")
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    

    return lane_lines

def display_lines(frame, lines, line_color=(255, 0, 0), line_width=10):
    # print("6")
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.5, line_image, 1, 1)
    return line_image




def compute_steering_angle(frame, lane_lines):
    # print("7")
    """ Find the steering angle based on lane line coordinate
        We assume that camera is calibrated to point to dead center
    """
    if len(lane_lines) == 0:
        
        return -90

    height, width, _ = frame.shape
    if len(lane_lines) == 1:
        
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        camera_mid_offset_percent = 0.02 # 0.0 means car pointing to center, -0.03: car is centered to left, +0.03 means car pointing to right
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    # find the steering angle, which is angle between navigation direction to end of center line
    y_offset = int(height / 2)

    angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel

    
    return steering_angle


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=10 ):
    # print("8")
    heading_image = np.zeros_like(frame)
    height, width, _ = frame.shape

    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right 
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)

    return heading_image



def action(img):
    # print("9")
    # img =cv2.imread(image)

    height = 704
    width = 1279
    lane_image=cv2.resize(np.copy(img) , (width , height))
    edges=detect_edges(lane_image)
    cropped_edges=region_of_interest(edges)
    line_segments=detect_line_segments(cropped_edges)
    lane_lines=average_slope_intercept(lane_image,line_segments)
    lane_lines_image=display_lines(lane_image,lane_lines)
    combo_image = cv2.addWeighted(lane_image , 0.3, lane_lines_image , 1 ,1)
    angle = compute_steering_angle(lane_image , lane_lines)
    combo_heading_image = display_heading_line( combo_image,angle )
    
    # if angle == 90 :
    #     return (combo_heading_image,'F')
    # elif( angle > 90):
    #     return (combo_heading_image,'R')
    # else:
    #     return (combo_heading_image,'L')
    if angle >= 70 and angle <= 110:
        return (combo_heading_image,'F',angle)
    elif( angle > 110):
        return (combo_heading_image,'O', angle)
    elif (angle == -90 ):
        return (combo_heading_image,'S' ,angle)
    else:
        return (combo_heading_image,'K' ,angle)
    # else:
    #     return (combo_heading_image,'S' ,angle)

    # return (combo_heading_image,angle)
    # return (combo_heading_image,angle)


	


# print(action('video_data/image_169.jpg'))
# action('E:/4th year/Electronics/Task3_important/Server/static/test1.jpg')
#action('')