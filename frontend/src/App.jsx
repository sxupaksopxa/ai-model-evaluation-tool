import {
  Routes,
  Route,
} from "react-router-dom";

import Layout from "./components/Layout";

import Home from "./pages/Home";
import EvaluationDetails from "./pages/EvaluationDetails";


import Models from "./pages/Models";
import Tasks from "./pages/Tasks";
import About from "./pages/About";

import Privacy from "./pages/Privacy";
import Terms from "./pages/Terms";

function App() {
  return (
      <Layout>
        <Routes>
          <Route
            path="/"
            element={<Home />}
          />

          <Route
            path="/models"
            element={<Models />}
          />

          <Route
            path="/tasks"
            element={<Tasks />}
          />

          <Route
            path="/details"
            element={<EvaluationDetails />}
          />

          <Route
            path="/about"
            element={<About />}
          />

          <Route
            path="/privacy"
            element={<Privacy />}
          />

          <Route
            path="/terms"
            element={<Terms/>}
          />
        </Routes>
      </Layout>
  );
}

export default App;