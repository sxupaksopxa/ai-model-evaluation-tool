import TaskSelector from "../tasks/TaskSelector";
import ModelSelector from "../models/ModelSelector";
import ApiKeySection from "../apiKeys/ApiKeySection";

export default function EvaluationForm({
  tasks,
  models,
  selectedTaskId,
  selectedModelIds,
  inputText,
  loading,
  apiKeys,
  needsOpenRouterKey,
  onApiKeysChange,
  onTaskChange,
  onModelsChange,
  onInputChange,
  onStartNewTest,
  onSubmit,
}) {
  return (
    <form className="evaluation-form" onSubmit={onSubmit}>
      <TaskSelector
        tasks={tasks}
        selectedTaskId={selectedTaskId}
        onChange={onTaskChange}
      />

      <ModelSelector
        models={models}
        selectedModelIds={selectedModelIds}
        onChange={onModelsChange}
      />

      <ApiKeySection
        models={models}
        selectedModelIds={selectedModelIds}
        apiKeys={apiKeys}
        onApiKeysChange={onApiKeysChange}
      />

      <div className="field">
        <label
          htmlFor="input-text"
          className="field-title"
        >
          Input text
        </label>

        <div className="textarea-wrapper">
          <textarea
            value={inputText}
            onChange={(event) => onInputChange(event.target.value)}
            placeholder="Paste a business text here..."
            rows={8}
            maxLength={1000}
          />

          <span className="char-counter">
            {inputText.length}/1000
          </span>
        </div>
      </div>

      <div className="action-buttons">
      <button
        type="submit"
        disabled={
          loading ||
          !selectedTaskId ||
          selectedModelIds.length === 0 ||
          !inputText.trim() ||
          (needsOpenRouterKey && !apiKeys?.openrouter?.trim())
        }
      >
        {loading ? "Running..." : "Run evaluation"}
      </button>

      {loading && (
        <p className="field-help">
          ⏳ Please wait...
        </p>
      )}

      <button
        type="button"
        onClick={onStartNewTest}
        className="secondary-button"
      >
        Start New Test
      </button>
      </div>
    </form>
  );
}