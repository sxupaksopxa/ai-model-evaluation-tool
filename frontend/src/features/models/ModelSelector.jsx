export default function ModelSelector({
  models,
  selectedModelIds,
  onChange,
}) {
  const allSelected =
    models.length > 0 && selectedModelIds.length === models.length;

  function toggleModel(modelId) {
    if (selectedModelIds.includes(modelId)) {
      onChange(selectedModelIds.filter((id) => id !== modelId));
    } else {
      onChange([...selectedModelIds, modelId]);
    }
  }

  function toggleAllModels() {
    if (allSelected) {
      onChange([]);
    } else {
      onChange(models.map((model) => model.id));
    }
  }
  
  const sortedModels = [...models].sort((a, b) => {
    if (a.provider === "Local" && b.provider !== "Local") {
      return -1;
    }

    if (a.provider !== "Local" && b.provider === "Local") {
      return 1;
    }

    return a.name.localeCompare(b.name);
  });

  return (
    <div className="field">
      <label
        htmlFor="model-select"
        className="field-title"
      >
        Models
      </label>

        <div className="models-actions">
          <label className="select-all-label">
            <input
              type="checkbox"
              checked={allSelected}
              onChange={toggleAllModels}
            />
            <span>Select All</span>
          </label>

        </div>

      <div className="model-list">
        {sortedModels.map((model) => (
          <label
            key={model.id}
            className="model-option"
          >
            <div className="model-header">
              <input
                type="checkbox"
                checked={selectedModelIds.includes(model.id)}
                onChange={() => toggleModel(model.id)}
              />

              <span className="model-name">
                {model.name}

                {model.provider === "OpenRouter" && (
                  <span className="api-required-star">*</span>
                )}
              </span>
            </div>

            <div className="model-provider">
              {model.provider}
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}