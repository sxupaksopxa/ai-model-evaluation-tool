from app.modules.providers.base import BaseProvider
from transformers import (pipeline,
                          AutoTokenizer,
                          AutoModelForSeq2SeqLM,
                          AutoModelForSequenceClassification,
                          AutoModelForQuestionAnswering)

from sentence_transformers import (SentenceTransformer,
                                   util)
import json
import torch
import torch.nn.functional as F
import asyncio

_DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

_GENERATORS = {}

async def get_generator(model_ref):
    if model_ref not in _GENERATORS:
        _GENERATORS[model_ref] = await asyncio.to_thread(
            pipeline,
            "text-generation",
            model=model_ref,
            device_map="auto",
        )
    return _GENERATORS[model_ref]

_NER_PIPELINES = {}

async def get_ner_pipeline(model_ref):
    if model_ref not in _NER_PIPELINES:
        _NER_PIPELINES[model_ref] = await asyncio.to_thread(
            pipeline,
            "token-classification",
            model=model_ref,
            aggregation_strategy="simple",
            device_map="auto",
        )
    return _NER_PIPELINES[model_ref]

_SUMMARIZERS = {}

async def get_summarizer(model_ref):
    if model_ref not in _SUMMARIZERS:
        tokenizer = await asyncio.to_thread(
            AutoTokenizer.from_pretrained,
            model_ref,
        )
        model = await asyncio.to_thread(
            AutoModelForSeq2SeqLM.from_pretrained,
            model_ref,
        )
        if _DEVICE != "cpu":
            model = model.to(_DEVICE)
        _SUMMARIZERS[model_ref] = {
            "tokenizer": tokenizer,
            "model": model,
        }
    return _SUMMARIZERS[model_ref]

_CLASSIFIERS = {}
_TOKENIZERS = {}

async def get_classifier(model_ref):
    if model_ref not in _CLASSIFIERS:
        _TOKENIZERS[model_ref] = await asyncio.to_thread(
            AutoTokenizer.from_pretrained,
            model_ref,
        )
        model = await asyncio.to_thread(
            AutoModelForSequenceClassification.from_pretrained,
            model_ref,
        )
        if _DEVICE != "cpu":
            model = model.to(_DEVICE)
        _CLASSIFIERS[model_ref] = model
    return (
        _TOKENIZERS[model_ref],
        _CLASSIFIERS[model_ref],
    )

_QA_MODELS = {}
_QA_TOKENIZERS = {}

async def get_qa_model(model_ref):
    if model_ref not in _QA_MODELS:
        _QA_TOKENIZERS[model_ref] = await asyncio.to_thread(
            AutoTokenizer.from_pretrained,
            model_ref,
        )
        model = await asyncio.to_thread(
            AutoModelForQuestionAnswering.from_pretrained,
            model_ref,
        )
        if _DEVICE != "cpu":
            model = model.to(_DEVICE)
        _QA_MODELS[model_ref] = model
    return (
        _QA_TOKENIZERS[model_ref],
        _QA_MODELS[model_ref],
    )

_EMBEDDING_MODELS = {}

async def get_embedding_model(model_ref):
    if model_ref not in _EMBEDDING_MODELS:
        _EMBEDDING_MODELS[model_ref] = await asyncio.to_thread(
            SentenceTransformer,
            model_ref,
            device=_DEVICE,
        )
    return _EMBEDDING_MODELS[model_ref]

