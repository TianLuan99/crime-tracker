import React from "react";
import "./style.css";
import EditDeleteCrimeReportForm from "./EditDeleteCrimeReportForm";

function CrimeReportList({
  crimeReports,
  onSelect,
  onUpdate,
  onDelete,
  selected,
}) {
  return (
    <>
      <h5>Crime Reports</h5>
      <ul>
        {crimeReports.map((crimeReport) => (
          <li key={crimeReport.report_id} onClick={() => onSelect(crimeReport)}>
            <div className="crime-report">
              <span className="crime-report-label">Date:</span>
              <span className="crime-report-value">{crimeReport.date}</span>

              <span className="crime-report-label">Premise:</span>
              <span className="crime-report-value">
                {crimeReport.premise || "Unknown"}
              </span>

              <span className="crime-report-label">Weapon:</span>
              <span className="crime-report-value">
                {crimeReport.weapon || "Unknown"}
              </span>

              <span className="crime-report-label">Victim Age:</span>
              <span className="crime-report-value">
                {crimeReport.victim_age || "Unknown"}
              </span>

              <span className="crime-report-label">Victim Sex:</span>
              <span className="crime-report-value">
                {crimeReport.victim_sex || "Unknown"}
              </span>

              <span className="crime-report-label">Victim Descent:</span>
              <span className="crime-report-value">
                {crimeReport.victim_descent || "Unknown"}
              </span>
            </div>
            {selected == crimeReport && (
              <div>
                <EditDeleteCrimeReportForm
                  crimeReport={crimeReport}
                  onUpdate={onUpdate}
                  onDelete={onDelete}
                />
              </div>
            )}
          </li>
        ))}
      </ul>
    </>
  );
}

export default CrimeReportList;
