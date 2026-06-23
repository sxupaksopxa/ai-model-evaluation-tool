import { useNavigate } from "react-router-dom";

export default function EvaluationResultsTable({ result}) {

  const navigate = useNavigate();

  if (!result) {
    return null;
  }

  return (
    <table className="results-table">
      <thead>
        <tr>
          <th>Model</th>
          <th>Provider</th>
          <th>Status</th>
          <th>Score</th>
          <th>Latency</th>
          <th>Cost</th>
          <th>Details</th>
        </tr>
      </thead>

      <tbody>
        {result.results.map((item) => (
          <tr key={item.model_id}>
            <td>{item.model_name}</td>

            <td>{item.provider || "N/A"}</td>

            <td>{item.status || "N/A"}</td>

            <td>
              {item.score !== undefined &&
              item.score !== null
                ? item.score
                : "N/A"}
            </td>

            <td>
              {item.latency_ms
                ? `${item.latency_ms} ms`
                : "N/A"}
            </td>

            <td>
              {item.estimated_cost ??
                item.cost ??
                "N/A"}
            </td>

            <td>
              <button
                type="button"
                className="view-button"
                onClick={() => {
                  navigate("/details", {
                    state: {
                      taskName: result.task_name,
                      inputText: result.input_text,
                      modelResult: item,
                    },
                  });
                }}
                >
                View
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}