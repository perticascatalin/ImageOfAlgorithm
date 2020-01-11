import matplotlib.pyplot as plt

def plotter(history, task, fig_name):
	plt.plot(history.history['acc'])
	plt.plot(history.history['val_acc'])
	plt.title(task + ' ' + 'accuracy')
	plt.ylabel('accuracy')
	plt.xlabel('epoch')
	plt.legend(['train', 'validation'], loc = 'upper left')
	plt.savefig(fig_name)
	plt.clf()