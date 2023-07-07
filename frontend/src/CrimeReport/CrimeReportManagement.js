import React, { useState, useEffect } from "react";
import AddCrimeReportForm from "./AddCrimeReportForm";
import CrimeReportList from "./CrimeReportList";
import axios from "axios";

const API_BASE_URL = "https://crime-tracker-backend-dot-cs411-pt1-crimetracker.uc.r.appspot.com/";

function CrimeReportManagement({ selectedIncident }) {
  const [crimeReports, setCrimeReports] = useState([]);
  const [selectedCrimeReport, setSelectedCrimeReport] = useState(null);

  useEffect(() => {
    fetchCrimeReports(selectedIncident);
  }, [selectedIncident]);

  const fetchCrimeReports = async (incidentId) => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/crime-report/${incidentId}`
      );
      setCrimeReports(response.data);
    } catch (error) {
      console.error("Error fetching crime reports:", error);
    }
  };

  const handleAddCrimeReport = (newCrimeReport) => {
    try {
      axios.post(`${API_BASE_URL}/crime-report/`, {
        ...newCrimeReport,
        incident_id: selectedIncident,
        user_id: 0,
      });
      setCrimeReports([...crimeReports, newCrimeReport]);
    } catch (error) {
      console.error("Error adding crime report:", error);
    }
  };

  const handleSelectCrimeReport = (crimeReport) => {
    setSelectedCrimeReport(crimeReport);
  };

  const handleUpdateCrimeReport = (updatedCrimeReport) => {
    try {
      axios.put(
        `${API_BASE_URL}/crime-report/${updatedCrimeReport.incident_id}/${updatedCrimeReport.user_id}/${updatedCrimeReport.report_id}`,
        {
          ...updatedCrimeReport,
          incident_id: selectedIncident,
          user_id: 0,
          report_id: selectedCrimeReport.report_id,
        }
      );
      setCrimeReports(
        crimeReports.map((crimeReport) =>
          crimeReport.report_id === updatedCrimeReport.report_id
            ? updatedCrimeReport
            : crimeReport
        )
      );
    } catch (error) {
      console.error("Error updating crime report:", error);
    }
    setSelectedCrimeReport(null);
  };

  const handleDeleteCrimeReport = () => {
    try {
      axios.delete(
        `${API_BASE_URL}/crime-report/${selectedCrimeReport.incident_id}/${selectedCrimeReport.user_id}/${selectedCrimeReport.report_id}`
      );
      setCrimeReports(
        crimeReports.filter(
          (crimeReport) => crimeReport !== selectedCrimeReport
        )
      );
    } catch (error) {
      console.error("Error deleting crime report:", error);
    }
    setSelectedCrimeReport(null);
  };

  return (
    <>
      {selectedIncident && (
        <div>
          <CrimeReportList
            incidentId={selectedIncident}
            crimeReports={crimeReports}
            onSelect={handleSelectCrimeReport}
            onUpdate={handleUpdateCrimeReport}
            onDelete={handleDeleteCrimeReport}
            selected={selectedCrimeReport}
          />
        </div>
      )}

      {selectedIncident && (
        <div>
          <AddCrimeReportForm onAdd={handleAddCrimeReport} />
        </div>
      )}
    </>
  );
}

export default CrimeReportManagement;
