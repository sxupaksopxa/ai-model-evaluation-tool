import { Link } from "react-router-dom";

function Footer() {
  return (
    <footer className="footer">
      <div className="app-container">

        <div className="footer-top">
          <p>
            No data is stored. Evaluations run in-memory only.
          </p>

          <div className="footer-links">
            <Link to="/privacy">Privacy</Link>
            <span>|</span>
            <Link to="/terms">Terms</Link>
          </div>
        </div>

        <div className="footer-bottom">
          <div>
            <strong>BKlein Digital Labs</strong>
            <span className="footer-separator"> • </span>
            <span>contact@bkleindigital.com</span>
          </div>

          <div className="footer-copyright">
            © 2026 BKlein Digital Labs. All rights reserved.
          </div>
        </div>

      </div>
    </footer>
  );
}

export default Footer;