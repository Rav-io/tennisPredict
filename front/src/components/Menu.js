import React from 'react';
import { Link } from 'react-router-dom';
import './Menu.css';

const Menu = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/glicko-history">Glicko History</Link>
        </li>
        <li>
          <Link to="/elo-history">Elo History</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Menu;
