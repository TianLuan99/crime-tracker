import React, { useState } from "react";
import CrimeReportManagement from "../CrimeReport/CrimeReportManagement";
import "./style.css";

function CrimeIncident({
  incident,
  onDelete,
  onUpdate,
  onSelect,
  selected,
  onShowPosition,
}) {
  const [updatedIncident, setUpdatedIncident] = useState({
    date: "",
    time: "",
    status: "",
  });

  return (
    <li className="crime-incident">
      <span className="id">No. {incident.incident_id || "No Incident ID"}</span>
      <span className="location">
        Crime Location: {incident.location_name || "No Location Name"}
      </span>
      <span className="date">Crime Date: {incident.date || "No Date"}</span>
      <span className="time">Crime Time: {incident.time || "No Time"}</span>
      <span className="status">
        Crime Status: {incident.status || "No Status"}
      </span>
      <span className="actions">
        <button onClick={() => onSelect(incident.incident_id)}>
          Show Crime Reports
        </button>
        <button onClick={() => onShowPosition(incident.location_name)}>
          Show Position
        </button>
        <button onClick={() => onDelete(incident.incident_id)}>Delete</button>
      </span>
      {selected && (
        <CrimeReportManagement selectedIncident={incident.incident_id} />
      )}
      <label> Date: </label>
      <input
        type="text"
        value={updatedIncident.date}
        onChange={(e) =>
          setUpdatedIncident({ ...updatedIncident, date: e.target.value })
        }
      />
      <label> Time: </label>
      <input
        type="text"
        value={updatedIncident.time}
        onChange={(e) =>
          setUpdatedIncident({ ...updatedIncident, time: e.target.value })
        }
      />
      <label> Status: </label>
      <input
        type="text"
        value={updatedIncident.status}
        onChange={(e) =>
          setUpdatedIncident({ ...updatedIncident, status: e.target.value })
        }
      />
      <span className="actions">
        <button
          className="actions"
          onClick={() => {
            onUpdate(incident.incident_id, updatedIncident);
            setUpdatedIncident({ date: "", time: "", status: "" });
          }}
        >
          Update
        </button>
      </span>
      <hr />
    </li>
  );
}

export default CrimeIncident;
