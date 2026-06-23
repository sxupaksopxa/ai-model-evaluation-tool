# AI Model Evaluation Tool

AI Model Evaluation Tool is a practical application for comparing AI models across common Natural Language Processing (NLP) tasks. The project helps users understand how different models perform, compare outputs side by side, and explore the strengths and limitations of modern AI systems.

Developed by BKlein Digital Labs.

## Overview

The tool provides a unified interface for evaluating multiple AI models on the same task and input. Users can compare outputs, latency, and model behavior while learning how different AI systems respond to practical NLP scenarios.

The project focuses on practical experimentation, model exploration, and understanding model behavior rather than benchmark scores.

## Status

Current status: MVP.

The project is under active development. Additional providers, models, and evaluation capabilities may be added in future releases.

## Features

### Supported Tasks

* Text Classification
* Summarization
* Entity Extraction
* Question Answering
* Semantic Similarity

### Supported Model Types

* Classification Models
* Summarization Models
* Question Answering Models
* Embedding Models
* Instruction-Tuned Language Models (LLMs)

### Evaluation Capabilities

* Multi-model comparison
* Side-by-side output review
* Latency measurement
* Detailed evaluation view
* Task-specific prompts
* Local model execution
* Local and OpenRouter model support
* Bring Your Own Key (BYOK) support
* Output quality validation
* Model behavior comparison
* Structured result analysis

### Testing & Validation

* Automated regression testing
* Model output verification
* Prompt leakage detection
* Over-generation detection
* Latency monitoring
* Markdown regression reports

### Privacy

* No data persistence
* In-memory evaluation processing
* API keys are not stored
* User-controlled API access (BYOK)

## Architecture

### Frontend

* React
* Vite

### Backend

* FastAPI

### Model Providers

* Local Models
* OpenRouter

### Testing

* Automated Regression Testing

## How It Works

1. Select a task.
2. Select one or more models.
3. If OpenRouter models are selected, provide an OpenRouter API key (BYOK).
4. Provide input text.
5. Run the evaluation.
6. Compare outputs, latency, and model behavior.
7. Review detailed model results.

## Bring Your Own Key (BYOK)

The tool supports local models and OpenRouter models.

* Local models do not require an API key.
* OpenRouter models require an OpenRouter API key.
* API keys are used only for the current evaluation request.
* API keys are not stored.
* Evaluations run in-memory only.
* API usage costs are billed directly through the user's OpenRouter account.

## Local Execution

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

Backend:

```text
http://localhost:8000
```

## Regression Testing

The project includes an automated regression testing framework to validate model behavior across supported NLP tasks.

The regression suite:

* Executes all supported task/model combinations.
* Validates model outputs against reference examples.
* Detects failures, warnings, prompt leakage, and over-generation.
* Measures response latency.
* Generates a detailed Markdown report for review.

Generated report:

```text
backend/scripts/regression_report.md
```

### Run Regression Tests

```bash
python backend/scripts/run_regression.py
```

For OpenRouter models:

```bash
export OPENROUTER_API_KEY=your_key_here
python backend/scripts/run_regression.py
```

## Current Limitations

* English-focused evaluation
* Limited number of built-in models
* No automated scoring framework
* No benchmark datasets included
* Local hardware impacts latency
* OpenRouter models require a user-provided API key

## Planned Improvements

* Additional open-source models
* Cost comparison
* Model statistics dashboard
* Evaluation history
* User ratings and feedback
* Export results
* Advanced prompt templates

## Use Cases

* AI model exploration
* Learning NLP concepts
* Model comparison
* Educational demonstrations
* Prompt experimentation
* AI capability assessment

## License

Licensed under the Apache License, Version 2.0.
See the LICENSE file for details.

## Author

BKlein Digital Labs

Building practical AI solutions for a digital world.