import React, { useState } from "react";
import axios from "axios";
import "./regstyle.css";
import { useNavigate } from 'react-router-dom';

const RegisterPage = ({ tologin }) => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSendOtp = async (event) => {
    event.preventDefault();
    
    const userData = {
      username: username,
      email: email
    };

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
        setStep(2);
      } else {
        console.error('Failed to send OTP');
      }
    } catch (error) {
      console.error('Error during OTP send:', error);
    }
  };

  const handleRegister = async (event) => {
    event.preventDefault();
    
    const userData = {
      username: username,
      email: email,
      otp: otp,
      password: password
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      if (response.ok) {
        console.log('Registration successful');
        navigate('/login');
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Registration failed');
        navigate('/register');
      }
    } catch (error) {
      console.error('Error during registration:', error);
    }
  };

  return (
    <div className="register-container">
      {step === 1 && (
        <form onSubmit={handleSendOtp}>
          <div className="top-right">
            <p>Already have an account? <span id="log-in" onClick={tologin}>log-in</span> </p>
          </div>
          <div className="logo">
            <img src="./images/logo.png" alt="Logo" className="logo" />
          </div>
          <div className="register-box">
            <div className="header">
              <h2>Create an account</h2>
            </div>
            <div className="input-group">
              <label>Username:</label>
              <div>
                <input type="text" value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required />
              </div>
            </div>
            <div className="input-group">
              <label>Email:</label>
              <div>
                <input type="email" value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required />
              </div>
              <p className="note">
                We strongly recommend adding an email address. This will help verify
                your account and keep it safe.
              </p>
            </div>
            <button type="submit" className="button">Send OTP</button>
          </div>
        </form>
      )}

      {step === 2 && (
        <form onSubmit={handleRegister}>
          <div className="input-group">
            <label>Email:</label>
            <div>
              <input type="email" value={email} readOnly />
            </div>
          </div>
          <div className="input-group">
            <label>Enter OTP:</label>
            <div>
              <input type="text" value={otp}
                onChange={(e) => setOtp(e.target.value)}
                required />
            </div>
          </div>
          <div className="input-group">
            <label>Password:</label>
            <div>
              <input type="password" value={password}
                onChange={(e) => setPassword(e.target.value)}
                required />
            </div>
          </div>
          <div className="bullet-points">
            <ul>
              <li>Use 8 or more characters</li>
              <li>Use upper and lower case letters (e.g., Aa)</li>
              <li>Use a number (e.g., 1234)</li>
              <li>Use a symbol (e.g., #@!)</li>
            </ul>
          </div>
          {error && <p className="error">{error}</p>}
          <button type="submit" className="button">Sign Up</button>
          <div className="terms">
            By creating an account, you agree to the{" "}
            <a href="/terms" className="highlight">
              Terms of Use
            </a>{" "}
            and{" "}
            <a href="/privacy" className="highlight">
              Privacy Policy
            </a>
            .
          </div>
        </form>
      )}
    </div>
  );
};

export default RegisterPage;
