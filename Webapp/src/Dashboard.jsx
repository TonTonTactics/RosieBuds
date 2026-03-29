/* All components on the dashboard page

Antony Wiegand, Mcmaster, 2026*/
import { GoStartdashboard,GoGuidebook } from "./Routes.jsx";
import { GetSensors } from "./Fetch.jsx"
import { useState, useEffect } from "react";
import "./Dashboard.css"
import "./index.css"
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  /*
  Input: None
  1. Title: dashboard
  2. routes: start, guidebook
  3. grabs sensor data from today
  Output: None
  */
    const navigate = useNavigate();
    const [transitioning, setTransitioning] = useState(false);
    const [flare, setFlare] = useState(false);

    function handleNavigate(path) {
    if (transitioning) return;

    setTransitioning(true);

    // flare after 1 second
    setTimeout(() => {setFlare(true);}, 1000);

    // navigate after animation
    setTimeout(() => {navigate(path);}, 1500);}

  return (
    <div className="page">
    <div className={"fade-in-on-load"}>
      <img className="dashboard" src="dashboard.png" alt="background" />
      <GoStartdashboard go={handleNavigate}/>
      <GoGuidebook go={handleNavigate}/>
      <Slot1 />
      <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/>
      </div>
    </div>
  );
}

function Slot1() {
  const [open, setOpen] = useState(false);
  const [connected, setConnected] = useState(false);
  const [plant, setPlant] = useState(localStorage.getItem("plant1") || "");

  function handleConnect() {
    if (!plant) return;

    localStorage.setItem("plant1", plant);
    localStorage.setItem("connected1", "true");
    setConnected(true);
  }

  function handleRemove() {
    localStorage.removeItem("plant1");
    localStorage.setItem("connected1", "false");
    setPlant("");
    setConnected(false);
  }

  return (
    <>
      <img
        className="slot1"
        src="clickable/notclick/slotclosed.png"
        onClick={() => setOpen(true)}
      />

      {open && (
        <div>
          <img className="slotbox" src="squarebox.png" />
          <div className="overlay"></div>

          <img
            className="slotclose"
            src="clickable/notclick/back.png"
            onClick={() => setOpen(false)}
          />

          <div className="slottext">
            <div>Slot Status: {connected ? "(CLOSED)" : "(OPEN)"}</div>

            {!connected && (
              <PlantSelect plant={plant} setPlant={setPlant} />
            )}

            {connected && (
              <div>Selected Plant ID: {plant}</div>
            )}

            {connected && (
              <div onClick={handleRemove}>Remove Plant</div>
            )}

            <div>
              {connected && (
                <GetSensors sensor_id={"1"} plant_type={plant} />
              )}
            </div>

            {!connected && (
              <div onClick={handleConnect}>
                Connect
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function PlantSelect({ plant, setPlant }) {
  const [plants, setPlants] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/guidebook")
      .then(res => res.json())
      .then(data => setPlants(data))
      .catch(() => setPlants([]));
  }, []);

  return (
    <select value={plant} onChange={(e) => setPlant(e.target.value)}>
      <option value="">Select a plant</option>
      {plants.map((item) => (
        <option key={item.id} value={item.id}>
          {item.name}
        </option>
      ))}
    </select>
  );
}