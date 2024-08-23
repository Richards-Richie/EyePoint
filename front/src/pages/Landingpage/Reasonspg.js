import React from 'react';
import './rstyle.css';

const Reasonspg = () => {
    return (
        <div id="container">
            <div id="firstcontainer">
                <p>Reasons We Are No. 1</p>
            </div>
            <div id="secondcontainer">
                <p>Customer satisfaction is our priority, and we ensure to deliver what we promise. Let us align our innovative ideas and strategies to your needs to generate unique and powerful results.</p>
            </div>
            <div className='rboxes'>
                <div id='rb1'>
                    <img src='./images/icon1.png' alt="icon"/>
                    <p id="box-content" >Cost Effective</p>
                </div>
                <div id='rb2'>
                    <img src='./images/icon2.png' alt="icon"/>
                    <p id="box-content" >Complete Research</p>
                </div>
                <div id='rb3'>
                    <img src='./images/icon3.png' alt="icon"/>
                    <p id="box-content" >Optimized to Hardware</p>
                </div>
            </div>
            <div className='rboxes'>
            <div id='rb4'>
                    <img src='./images/icon4.png' alt="icon"/>
                    <p id="box-content" >User friendly</p>
                </div>
                <div id='rb5'>
                    <img src='./images/icon5.png' alt="icon"/>
                    <p id="box-content" >RTD Processing</p>
                </div>
                <div id='rb6'>
                    <img src='./images/icon6.png' alt="icon"/>
                    <p id="box-content" >Lighting Compensation</p>
                </div>
            </div>
            <div className='rboxes'>
                <div id='rb7'>
                    <img src='./images/icon3.png' alt="icon"/>
                    <p id="box-content" >Advanced Image AI Processing</p>
                </div>

            </div>
        </div>
    );
}

export default Reasonspg;
