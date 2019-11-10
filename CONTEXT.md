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

## 4. Program induction applications

## 5. Challenges

- Finding meaningful program representations which can be
learned statistically
- Embedding together different types of representations
- Modelling the cognitive patterns which enable code
generation