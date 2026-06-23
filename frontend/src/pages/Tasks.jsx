import { fetchTasks } from "../features/tasks/taskApi";
import { useEffect, useState } from "react";

export default function Tasks() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/tasks`)
      .then((res) => res.json())
      .then((data) => setTasks(data))
      .catch((error) => {
      });
  }, []);

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <h1 className="text-3xl font-bold text-slate-900">Evaluation Tasks</h1>

      <p className="mt-3 max-w-3xl text-slate-600">
        The AI Model Evaluation Tool compares model behavior across practical
        language tasks.
      </p>

      <section className="tasks-grid">
        {tasks.map((task) => (
        <article key={task.id} className="task-card">
          <h2>{task.name}</h2>

          <p className="task-description">
            {task.description}
          </p>

          <div className="task-example-block">
            <p className="task-example-label">
              Example Input
            </p>

            <div className="task-example-box">
              {task.example_input}
            </div>
          </div>

          <div className="task-example-block">
            <p className="task-example-label">
              Example Output
            </p>

          <div className="task-output-box">
            {task.example_output}
          </div>
        </div>
      </article>
      ))}
      </section> 
    </main>
  );
}