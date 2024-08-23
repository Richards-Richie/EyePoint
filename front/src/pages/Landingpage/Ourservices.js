import React from 'react';
import './ostyle.css';

const Ourservices = () => {
    return (
        <div id="Ourservices" >
          <header className="header">
            <h1>Our Services</h1>
          </header>
          <div className="services-main-content">
            <div className="services-box-container">
              <div className="services-image-container">
                <img src='./images/topLeftcloud.png' alt="Top Left" className="top-left-image" />
                <img src='./images/topRightcloud.png' alt="Top Right" className="top-right-image" />
                <img src='./images/bottomRightcloud.png' alt="Bottom Right" className="bottom-right-image" />
              </div>
              <div className="services-box">
                <div className="services-logo-heading">
                  <img src='./images/message.png' alt="Logo" className="services-logo" /><br />
                  <p className="FunWindow">Fun Window</p>
                </div>
                <p className="services-description">
                  Eye points solution to gaze visualization involves key components such as advanced
                  image processing AI algorithm, seamless integration and compatibility, Real time data 
                  processing and optimizing for hardware constraints.
                </p>
                <p className="services-description">
                  Eyepoint aims to overcome the significant hurdles in standard camera based iris 
                  tracking, providing an accurate, adaptable and accessible tool for a wide range of
                  applications in user interaction and technology.
                </p>
                <div className="arrow-container">
                  <img src='./images/arrow_services.png' alt="arrow" className="arrow" /><br />
                </div>
              </div>
            </div>
          </div>      
   
        </div>
  );
}

export default Ourservices;