import React, { useState } from 'react';
import { searchPlayers } from '../api';

const PlayerSearch = ({ onSubmit, surface, onSurfaceChange }) => {
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');

  const handleSearch = (player, setPlayer) => {
    searchPlayers(player)
      .then(data => {
        setPlayer(data);
      })
      .catch(error => {
        console.error('Error fetching players:', error);
      });
  };

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      onSubmit(player1, player2);
    }}>
      <select value={surface} onChange={onSurfaceChange}>
        <option value="hard">Hard</option>
        <option value="clay">Clay</option>
        <option value="grass">Grass</option>
      </select>
      <input type="submit" value="Predict" />
    </form>
  );
};

export default PlayerSearch;
