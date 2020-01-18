import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from skimage import io

LEARNING_RATE = 1e-4
# set to 20000 on local environment to get 0.99 accuracy
TRAINING_ITERATIONS = 4000
DROPOUT = 0.5
BATCH_SIZE = 50
# set to 0 to train on all available data
VALIDATION_SIZE = 2000
# image number to output
IMAGE_TO_DISPLAY = 1

# Display image
def display(img):
	one_image = img.reshape(image_height, image_width)
	plt.axis('off')
	plt.imshow(one_image, cmap=cm.binary)
	plt.show()

def saveImage(img, name):
	one_image = img.reshape(image_height, image_width)
	io.imsave(name, one_image)

# weight initialization
def weight_variable(shape):
	initial = tf.truncated_normal(shape, stddev=0.1)
	return tf.Variable(initial)

def bias_variable(shape):
	initial = tf.constant(0.1, shape=shape)
	return tf.Variable(initial)

# convolution
def conv2d(x, W):
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

# pooling
# [[0,3],
#  [4,2]] => 4
# [[0,1],
#  [1,1]] => 1
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# serve data by batches
def next_batch(batch_size):

	global train_images
	global train_labels
	global index_in_epoch
	global epochs_completed

	start = index_in_epoch
	index_in_epoch += batch_size

	# when all trainig data have been already used, it is reordered randomly    
	if index_in_epoch > num_examples:
		# finished epoch
		epochs_completed += 1
		# shuffle the data
		perm = np.arange(num_examples)
		np.random.shuffle(perm)
		train_images = train_images[perm]
		train_labels = train_labels[perm]
		# start next epoch
		start = 0
		index_in_epoch = batch_size
		assert batch_size <= num_examples
	end = index_in_epoch
	return train_images[start:end], train_labels[start:end]

# Convert class labels from scalars to one-hot vectors
# 0 => [1 0 0 0 0 0 0 0 0 0]
# 1 => [0 1 0 0 0 0 0 0 0 0]
# ...
# 9 => [0 0 0 0 0 0 0 0 0 1]
def dense_to_one_hot(labels_dense, num_classes):
	num_labels = labels_dense.shape[0]
	index_offset = np.arange(num_labels) * num_classes
	labels_one_hot = np.zeros((num_labels, num_classes))
	labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
	return labels_one_hot

# Normalization on a multi-dimensional sphere of radius 1
def process_norm(samples):
	for sample in samples:
		#print sample
		K = np.sum(sample)
		sample = (1/K) * sample
		#print sample
		sample = np.sqrt(sample)
		#print sample
	return samples

# Extracts images and labels from data in location provided
def process_data(location, arr_size):

	global image_size
	global image_width
	global image_height
	global labels_count

	data = pd.read_csv(location)
	images = data.iloc[:,1:].values
	images = images.astype(np.float)

	image_size = images.shape[1]
	image_width = arr_size
	image_height = image_size/arr_size

	labels_flat = data[[0]].values.ravel().astype(np.uint8)
	print('labels_flat({0})'.format(len(labels_flat)))
	print ('labels_flat[{0}] => {1}'.format(IMAGE_TO_DISPLAY,labels_flat[IMAGE_TO_DISPLAY]))
	labels_count = np.unique(labels_flat).shape[0]
	print('labels_count => {0}'.format(labels_count))
	labels = dense_to_one_hot(labels_flat, labels_count)
	labels = labels.astype(np.uint8)
	print('labels({0[0]},{0[1]})'.format(labels.shape))
	print ('labels[{0}] => {1}'.format(IMAGE_TO_DISPLAY,labels[IMAGE_TO_DISPLAY]))

	return process_norm(images), labels

images, labels = process_data(location = './data/IOA_IBHQR_ID/train_1000.csv', arr_size = 10)
# Uncomment following line if you want to output a certain image     
#display(images[IMAGE_TO_DISPLAY])
IMAGE_TO_DISPLAY = 0
#saveImage(images[IMAGE_TO_DISPLAY], './output/NormalizedSortingAlgorithms/insertInc.png')
print len(images)

import sys
#sys.exit()

# split data into training & validation
validation_images = images[:VALIDATION_SIZE]
validation_labels = labels[:VALIDATION_SIZE]

train_images = images[VALIDATION_SIZE:]
train_labels = labels[VALIDATION_SIZE:]

print('train_images({0[0]},{0[1]})'.format(train_images.shape))
print('validation_images({0[0]},{0[1]})'.format(validation_images.shape))

# images
x = tf.placeholder('float', shape=[None, image_size])
# labels
y_ = tf.placeholder('float', shape=[None, labels_count])

epochs_completed = 0
index_in_epoch = 0
num_examples = train_images.shape[0]

