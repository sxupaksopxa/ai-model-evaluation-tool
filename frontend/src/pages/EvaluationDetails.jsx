import { useLocation, useNavigate } from "react-router-dom";

export default function EvaluationDetails() {
  const location = useLocation();
  const navigate = useNavigate();

  const {
    taskName,
    inputText,
    modelResult,
  } = location.state || {};

  const hasAnalysis =
  modelResult?.analysis &&
  (
    modelResult.analysis.strengths ||
    modelResult.analysis.weaknesses ||
    modelResult.analysis.notes ||
    modelResult.analysis.recommended_use_case
  );

  if (!modelResult) {
    return (
      <div className="details-page">
        <h1>No Evaluation Selected</h1>

        <button
          type="button"
          onClick={() => navigate("/")}
        >
          Back
        </button>
      </div>
    );
  }

  const analysis = modelResult.analysis || {};

  return (
    <div className="details-page">
      <button
        type="button"
        className="back-button"
        onClick={() => navigate(-1)}
      >
        ← Back
      </button>

      <h1>Model Details</h1>

      <div className="details-section">
        <h2>Model Information</h2>

        <p>
          <strong>Model:</strong>{" "}
          {modelResult.model_name}
        </p>

        <p>
          <strong>Provider:</strong>{" "}
          {modelResult.provider}
        </p>

        <p>
          <strong>Task:</strong>{" "}
          {taskName || "N/A"}
        </p>
      </div>

      <div className="details-section">
        <h2>Input</h2>

        <div className="details-text">
          {inputText || "N/A"}
        </div>
      </div>

      <div className="details-section">
        <h2>Output</h2>

        {typeof modelResult?.output === "string" ? (
          <div className="details-text">
          {modelResult.output}
            </div>
            ) : (
            <pre>
              {JSON.stringify(
              modelResult?.output,
              null,
              2
              )}
            </pre>
          )}
        </div>

      {hasAnalysis && (
        <section className="details-section">
        <h2>Analysis</h2>

        {modelResult.analysis.strengths && (
          <p><strong>Strengths:</strong> {modelResult.analysis.strengths}</p>
        )}

        {modelResult.analysis.weaknesses && (
          <p><strong>Weaknesses:</strong> {modelResult.analysis.weaknesses}</p>
        )}

        {modelResult.analysis.notes && (
          <p><strong>Notes:</strong> {modelResult.analysis.notes}</p>
        )}

        {modelResult.analysis.recommended_use_case && (
          <p>
            <strong>Recommended Use Case:</strong>{" "}
        {modelResult.analysis.recommended_use_case}
      </p>
    )}
  </section>
)}

      <div className="details-section">
        <h2>Technical Details</h2>

        <p>
          <strong>Status:</strong>{" "}
          {modelResult.status || "N/A"}
        </p>

        <p>
          <strong>Latency:</strong>{" "}
          {modelResult.latency_ms
            ? `${modelResult.latency_ms} ms`
            : "N/A"}
        </p>

        <p>
          <strong>Cost:</strong>{" "}
          {modelResult.estimated_cost || "N/A"}
        </p>
      </div>
    </div>
  );
}