import { API_BASE_URL } from "../../config";

export async function fetchModels(taskId) {
  const url = taskId
    ? `${API_BASE_URL}/api/models/?task_id=${taskId}`
    : `${API_BASE_URL}/api/models/`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to load models");
  }

  return response.json();
}