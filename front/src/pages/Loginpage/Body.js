import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

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

function Body() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

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
            navigate('/eyepoint');
        })
        .catch(error => {
            console.error('There was an error!', error);
            setMessage('Login failed. Please try again.');
        });
    }

    return (
        <div id="view">
            <div className="box">
                <div id="box-in">
                    <h3 id="box-heading">Log in</h3>
                    <label id="etext" className='ltext' htmlFor="email">Email address</label><br />
                    <input id='ebox' className='lbtext' type='email' value={email} onChange={(e) => setEmail(e.target.value)} /><br/><br/>
                    <label id="passtext" className='forhei' htmlFor="Password">Password</label><br/>
                    <input id='pbox' className='forhei' type="password" value={password} onChange={(e) => setPassword(e.target.value)} /><br/><br/>
                    <button id='log1' className='forhei' onClick={handleLogin} type="submit">Log in</button>
                </div>
            </div>
            <div>
                <div className="line"></div>
                <div id="or"> OR </div>
                <div className="line"></div>
            </div>
            <div className="box" id="box">
                <p className='google'>Continue with Google</p>
                <p className='email'>Sign up with email</p>
            </div>
            {message && <p>{message}</p>}
        </div>
    );
}

export default Body;
