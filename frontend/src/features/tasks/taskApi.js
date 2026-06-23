import { API_BASE_URL } from "../../config";

export async function fetchTasks() {
  const response = await fetch(`${API_BASE_URL}/api/tasks/`);

  if (!response.ok) {
    throw new Error("Failed to load tasks");
  }

  return response.json();
}