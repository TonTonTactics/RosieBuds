/* Shows the infromation from all plants in the database.

Antony Wiegand, Mcmaster, 2026*/

import { GoDashboard } from "./Routes.jsx";
import { GetGuidebook } from "./Fetch.jsx";
import { useState } from "react";
import "./Guidebook.css";
import "./index.css"
import { useNavigate } from "react-router-dom";

export default function GuideBook() {
    /*
    Input: None
    1. Title: Guidebook
    2. routes: Dashboard
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

   const items = [
    <GetGuidebook id={1} />,
    <GetGuidebook id={2} />,
    <GetGuidebook id={3} />,
   ]
   const [index, setIndex] = useState(0);

   function next() {
    if (index < items.length -1) {
        setIndex(index + 1);
    }
   }

   function back() {
    if (index > 0) {
        setIndex(index - 1);
    }
   }

    return (
        <div className={"fade-in-on-load"}>
            <div className="page">
            <img className="guidebook" src="guidebook.png" alt="background" />
            <h1>GUIDEBOOK</h1>
            <div>{items[index]}</div>
            <GoDashboard go={handleNavigate}/>
            <div onClick ={back} disabled ={index === 0}>Back</div>
            <div onClick ={next} disabled ={index === items.length -1}>Next</div>
            <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/>
            </div>
        </div>
    );
}