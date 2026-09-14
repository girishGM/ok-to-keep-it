import { useEffect, useState } from "react";

function greetingForHour(hour) {
  if (hour < 5) return "Good night";
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  if (hour < 21) return "Good evening";
  return "Good night";
}

export default function App() {
  const [info, setInfo] = useState(null);
  const [error, setError] = useState(false);
  const greeting = greetingForHour(new Date().getHours());

  useEffect(() => {
    fetch("/api/hello")
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then(setInfo)
      .catch(() => setError(true));
  }, []);

  return (
    <main className="page">
      <div className="glow glow-a" aria-hidden="true" />
      <div className="glow glow-b" aria-hidden="true" />

      <section className="card">
        <span className="wave" role="img" aria-label="waving hand">
          👋
        </span>
        <p className="eyebrow">{greeting}, and welcome!</p>
        <h1>
          So glad you're here.
        </h1>
        <p className="lead">
          This little page was built to give the Telegram command flow
          something friendly to say hello with. Pull up a chair, have a look
          around, and know that everything here is running just for you.
        </p>

        <div className="pill" data-state={error ? "down" : info ? "up" : "loading"}>
          <span className="dot" />
          {error
            ? "Backend is taking a nap"
            : info
            ? `${info.project} is awake and saying: "${info.message}"`
            : "Checking in with the backend…"}
        </div>

        <ul className="links">
          <li>
            <a href="/health">/health</a>
          </li>
          <li>
            <a href="/healthz">/healthz</a>
          </li>
          <li>
            <a href="/api/hello">/api/hello</a>
          </li>
        </ul>

        <p className="footer">Made with warmth · Test-telegram-cmd</p>
      </section>
    </main>
  );
}