class LocalProvider(BaseProvider):

    async def run(
      self,
      model: dict,
      task_id: str,
      prompt: str,
      api_keys: dict[str, str] | None = None,
    ):

      if model["type"] == "ner":
        return await self._run_ner(
          model,
          prompt,
        )

      elif model["type"] == "llm":
        return await self._run_llm(
          model,
          task_id,
          prompt,
        )

      elif model["type"] == "summarization":
        return await self._run_summarization(
          model,
          task_id,
          prompt,
        )

      elif model["type"] == "classification":
        return await self._run_classification(
          model,
          task_id,
          prompt,
        )

      elif model["type"] == "question_answering":
        return await self._run_question_answering(
          model,
          task_id,
          prompt,
        )

      elif model["type"] == "embedding":
        if task_id == "semantic_similarity":
          return await self._run_semantic_similarity(
            model,
            task_id,
            prompt,
          )

      raise ValueError(
        f"Unsupported model type: {model['type']}"
      )

    async def _run_ner(
      self,
      model: dict,
      prompt: str,
      ):
        ner = await get_ner_pipeline(model["model_ref"])

        output = await asyncio.to_thread(ner, prompt)

        entities = {
          "persons": [],
          "organizations": [],
          "locations": [],
          "misc": [],
        }

        scores = []

        for item in output:
          scores.append(float(item["score"]))

          if item["entity_group"] == "PER":
            entities["persons"].append(item["word"])

          elif item["entity_group"] == "ORG":
            entities["organizations"].append(item["word"])

          elif item["entity_group"] == "LOC":
            entities["locations"].append(item["word"])

          elif item["entity_group"] == "MISC":
            entities["misc"].append(item["word"])

        average_score = (
          round(sum(scores) / len(scores), 3)
          if scores
            else None
        )

        for entity in output:
          for key, value in entity.items():
            if hasattr(value, "item"):
              entity[key] = value.item()

        return {
          "output": entities,
          "score": average_score,
          "estimated_cost": "Local",
          "raw_response": output,
        }

    async def _run_llm(
        self,
        model: dict,
        task_id: str,
        prompt: str,
    ):

      max_tokens_by_task = {
        "classification": 50,
        "summarization": 180,
        "entity_extraction": 256,
        "question_answering": 120,
      }

      max_new_tokens = max_tokens_by_task.get(task_id, 128)

      if task_id == "entity_extraction":
        llm_prompt = f"""
        Extract entities from the text.

        Rules:
        - Identify persons.
        - Identify organizations.
        - Identify locations.
        - Identify miscellaneous entities.
        - A company, employer, bank, government body, university or business name is an organization.
        - Return ONLY JSON.
        - Do not explain.

        Text:
        {prompt}

        Output:
        """

      else:
        llm_prompt = prompt

      generator = await get_generator(
          model["model_ref"]
        )

      result = await asyncio.to_thread(
          generator,
          llm_prompt,
          max_new_tokens=max_new_tokens,
          do_sample=False,
          return_full_text=False,
        )

      output = result[0]["generated_text"].strip()

      if task_id in ["classification", "question_answering"]:
        output = output.split("\n\nInput:", 1)[0].strip()
        output = output.split("\nInput:", 1)[0].strip()

      if not output or output.lower() in {
    "reason:",
    "label:",
    "output:",
}:
        return {
          "output": "No meaningful output returned by this model.",
          "score": None,
          "estimated_cost": "Local",
          "raw_response": result,
        }

      try:
          parsed_output = json.loads(output)

      except (json.JSONDecodeError, TypeError):
          parsed_output = output

      return {
          "output": parsed_output,
          "score": None,
          "estimated_cost": "Local",
          "raw_response": result,
        }

    async def _run_summarization(
      self,
      model: dict,
      task_id: str,
      prompt: str,
    ):

      summarizer = await get_summarizer(
        model["model_ref"]
      )

      tokenizer = summarizer["tokenizer"]
      model_obj = summarizer["model"]

      input_text = prompt

      if model["id"] in ["t5_small", "bart_base"]:

        if "Text:" in prompt:
          input_text = prompt.split("Text:", 1)[1].strip()

        if model["id"] == "t5_small":
          input_text = f"summarize: {input_text}"

      inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
      )

      if _DEVICE != "cpu":
        inputs = {k: v.to(_DEVICE) for k, v in inputs.items()}

      summary_ids = await asyncio.to_thread(
        model_obj.generate,
        **inputs,
        max_new_tokens=80,
        min_new_tokens=10,
        do_sample=False,
      )

      summary = await asyncio.to_thread(
        tokenizer.decode,
        summary_ids[0],
        skip_special_tokens=True,
      )

      return {
        "output": summary,
        "score": None,
        "estimated_cost": "Local",
        "raw_response": None,
      }

    async def _run_classification(
      self,
      model: dict,
      task_id: str,
      prompt: str,
    ):

      tokenizer, classifier = await get_classifier(
        model["model_ref"]
      )

      inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
      )

      if _DEVICE != "cpu":
        inputs = {k: v.to(_DEVICE) for k, v in inputs.items()}

      with torch.no_grad():
        outputs = await asyncio.to_thread(classifier, **inputs)

      probabilities = torch.softmax(
        outputs.logits,
        dim=-1,
      )[0]

      predicted_id = torch.argmax(
        probabilities
      ).item()

      label = classifier.config.id2label[
        predicted_id
      ]

      confidence = round(
        probabilities[predicted_id].item(),
        3,
      )

      return {
        "output": label,
        "score": confidence,
        "estimated_cost": "Local",
        "raw_response": {
            "label": label,
            "confidence": confidence,
        },
      }

    async def _run_question_answering(
      self,
      model: dict,
      task_id: str,
      prompt: str,
    ):

      if "Context:" not in prompt:
        return {
            "output": "Invalid QA input. Expected Question and Context.",
            "score": None,
            "estimated_cost": "Local",
            "raw_response": None,
        }

      tokenizer, qa_model = await get_qa_model(
        model["model_ref"]
      )

      parts = prompt.split("Context:", 1)

      question = (
        parts[0]
        .replace("Question:", "")
        .strip()
      )

      context = parts[1].strip()

      if not question or not context:
        return {
            "output": "Invalid QA input. Question and Context cannot be empty.",
            "score": None,
            "estimated_cost": "Local",
            "raw_response": None,
        }

      inputs = tokenizer(
        question,
        context,
        return_tensors="pt",
        truncation=True,
      )

      if _DEVICE != "cpu":
        inputs = {k: v.to(_DEVICE) for k, v in inputs.items()}

      with torch.no_grad():
        outputs = await asyncio.to_thread(qa_model, **inputs)

      start_idx = torch.argmax(
        outputs.start_logits
      ).item()

      end_idx = torch.argmax(
        outputs.end_logits
      ).item() + 1

      if end_idx <= start_idx:
        return {
            "output": "No answer found.",
            "score": None,
            "estimated_cost": "Local",
            "raw_response": {
                "question": question,
                "context": context,
            },
        }

      answer = tokenizer.decode(
        inputs["input_ids"][0][start_idx:end_idx],
        skip_special_tokens=True,
      ).strip()

      confidence = round(
        (
            torch.max(outputs.start_logits)
            + torch.max(outputs.end_logits)
        ).item()
        / 2,
        3,
      )

      return {
        "output": answer or "No answer found.",
        "score": confidence,
        "estimated_cost": "Local",
        "raw_response": {
            "question": question,
            "context": context,
            "answer": answer,
        },
      }

    async def _run_semantic_similarity(
      self,
      model: dict,
      task_id: str,
      prompt: str,
    ):
      try:

        data = json.loads(prompt)
        text_a = data.get("text_a", "")
        text_b = data.get("text_b", "")

      except (json.JSONDecodeError, TypeError):
        if "Text A:" in prompt and "Text B:" in prompt:
          parts = prompt.split("Text B:", 1)

          text_a = (
            parts[0]
            .replace("Text A:", "")
            .strip()
          )

          text_b = parts[1].strip()
        else:
          return {
            "output": "Invalid input format. Expected text_a and text_b.",
            "score": None,
            "estimated_cost": "Local",
            "raw_response": None,
          }

        if not text_a.strip() or not text_b.strip():
          return {
            "output": "Both Text A and Text B are required.",
            "score": None,
            "estimated_cost": "Local",
            "raw_response": None,
        }

        embedding_model = await get_embedding_model(
          model["model_ref"]
        )

        embedding_a = await asyncio.to_thread(
          embedding_model.encode,
          text_a,
          convert_to_tensor=True,
        )

        embedding_b = await asyncio.to_thread(
          embedding_model.encode,
          text_b,
          convert_to_tensor=True,
        )

        similarity = (
          await asyncio.to_thread(
            util.cos_sim,
            embedding_a,
            embedding_b,
          )
        ).item()

        score = round(similarity, 3)

        if score >= 0.9:
          interpretation = "Very High Similarity"
        elif score >= 0.75:
          interpretation = "High Similarity"
        elif score >= 0.5:
          interpretation = "Moderate Similarity"
        elif score >= 0.25:
          interpretation = "Low Similarity"
        else:
          interpretation = "Very Low Similarity"

        return {
          "output": f"Similarity Score: {score} — {interpretation}",
          "score": score,
          "estimated_cost": "Local",
          "raw_response": {
            "text_a": text_a,
            "text_b": text_b,
            "similarity": score,
            "interpretation": interpretation,
          },
        }
