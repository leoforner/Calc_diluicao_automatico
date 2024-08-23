# Importing Required Modules 
from rembg import remove 
import cv2

# Store path of the image in the variable input_path 
input_path = 'F:/backup de arquivos/fotos/IC/Nova pasta/teste3.png' 

# Store path of the output image in the variable output_path 
output_path = 'F:/backup de arquivos/fotos/IC/Nova pasta/teste3b2g.png' 


input = cv2.imread(input_path)
output = remove(input)
cv2.imwrite(output_path, output) # type: ignore



import numpy as np
import math

# input image
path = output_path   
# 1 EUR coin diameter in cm
coinDiameter = 2.325
# real area for the coin in cm^2
coinArea = (coinDiameter/2)**2 * math.pi
# initializing the multiplying factor for real size
realAreaPerPixel = 1


# pixel to cm^2
def pixelToArea(objectSizeInPixel, coinSizeInPixel):
    # how many cm^2 per pixel?
    realAreaPerPixel = coinArea / coinSizeInPixel
    print("realAreaPerPixel: ", realAreaPerPixel)
    # object area in cm^2
    objectArea = realAreaPerPixel * objectSizeInPixel
    return objectArea    


# finding coin and steak contours
def getContours(img, imgContour):
    
    # find all the contours from the B&W image
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # needed to filter only our contours of interest
    finalContours = []
    
    # for each contour found
    for cnt in contours:
        # cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 2)
        # find its area in pixel
        area = cv2.contourArea(cnt)
        print("Detected Contour with Area: ", area)

        # minimum area value is to be fixed as the one that leaves the coin as the small object on the scene
        if (area > 400):
            print("Area: ", area)
            perimeter = cv2.arcLength(cnt, True)
            
            # smaller epsilon -> more vertices detected [= more precision]
            epsilon = 0.002*perimeter
            # check how many vertices         
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            #print(len(approx))
            
            finalContours.append([len(approx), area, approx, cnt])


    # we want only two objects here: the coin and the meat slice
    print("---\nFinal number of External Contours: ", len(finalContours))
    # so at this point finalContours should have only two elements
    # sorting in ascending order depending on the area
    finalContours = sorted(finalContours, key = lambda x:x[1], reverse=False)
    
    # drawing contours for the final objects
    for con in finalContours:
        cv2.drawContours(imgContour, con[3], -1, (0, 0, 255), 3)

    return imgContour, finalContours

    
# sourcing the input image
img = cv2.imread(path)

# Definindo o tamanho da janela
cv2.namedWindow("Starting image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Starting image", 800, 600)  # Largura: 800, Altura: 600
cv2.imshow("Starting image", img)
cv2.waitKey()





# blurring
imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
cv2.namedWindow("blur image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("blur image", 800, 600)  # Largura: 800, Altura: 600
cv2.imshow("blur image", imgBlur)
cv2.waitKey()

# graying
imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

cv2.namedWindow("imgGray image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("imgGray image", 800, 600)  # Largura: 800, Altura: 600
cv2.imshow("imgGray image", imgGray)


mask = imgGray > 20
imgGray[mask] = 255


cv2.namedWindow("Starting image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Starting image", 800, 600)  # Largura: 800, Altura: 600
cv2.imshow("Starting image", imgGray)
cv2.waitKey()
# canny
imgCanny = cv2.Canny(imgGray, 255, 15)
cv2.namedWindow("Starting image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Starting image", 800, 600)  # Largura: 800, Altura: 600
cv2.imshow("Starting image", imgCanny)
cv2.waitKey()

kernel = np.ones((2, 2))
imgDil = cv2.dilate(imgCanny, kernel, iterations = 3)
# cv2.imshow("Diluted", imgDil)
imgThre = cv2.erode(imgDil, kernel, iterations = 3)

imgFinalContours, finalContours = getContours(imgThre, img)

# first final contour has the area of the coin in pixel
coinPixelArea = 5000#finalContours[0][1]
print("Coin Area in pixel", coinPixelArea)
# second final contour has the area of the meat slice in pixel
slicePixelArea = finalContours[0][1]#finalContours[1][1]
print("Entire Slice Area in pixel", slicePixelArea)

# let's go cm^2
print("Coin Area in cm^2:", coinArea)
print("Entire Slice Area in cm^2:", pixelToArea(slicePixelArea, coinPixelArea))

# show  the contours on the unfiltered starting image
cv2.namedWindow("Final External Contours", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Final External Contours", 800, 600)  # Largura: 800, Altura: 600

cv2.imshow("Final External Contours", imgFinalContours)
cv2.waitKey()


# now let's detect and quantify the lean part

# convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
# set lower and upper color limits
lowerVal = np.array([0, 159, 160])
upperVal = np.array([101, 255, 253])
# Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lowerVal, upperVal)
# apply mask to original image - this shows the red with black blackground
final = cv2.bitwise_and(img, img, mask= mask)

# show selection
cv2.namedWindow("Lean Cut", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Lean Cut", 800, 600)  # Largura: 800, Altura: 600

cv2.imshow("Lean Cut", final)
cv2.waitKey()

# convert it to grayscale because countNonZero() wants 1 channel images
gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Gray", gray)
# cv2.waitKey()
meatyPixelArea = cv2.countNonZero(gray)

print("Red Area in pixel: ", meatyPixelArea)
print("Red Area in cm^2: ", pixelToArea(meatyPixelArea, coinPixelArea))

# finally the body-fat ratio calculation
print("Body-Fat Ratio: ", meatyPixelArea/slicePixelArea*100, "%")

cv2.destroyAllWindows()