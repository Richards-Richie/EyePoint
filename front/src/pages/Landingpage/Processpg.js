import React from 'react';
import './pstyle.css';

function Processpg({toregister, tologin}) {
  return (
    <div id="App">

      <div className="process-container">
        <div className="firstcont">
          <p id="pfirst">Our Simple Process to Order</p>
          <p id="psecond"> Customer satisfaction is our priority, and we ensure to deliver what we promise. The simpler the process the better the product.</p>
          <p id="pthird">The user has to register themselves and later on a small Biometric registration takes place which in most cases takes in a blink of an eye</p>
          <div className="submit-container">
            <div id="reg" className="submit" onClick={toregister} >Register</div>
            <div id="log" className="submit" onClick={tologin} >Login</div>
          </div>
        </div>

        <div className="imboxes">
            <div id="firstimgbox" className="process-step">
                <img src='./images/rocket.png' alt="rocket"/>
                <p>Register</p>
            </div>

            <div id="secimgbox" className="process-step">
                <img src='./images/info.png' alt="Registration"/>
                <p>BioMetric Registration</p>
            </div>

            <div id="thirdimgbox" className="process-step">
                <img src='./images/reviews.png' alt="Reviews"/>
                <p>Fun Window</p>
            </div>

        </div>
      </div>
    </div>
  );
}

export default Processpg;
