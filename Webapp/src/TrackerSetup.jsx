import { useEffect, useRef, useState } from "react";
import "./index.css";

export default function TrackerSetup() {
  const [pairState, setPairState] = useState("idle");
  const [message, setMessage] = useState("Tracker not connected.");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const pollRef = useRef(null);

  function stopPolling() {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }

  function getStatusMessage(state) {
    switch (state) {
      case "idle":
        return "Tracker not connected.";
      case "starting":
        return "Starting Hub setup mode...";
      case "waiting_for_tracker":
        return "Waiting for tracker to connect...";
      case "tracker_connected":
        return "Tracker found. Sending Wi-Fi credentials...";
      case "credentials_sent":
        return "Credentials sent. Waiting for tracker to join Wi-Fi...";
      case "tracker_confirmed":
        return "Tracker connected successfully.";
      case "timeout":
        return "Setup timed out. Try again.";
      case "error":
        return "Something went wrong during setup.";
      default:
        return "Checking tracker status...";
    }
  }

  async function fetchStatus() {
    try {
      const res = await fetch(`/provision/status`);
      if (!res.ok) {
        throw new Error(`Status request failed: ${res.status}`);
      }

      const data = await res.json();
      const state = data.state || "idle";

      setPairState(state);
      setMessage(getStatusMessage(state));

      if (state === "tracker_confirmed" || state === "timeout" || state === "idle") {
        setLoading(false);
        stopPolling();
      }
    } catch (err) {
      setError(err);
      setLoading(false);
      stopPolling();
    }
  }

  async function startPairing() {
    setError("");
    setLoading(true);
    setPairState("starting");
    setMessage(getStatusMessage("starting"));

    try {
      const res = await fetch(`/provision/start`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        throw new Error(`Start request failed: ${res.status}`);
      }

      const data = await res.json();
      const state = data.state || "waiting_for_tracker";

      setPairState(state);
      setMessage(getStatusMessage(state));

      stopPolling();
      pollRef.current = setInterval(fetchStatus, 1500);
    } catch (err) {
      setError(err);
      setLoading(false);
      setPairState("error");
      setMessage(getStatusMessage("error"));
    }
  }

  async function cancelPairing() {
    stopPolling();
    setLoading(false);
    setPairState("idle");
    setMessage(getStatusMessage("idle"));

    try {
      await fetch(`/provision/cancel`, {
        method: "POST",
      });
    } catch {
      // okay if this fails, UI still resets
    }
  }

  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, []);

  return (
    <div className="tracker-setup-card">
      <p>{message}</p>

      {error && <p className="tracker-error">{error}</p>}

      <div className="tracker-buttons">
        <button onClick={startPairing} disabled={loading}>
          {loading ? "Connecting..." : "Connect Tracker"}
        </button>

        {loading && (
          <button onClick={cancelPairing}>
            Cancel
          </button>
        )}
      </div>
      <div className="tracker-debug">
        <strong>Status:</strong> {pairState}
      </div>
    </div> 
  );
}