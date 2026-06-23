def build_prompt(task_id: str, input_text: str) -> str:

    if task_id == "semantic_similarity":
        return input_text

    
    prompts = {
        "classification": f"""
          Classify the following business text.

          Text:
          {input_text}

          Return only a short classification and reason.
        """,

        "summarization": f"""
Summarize the following business text clearly and concisely.

Text:
{input_text}
""",

        "entity_extraction": f"""
Extract entities from the text.

Return ONLY valid JSON.

{{
  "persons": [],
  "organizations": [],
  "locations": [],
  "misc": []
}}

Text:
{input_text}
""",

        "question_answering": f"""
          Answer the question using the provided context.

          Input:
          {input_text}

          Return:
          Answer:
        """,
    }

    if task_id not in prompts:
        raise ValueError(f"Unsupported task_id: {task_id}")

    return prompts[task_id]