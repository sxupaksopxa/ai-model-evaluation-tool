export default function Privacy() {
  return (
    <section className="px-4 py-16">
        <title>Privacy Policy — BKlein Digital Labs</title>
        <meta
          name="description"
          content="Privacy policy for BKlein Digital Labs."
        />
      <div className="mx-auto max-w-3xl">
        <h1 className="text-3xl font-bold tracking-tight text-slate-950 md:text-4xl">
          Privacy Policy
        </h1>
        <p className="mt-4 text-slate-600">Last updated: June 16, 2026</p>

        <div className="mt-10 space-y-8 text-slate-700">
          <div>
            <h2 className="text-xl font-semibold text-slate-950">1. Overview</h2>
            <p className="mt-2 leading-7">
              BKlein Digital Labs respects your privacy. This policy explains what information we collect, how we use it, and your rights.
              We do not use cookies, analytics, databases, or any form of data persistence.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-950">2. Information We Collect</h2>
            <p className="mt-2 leading-7">
              This website does not use cookies, analytics, or tracking scripts. We do not collect personal data automatically.
            </p>
            <p className="mt-2 leading-7">
              If you contact us via email, we receive only the information you choose to include in your message.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-950">3. How We Use Information</h2>
            <p className="mt-2 leading-7">
              Email correspondence is used solely to respond to your inquiry. We do not share, sell, or market your contact information.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-950">4. Third-Party Services</h2>
            <p className="mt-2 leading-7">
              This site is hosted on Vercel. Vercel may process basic server logs (IP address, browser type, timestamp) for operational and security purposes. We do not have access to or control over these logs.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-950">5. Your Rights</h2>
            <p className="mt-2 leading-7">
              You may request deletion of any personal data you have shared with us by emailing{" "}
              <a href="mailto:contact@bkleindigital.com" className="text-blue-700 hover:underline">
                contact@bkleindigital.com
              </a>.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-950">6. Contact</h2>
            <p className="mt-2 leading-7">
              Questions about this policy can be sent to{" "}
              <a href="mailto:contact@bkleindigital.com" className="text-blue-700 hover:underline">
                contact@bkleindigital.com
              </a>.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-950">7. AI Model Processing & Third-Party Providers</h2>
            <p className="mt-2 leading-7">
              When you select OpenRouter models, your input text is transmitted to OpenRouter for processing.
              OpenRouter may log and process this data under their own{" "}
              <a href="https://openrouter.ai/privacy" className="text-blue-700 hover:underline" target="_blank" rel="noopener noreferrer">
                Privacy Policy
              </a>.
              We do not control how OpenRouter handles this data.
            </p>
            <p className="mt-2 leading-7">
              <strong>Do not submit personal, sensitive, or confidential information through the evaluation tool.</strong>
            </p>
            <p className="mt-2 leading-7">
              Local models process your input entirely on the server infrastructure where this application is deployed.
              No data is retained after the evaluation completes.
            </p>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-slate-950">8. Data Retention</h2>
            <p className="mt-2 leading-7">
              All evaluations are processed in-memory only. Input text, model outputs, and ratings are not stored in any database.
              Data exists only for the duration of the HTTP request and is discarded immediately afterward.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
