# Initialize Learnable Values
def network_layer(input_nodes, output_nodes):
  layer = {
    'weights': tf.Variable(tf.random_normal([input_nodes, output_nodes])),
    'biases': tf.Variable(tf.random_normal([output_nodes]))
  }
  return layer

# Create Computation Graph
def network_model(data, layer_sizes):
  # Network Architecture
  hidden_layers = []
  hidden_layers.append(network_layer(n_nodes_input, layer_sizes[0]))
  for i in range(1, len(layer_sizes)):
    hidden_layers.append(network_layer(layer_sizes[i-1], layer_sizes[i]))
  output_layer = network_layer(layer_sizes[-1], n_classes)
  # Computation Pipeline
  activations = []
  activations.append(tf.nn.relu(tf.add(tf.matmul(data, hidden_layers[0]['weights']), hidden_layers[0]['biases'])))
  for i in range(1, len(layer_sizes)):
    activations.append(tf.nn.relu(tf.add(tf.matmul(activations[i-1], hidden_layers[i]['weights']), hidden_layers[i]['biases'])))
  output = tf.add(tf.matmul(activations[-1], output_layer['weights']), output_layer['biases'])
  return output

def network_train(x, layer_sizes):
  # Hypothesis
  prediction = network_model(x, layer_sizes)
  # Loss/Cost Function
  cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = prediction, labels = y_))
  # Optimization Function (Gradient Descent)
  optimizer = tf.train.AdamOptimizer().minimize(cost)
  obtained_accuracy = 0.0
  # Launch tensorflow session
  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
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
    obtained_accuracy = accuracy.eval({x:validation_samples, y_:validation_labels})
    print ('Accuracy:', obtained_accuracy)
  return obtained_accuracy