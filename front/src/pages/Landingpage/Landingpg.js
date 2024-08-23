import React from "react";
import "./lstyle.css";

function Landingpg() {
    return(
        <div id="c1">
            <div className="landing-text-container">
                <div id="line1" className="content1"><p>Revolutionize</p></div>
                <div id="line2" className="content1"><p>Interaction</p></div>
                <div className="line3"><p>UNLOCK NEW DIMENSIONS  OF INTERACTION WITH EYEPOINT’S CUTTING EDGE GAZE TRACKING </p></div>
                <div className="line3"><p>TECHNOLOGY</p></div>
                <div className="line4"><p>Experience seamless integration</p></div>
                <div id="lastline" className="line4"><p>and unrivaled precision with EyePoint’s adaptable eye tracking software</p></div>
                <button className="servicesbutton">Services</button>
            </div>
            <div className="robo-image">
                <img src="./images/robo.png" alt="robo" />
            </div>
        </div>
    );
};

export default Landingpg;
