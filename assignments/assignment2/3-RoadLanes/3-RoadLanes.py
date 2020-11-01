import matplotlib.pyplot as plt
import cv2
import glob, os
import numpy as np

def show_images(images, cmap=None):
    cols = 2
    rows = (len(images)+1)//cols
    
    plt.figure(figsize=(10,11))
    for i, image in enumerate(images):
        plt.subplot(rows, cols, i+1)
        cmap = 'gray' if len(image.shape) == 2 else cmap
        plt.imshow(image, cmap=cmap)
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout(pad=0, h_pad=0, w_pad=0)
    plt.show()

def convert_hls(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

def select_white_yellow(image):
    lower = np.uint8([0,200,0])
    upper = np.uint8([255,255,255])
    whiteMask = cv2.inRange(image, lower, upper)
    
    lower = np.uint8([10,0,100])
    upper = np.uint8([40,255,255])
    yellowMask = cv2.inRange(image, lower, upper)
    
    mask = cv2.bitwise_or(whiteMask, yellowMask)
    return cv2.bitwise_and(image, image, mask = mask)

def convert_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def apply_smoothing(image, kernelSize=15):
    return cv2.GaussianBlur(image, (kernelSize, kernelSize), 0)

def detect_edges(image, low_threshold=50, high_threshold=150):
    return cv2.Canny(image, low_threshold, high_threshold)

def filter_region(image, vertices):
    mask = np.zeros_like(image)
    if len(mask.shape)==2:
        cv2.fillPoly(mask, vertices, 255)
    else:
        cv2.fillPoly(mask, vertices, (255,)*mask.shape[2])
    return cv2.bitwise_and(image, mask)

def select_region(image):
    rows, cols = image.shape[:2]
    bottomLeft = [cols*0.1, rows*0.95]
    topLeft = [cols*0.4, rows*0.6]
    bottomRight = [cols*0.9, rows*0.95]
    topRight = [cols*0.6, rows*0.6]
    
    vertices = np.array([[bottomLeft, topLeft, topRight, bottomRight]], dtype = np.int32)
    return filter_region(image, vertices)
                     
def hough_lines(image):
    return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=300)
                     
def draw_lines(image, lines, color=[255,0,0], thickness=2, make_copy=True):
    if make_copy:
        image = np.copy(image)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(image, (x1,y1), (x2,y2), color, thickness)
    return image

def average_slope_intercept(lines):
    leftLines = []
    leftWeights = []
    rightLines = []
    rightWeights = []
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x2==x1:
                continue
            slope = (y2-y1)/(x2-x1)
            intercept = y1 - slope * x1
            length = np.sqrt((y2-y1)**2+(x2-x1)**2)
            
            if slope < 0:
                leftLines.append((slope, intercept))
                leftWeights.append((length))
            else:
                rightLines.append((slope, intercept))
                rightWeights.append((length))
                
    leftLane = np.dot(leftWeights, leftLines) / np.sum(leftWeights) if len(leftWeights) > 0 else None
    rightLane = np.dot(rightWeights, rightLines) / np.sum(rightWeights) if len(rightWeights) > 0 else None
    
    return leftLane, rightLane

def make_line_points(y1, y2, line):
    if line is None:
        return None
    
    slope, intercept = line
    
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    y1 = int(y1)
    y2 = int(y2)
    
    return ((x1, y1), (x2, y2))

def lane_lines(image, lines):
    leftLane, rightLane = average_slope_intercept(lines)
    
    y1 = image.shape[0]
    y2 = y1*0.6
    
    leftLine = make_line_points(y1, y2, leftLane)
    rightLine = make_line_points(y1, y2, rightLane)
    
    return leftLine, rightLine

def draw_lane_lines(image, lines, color=[255,0,0], thickness=20):
    lineImage = np.zeros_like(image)
    for line in lines:
        if line is not None:
            cv2.line(lineImage, *line, color, thickness)
            
    return cv2.addWeighted(image, 1.0, lineImage, 0.95, 0.0)

testImages = [plt.imread(path) for path in glob.glob('test_images/*.jpg')]
print(len(testImages), "Images Found")

hlsImages = list(map(convert_hls, testImages))
whiteYellowImages = list(map(select_white_yellow, hlsImages))
grayImages = list(map(convert_grayscale, whiteYellowImages))
blurredImages = list(map(lambda image: apply_smoothing(image), grayImages))
edgeImages = list(map(lambda image: detect_edges(image), blurredImages))
roiImages = list(map(select_region, edgeImages))
lines = list(map(hough_lines, roiImages))

lineImages = []
for image, lines in zip(testImages, lines):
    lineImages.append(draw_lane_lines(image, lane_lines(image, lines)))
    
show_images(lineImages)
