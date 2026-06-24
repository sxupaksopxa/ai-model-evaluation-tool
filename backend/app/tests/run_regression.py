import json
import requests
import os
from pathlib import Path
from datetime import datetime


API_BASE_URL = "http://localhost:8000"
API_EVALUATIONS_URL = f"{API_BASE_URL}/api/evaluations/"
API_MODELS_URL = f"{API_BASE_URL}/api/models"

TASK_REGISTRY_PATH = Path(__file__).resolve().parent.parent / "datasets" / "seed" / "task_registry.json"
REPORT_PATH = Path(__file__).resolve().parent / "regression_report.md"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def load_tasks():
    with TASK_REGISTRY_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def clean_markdown_table_text(value, max_length=180):
    if value is None:
        return "null"

    text = str(value)
    text = text.replace("\n", " ")
    text = text.replace("|", "\\|")
    text = " ".join(text.split())

    if len(text) > max_length:
        return text[:max_length] + "..."

    return text


def extract_expected_keywords(task):
    expected_output = task.get("example_output", "")

    return [
        word.strip(".,:;()[]{}<>").lower()
        for word in expected_output.split()
        if len(word.strip(".,:;()[]{}<>")) > 4
    ]


def detect_output_issues(output_text):
    lowered = output_text.lower()

    issue_markers = [
        "input:",
        "test case",
        "example:",
        "def ",
        "print(",
        "you are an ai assistant",
        "as an ai",
    ]

    detected = [
        marker
        for marker in issue_markers
        if marker in lowered
    ]

    return detected


def describe_result(task, model_result):
    status = model_result.get("status")
    output = model_result.get("output")
    latency = model_result.get("latency_ms")
    error = model_result.get("error")

    def is_entity_output(output):
      return (
        isinstance(output, dict)
        and "persons" in output
        and "organizations" in output
        and "locations" in output
        and "misc" in output
      )

    if status != "success":
        if error:
            return "FAIL", f"Model failed with error: {clean_markdown_table_text(error, 120)}"
        return "FAIL", f"Model returned status `{status}`."

    if output is None or str(output).strip() == "":
        return "FAIL", "Output is empty or null."
    
    if is_entity_output(output):
        has_any_entity = any(
            output.get(key)
            for key in [
                "persons",
                "organizations",
                "locations",
                "misc",
            ]
        )

        if has_any_entity:
            return (
                "PASS",
                "Structured entity output returned with at least one detected entity."
            )

        return (
            "WARNING",
            "Structured entity output returned, but no entities were detected."
        )

    output_text = str(output).strip()

    expected_keywords = extract_expected_keywords(task)
    matched_keywords = [
        word for word in expected_keywords
        if word in output_text.lower()
    ]

    output_issues = detect_output_issues(output_text)

    if output_issues:
        return (
            "WARNING",
            "Output is present but contains possible over-generation or prompt leakage: "
            + ", ".join(output_issues)
        )

    if len(output_text) > 1000:
        return "WARNING", "Output is present but very long. Model may be over-generating."

    if latency and latency > 10000:
        return "WARNING", "Output is present, but latency is high."

    if expected_keywords and not matched_keywords:
        return "WARNING", "Output exists but does not clearly match the example output keywords."

    return "PASS", "Output is present and broadly matches expected task behavior."


def get_models_for_task(task_id):
    response = requests.get(
        API_MODELS_URL,
        params={"task_id": task_id},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def run_task(task):
    models = get_models_for_task(task["id"])

    model_ids = [
        model["id"]
        for model in models
    ]

    if not model_ids:
        return None, "No supported models found for this task."

    payload = {
        "task_id": task["id"],
        "model_ids": model_ids,
        "input_text": task["example_input"],
        "api_keys": {
          "openrouter": OPENROUTER_API_KEY,
          } if OPENROUTER_API_KEY else {},
    }

    response = requests.post(
        API_EVALUATIONS_URL,
        json=payload,
        timeout=300,
    )

    response.raise_for_status()
    return response.json(), None


def main():
    tasks = load_tasks()

    lines = [
        "# Regression Test Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "Purpose: verify all supported task/model combinations after code changes.",
        "",
        "## Summary",
        "",
    ]

    total = 0
    passed = 0
    warnings = 0
    failed = 0

    task_sections = []

    for task in tasks:
        task_sections.append(f"## Task: {task['name']}")
        task_sections.append("")
        task_sections.append(f"Task ID: `{task['id']}`")
        task_sections.append("")
        task_sections.append("### Input")
        task_sections.append("")
        task_sections.append("```text")
        task_sections.append(task.get("example_input", ""))
        task_sections.append("```")
        task_sections.append("")

        if task.get("example_output"):
            task_sections.append("### Expected Reference Output")
            task_sections.append("")
            task_sections.append("```text")
            task_sections.append(task.get("example_output", ""))
            task_sections.append("```")
            task_sections.append("")

        try:
            result, error = run_task(task)

        except Exception as exc:
            failed += 1
            task_sections.append(f"**Task execution failed:** {str(exc)}")
            task_sections.append("")
            continue

        if error:
            warnings += 1
            task_sections.append(f"**Result:** WARNING - {error}")
            task_sections.append("")
            continue

        task_sections.append("### Model Results")
        task_sections.append("")
        task_sections.append(
            "| Model | Provider | Status | Latency | Output Preview | Feedback |"
        )
        task_sections.append(
            "|---|---|---:|---:|---|---|"
        )

        for model_result in result.get("results", []):
            total += 1

            verdict, feedback = describe_result(
                task,
                model_result,
            )

            if verdict == "PASS":
                passed += 1
            elif verdict == "WARNING":
                warnings += 1
            else:
                failed += 1

            output_preview = clean_markdown_table_text(
                model_result.get("output"),
                max_length=180,
            )

            latency = (
                f"{model_result.get('latency_ms')} ms"
                if model_result.get("latency_ms") is not None
                else "N/A"
            )

            task_sections.append(
                "| "
                f"{clean_markdown_table_text(model_result.get('model_name'))} | "
                f"{clean_markdown_table_text(model_result.get('provider'))} | "
                f"{verdict} | "
                f"{latency} | "
                f"{output_preview} | "
                f"{clean_markdown_table_text(feedback, 220)} |"
            )

        task_sections.append("")

    lines.append(f"- Total model checks: {total}")
    lines.append(f"- Passed: {passed}")
    lines.append(f"- Warnings: {warnings}")
    lines.append(f"- Failed: {failed}")
    lines.append("")
    lines.extend(task_sections)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Regression report generated: {REPORT_PATH}")


if __name__ == "__main__":
    main()