# AI Model Evaluation Tool - User Manual

## Introduction

AI Model Evaluation Tool helps users compare the performance of multiple AI models across common Natural Language Processing (NLP) tasks.

The application allows users to submit the same input to multiple models and review the generated outputs, response times, and detailed evaluation information.

Developed by BKlein Digital Labs.

---

# Getting Started

## Step 1: Select a Task

Choose one of the available evaluation tasks from the Task dropdown list.

Available tasks:

* Classification
* Summarization
* Entity Extraction
* Question Answering
* Semantic Similarity

Each task evaluates a different AI capability.

---

## Step 2: Select Models

Choose one or more AI models.

You may:

* Select a single model
* Compare multiple models
* Use "Select All" to evaluate all available models for the selected task

Only models supporting the selected task are displayed.

---

## Step 3: Enter Input

Provide input text appropriate for the selected task.

Examples:

### Classification

Input:

```text
The customer was very satisfied with the service.
```

### Summarization

Input:

```text
The company's quarterly revenue increased by 15% compared to the previous quarter. Customer retention improved significantly due to new marketing initiatives.
```

### Entity Extraction

Input:

```text
John Smith works at Microsoft in Seattle.
```

### Question Answering

Input:

```text
Question:
What is the capital of Austria?

Context:
Austria is a country in Central Europe.
Vienna is the capital of Austria.
```

### Semantic Similarity

Input:

```text
Text A: The meeting starts at 10 AM.

Text B: The meeting begins at 10 o'clock.
```

---

## Step 4: Run Evaluation

Click:

```text
Run Evaluation
```

The application will:

1. Process the input.
2. Send the request to selected models.
3. Collect outputs.
4. Display results.

A loading indicator appears while processing.

---

# Understanding Results

## Results Table

The results table displays:

* Model Name
* Provider
* Status
* Latency
* Cost
* View Details

### Status

Possible values:

* Success
* Failed

### Latency

Response time in milliseconds.

Lower latency indicates faster model performance.

### Cost

Current version primarily uses local models.

Examples:

```text
Local
```

Future versions may include API-based models.

---

# Viewing Details

Click:

```text
View
```

to open the detailed result page.

The details page displays:

* Task
* Input
* Model
* Output
* Analysis
* Latency
* Cost

This view is useful when comparing model behavior.

---

# Task Guide

## Classification

Purpose:

Assign a category or label to text.

Typical use cases:

* Sentiment Analysis
* Topic Classification
* Intent Detection

---

## Summarization

Purpose:

Generate a concise summary of longer content.

Typical use cases:

* Reports
* Articles
* Meeting Notes

---

## Entity Extraction

Purpose:

Identify named entities within text.

Supported entity types:

* Persons
* Organizations
* Locations
* Miscellaneous

Typical use cases:

* Information Extraction
* Data Processing
* Document Analysis

---

## Question Answering

Purpose:

Answer a question using the supplied context.

Typical use cases:

* Knowledge Retrieval
* Document Question Answering
* Educational Examples

---

## Semantic Similarity

Purpose:

Measure how similar two texts are in meaning.

Example:

```text
Text A:
The meeting starts at 10 AM.

Text B:
The meeting begins at 10 o'clock.
```

Output example:

```text
Similarity Score: 0.97
Very High Similarity
```

Typical use cases:

* Duplicate Detection
* Search
* Retrieval Systems
* RAG Applications

---

# Supported Model Categories

## Classification Models

Examples:

* DistilBERT Sentiment
* RoBERTa Sentiment

---

## Summarization Models

Examples:

* T5 Small
* BART Base

---

## Embedding Models

Examples:

* BGE Base
* all-MiniLM-L6-v2

---

## Instruction-Tuned LLMs

Examples:

* Qwen Small Instruct
* Phi-3 Mini

---

# Tips

* Compare multiple models for the same input.
* Review latency as well as output quality.
* Use the Details page for deeper analysis.
* Test both short and long inputs.
* Experiment with different task types.

---

# Known Limitations

* English-focused evaluation.
* Results depend on selected models.
* Local hardware impacts performance.
* Some models may require additional downloads on first use.

---

# Feedback

Feedback and suggestions are welcome.

BKlein Digital Labs