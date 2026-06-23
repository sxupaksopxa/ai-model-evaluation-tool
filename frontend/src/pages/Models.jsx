import { useEffect, useState } from "react";
import { fetchModels } from "../features/models/modelApi";

function Models() {
  const [models, setModels] = useState([]);

  useEffect(() => {
    fetchModels()
      .then(setModels)
      .catch((err));
  }, []);

  return (
    <div className="page">
      <h2 className="page-title">Models</h2>

      {models.map((model) => (
        <div key={model.id} className="card">
          <h3>{model.name}</h3>

          <p className="model-description">
            {model.description}
          </p>

          <p>
            <strong>Provider:</strong>{" "}
            {model.provider}
          </p>

          <p>
            <strong>Type:</strong>{" "}
            {model.type}
          </p>

          <p>
            <strong>Source:</strong>{" "}
            {model.source}
          </p>

          <p>
            <strong>Tasks:</strong>
          </p>

          <ul>
            {model.supported_tasks.map((task) => (
              <li key={task}>
                {task}
              </li>
            ))}
          </ul>

          {model.model_url && (
            <p>
              <strong>Model:</strong>{" "}
              <a
                href={model.model_url}
                target="_blank"
                rel="noreferrer"
              >
                View Model Card
              </a>
            </p>
          )}
        </div>
      ))}
    </div>
  );
}

export default Models;
