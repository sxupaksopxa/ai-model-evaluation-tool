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