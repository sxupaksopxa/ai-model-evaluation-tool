import { API_BASE_URL } from "/src/config.js";

export async function runEvaluation(payload) {
  const response = await fetch(
    `${API_BASE_URL}/api/evaluations/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Evaluation failed"
    );
  }

  return data;
}

export async function* runEvaluationStream(payload) {
  const response = await fetch(
    `${API_BASE_URL}/api/evaluations/stream`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Evaluation failed");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const chunks = buffer.split("\n\n");
    buffer = chunks.pop(); // keep incomplete chunk

    for (const chunk of chunks) {
      if (chunk.startsWith("data: ")) {
        const data = chunk.slice(6);
        if (data === "[DONE]") return;

        const parsed = JSON.parse(data);
        if (parsed.error) {
          throw new Error(parsed.error);
        }
        yield parsed;
      }
    }
  }
}
