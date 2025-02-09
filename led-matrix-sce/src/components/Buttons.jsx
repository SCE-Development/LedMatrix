import React from 'react';
import '../styles/Buttons.css';
import { useNavigate, useLocation } from 'react-router-dom';

const Buttons = () => {
    const navigate = useNavigate();
    const location = useLocation();

    return (
        <div className="button-stack">
            <button
                className={location.pathname === '/' ? 'selected' : ''}
                onClick={() => navigate('/')}
            >
                Leetcode Leaderboard
            </button>
            <button
                className={location.pathname === '/announcement' ? 'selected' : ''}
                onClick={() => navigate('/announcement')}
            >
                Announcement
            </button>
            <button>Clock & Weather</button>
        </div>
    );
};

export default Buttons;
