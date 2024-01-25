import React, { useState, useEffect } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import { useNavigate } from 'react-router-dom';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import InfoIcon from '@mui/icons-material/Info';
import Typography from '@mui/material/Typography';
import './styles.css';

const Home = () => {
    const [player1, setPlayer1] = useState('');
    const [player2, setPlayer2] = useState('');
    const [surface, setSurface] = useState('hard');
    const [model, setModel] = useState('GradientBoosting');
    const [playersList, setPlayersList] = useState([]);
    const [player1Id, setPlayer1Id] = useState('');
    const [player2Id, setPlayer2Id] = useState('');
    const [predictionResult, setPredictionResult] = useState(null);
    const navigate = useNavigate();
    const navigateToGlickoHistory = () => {
        navigate('/glicko-history');
    };
    const navigateToEloHistory = () => {
        navigate('/elo-history');
    };

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
            const selectedPlayerId = value.id;
            const selectedPlayerText = value.text;
    
            if (isPlayer1 && selectedPlayerId === player2Id) {
                alert('Player 1 and Player 2 cannot be the same.');
                return;
            } else if (!isPlayer1 && selectedPlayerId === player1Id) {
                alert('Player 1 and Player 2 cannot be the same.');
                return;
            }
    
            if (isPlayer1) {
                setPlayer1Id(selectedPlayerId);
                setPlayer1(selectedPlayerText);
            } else {
                setPlayer2Id(selectedPlayerId);
                setPlayer2(selectedPlayerText);
            }
        }
    };

    const handleSurfaceChange = (event) => {
        setSurface(event.target.value);
    };

    const handleModelChange = (event) => {
        setModel(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!player1Id || !player2Id) {
            alert('Please select both players.');
            return;
        }
        try {
            const postData = {
                player1_id: player1Id,
                player2_id: player2Id,
                surface: surface,
                model: model
            };
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(postData),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            setPredictionResult(result);
        } catch (error) {
            console.error('There was an error with the prediction request', error);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <Autocomplete
                        id="player1"
                        options={playersList}
                        value={{ id: player1Id, text: player1 }}
                        onChange={(event, value) => handlePlayerChange(event, value, true)}
                        getOptionLabel={(option) => option.text}
                        renderInput={(params) => <TextField {...params} label="Player 1" />}
                    />
                </div>

                <div className="form-group">
                    <Autocomplete
                        id="player2"
                        options={playersList}
                        value={{ id: player2Id, text: player2 }}
                        onChange={(event, value) => handlePlayerChange(event, value, false)}
                        getOptionLabel={(option) => option.text}
                        renderInput={(params) => <TextField {...params} label="Player 2" />}
                    />
                </div>
                <select
                    name="surface"
                    id="surface"
                    className="search-input"
                    value={surface}
                    onChange={handleSurfaceChange}
                >
                    <option value="hard">Hard</option>
                    <option value="clay">Clay</option>
                    <option value="grass">Grass</option>
                </select>

                <select
                    name="model"
                    id="model"
                    className="search-input"
                    value={model}
                    onChange={handleModelChange}
                    style={{ width: '205px' }}
                >
                    <option value="GradientBoosting">GradientBoosting</option>
                    <option value="RandomForest">RandomForest</option>
                </select>

                <div className="button-wrapper">
                    <button type="submit">Predict</button>
                </div>
            </form>
            {predictionResult && (
                <div className="prediction-result">
                    {predictionResult.elo_calculated_using_surface === false && (
                        <p style={{ color: 'red' }}>
                            ELO calculation not possible with the selected surface, calculations made using global ELO.
                        </p>
                    )}
                    {model === 'GradientBoosting' && (
                        <Tooltip
                            title={
                                <React.Fragment>
                                    <Typography variant="h6" align="center">Accuracy:</Typography>
                                    <Typography variant="body1" align="center">ELO AI: 64.27%</Typography>
                                    <Typography variant="body1" align="center">ELO HYPER AI: 63.09%</Typography>
                                    <Typography variant="body1" align="center">RANK AI: 62.49%</Typography>
                                    <Typography variant="body1" align="center">RANK HYPER AI: 60.66%</Typography>
                                    <Typography variant="body1" align="center">GLICKO AI: 72.89%</Typography>
                                    <Typography variant="body1" align="center">GLICKO HYPER AI: 71.56%</Typography>
                                </React.Fragment>
                            }
                        >
                            <IconButton size="small" style={{ color: 'white' }}>
                                <InfoIcon />
                            </IconButton>
                        </Tooltip>
                    )}

                    {model === 'RandomForest' && (
                        <Tooltip
                            title={
                                <React.Fragment>
                                    <Typography variant="h6" align="center">Accuracy:</Typography>
                                    <Typography variant="body1" align="center">ELO AI: 62.11%</Typography>
                                    <Typography variant="body1" align="center">ELO HYPER AI: 63.19%</Typography>
                                    <Typography variant="body1" align="center">RANK AI: 60.33%</Typography>
                                    <Typography variant="body1" align="center">RANK HYPER AI: 61.73%</Typography>
                                    <Typography variant="body1" align="center">GLICKO AI: 71.55%</Typography>
                                    <Typography variant="body1" align="center">GLICKO HYPER AI: 72.87%</Typography>
                                </React.Fragment>
                            }
                        >
                            <IconButton size="small" style={{ color: 'white' }}>
                                <InfoIcon />
                            </IconButton>
                        </Tooltip>
                    )}
                    <p>
                        (ELO): {predictionResult.player1_name}&nbsp;
                         <span style={{ color: predictionResult.winning_chance_player1 > 50 ? 'green' : predictionResult.winning_chance_player1 < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player1}%
                        </span> - <span style={{ color: predictionResult.winning_chance_player2 > 50 ? 'green' : predictionResult.winning_chance_player2 < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player2}%
                        </span>&nbsp;{predictionResult.player2_name}
                    </p>
                    <p>
                    (ELO AI): {predictionResult.player1_name}&nbsp;
                         <span style={{ color: predictionResult.winning_chance_player1_by_elo > 50 ? 'green' : predictionResult.winning_chance_player1_by_elo < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player1_by_elo}%
                        </span> - <span style={{ color: predictionResult.winning_chance_player2_by_elo > 50 ? 'green' : predictionResult.winning_chance_player2_by_elo < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player2_by_elo}%
                        </span>&nbsp;{predictionResult.player2_name}
                    </p>
                    <p>
                    (ELO HYPER AI): {predictionResult.player1_name}&nbsp;
                         <span style={{ color: predictionResult.winning_chance_player1_by_elo_hyper > 50 ? 'green' : predictionResult.winning_chance_player1_by_elo_hyper < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player1_by_elo_hyper}%
                        </span> - <span style={{ color: predictionResult.winning_chance_player2_by_elo_hyper > 50 ? 'green' : predictionResult.winning_chance_player2_by_elo_hyper < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player2_by_elo_hyper}%
                        </span>&nbsp;{predictionResult.player2_name}
                    </p>
                    <p>
                    (RANK AI): {predictionResult.player1_name}&nbsp;
                         <span style={{ color: predictionResult.winning_chance_player1_by_rank > 50 ? 'green' : predictionResult.winning_chance_player1_by_rank < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player1_by_rank}%
                        </span> - <span style={{ color: predictionResult.winning_chance_player2_by_rank > 50 ? 'green' : predictionResult.winning_chance_player2_by_rank < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player2_by_rank}%
                        </span>&nbsp;{predictionResult.player2_name}
                    </p>
                    <p>
                    (RANK HYPER AI): {predictionResult.player1_name}&nbsp;
                         <span style={{ color: predictionResult.winning_chance_player1_by_rank_hyper > 50 ? 'green' : predictionResult.winning_chance_player1_by_rank_hyper < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player1_by_rank_hyper}%
                        </span> - <span style={{ color: predictionResult.winning_chance_player2_by_rank_hyper > 50 ? 'green' : predictionResult.winning_chance_player2_by_rank_hyper < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player2_by_rank_hyper}%
                        </span>&nbsp;{predictionResult.player2_name}
                    </p>  
                    <p>
                    (GLICKO AI): {predictionResult.player1_name}&nbsp;
                         <span style={{ color: predictionResult.winning_chance_player1_by_glicko_normal > 50 ? 'green' : predictionResult.winning_chance_player1_by_glicko_normal < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player1_by_glicko_normal}%
                        </span> - <span style={{ color: predictionResult.winning_chance_player2_by_glicko_normal > 50 ? 'green' : predictionResult.winning_chance_player2_by_glicko_normal < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player2_by_glicko_normal}%
                        </span>&nbsp;{predictionResult.player2_name}
                    </p>  
                    <p>
                    (GLICKO AI HYPER): {predictionResult.player1_name}&nbsp;
                         <span style={{ color: predictionResult.winning_chance_player1_by_glicko_hyper > 50 ? 'green' : predictionResult.winning_chance_player1_by_glicko_hyper < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player1_by_glicko_hyper}%
                        </span> - <span style={{ color: predictionResult.winning_chance_player2_by_glicko_hyper > 50 ? 'green' : predictionResult.winning_chance_player2_by_glicko_hyper < 50 ? 'red' : 'grey' }}>
                            {predictionResult.winning_chance_player2_by_glicko_hyper}%
                        </span>&nbsp;{predictionResult.player2_name}
                    </p> 
                </div>
            )}
        </div>
    );
};

export default Home;
