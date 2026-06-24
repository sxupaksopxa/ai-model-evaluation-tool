export default function Privacy() {
  return (
    <main className="page app-container">
      <title>Privacy Policy — BKlein Digital Labs</title>
      <meta
        name="description"
        content="Privacy policy for BKlein Digital Labs."
      />
      <div className="legal-container">
        <h1 className="legal-title">Privacy Policy</h1>
        <p className="legal-updated">Last updated: June 16, 2026</p>

        <div className="legal-sections">
          <div className="legal-section">
            <h2>1. Overview</h2>
            <p>
              BKlein Digital Labs respects your privacy. This policy explains what information we collect, how we use it, and your rights.
              We do not use cookies, analytics, databases, or any form of data persistence.
            </p>
          </div>

          <div className="legal-section">
            <h2>2. Information We Collect</h2>
            <p>
              This website does not use cookies, analytics, or tracking scripts. We do not collect personal data automatically.
            </p>
            <p>
              If you contact us via email, we receive only the information you choose to include in your message.
            </p>
          </div>

          <div className="legal-section">
            <h2>3. How We Use Information</h2>
            <p>
              Email correspondence is used solely to respond to your inquiry. We do not share, sell, or market your contact information.
            </p>
          </div>

          <div className="legal-section">
            <h2>4. Third-Party Services</h2>
            <p>
              This site is hosted on Vercel. Vercel may process basic server logs (IP address, browser type, timestamp) for operational and security purposes. We do not have access to or control over these logs.
            </p>
          </div>

          <div className="legal-section">
            <h2>5. Your Rights</h2>
            <p>
              You may request deletion of any personal data you have shared with us by emailing{" "}
              <a href="mailto:contact@bkleindigital.com">
                contact@bkleindigital.com
              </a>.
            </p>
          </div>

          <div className="legal-section">
            <h2>6. Contact</h2>
            <p>
              Questions about this policy can be sent to{" "}
              <a href="mailto:contact@bkleindigital.com">
                contact@bkleindigital.com
              </a>.
            </p>
          </div>

          <div className="legal-section">
            <h2>7. AI Model Processing & Third-Party Providers</h2>
            <p>
              When you select OpenRouter models, your input text is transmitted to OpenRouter for processing.
              OpenRouter may log and process this data under their own{" "}
              <a href="https://openrouter.ai/privacy" target="_blank" rel="noopener noreferrer">
                Privacy Policy
              </a>.
              We do not control how OpenRouter handles this data.
            </p>
            <p>
              <strong>Do not submit personal, sensitive, or confidential information through the evaluation tool.</strong>
            </p>
            <p>
              Local models process your input entirely on the server infrastructure where this application is deployed.
              No data is retained after the evaluation completes.
            </p>
          </div>

          <div className="legal-section">
            <h2>8. Data Retention</h2>
            <p>
              All evaluations are processed in-memory only. Input text, model outputs, and ratings are not stored in any database.
              Data exists only for the duration of the HTTP request and is discarded immediately afterward.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
