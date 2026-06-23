def build_openrouter_prompt(
    task_id: str,
    input_text: str,
) -> str:
    prompts = {
        "classification": f"""
You are a sentiment classification assistant.

Classify the sentiment of the following text using exactly one label:
- Positive
- Neutral
- Negative

Text:
{input_text}

Return exactly:

Classification: <Positive|Neutral|Negative>

Reason: <one short sentence>
""",

        "summarization": f"""
You are a summarization assistant.

Summarize the following text clearly and concisely.

Text:
{input_text}

Return exactly:

Summary: <summary>
""",

        "entity_extraction": f"""
You are an entity extraction assistant.

Extract entities from the following text.

Entity types:
- persons
- organizations
- locations
- misc

Text:
{input_text}

Return ONLY valid JSON in this format:

{{
  "persons": [],
  "organizations": [],
  "locations": [],
  "misc": []
}}
""",

        "question_answering": f"""
You are a question answering assistant.

Answer the question using only the provided context.

{input_text}

Return exactly:

Answer: <answer>

Reason: <one short sentence>
""",
    }

    if task_id not in prompts:
        raise ValueError(
            f"Unsupported OpenRouter task_id: {task_id}"
        )

    return prompts[task_id]