#coding=utf-8

import os
import time
import caffe
import numpy as np

def is_file_exist():
	if os.path.isfile('bvlc_reference_caffenet.caffemodel'):
		print '[{}]:CaffeNet found'.format(time.strftime("%H:%M:%S"))
		return True
	else:
		print 'Please download the model'
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
	MEAN_PROTO_PATH = protoName              # 待转换的pb格式图像均值文件路径
	MEAN_NPY_PATH = npyName                         # 转换后的numpy格式图像均值文件路径

	blob = caffe.proto.caffe_pb2.BlobProto()           # 创建protobuf blob
	data = open(MEAN_PROTO_PATH, 'rb' ).read()         # 读入mean.binaryproto文件内容
	blob.ParseFromString(data)                         # 解析文件内容到blob

	array = np.array(caffe.io.blobproto_to_array(blob))# 将blob中的均值转换成numpy格式，array的shape （mean_number，channel, hight, width）
	mean_npy = array[0]                                # 一个array中可以有多组均值存在，故需要通过下标选择其中一组均值
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

if __name__ == "__main__":
	is_file_exist()
	#probin_to_npy('imagenet_mean.binaryproto', 'meanpy')
	net = init_net('deploy.prototxt','bvlc_reference_caffenet.caffemodel')
	transformer = init_transformer(net, 'meanpy.npy', True)
	inference(net, 'cat.jpg', 'synset_words.txt', transformer)
	print_blobs_info(net)
	print_layers_dim(net)