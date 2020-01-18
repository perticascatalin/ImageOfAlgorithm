import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Constants for multilayer perceptron
n_nodes_input = 420
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500
n_classes = 10
n_epochs = 30
batch_size = 100

BATCH_SIZE = 50
VALIDATION_SIZE = 2000
IMAGE_TO_DISPLAY = 11

# Display image
def display(img):
	one_image = img.reshape(image_height, image_width)
	plt.axis('off')
	plt.imshow(one_image, cmap=cm.binary)
	plt.show()

def network_layer(input_nodes, output_nodes):
	layer = {
		'weights': tf.Variable(tf.random_normal([input_nodes, output_nodes])),
		'biases': tf.Variable(tf.random_normal([output_nodes]))
	}
	return layer

def model_network_3_hidden(data):
	# Network Architecture
	hidden_1_layer = network_layer(n_nodes_input, n_nodes_hl1)
	hidden_2_layer = network_layer(n_nodes_hl1, n_nodes_hl2)
	hidden_3_layer = network_layer(n_nodes_hl2, n_nodes_hl3)
	output_layer = network_layer(n_nodes_hl3, n_classes)
	# Computation Pipeline
	l1 = tf.nn.relu(tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases']))
	l2 = tf.nn.relu(tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases']))
	l3 = tf.nn.relu(tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases']))
	output = tf.add(tf.matmul(l3, output_layer['weights']), output_layer['biases'])
	return output

def train_network_3_hidden(x):
	# Hypothesis
	prediction = model_network_3_hidden(x)
	# Loss/Cost Function
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction, y_))
	# Optimization Function (Gradient Descent)
	optimizer = tf.train.AdamOptimizer().minimize(cost)
	# Launch tensorflow session
	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())
		for epoch in range(n_epochs):
			epoch_cost = 0
			for _ in range(num_examples/batch_size):
				# Perform gradient descent in batches (Memory Consumption reasons)
				batch_x, batch_y = next_batch(batch_size)
				_, batch_cost = sess.run([optimizer, cost], feed_dict = {x: batch_x, y_: batch_y})
				epoch_cost += batch_cost
			print ('Epoch', epoch, 'completed out of', n_epochs, 'cost:', epoch_cost)

		correct = tf.equal(tf.argmax(prediction,1), tf.argmax(y_,1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
		print ('Accuracy:', accuracy.eval({x:validation_images, y_:validation_labels}))

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

	return images, labels

images, labels = process_data(location = './data/IOA_IBHQR_ID/train_1000.csv', arr_size = 10)
# Uncomment following line if you want to output a certain image     
# display(images[IMAGE_TO_DISPLAY])

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

# Uncomment following line to run multilayer neural network
train_network_3_hidden(x)