# first convolutional layer
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
# (40000,784) => (40000,28,28,1)
image = tf.reshape(x, [-1,image_width , image_height,1])
#print (image.get_shape()) # =>(40000,28,28,1)
h_conv1 = tf.nn.relu(conv2d(image, W_conv1) + b_conv1)
#print (h_conv1.get_shape()) # => (40000, 28, 28, 32)
h_pool1 = max_pool_2x2(h_conv1)
#print (h_pool1.get_shape()) # => (40000, 14, 14, 32)
# Prepare for visualization
# display 32 fetures in 4 by 8 grid
layer1 = tf.reshape(h_conv1, (-1, image_height, image_width, 4 ,8))  
# reorder so the channels are in the first dimension, x and y follow.
layer1 = tf.transpose(layer1, (0, 3, 1, 4,2))
layer1 = tf.reshape(layer1, (-1, image_height*4, image_width*8))

'''
# second convolutional layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
#print (h_conv2.get_shape()) # => (40000, 14,14, 64)
h_pool2 = max_pool_2x2(h_conv2)
#print (h_pool2.get_shape()) # => (40000, 7, 7, 64)
# Prepare for visualization
# display 64 fetures in 4 by 16 grid
layer2 = tf.reshape(h_conv2, (-1, 14, 14, 4 ,16))  # MODIF
# reorder so the channels are in the first dimension, x and y follow.
layer2 = tf.transpose(layer2, (0, 3, 1, 4,2))
layer2 = tf.reshape(layer2, (-1, 14*4, 14*16))
'''

# densely connected layer
W_fc1 = weight_variable([5 * 21 * 32, 1024])
b_fc1 = bias_variable([1024])
# (40000, 7, 7, 64) => (40000, 3136)
h_pool1_flat = tf.reshape(h_pool1, [-1, 5*21*32])
h_fc1 = tf.nn.relu(tf.matmul(h_pool1_flat, W_fc1) + b_fc1)
#print (h_fc1.get_shape()) # => (40000, 1024)

# dropout
keep_prob = tf.placeholder('float')
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# readout layer for deep net
W_fc2 = weight_variable([1024, labels_count])
b_fc2 = bias_variable([labels_count])
y = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
#print (y.get_shape()) # => (40000, 10)

# cost function
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# optimisation function
train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cross_entropy)
# evaluation
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))

# prediction function
#[0.1, 0.9, 0.2, 0.1, 0.1 0.3, 0.5, 0.1, 0.2, 0.3] => 1
predict = tf.argmax(y,1)

# start TensorFlow session
init = tf.initialize_all_variables()
sess = tf.InteractiveSession()
sess.run(init)

# visualisation variables
train_accuracies = []
validation_accuracies = []
x_range = []

display_step=1

for i in range(TRAINING_ITERATIONS):

    #get new batch
    batch_xs, batch_ys = next_batch(BATCH_SIZE)        
    # check progress on every 1st,2nd,...,10th,20th,...,100th... step
    if i%display_step == 0 or (i+1) == TRAINING_ITERATIONS:
        train_accuracy = accuracy.eval(feed_dict={x:batch_xs, y_: batch_ys, keep_prob: 1.0})       
        if(VALIDATION_SIZE):
            validation_accuracy = accuracy.eval(feed_dict={ x: validation_images[0:BATCH_SIZE], y_: validation_labels[0:BATCH_SIZE], keep_prob: 1.0})                                  
            print('training_accuracy / validation_accuracy => %.2f / %.2f for step %d'%(train_accuracy, validation_accuracy, i))
            validation_accuracies.append(validation_accuracy) 
        else:
            print('training_accuracy => %.4f for step %d'%(train_accuracy, i))
        train_accuracies.append(train_accuracy)
        x_range.append(i)
        
        # increase display_step
        if i%(display_step*10) == 0 and i:
            display_step *= 10
    # train on batch
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys, keep_prob: DROPOUT})

# check final accuracy on validation set  
if(VALIDATION_SIZE):
	validation_accuracy = accuracy.eval(feed_dict={x: validation_images, y_: validation_labels, keep_prob: 1.0})
	print('validation_accuracy => %.4f'%validation_accuracy)
	plt.plot(x_range, train_accuracies,'-b', label='Training')
	plt.plot(x_range, validation_accuracies,'-g', label='Validation')
	plt.legend(loc='lower right', frameon=False)
	plt.ylim(ymax = 1.1, ymin = 0.7)
	plt.ylabel('accuracy')
	plt.xlabel('step')
	plt.show()

layer1_grid = layer1.eval(feed_dict={x: validation_images[IMAGE_TO_DISPLAY:IMAGE_TO_DISPLAY+10], keep_prob: 1.0})
print 'should print feature map now'
plt.axis('off')
for i in range(0, 10):
	plt.imsave('./cnn_map_layer_1/' + str(i) + '_cnn_map_layer_1.png', layer1_grid[i], cmap=cm.seismic )
#plt.show()