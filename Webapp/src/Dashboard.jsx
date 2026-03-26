/* All components on the dashboard page

Antony Wiegand, Mcmaster, 2026*/
import { GoStart,GoGuidebook } from "./Routes.jsx";
import { GetSensors } from "./Fetch.jsx"
import { useState } from "react";
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
    <div className={"fade-in-on-load"}>
      <div className="page">
      <img className="dashboard" src="dashboard.png" alt="background" />
      <h1>DASHBOARD</h1>
      <GoStart go={handleNavigate}/>
      <GoGuidebook go={handleNavigate}/>
      <Slot1 />
      <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/>
      </div>
    </div>
  );
}

function Slot1() {
  const stored = localStorage.getItem("connected1") === "true";
  const [open, setOpen] = useState(false);
  const [connected, setConnected] = useState(stored);

  function Connection() {
    const newValue = !connected

    setConnected(newValue);
    localStorage.setItem("connected1",newValue);
    console.log("(Saved) connected1: ",newValue);
  }

  return (
    <>
      <div onClick ={()=> setOpen(true)}>
        Slot 1
      </div>

      {open && (
        <div>
          <div onClick={()=> setOpen(false)}>
            close
          </div>
          <div>
            <div>Slot Status: {connected ? "(CLOSED)":"(OPEN)"}</div>
            <div onClick={()=> setConnected(Connection)}>{connected ? "Remove Plant":""}</div>
            <div>{connected ? <GetSensors sensor_id={"1"}/>:""}</div>
          </div>
          <div onClick={()=> setConnected(Connection)}>
            {connected ? "":"Connect"}
          </div>
        </div>
      )}
    </>
  );
}