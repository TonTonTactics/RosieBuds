{/* Start Page

Antony Wiegand, Mcmaster, 2026*/}

import { GoSetup, GoGame } from "./Routes.jsx"
import { useState } from "react";


export default function Start() {
  /*
    Input: None
    1. Title: Start
    2. routes: setup, game
    Output: None
    */

  return (
    <>
      <h1>START</h1>
      <GoSetup />
      <GoGame />
      <CreditBox />
      <Volume />
    </>
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

function Volume() {
  const [on, setOn] = useState(false);

  function Mute() {
    setOn(!on);

    if (!on) {
      console.log("(TEST) Mute: On")
    } else {
      console.log("(TEST) Mute: Off")
    }
  }

  return(
    <>
      <div onClick ={()=> setOn(Mute)}>
        {on ? "Unmute":"Mute"}
      </div>
    </>
  );
}