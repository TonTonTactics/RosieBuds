{/* Start Page

Antony Wiegand, Mcmaster, 2026*/}

import { GoGame, GoDashboard } from "./Routes.jsx"
import { useState, useEffect } from "react";
import "./Start.css";
import "./index.css"
import { useNavigate } from "react-router-dom";

export default function Start() {
  const [bg, setBg] = useState("/intro.gif");

  useEffect(() => {
    const preloadLoop = new Image();
    preloadLoop.src = "/loop.gif";

    const timer = setTimeout(() => {
      setBg("/loop.gif");
    }, 4000);

    return () => clearTimeout(timer);
  }, []);

  const navigate = useNavigate();
  const [transitioning, setTransitioning] = useState(false);
  const [flare, setFlare] = useState(false);

  function handleNavigate(path) {
    if (transitioning) return;

    setTransitioning(true);

    // flare after 1 second
    setTimeout(() => {
      setFlare(true);
    }, 1000);

    // navigate after animation
    setTimeout(() => {
      navigate(path);
    }, 1500);
  }

  return (
    <div className="page">
      <div className={"fade-in-on-load"}>
      <img className="bg-gif" src={bg} alt="background" />

      <h1>START</h1>

      {/* pass navigation function */}
      <GoDashboard go={handleNavigate} />
      <GoGame go={handleNavigate} />

      <CreditBox />
      <Mute />
      <Accessability />
      <Settings />

      {/* 🔥 overlay */}
      <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/>
      </div>
    </div>
  );
}

function CreditBox() {
  const [open, setOpen] = useState(false);

  return(
    <>
    <div onClick ={()=> setOpen(true)}>
      Credits
    </div>

    {open && (
      <div>
        <div onClick={()=> setOpen(false)}>
          close
        </div>
        <p>Gabriel</p>
        <p>Yusuf</p>
        <p>Tonios</p>
        <p>Antony</p>
      </div>
    )}
    </>
  );
}

function Mute() {
  const stored = localStorage.getItem("mute") === "true";
  const [on, setOn] = useState(stored);

  function toggleMute() {
    const newValue = !on

    setOn(newValue);
    localStorage.setItem("mute",newValue);
    console.log("(Saved) mute: ",newValue);
    
  }

  return(
    <>
      <div onClick ={toggleMute}>
        {on ? "Unmute":"Mute"}
      </div>
    </>
  );
}

function Accessability() {
  const stored = (setting) => localStorage.getItem(setting) === "true";
  const [open, setOpen] = useState(false);
  const [s1on,setS1on] = useState(stored("setting1"))

  function toggleSetting1(setting) {
    const newValue = !s1on

    setS1on(newValue);
    localStorage.setItem(setting,newValue);
    console.log("(Saved)",setting,newValue);
    
  }

  return(
    <>
    <div onClick ={()=> setOpen(true)}>
      Accessability
    </div>

    {open && (
      <div>
        <div onClick={()=> setOpen(false)}>
          close
        </div>
        <p onClick={()=>toggleSetting1("setting1")}> Setting 1: {s1on ? "On":"Off"}</p>
      </div>
    )}
    </>
  );
}

function Settings() {
  const stored = (setting) => localStorage.getItem(setting) === "true";
  const [open, setOpen] = useState(false);
  const [s2on,setS2on] = useState(stored("setting2"))

  function toggleSetting2(setting) {
    const newValue = !s2on

    setS2on(newValue);
    localStorage.setItem(setting,newValue);
    console.log("(Saved)",setting,newValue);
    
  }

  return(
    <>
    <div onClick ={()=> setOpen(true)}>
      Settings
    </div>

    {open && (
      <div>
        <div onClick={()=> setOpen(false)}>
          close
        </div>
        <p onClick={()=>toggleSetting2("setting2")}> Setting 2: {s2on ? "On":"Off"}</p>
      </div>
    )}
    </>
  );
}