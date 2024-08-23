import React from 'react';
import Back from './Back';
import Heading from './Heading';
import Body from './Body';
import Bottom from './Bottom';

function Login({toreset, toregister}) {
    return ( 
        <div>
            <Back toregister={toregister}/>
            <Heading />
            <Body />
            <Bottom toreset={toreset}/>
        </div>
     );
}

export default Login;