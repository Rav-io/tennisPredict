import React from 'react';
import logo from '../logo.png';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header>
       <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
        <h1>
        <img src={logo} alt="Logo" style={{ height: '8vw' }} />
        Tennis App
        </h1>
        </Link>
    </header>
  );
};

export default Header;
