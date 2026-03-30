/* Routes to Functions

Main file.

Antony Wiegand, Mcmaster, 2026*/

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Start from "./Start.jsx";
import Game from "./Game.jsx";
import Dashboard from "./Dashboard.jsx";
import Guidebook from "./Guidebook.jsx";
import './Start.css';
import { useRef,useState,useEffect } from "react";

// RUN npm run dev -- --host (from inside Webapp folder, needs access to package.json)

export default function App() {
  /* 
  Input: None
  1. Connects all routes to functions.
  Output: Routes to functions
  */
  const audioRef=useRef(null);

  const [muted, setMuted] = useState(
    localStorage.getItem("mute") === "true"
  );

    useEffect(() => {
      if (!audioRef.current) return;
  
      if (muted) {
        audioRef.current.pause();
      } else {
        audioRef.current.volume = 0.5;
        audioRef.current.play().catch(() => {});
      }
    }, [muted]);

  return (
    <>
    <audio ref={audioRef} loop controls>
      <source src="/music/background.mp3" type="audio/mpeg"/>
    </audio>

    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Start muted={muted} setMuted={setMuted} />} />
        <Route path="/game" element={<Game />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/guidebook" element={<Guidebook />} />
      </Routes>
    </BrowserRouter>
    </>
  );
}