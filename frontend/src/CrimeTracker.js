import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import CrimeIncident from "./CrimeIncident/CrimeIncident";
import FloatingWindow from "./QueryWindow/FloatingWindow";
import "bootstrap/dist/css/bootstrap.min.css";
import { Row, Col } from "react-bootstrap";
import MyMap from "./Map/MyMap";
import "./CrimeTracker.css";
import CustomReport from "./CustomReport/CustomReport";

const API_BASE_URL = "https://crime-tracker-backend-dot-cs411-pt1-crimetracker.uc.r.appspot.com/";

const CrimeTracker = () => {
  const [incidents, setIncidents] = useState([]);
  const [searchLocation, setSearchLocation] = useState("");
  const [searchStatus, setSearchStatus] = useState("");
  const [newIncidentLocation, setNewIncidentLocation] = useState("");
  const [newIncidentDate, setNewIncidentDate] = useState("");
  const [newIncidentTime, setNewIncidentTime] = useState("");
  const [newIncidentStatus, setNewIncidentStatus] = useState("");
  const [selectedIncident, setSelectedIncident] = useState(null);

  const mapRef = useRef();

  useEffect(() => {
    fetchIncidents();
  }, []);

  const handleShowPositionClick = (location_name) => {
    try {
      axios.get(`${API_BASE_URL}/location/${location_name}`).then((res) => {
        if (res.data != null) {
          const { latitude, longitude } = res.data;
          mapRef.current.props.onChangeMap(Number(latitude), Number(longitude));
          mapRef.current.map.setCenter({
            lat: Number(latitude),
            lng: Number(longitude),
          });
        } else {
          mapRef.current.props.onChangeMap(null, null);
          mapRef.current.map.setCenter({ lat: 34.0522, lng: -118.2437 });
        }
      });
    } catch (err) {
      console.log(err);
    }
  };

  const fetchIncidents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/crime-incident`);
      setIncidents(response.data);
    } catch (error) {
      console.error("Error fetching crime incidents:", error);
    }
  };

  const searchIncidents = async () => {
    try {
      const response = await axios.post(
        `${API_BASE_URL}/crime-incident/query`,
        {
          location_name: searchLocation,
          status: searchStatus,
        }
      );
      setSearchLocation("");
      setSearchStatus("");
      setIncidents(response.data);
    } catch (error) {
      console.error("Error fetching crime incidents:", error);
    }
  };

  const addIncident = async () => {
    try {
      await axios.post(`${API_BASE_URL}/crime-incident/`, {
        location_name: newIncidentLocation,
        date: newIncidentDate,
        time: newIncidentTime,
        status: newIncidentStatus,
      });
      setNewIncidentDate("");
      setNewIncidentLocation("");
      setNewIncidentStatus("");
      setNewIncidentTime("");
      fetchIncidents();
    } catch (error) {
      console.error("Error adding crime incident:", error);
    }
  };

  const updateIncident = async (incidentId, incident) => {
    try {
      await axios.put(`${API_BASE_URL}/crime-incident/${incidentId}`, incident);
      fetchIncidents();
    } catch (error) {
      console.error("Error updating crime incident:", error);
    }
  };

  const deleteIncident = async (incidentId) => {
    try {
      await axios.delete(`${API_BASE_URL}/crime-incident/${incidentId}`);
      fetchIncidents();
    } catch (error) {
      console.error("Error deleting crime incident:", error);
    }
  };
  const isLoggedIn = false;

  return (
    <div className="crime-tracker-container">
      <h1 className="crime-tracker-title">Crime Tracker</h1>
      {/* <div className="crime-tracker-auth">
        {isLoggedIn ? (
          <a href="#" className="crime-tracker-auth-link">
            Log out
          </a>
        ) : (
          <div>
            <a href="/login" className="crime-tracker-auth-link">
              Sign in
            </a>{" "}
            |{" "}
            <a href="/register" className="crime-tracker-auth-link">
              Sign up
            </a>
          </div>
        )}
      </div> */}
      <hr />
      <Row>
        <Col sm={3}>
          <div className="crime-tracker-search">
            <h2 className="crime-tracker-section-title">Search Incidents</h2>
            <label>
              Location:
              <br />
              <input
                type="text"
                value={searchLocation}
                onChange={(e) => setSearchLocation(e.target.value)}
              />
            </label>
            <br />
            <label>
              Status:
              <br />
              <input
                type="text"
                value={searchStatus}
                onChange={(e) => setSearchStatus(e.target.value)}
              />
            </label>
            <br />
            <button className="crime-tracker-button" onClick={searchIncidents}>
              Search
            </button>
          </div>
          <br />
          <div className="crime-tracker-report">
            <h2 className="crime-tracker-section-title">Report Incident</h2>
            <div>
              <label>
                Location Name:
                <br />
                <input
                  type="text"
                  value={newIncidentLocation}
                  onChange={(e) => setNewIncidentLocation(e.target.value)}
                />
              </label>
              <br />
              <label>
                Date:
                <br />
                <input
                  type="text"
                  value={newIncidentDate}
                  onChange={(e) => setNewIncidentDate(e.target.value)}
                />
              </label>
              <br />
              <label>
                Time:
                <br />
                <input
                  type="text"
                  value={newIncidentTime}
                  onChange={(e) => setNewIncidentTime(e.target.value)}
                />
              </label>
              <br />
              <label>
                Status:
                <br />
                <input
                  type="text"
                  value={newIncidentStatus}
                  onChange={(e) => setNewIncidentStatus(e.target.value)}
                />
              </label>
              <br />
              <button className="crime-tracker-button" onClick={addIncident}>
                Report
              </button>
            </div>
          </div>
        </Col>
        <Col sm={6}>
          <div className="crime-tracker-map">
            <MyMap mapRef={mapRef} />
          </div>
          <br />
          <div className="crime-tracker-list">
            <ul>
              {incidents.map((incident) => (
                <CrimeIncident
                  key={incident.incident_id}
                  incident={incident}
                  onDelete={deleteIncident}
                  onUpdate={updateIncident}
                  onSelect={() => setSelectedIncident(incident)}
                  selected={selectedIncident === incident}
                  onShowPosition={handleShowPositionClick}
                />
              ))}
            </ul>
          </div>
        </Col>
        <Col sm={3}>
          <FloatingWindow />
        </Col>
      </Row>
      <CustomReport />
    </div>
  );
};

export default CrimeTracker;
