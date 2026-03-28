/* Shows the infromation from all plants in the database.

Antony Wiegand, Mcmaster, 2026*/

import { GoDashboardguide } from "./Routes.jsx";
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
        <div className="page">
        <div className={"fade-in-on-load"}>
            <img className="guidebook" src="guidebook.png" alt="background" />
            <div className="GuideText">{items[index]}</div>
                <GoDashboardguide go={handleNavigate}/>
                <img className="left" src="clickable/notclick/left.png" onClick ={back} disabled ={index === 0}></img>
                <img className="right" src="clickable/notclick/right.png" onClick ={next} disabled ={index === items.length -1}></img>
                <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/>
            </div>
        </div>
    );
}