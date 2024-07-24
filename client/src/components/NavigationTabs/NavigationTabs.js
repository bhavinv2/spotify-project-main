import React from 'react';
import { NavLink } from 'react-router-dom';
import './NavigationTabs.css';

const NavigationTabs = () => {
  return (
    <nav className="navigation-tabs">
      <NavLink exact to="/" activeClassName="active">
        Home
      </NavLink>
      <NavLink to="/chatbot" activeClassName="active">
        Chat with Your Stats
      </NavLink>
      <NavLink to="/mood-playlist" activeClassName="active">
        Mood Playlist
      </NavLink>
    </nav>
  );
};

export default NavigationTabs;