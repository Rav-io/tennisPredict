import React, { useState } from 'react';
import PlayerSearch from './PlayerSearch';
import { predictMatch } from '../api';

const PredictionForm = () => {
  const [surface, setSurface] = useState('hard');
  
  const handleSurfaceChange = (e) => {
    setSurface(e.target.value);
  };

  const handleSubmit = (player1Id, player2Id) => {
    predictMatch(player1Id, player2Id, surface)
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('There was an error fetching the prediction:', error);
      });
  };

  return (
    <div>
      <PlayerSearch onSubmit={handleSubmit} surface={surface} onSurfaceChange={handleSurfaceChange} />
    </div>
  );
};

export default PredictionForm;
