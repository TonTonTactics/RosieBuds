/* Creates Route entrances.

when clicked, routes you to their connected function.

Antony Wiegand, Mcmaster, 2026*/

import { useNavigate } from "react-router-dom";

export function GoStart () {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to start.
    */
    const navigate = useNavigate();
    return (
        <div className="gostart" onClick={() => navigate("/")}>Start</div>
  );
}

export function GoSetup () {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to setup.
    */
    const navigate = useNavigate();
    return (
        <div className="gosetup" onClick={() => navigate("/setup")}>Setup</div>
  );
}

export function GoGame () {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to game.
    */
    const navigate = useNavigate();
    return (
        <div className="gogame" onClick={() => navigate("/game")}>Game</div>
  );
}

export function GoDashboard () {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to dashboard.
    */
    const navigate = useNavigate();
    return (
        <div className="godashboard" onClick={() => navigate("/dashboard")}>Dashboard</div>
  );
}

export function GoGuidebook () {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to guidebook.
    */
    const navigate = useNavigate();
    return (
        <div className="goguidebook" onClick={() => navigate("/guidebook")}>Guidebook</div>
  );
}



