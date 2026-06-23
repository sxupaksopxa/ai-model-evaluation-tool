function About() {
  return (
    <main className="page">
      <section className="hero">
        <h1>About</h1>

        <p>
          AI Model Evaluation Tool is a practical platform for comparing AI
          models on real-world tasks.
        </p>
      </section>

      <section className="details-section">
        <h2>Why This Project Exists</h2>

        <p>
          The AI landscape is growing rapidly. New models are released every
          month, each claiming improvements in quality, speed, reasoning, or
          cost efficiency. While public benchmarks and leaderboards provide
          useful information, they do not always reflect how a model performs
          on your own tasks.
        </p>

        <p>
          This project focuses on practical evaluation. Instead of relying only
          on benchmark scores, users can run the same input against multiple
          models and compare the results side-by-side.
        </p>
      </section>

      <section className="details-section">
        <h2>What You Can Evaluate</h2>

        <p>
          The current version supports several common Natural Language
          Processing (NLP) tasks:
        </p>

        <ul>
          <li>Entity Extraction</li>
          <li>Summarization</li>
          <li>Classification</li>
          <li>Question Answering</li>
          <li>Semantic Similarity</li>
        </ul>

        <p>
          Each task can be executed across multiple models, allowing users to
          compare output quality, response consistency, latency, and overall
          usefulness.
        </p>
      </section>

      <section className="details-section">
        <h2>Who Is It For?</h2>

        <ul>
          <li>Developers evaluating open-source models</li>
          <li>Students learning about AI capabilities</li>
          <li>Researchers exploring model behavior</li>
          <li>Organizations assessing models before adoption</li>
          <li>Anyone interested in practical AI comparison</li>
        </ul>
      </section>

      <section className="details-section">
        <h2>Current Focus</h2>

        <p>
          The project currently focuses on small, local, free, and
          cost-efficient models. The goal is to understand how these models
          perform in practical scenarios and where they can provide value
          without requiring expensive infrastructure.
        </p>
      </section>

      <section className="details-section">
        <h2>Roadmap</h2>

        <ul>
          <li>Additional OpenRouter and Local Models</li>
          <li>Ollama Integration</li>
          <li>Cost Comparison and Usage Insights</li>
          <li>Model Statistics Dashboard</li>
          <li>Evaluation History</li>
          <li>Export Evaluation Results</li>
          <li>User Ratings and Feedback</li>
          <li>Advanced Prompt Templates</li>
        </ul>
      </section>

      <section className="details-section">
        <h2>Open and Extensible</h2>

        <p>
          The long-term vision is to create an extensible evaluation platform
          where users can register their own models through a standardized
          model registry format and compare local, hosted, and open-source
          models within the same interface.
        </p>
      </section>

      <section className="details-section">
        <h2>Contact</h2>

        <p>
          Questions, feedback, and collaboration opportunities are welcome.
        </p>

        <p>
          <strong>contact@bkleindigital.com</strong>
        </p>
      </section>
    </main>
  );
}

export default About;