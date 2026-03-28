/* All components on the dashboard page

Antony Wiegand, Mcmaster, 2026*/
import { GoStartdashboard,GoGuidebook } from "./Routes.jsx";
import { GetSensors } from "./Fetch.jsx"
import { useState } from "react";
import "./Dashboard.css"
import "./index.css"
import { useNavigate } from "react-router-dom";
import TrackerSetup from "./TrackerSetup.jsx";

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
      <img className="slot1" src="clickable/notclick/slotclosed.png" onClick ={()=> setOpen(true)}/>

      {open && (
        <div>
          <img className="slotbox" src="squarebox.png" />
          <div className="overlay"></div>
          <img className="slotclose" src="clickable/notclick/back.png" onClick={()=> setOpen(false)}/>
          <div className="slottext">
            <div>Slot 1 Status: {connected ? "(CLOSED)":"(OPEN)"}</div>
            <div>
              <div>How to connect:</div>
              <div>1. Turn on tracker.</div>
              <div>2. Click "Connect".</div>
              <div>3. Wait for tracker to connect.</div>
              <div>Note: The website will go down for 30sec.</div>
            </div>
            <TrackerSetup />
            <div onClick={()=> setConnected(Connection)}>{connected ? "Remove Plant":""}</div>
            <div>{connected ? <GetSensors sensor_id={"1"}/>:""}</div>
          
          <div onClick={()=> setConnected(Connection)}>
            {connected ? "":"Connect"}
          </div>
          </div>
        </div>
      )}
    </>
  );
}