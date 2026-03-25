/* Shows the infromation from all plants in the database.

Antony Wiegand, Mcmaster, 2026*/

import { GoDashboard } from "./Routes.jsx";
import { GetGuidebook } from "./Fetch.jsx";
import { useState } from "react";

export default function GuideBook() {
    /*
    Input: None
    1. Title: Guidebook
    2. routes: Dashboard
    Output: None
    */
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
        <>
            <h1>GUIDEBOOK</h1>
            <div>{items[index]}</div>
            <GoDashboard />
            <div onClick ={back} disabled ={index === 0}>Back</div>
            <div onClick ={next} disabled ={index === items.length -1}>Next</div>
        </>
    );
}