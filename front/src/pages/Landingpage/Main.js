import React from"react";
import Landingnav from "./Landingnav";
import Landingpg from "./Landingpg";
import Ourservices from "./Ourservices";
import Processpg from "./Processpg";
import Reasonspg from "./Reasonspg";
import Contactpg from "./Contactpg";
import "./globalstyles.css";

function Main({toregister, tologin}) {
    return(

        <div>
            <Landingnav toregister={toregister} tologin={tologin}/>
            <Landingpg/>
            <Ourservices/>
            <Processpg toregister={toregister} tologin={tologin}/>
            <Reasonspg/>
            <Contactpg/>
        </div>
    );
};
export default Main;