import React from 'react';
import { Link } from 'react-router-dom';
import TickerSearch from '../Search/TickerSearch';

const Navbar: React.FC = () => {
  return (
    <nav className="navbar glass-card animate-fade-in">
      <div className="logo">
        <Link to="/">
          <span className="neon-gradient-text">SignalStack</span>
        </Link>
      </div>
      <div className="nav-search">
         <TickerSearch />
      </div>
      <div className="nav-actions">
        <button className="btn-secondary">Settings</button>
      </div>
    </nav>
  );
};

export default Navbar;
