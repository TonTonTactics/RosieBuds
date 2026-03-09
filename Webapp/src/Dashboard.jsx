/* All components on the dashboard page

Antony Wiegand, Mcmaster, 2026*/
import { GoStart,GoGuidebook } from "./Routes.jsx";
import { GetSensors } from "./Fetch.jsx"
import { useState } from "react";

export default function Dashboard() {
  /*
  Input: None
  1. Title: dashboard
  2. routes: start, guidebook
  3. grabs sensor data from today
  Output: None
  */
  return (
    <>
      <h1>DASHBOARD</h1>
      <GoStart />
      <GoGuidebook />
      <Slot1 />
    </>
  );
}

function Slot1() {
  const [open, setOpen] = useState(false);
  const [connected, setConnected] = useState(false);

  function Connection() {
    return true
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
            <div onClick={()=> setConnected(false)}>{connected ? "Remove Plant":""}</div>
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