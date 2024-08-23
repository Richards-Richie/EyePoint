import React, { useState } from 'react';
import axios from 'axios';

// Utility function to get the CSRF token from the cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    const csrftoken = getCookie('csrftoken');

    axios.post('http://127.0.0.1:8000/login/', {
      email: email,
      password: password
    }, {
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
      }
    })
    .then(res => {
      console.log(res);
      
      setMessage('Login successful!');
    })
    .catch(error => {
      console.error('There was an error!', error);
      setMessage('Login failed. Please try again.');
    });
  }

  return (
    <div>
      <h2>Login</h2>
      {/* <form onSubmit={(e) => {
        e.preventDefault();
        handleLogin();
      }}> */}
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button onClick={() => handleLogin()} type="submit">Login</button>
      {/* </form> */}
      {message && <p>{message}</p>}
    </div>
  );
}

export default Login;
