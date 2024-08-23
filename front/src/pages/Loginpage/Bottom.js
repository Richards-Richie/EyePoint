import React from 'react';

function Bottom({toreset}) {
    return ( 
        <div>
            <div>
                <p id="foot" onClick={toreset}>Can't log-in </p>
            </div>
        </div>
     );
}

export default Bottom;