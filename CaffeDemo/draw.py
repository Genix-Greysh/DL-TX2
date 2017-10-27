	'''
	'''
	print out

	import numpy as np  
	import cv2  
  
	img = np.zeros((512,512,3), np.uint8)  
  
	cv2.line(img, (0,0), (511, 511), (255,0,0), 5) #line color (BGR)  
  
	cv2.rectangle(img, (384,0), (510, 128), (0, 255, 0), 3)  
  
	cv2.circle(img, (447, 63), 2, (0,0,255), -1) #linewidth -1 means fill circle using setted color  
  
	cv2.ellipse(img, (256,256), (100,50),45,0,270,(0,0,255),-1) #椭圆的第二个参数是椭圆中心，第三个参数是椭圆长轴和短轴对应的长度，第四个参数45是顺时针旋转45度， 第五个参数是从0度开始，顺时针画270的弧，第七个参数是颜色，最后一个是用颜色填充椭圆内部  
	font = cv2.FONT_HERSHEY_SIMPLEX  
	cv2.putText(img, 'Hello', (10,500), font, 4, (255,255,255), 2)  
  	

  	cv2.line(img, (256, 256), (256,256), (255,0,0), 5)
	cv2.imshow('image', img)  
	cv2.waitKey(0)  
'''
