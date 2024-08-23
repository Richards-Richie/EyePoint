import React from "react";
import "./lstyle.css";
import { useNavigate } from "react-router-dom";

function Landingnav() {
    const navigate = useNavigate();
    return (
        <div className="landing-header">
            <div className="landing-logo">
                <img src="./images/logo.png" alt="Logo" className="landing-logo" />
            </div>
            <div className="landing-nav">
                <nav className="landing-navigation">
                    <ul>
                        <li>
                            <a href="#c1">Home</a>
                        </li>
                        <li>
                            <a href="#Ourservices">Our Services</a>
                        </li>
                        <li>
                            <a href="#App">Process</a>
                        </li>
                        <li>
                            <a href="#container">Why Choose Us</a>
                        </li>
                        <li>
                            <a href="#about-us">About Us</a>
                        </li>
                    </ul>
                </nav>
                <div className="landing-buttons">
                    <button className="landing-register-btn" onClick={() => navigate('/register')}>Register</button>
                    <button className="landing-login-btn" onClick={() => navigate('/login')}>Login</button>
                </div>
            </div>
        </div>
    );
};

export default Landingnav;
