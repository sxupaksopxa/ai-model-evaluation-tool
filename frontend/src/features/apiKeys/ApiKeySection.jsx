export default function ApiKeySection({
  models,
  selectedModelIds,
  apiKeys,
  onApiKeysChange,
}) {
  const selectedModels = models.filter((model) =>
    selectedModelIds.includes(model.id)
  );

  const needsOpenRouterKey = selectedModels.some(
    (model) => model.provider === "OpenRouter"
  );

  if (!needsOpenRouterKey) {
    return null;
  }

  return (
    <div className="field api-key-section">
      <label
        htmlFor="openrouter-api-key"
        className="field-title"
      >
        OpenRouter API Key
      </label>

      <p className="field-help">
        Required for OpenRouter models. Used only for this evaluation request and not stored.
      </p>

      <input
        id="openrouter-api-key"
        name="openrouter_api_key"
        type="password"
        value={apiKeys?.openrouter || ""}
        onChange={(event) =>
          onApiKeysChange({
            ...apiKeys,
            openrouter: event.target.value,
          })
        }
        placeholder="sk-or-v1-..."
        autoComplete="off"
      />
    </div>
  );
}