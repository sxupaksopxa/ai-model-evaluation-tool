import { useEffect, useState } from "react";

import EvaluationForm from "../features/evaluation/EvaluationForm";
import OutputCard from "../features/evaluation/OutputCard";
import { fetchTasks } from "../features/tasks/taskApi";
import { fetchModels } from "../features/models/modelApi";
import { runEvaluation } from "../features/evaluation/evaluationApi";
import EvaluationResultsTable from "../features/evaluation/EvaluationResultsTable";
import EvaluationDetails from "./EvaluationDetails";
import ModelResults from "../features/evaluation/ModelResults";

export default function Home() {
  const [tasks, setTasks] = useState([]);
  const [models, setModels] = useState([]);

  const [selectedTaskId, setSelectedTaskId] = useState("");
  const [selectedModelIds, setSelectedModelIds] = useState([]);
  const [inputText, setInputText] = useState("");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const [apiKeys, setApiKeys] = useState({
    openrouter: "",
  });

  const selectedModels = models.filter((model) =>
    selectedModelIds.includes(model.id)
  );

  const needsOpenRouterKey = selectedModels.some(
    (model) => model.provider === "OpenRouter"
  );

  const handleStartNewTest = () => {
    setInputText("");
    setResult(null);
    setError("");
    sessionStorage.removeItem("latestEvaluation");
  };

  useEffect(() => {
    const savedEvaluation =
      sessionStorage.getItem(
        "latestEvaluation"
      );

    if (savedEvaluation) {
      setResult(
        JSON.parse(savedEvaluation)
      );
    }
  }, []);

  useEffect(() => {
    fetchTasks()
      .then(setTasks)
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    if (!selectedTaskId) {
      setModels([]);
      setSelectedModelIds([]);
      return;
    }

    fetchModels(selectedTaskId)
      .then((data) => {
        setModels(data);
        setSelectedModelIds([]);
      })
      .catch((err) => setError(err.message));
  }, [selectedTaskId]);

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await runEvaluation({
        task_id: selectedTaskId,
        model_ids: selectedModelIds,
        input_text: inputText,
        api_keys: apiKeys,
      });

      setResult(data);

      sessionStorage.setItem(
        "latestEvaluation",
        JSON.stringify(data)
      );

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <section className="hero">
        <h2>AI Model Evaluation Tool</h2>
        <p>
          Compare and learn how different AI models perform on real-world NLP tasks using practical examples and everyday language.
        </p>
      </section>

      {error && <div className="error-box">{error}</div>}

      <EvaluationForm
        tasks={tasks}
        models={models}
        selectedTaskId={selectedTaskId}
        selectedModelIds={selectedModelIds}
        inputText={inputText}
        loading={loading}
        apiKeys={apiKeys}
        needsOpenRouterKey={needsOpenRouterKey}
        onApiKeysChange={setApiKeys}
        onTaskChange={setSelectedTaskId}
        onModelsChange={setSelectedModelIds}
        onInputChange={setInputText}
        onStartNewTest={handleStartNewTest}
        onSubmit={handleSubmit}
      />

      {result && (
        <>
      <ModelResults
        results={result.results}
      />

      <section className="results">
        <h2>Evaluation Results</h2>

        <p>
          <strong>Task:</strong>{" "}
          {result.task_name}
        </p>

        <EvaluationResultsTable
          result={result}
        />
      </section>
    </>
    )}
    </main>
  );
}