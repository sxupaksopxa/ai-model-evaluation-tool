export default function Terms() {
  return (
    <main className="page app-container">
      <title>Terms of Service — BKlein Digital Labs</title>
      <meta
        name="description"
        content="Terms of service for BKlein Digital Labs."
      />
      <div className="legal-container">
        <h1 className="legal-title">Terms of Service</h1>
        <p className="legal-updated">Last updated: June 16, 2026</p>

        <div className="legal-sections">
          <div className="legal-section">
            <h2>1. Agreement</h2>
            <p>
              By accessing or using the BKlein Digital Labs website, you agree to these terms. If you do not agree, please do not use the site.
            </p>
          </div>

          <div className="legal-section">
            <h2>2. Use of the Site</h2>
            <p>
              The content on this site is provided for informational purposes.
              The tool is intended for evaluation, experimentation, and educational purposes.
              You may browse, read, and share links freely.
              You may not copy, redistribute, or commercially exploit the content without written permission.
              Users are responsible for any API usage and costs incurred through their own API keys.
              BKlein Digital Labs does not store API keys and is not responsible for charges incurred through third-party AI providers.
            </p>
          </div>

          <div className="legal-section">
            <h2>3. External Links</h2>
            <p>
              This site contains links to external projects and services. We are not responsible for the content, privacy practices, or availability of third-party sites.
            </p>
          </div>

          <div className="legal-section">
            <h2>4. Disclaimers</h2>
            <p>
              Information on this site is provided "as is" without warranties of any kind. Project statuses and features may change without notice.
            </p>
          </div>

          <div className="legal-section">
            <h2>5. Changes to Terms</h2>
            <p>
              We may update these terms from time to time. Continued use of the site after changes constitutes acceptance of the revised terms.
            </p>
          </div>

          <div className="legal-section">
            <h2>6. Contact</h2>
            <p>
              Questions about these terms can be sent to{" "}
              <a href="mailto:contact@bkleindigital.com">
                contact@bkleindigital.com
              </a>.
            </p>
          </div>

          <div className="legal-section">
            <h2>7. AI-Generated Content</h2>
            <p>
              This tool uses artificial intelligence models to generate outputs.
              These outputs are provided "as is" without warranty of accuracy,
              completeness, or fitness for any purpose.
              You are responsible for reviewing and validating any output before use.
            </p>
          </div>

          <div className="legal-section">
            <h2>8. Third-Party Services</h2>
            <p>
              Use of OpenRouter models is subject to{" "}
              <a href="https://openrouter.ai/terms" target="_blank" rel="noopener noreferrer">
                OpenRouter's Terms of Service
              </a>{" "}
              and{" "}
              <a href="https://openrouter.ai/privacy" target="_blank" rel="noopener noreferrer">
                Privacy Policy
              </a>.
              We are not responsible for the availability, accuracy, or pricing of third-party models.
            </p>
          </div>

          <div className="legal-section">
            <h2>9. Prohibited Use</h2>
            <p>
              You agree not to submit personal data, sensitive information,
              copyrighted material you do not have rights to, or illegal content
              through this tool.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
