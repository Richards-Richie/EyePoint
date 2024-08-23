import React from 'react';
import './logstyle.css';

function Back({toregister}) {
    return ( 
        <div className="topclass">
            <div id="top">
                <button id='back' type="submit"> <span className="material-icons arrow">arrow_back</span>Back</button>
                <button id='new'  type="submit" onClick={toregister}>Create New Account</button>
                <div className="hline"></div>
            </div>
        </div>
     );
}

export default Back;

