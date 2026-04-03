import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar">
      <ul className="sidebar-nav">
        <li>
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
             Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink to="/opportunities" className={({ isActive }) => (isActive ? 'active' : '')}>
             Opportunities
          </NavLink>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
