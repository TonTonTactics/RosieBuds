/* Tic-Tac-Toe Game

Antony Wiegand, Mcmaster, 2026*/

import { useState } from 'react';
import { GoStart } from './Routes.jsx';
import "./Game.css"
import "./index.css"
import { useNavigate } from "react-router-dom";

export default function Game() {
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

    const initialBoard = Array(9).fill(null);
    // changes state from X to O (or vice versa)
    const [_IsNext, set_IsNext] = useState(true);

    // creates an array on 9 (one for each square). Allows for saving values
    const [squares, setSquares] = useState(initialBoard)

    function handleClick(i) {

        // determines winner
        if (squares[i] || calculateWinner(squares)){
            return;
        }
        //prevents overwritting squares
        if (squares[i]) {
            return;
        }

        // copies array, updates square clicked, sets game state to show changes
        const nextSquares = squares.slice();

        // allows for alternating between X and O.
        if (_IsNext) {
            nextSquares[i] = "X";
        } else {
            nextSquares[i] = "O";
        }

        // sets game state to show changes
        setSquares(nextSquares);

        // makes it so X or O can't go twice in a row
        set_IsNext(!_IsNext);
    }

    function handleRestart() {
        setSquares(initialBoard)
        set_IsNext(true);
    }

    const winner = calculateWinner(squares);
        let status;
        if (winner) {
        status = "Winner: " + winner;
        } else {
        status = "Next player: " + (_IsNext ? "X" : "O");
    }



    return (
        <div className="page">
            <div className={"fade-in-on-load"}>
            <img className="game" src="game.png" alt="background" />
            <h1>GAME</h1>
            <div className="status">{status}</div>

            <div className="board-row">
                <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
                <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
                <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
            </div>
            <div className="board-row">
                <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
                <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
                <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
            </div>
            <div className="board-row">
                <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
                <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
                <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
            </div>
            <button onClick={handleRestart} > Restart </button>
            <GoStart go= {handleNavigate} />
            <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/>
            </div>
        </div>
    );
}

function Square( {value, onSquareClick} ) {
    return (
        <button className="square" onClick={onSquareClick}>
            {value} 
        </button>
    );
}

function calculateWinner(squares) {
    const lines = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ];
    for (let i = 0; i < lines.length; i++) {
        const [a, b, c] = lines [i];
        if (squares[a] && squares[a] === squares[b] && squares[a] == squares[c]) {
            return squares[a];
        }
    }
    return null;
}