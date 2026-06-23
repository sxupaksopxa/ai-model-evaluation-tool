export default function TaskSelector({ tasks, selectedTaskId, onChange }) {
  return (
    <div className="field">
      <label
        htmlFor="task-select"
        className="field-title"
      >
        Task type
      </label>
      
      <p className="field-help">
        Choose the evaluation task you want to run.
      </p>

      <select
        id="task-select"
        name="task"
        value={selectedTaskId}
        onChange={(event) =>
          onChange(event.target.value)
        }
        >
        <option value="">
          Select a task
        </option>

        {tasks.map((task) => (
          <option
          key={task.id}
          value={task.id}
        >
        {task.name}
          </option>
        ))}
      </select>
    </div>
  );
}