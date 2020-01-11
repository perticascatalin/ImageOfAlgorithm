import pickle
import numpy as np
import sys
from keras.models import Sequential
from keras.layers import Flatten, Dense, Conv2D, MaxPooling2D, LSTM
from default_plot import plotter

X_ploc = 'datasets/X_GPC_20_1000_0after.p'
y_ploc = 'datasets/y_GPC_20_1000_0after.p'
no_epochs = 4

task = X_ploc.split('/')[1].split('_')[1]
no_samples_per_class = int(X_ploc.split('/')[1].split('_')[3])
padding = X_ploc.split('/')[1].split('_')[4].split('.')[0]
print (task)
print (no_samples_per_class)
print (padding)

X = pickle.load(open(X_ploc, 'rb'))
print (X.shape)
y = pickle.load(open(y_ploc, 'rb'))
print (y.shape)

no_samples = X.shape[0]
max_length = X.shape[1]
no_features = X.shape[2]
no_classes = y.shape[1]

# MLP with one hidden layer
def mlp1():
	model = Sequential()
	model.add(Flatten(input_shape = (max_length, no_features)))
	model.add(Dense(1024, activation = 'relu'))
	model.add(Dense(no_classes, activation = 'softmax'))

	model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
	history = model.fit(X, y, validation_split = 0.2, epochs = no_epochs, batch_size = 20)

	fig_name = 'plots/mlp1_' + '_' + task + '_' + str(no_features) + '_' + str(no_samples_per_class) + '_' + padding + '.png'
	plotter(history, task, fig_name)

# CNN with one convolutional layer, one maxpool and one hidden layer
def cnn11():
	global X
	X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2], 1))

	model = Sequential()
	model.add(Conv2D(32, kernel_size = (2,2), strides = (1,1), activation = 'relu', input_shape = (max_length, no_features, 1)))
	model.add(MaxPooling2D(pool_size = (2,2)))
	model.add(Flatten())
	model.add(Dense(1024, activation = 'relu'))
	model.add(Dense(no_classes, activation = 'softmax'))

	model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
	history = model.fit(X, y, validation_split = 0.2, epochs = no_epochs, batch_size = 20)

	fig_name = 'plots/cnn11_' + '_' + task + '_' + str(no_features) + '_' + str(no_samples_per_class) + '_' + padding + '.png'
	plotter(history, task, fig_name)

	X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2]))

# LSTM with one layer
def lstm1():
	model = Sequential()
	model.add(LSTM(64, input_shape = (max_length, no_features)))
	model.add(Dense(no_classes, activation = 'softmax'))

	model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])
	history = model.fit(X, y, validation_split = 0.2, epochs = no_epochs, batch_size = 20)

	fig_name = 'plots/lstm1_' + '_' + task + '_' + str(no_features) + '_' + str(no_samples_per_class) + '_' + padding + '.png'
	plotter(history, task, fig_name)

mlp1()
cnn11()
lstm1()
