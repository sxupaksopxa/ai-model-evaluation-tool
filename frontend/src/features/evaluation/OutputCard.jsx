export default function OutputCard({ result }) {
  return (
    <div className="output-card">
      <h3>{result.model_name || result.model_id}</h3>

      <p className={`status status-${result.status}`}>
        Status: {result.status}
      </p>

      {result.error && <p className="error">{result.error}</p>}

      {result.output && (
        <pre>{result.output}</pre>
      )}

      <div className="meta">
        <span>Provider: {result.provider || "N/A"}</span>
        <span>Latency: {result.latency_ms ?? "N/A"} ms</span>
        <span>Cost: {result.estimated_cost ?? "N/A"}</span>
      </div>
    </div>
  );
}