import React, { useState, useEffect } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

const EloHistory = () => {
    const [player1, setPlayer1] = useState('');
    const [playerId, setPlayerId] = useState('');
    const [eloPlot, setEloPlot] = useState('');
    const [playersList, setPlayersList] = useState([]);

    useEffect(() => {
        fetchAllPlayers();
    }, []);

    const fetchAllPlayers = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/search_players');
            if (response.ok) {
                const players = await response.json();
                setPlayersList(players);
            } else {
                console.error('Error fetching players');
            }
        } catch (error) {
            console.error('Error fetching players:', error);
        }
    };
    const handlePlayerChange = (event, value, isPlayer1 = true) => {
        if (value) {
            if (isPlayer1) {
                setPlayerId(value.id);
                setPlayer1(value.text);
            }
        }
    };

    const fetchEloPlot = async () => {
        const response = await fetch('http://127.0.0.1:5000/get_glicko_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ player_id: playerId }),
        });
        if (response.ok) {
            const data = await response.json();
            setEloPlot(data.image);
        } else {
            console.error('Failed to fetch Glicko plot');
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (playerId) {
            fetchEloPlot();
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="player1"></label>
                    <Autocomplete
                        id="player1"
                        options={playersList}
                        value={{ id: playerId, text: player1 }}
                        onChange={(event, value) => handlePlayerChange(event, value, true)}
                        getOptionLabel={(option) => option.text}
                        renderInput={(params) => <TextField {...params} label="Select Player" />}
                    />
                </div>
                <div className="button-wrapper">
                    <button type="submit" id="plot_button">Plot</button>
                </div>
            </form>
            {eloPlot && <img src={`data:image/png;base64,${eloPlot}`} id="plot" alt="Glicko History Plot" />}
        </div>
    );
};

export default EloHistory;
