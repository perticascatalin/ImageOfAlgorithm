# Image of Algorithm

Repository for all experiments performed in the area of detection, emulation and clustering of programs based on execution traces.

## Experiments

### 1. Sorting

### 2. Detection

### 3. Classification

- algorithms.py: implementation for IOAs
- extractor.py: extracts features from IOAs
- generator.py: generates IOAs and saves them to csv (any length)
- process.py: prepares IOAs for training (standardizes length)
- models.py: training and validation MLP, CNN & LSTM with IOAs
- default_plot.py: plots training and validation results

### 4. Clustering

### 5. Emulation

## Ideas from Notebook

### First IOA

The ability to group programs based on their semantics.

### Second IOA

The ability to interact with the programs learned from  (to emulate/predict).

### Similar to 2 Mentors

First one behaves like an oracle: only provides the right answers.
Second one describes the thought process, so the observer can see how certain answers are arrived to.
