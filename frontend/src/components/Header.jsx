import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="header">
      <div className="header-brand">
        <img
          src="/logo.png"
          alt="BKlein Digital Labs"
          className="header-logo"
        />

        <h1 className="header-title">
          BKlein Digital Labs
        </h1>
      </div>

      <nav className="header-nav">
        <Link to="/">Home</Link>
        <Link to="/models">Models</Link>
        <Link to="/tasks">Tasks</Link>
        <Link to="/about">About</Link>
      </nav>
    </header>
  );
}

export default Header;