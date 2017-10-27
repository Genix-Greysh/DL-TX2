#coding=utf-8

import os
import time
import caffe
import numpy as np
import cv2
import os

def is_file_exist(modelFile):

	if os.path.isfile(modelFile):
		print '[{}]:CaffeNet found'.format(time.strftime("%H:%M:%S"))
		return True
	else:
		print 'Please check the model workdir!'
		return False

def init_net(modelFile, weighFile):
	caffe.set_mode_cpu()
	model_def = modelFile
	model_weights = weighFile

	net = caffe.Net(model_def,
					model_weights,
					1)
	return net

def probin_to_npy(protoName, npyName):
	MEAN_PROTO_PATH = protoName              
	MEAN_NPY_PATH = npyName                         

	blob = caffe.proto.caffe_pb2.BlobProto()           
	data = open(MEAN_PROTO_PATH, 'rb' ).read()         
	blob.ParseFromString(data)                         

	array = np.array(caffe.io.blobproto_to_array(blob))
	mean_npy = array[0]                                
	np.save(MEAN_NPY_PATH ,mean_npy)

	return True

def  init_transformer(net, meanFile, isMeaned):
	if not isMeaned:
		return False

	transformer = caffe.io.Transformer({"data": net.blobs['data'].data.shape})
	
	transformer.set_transpose('data', (2, 0, 1))
	transformer.set_mean('data', np.load(meanFile).mean(1).mean(1)) 
	transformer.set_raw_scale('data', 255)
	transformer.set_channel_swap('data', (2,1,0))

	return transformer

def inference(net, imageName, labelFile, transformer):
	im=caffe.io.load_image(imageName)
	net.blobs['data'].data[...] = transformer.preprocess('data',im)
	labels = np.loadtxt(labelFile, str, delimiter='\t')

	out = net.forward()
	
	top_k = net.blobs['prob'].data[0].flatten().argsort()[-1:-6:-1]
	for i in np.arange(top_k.size):
		print top_k[i], labels[top_k[i]]

def print_blobs_info(net):
	print 'layer_name' + '\t' + 'blobsShape'
	for layer_name, blob in net.blobs.iteritems():
		print layer_name + '\t' + str(blob.data.shape)

def print_layers_dim(net):
	print 'layer_name' + '\t' + 'ParamsShape'
	for layer_name, param in net.params.iteritems():
		print layer_name + '\t' + str(param[1].data.shape)

def salt(img, n):  
    for k in range(n):  
        i = int(np.random.random() * img.shape[1]);  
        j = int(np.random.random() * img.shape[0]);  
        if img.ndim == 2:   
            img[j,i] = 255  
        elif img.ndim == 3:   
            img[j,i,0]= 0  
            img[j,i,1]= 18  
            img[j,i,2]= 10  
    return img  
  
def resize_img(img_Name):
	image=cv2.imread(img_Name)
	res=cv2.resize(image,(32,32),interpolation=cv2.INTER_CUBIC)
	print res.shape
	cv2.imshow('iker',res)
	cv2.imshow('image',image)
	cv2.waitKey(0)


if __name__ == "__main__":
	model_path = './multi_view/'
	#is_file_exist('{}bvlc_reference_caffenet.caffemodel'.format(model_path))
	#probin_to_npy('/home/hanqing/Development/DL-TX2/CaffeDemo/multi_view/facialLandmarksModel.binaryproto', 'landmarkModel.npy')
	'''
	net = init_net('{}deploy.prototxt'.format(model_path),'{}bvlc_reference_caffenet.caffemodel'.format(model_path))
	transformer = init_transformer(net, '{}meanpy.npy'.format(model_path), True)
	inference(net, 'cat.jpg', '{}synset_words.txt'.format(model_path), transformer)
	print_blobs_info(net)
	print_layers_dim(net)
	'''
	net = caffe.Classifier(model_path + 'net_deploy_stageII.prototxt',
						model_path + 'model_weight_stageII.caffemodel'
						)

	img = caffe.io.load_image('me.jpg')
	img = cv2.resize(img,(144, 144),interpolation=cv2.INTER_CUBIC)
	grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  

	out = net.predict([img])
	print out[0]
	index =  1
	
	cv2.waitKey(0)  
	#for i in range(0, len(out[0]) / 2):
		#cv2.circle(grayimg, (out[0][i], out[0][i+1]), 3, (0, 255, 0), -1)
	x = [out[0][i] for i in range(0, 144) if i % 2 == 0 ]
	y = [out[0][i] for i in range(0, 144) if i % 2 != 0 ]
	for i in range(0, 72):
		cv2.circle(grayimg, (int(x[i] + 6  ), int(y[i] )), 1, (255, 180, 180), -1)
	print type(x[0])
	cv2.imshow('image', grayimg)
	cv2.waitKey(0)  

