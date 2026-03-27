{/* Start Page

Antony Wiegand, Mcmaster, 2026*/}

import { GoGame, GoDashboardstart } from "./Routes.jsx"
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
          <GoDashboardstart go={handleNavigate} />
          <GoGame go={handleNavigate} />
          <CreditBox />
          <Mute />
          <Accessability />
          <Settings />

        <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/></div>
      </div>
  );
}

function CreditBox() {
  const [open, setOpen] = useState(false);

  return(
    <>
    <img className="credits" src="clickable/notclick/credits.png" onClick ={()=> setOpen(true)}/>
    {open && (
      <div>
        <img className="creditsbox" src="squarebox.png"/>
        <div class="overlay"></div>
        <div class="creditstext">
          <img className="creditsclose" src="clickable/notclick/back.png" onClick={()=> setOpen(false)}/>
          <p>Gabriel W. (top right)</p>
          <p>Yusuf E. (bottom right)</p>
          <p>Tonios M. (bottom left)</p>
          <p>Antony W. (top left)</p>
        </div>
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
    <img className="volume" onClick ={toggleMute} src={on ? "clickable/notclick/volume.png":"clickable/clicked/CLICKEDvolume.png"}/>
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
    <img className="accessability" src="clickable/notclick/accessability.png" onClick ={()=> setOpen(true)}/>
    {open && (
      <div>
        <img className="accessabilitybox" src="squarebox.png"/>
        <div class="overlay"></div>
        <img className="accessabilityclose" src="clickable/notclick/back.png" onClick={()=> setOpen(false)}/>
        <div className="accessabilitytext">
          <p class="a" onClick={()=>toggleSetting1("setting1")}> Setting 1: {s1on ? "On":"Off"}</p>
        </div>
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
    <img className="settings" src="clickable/notclick/settings.png" onClick ={()=> setOpen(true)}/>
    {open && (
      <div>
        <img className="settingsbox" src="squarebox.png"/>
        <div class="overlay"></div>
        <img className="settingsclose" src="clickable/notclick/back.png" onClick={()=> setOpen(false)}/>
        
        <div className="settingstext">
          <p onClick={()=>toggleSetting2("setting2")}> Setting 2: {s2on ? "On":"Off"}</p>
        </div>
      </div>
    )}
    </>
  );
}