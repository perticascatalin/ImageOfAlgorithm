# Introduction to Program Induction
#### Tensorflow & Models

POSTER

## 1. Presentation overview

WHAT?

- The ability to generate, replicate or infer code using a computer.

HOW?

- **NOW**: Write programs for computer to execute.
- **RESEARCH**: Use data to develop models for writing programs
- **DREAM**: Let the computer write and execute its own program

![data](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/data.jpg)

HIGHLIGHTS

OVERVIEW OF PRESENTATION

- Part 2: Machine Learning Overview (types of problems in PI, CV and NLP)
- Part 3: Tensorflow Intro & Models
- Part 4: Program Induction Applications
- Parts 5, 6, 7: Further Ideas

*down to here should take around 10 minutes*

## 2. Problems solved using machine learning (add pictures, input -> output)

Computer Vision

Train with images to infer image properties:

- T1.hand-written digit recognition
- T2.object detection
- T3.segmentation

Natural Language Processing

Train with text to infer text properties

- T4.spam detection
- T5.sentiment analysis
- T6.translation

Program Induction

Train with code/IO pairs to infer code/IO pairs

- T7.program synthesis
- T8.neural programming
- T9.software applications (understand already written software):
  - defect prediction
  - semantics extraction, grouping
  - target areas

*down to here we have a total of 30 minutes*

## 3. Models

### Tensorflow (neural networks in browser)

Link: https://playground.tensorflow.org/

|Tensor|Flow|
|:----:|:--:|
|![tensor](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/tensor.png)|![flow](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/flow.png)|
|Computational Units|Computational Graphs|

### MLP

#### Formula/Theory

`activ(Wx + b) -> y`

#### TF code walkthrough

##### 3.1 Defining a Layer

```python
# Initialize Learnable Values
def network_layer(input_nodes, output_nodes):
  layer = {
    'weights': tf.Variable(tf.random_normal([input_nodes, output_nodes])),
    'biases': tf.Variable(tf.random_normal([output_nodes]))
  }
  return layer
```

To explain:

- `tf.Variable`
- `tf.random_normal`

##### 2.2 Defining a Model

```python
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
```

To explain:

- `tf.add`
- `tf.matmul`
- `tf.nn.relu`

##### 3.3 Defining a Training Procedure

```python
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
```

To explain:

- `tf.Session`, `sess.run`
- `tf.reduce_mean`
- `tf.equal`
- `tf.argmax`
- `tf.cast`
- `eval`
- `tf.nn.softmax_cross_entropy_with_logits`
- `tf.train.AdamOptimizer().minimize(cost)`
- `next_batch(batch_size)`

To explain better: 
- optimizer and gradient descent
- what a session is

=======
24 lines of code (1,2)
24 lines of code (3)
14 operations
TOTAL: 48 (lines), 14 (operations)

*down to here we have a total of 1 hour*

## 4. Program induction applications

### 4.1 Deep Coder

Link: https://www.microsoft.com/en-us/research/wp-content/uploads/2017/03/main.pdf

**Idea:** Use inference power of deep learning models to speed up search of target program. The target program is supposed to satisfy a list of input-output pairs.

**Walkthrough:**
  - specify domain specific language
  - encoding input-output pairs (multi-label multi-class problem, probability of attribute)
  - map input/output pairs to program attributes
  - narrow program search using predicted program attributes
  - program search through DFS on a grammar

|Problem Samples|Program Attributes|
|:----:|:--:|
|![problem](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/problem_samples.png)|![program](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/program_attributes.png)|
|Problem Samples|Program Attributes|

![deep coder](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/deep_coder.png)

### 4.2 Pix2Code

Link: https://arxiv.org/pdf/1705.07962.pdf

**Idea:** Learn to map graphical user interfaces to the code that generates them. This is done through a domain specific language and a compiler.

**Walkthrough:**
  - encoder LSTM
  - encoder CNN
  - decoder LSTM
  - end-to-end learning

![pix2code](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/pix2code.png)

![gui](https://raw.githubusercontent.com/perticascatalin/ImageOfAlgorithm/master/misc/images/gui.png)

*down to here we have a total of 1 hour and a half*

## 5. Challenges

- Finding meaningful program representations which can be
learned statistically
- Embedding together different types of representations
- Modelling the cognitive patterns which enable code
generation

## 6. Interesting Subjects

Solving problems in physics: https://arxiv.org/abs/1910.07291
Solving graph problems: https://www.gwern.net/docs/rl/2016-graves.pdf