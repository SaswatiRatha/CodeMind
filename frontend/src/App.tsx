import axios from "axios";
import { useEffect, useState, type SubmitEvent } from "react";
import "./App.css";

type HealthResponse = {
  status: string;
  environment: string;
};

type RepositoryResult = {
  id: string;
  status: string;
};

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [url, setUrl] = useState<string>("");
  const [branch, setBranch] = useState<string>("");
  const [result, setResult] = useState<RepositoryResult | null>(null);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await axios.get("http://localhost:8000/health");
        const data: HealthResponse = res.data;
        setHealth(data);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Could not reach the backend",
        );
      }
    };
    checkBackend();
  }, []);

  const handleSubmit = async (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();
    setResult(null);
    setError(null);

    try {
      const response = await axios.post("http://localhost:8000/repositories/", {
        url,
        branch,
      });
      const data: RepositoryResult = response.data;
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    }
  };

  return (
    <main className="app">
      <h1>CodeMind</h1>
      <p>GitHub repository QnA</p>
      <section className="status">
        <h2>Backend Connection</h2>
        {error && <p className="error">Connection failed: {error}</p>}
        {!health && !error && <p>Checking backend...</p>}
        {health && (
          <p className="success">
            Connected: {health.status}
            {health.environment && ` (${health.environment})`}
          </p>
        )}
      </section>
      <section>
        <h2>Add a github repo</h2>
        <form onSubmit={handleSubmit}>
          <label htmlFor="url">Repository URL</label>
          <input
            type="url"
            id="url"
            name="url"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://github.com/owner/repository"
            required
          />
          <label htmlFor="branch">Repository URL</label>
          <input
            type="text"
            id="branch"
            name="branch"
            value={branch}
            onChange={(event) => setBranch(event.target.value)}
            required
          />
          <button type="submit">Clone Repository</button>
        </form>

        {result && (
          <p>
            Repository cloned. ID: {result.id} (status: {result.status})
          </p>
        )}

        {error && <p className="error">Clone Failed: {error}</p>}
      </section>
    </main>
  );
}

export default App;
