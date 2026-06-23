import { useState, useEffect } from "react";

export default function ModelResults({ results = [] }) {
  const [selectedModelId, setSelectedModelId] =
    useState(null);

  useEffect(() => {
    if (
      results.length > 0 &&
      !selectedModelId
    ) {
      setSelectedModelId(
        results[0].model_id
      );
    }
  }, [results, selectedModelId]);

  if (!results.length) {
    return null;
  }

  const selectedResult = results.find(
    (item) =>
      item.model_id === selectedModelId
  );

  if (!selectedResult) {
    return null;
  }

  return (
    <div className="model-results">
      <h2>Model Results</h2>

      <div className="model-tabs">
        {results.map((item) => (
          <button
            key={item.model_id}
            type="button"
            className={
              item.model_id === selectedModelId
                ? "model-tab active"
                : "model-tab"
            }
            onClick={() =>
              setSelectedModelId(
                item.model_id
              )
            }
          >
            {item.model_name}
          </button>
        ))}
      </div>

      <div className="model-result-panel">
        <div className="result-meta">
          <strong>
            {selectedResult?.model_name}
          </strong>
          {" • "}
          {selectedResult?.provider}
        </div>

        <div className="result-content">
          <pre>
            {typeof selectedResult?.output === "string"
              ? selectedResult.output
              : JSON.stringify(
              selectedResult?.output,
              null,
              2
            )}
          </pre>
        </div>
      </div>
    </div>
  );
}