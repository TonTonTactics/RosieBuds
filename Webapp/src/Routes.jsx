/* Creates Route entrances.

when clicked, routes you to their connected function.

Antony Wiegand, Mcmaster, 2026*/

export function GoStart ( { go }) {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to start.
    */
    return (
    <div onClick={() => go("/")}>
      Start
    </div>
  );
}

export function GoGame ( { go } ) {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to game.
    */
    return (
    <div onClick={() => go("/game")}>
      Game
    </div>
  );
}


export function GoDashboard ( { go } ) {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to dashboard.
    */
    return (
        <div className="godashboard" onClick={() => go("/dashboard")}>Dashboard</div>
  );
}

export function GoGuidebook ( { go } ) {
    /*
    Input: None
    1. creates navigate variable using useNavigate function.
    Output: When clicked, takes you to guidebook.
    */
    return (
        <div className="goguidebook" onClick={() => go("/guidebook")}>Guidebook</div>
  );
}




