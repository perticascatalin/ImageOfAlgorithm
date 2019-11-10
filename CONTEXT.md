# Introduction to Program Induction (Tensorflow & Models)

## 1. Introduction to introduction

WHAT?

- The ability to generate, replicate or infer code using a computer.

HOW?

- **NOW**: Write programs for computer to execute.
- **RESEARCH**: Use data to develop models for writing programs
- **DREAM**: Let the computer write and execute its own program

## 2. Tests

	> This is a blockquote
	> inside a list item.
	
<p>This is a normal paragraph:</p>

<pre><code># Sample program
include tensorflow as tf
num_steps = 1000
</code></pre>

Python syntax highlight:

```python
include tensorflow as tf
num_steps = 1000
def foo():
  a = 2
  b = 3
  return a + b
s = foo()
s = "Python syntax highlighting"
print s
```

## 3. Models

### MLP

#### Formula/Theory

`activ(Wx + b) -> y`

#### TF code walkthrough

##### 1. Defining a Layer

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

##### 2. Defining a Model

```python
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

## 4. Program induction applications

## 5. Challenges

- Finding meaningful program representations which can be
learned statistically
- Embedding together different types of representations
- Modelling the cognitive patterns which enable code
generation