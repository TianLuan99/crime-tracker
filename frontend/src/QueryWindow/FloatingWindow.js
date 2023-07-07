import React, { useState, useEffect } from "react";
import axios from "axios";
import "./style.css";

const API_BASE_URL = "https://crime-tracker-backend-dot-cs411-pt1-crimetracker.uc.r.appspot.com/";

const FloatingWindow = () => {
  const [
    centralWestFemaleVictimDescentData,
    setCentralWestFemaleVictimDescentData,
  ] = useState([]);
  const [
    patrolDivisionYoungVictimData,
    setPatrolDivisionYoungVictimData,
  ] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/query/female-crime-descent-count`
      );
      setCentralWestFemaleVictimDescentData(response.data);
      const response2 = await axios.get(`${API_BASE_URL}/query/crime_stats`);
      setPatrolDivisionYoungVictimData(response2.data);
      // console.log(response2.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleRefreshClick = async () => {
    fetchData();
  };

  return (
    <div className="floating-window">
      <b>
        <h2 className="floating-window-title">Statistics</h2>
      </b>
      <div className="floating-window-section">
        <h5 className="floating-window-section-title">
          Central West Female Victim Descent Data
        </h5>
        <ul>
          {centralWestFemaleVictimDescentData.map((item) => (
            <li key={item.Descent}>
              {item.Descent}: {item.Crime_Count}
            </li>
          ))}
        </ul>
      </div>
      <div className="floating-window-section">
        <h5 className="floating-window-section-title">
          Battery Crime Young Victim Patrol Division Data
        </h5>
        <ul>
          {patrolDivisionYoungVictimData.map((item) => (
            <li key={item.Patrol_Division}>
              {item.Patrol_Division}: {item.Crime_Count}
            </li>
          ))}
        </ul>
      </div>
      <button className="floating-window-button" onClick={handleRefreshClick}>
        Refresh
      </button>
    </div>
  );
};

export default FloatingWindow;
