/* Tic-Tac-Toe Game

Antony Wiegand, Mcmaster, 2026*/

import { useState } from 'react';
import { GoStartgame } from './Routes.jsx';
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
        if (winner) {
        winner;
        } else {
        (_IsNext ? "X" : "O");
    }



    return (
        <div className="page">
            <div className={"fade-in-on-load"}>
            <img className="game" src="game.png" alt="background" />
            <div className="status">
                {winner ? (
                    <div className="next-player">
                    <img src={_IsNext ? "clickable/notclick/nexto.png" : "clickable/notclick/nextx.png"}
                    className="next-img"
                    />
                    </div>
                ) : (
                    <div className="next-player">
                    <img src={_IsNext ? "clickable/notclick/nextx.png" : "clickable/notclick/nexto.png"}
                    className="next-img"
                    />
                    </div>
                )
            }
                </div>

            <div className="board-row">
                <Square value={squares[0]} onSquareClick={() => handleClick(0)} className="sq0" />
                <Square value={squares[1]} onSquareClick={() => handleClick(1)} className="sq1" />
                <Square value={squares[2]} onSquareClick={() => handleClick(2)} className="sq2" />
            </div>
            <div className="board-row">
                <Square value={squares[3]} onSquareClick={() => handleClick(3)} className="sq3" />
                <Square value={squares[4]} onSquareClick={() => handleClick(4)} className="sq4" />
                <Square value={squares[5]} onSquareClick={() => handleClick(5)} className="sq5" />
            </div>
            <div className="board-row">
                <Square value={squares[6]} onSquareClick={() => handleClick(6)} className="sq6" />
                <Square value={squares[7]} onSquareClick={() => handleClick(7)} className="sq7" />
                <Square value={squares[8]} onSquareClick={() => handleClick(8)} className="sq8" />
            </div>
            <img className="reset" src="clickable/notclick/reset.png" onClick={handleRestart} />
            <GoStartgame go= {handleNavigate} />
            <div className={`screen-transition ${transitioning ? "active" : ""} ${flare ? "flare" : ""}`}/>
            </div>
        </div>
    );
}

function Square( {value, onSquareClick, className} ) {
    return (
        <button className={`square ${className || ""}`} onClick={onSquareClick}>
            {value === "X" && <img src="clickable/clicked/x.gif" alt="X" className="xo-img"/>}
            {value === "O" && <img src="clickable/clicked/o.gif" alt="O" className="xo-img"/> }  
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