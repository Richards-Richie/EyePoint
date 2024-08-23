// src/Resetpg.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './resetstyle.css';

function Resetpg() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [password, setPassword] = useState('');
    const [otpSent, setOtpSent] = useState(false);
    const [error, setError] = useState('');

    const handleSendOtp = async (event) => {
        event.preventDefault();
        setError('');
        const userData = { email };

        try {
            const response = await fetch('http://127.0.0.1:8000/send_otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                console.log('OTP sent successfully');
                setOtpSent(true);
            } else {
                setError('Failed to send OTP. Please check the email address.');
            }
        } catch (error) {
            setError('Error during OTP request: ' + error.message);
        }
    };

    const handleResetPassword = async (event) => {
        event.preventDefault();
        setError('');
        const resetData = { email, otp, password };

        try {
            const response = await fetch('http://127.0.0.1:8000/reset_password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(resetData)
            });

            if (response.ok) {
                console.log('Password reset successfully');
                navigate('/login');
            } else {
                setError('Failed to reset password. Please check the OTP and try again.');
            }
        } catch (error) {
            setError('Error during password reset: ' + error.message);
        }
    };

    return (
        <div className="reset-page-container">
            <div className="reset-back-link" onClick={() => navigate(-1)}>
                <span className="material-icons arrow">arrow_back</span>Back
            </div>
            <div className="horizontal-line"></div>
            <img src="./images/logo.png" alt="Logo" className="reset-logo" />
            <div className="reset-container">
                <h1 className="reset-title">Reset Your Password</h1>
                <div className="reset-content">
                    <div className="left">
                        <div className="input-group">
                            <label htmlFor="email">Email Address</label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                        {otpSent && (
                            <>
                                <div className="input-group">
                                    <label htmlFor="otp">Enter OTP</label>
                                    <input
                                        type="text"
                                        id="otp"
                                        value={otp}
                                        onChange={(e) => setOtp(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className="input-group">
                                    <label htmlFor="password">New Password</label>
                                    <input
                                        type="password"
                                        id="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                    />
                                </div>
                            </>
                        )}
                    </div>
                    <div className="right">
                        {!otpSent ? (
                            <button className="otp-button" onClick={handleSendOtp}>Send OTP</button>
                        ) : (
                            <button className="otp-button" onClick={handleResetPassword}>Reset Password</button>
                        )}
                    </div>
                </div>
                {error && <div className="error-message">{error}</div>}
            </div>
        </div>
    );
};

export default Resetpg;
