import React, { useState } from "react";

function AddCrimeReportForm({ onAdd }) {
  const [newCrimeReport, setNewCrimeReport] = useState({
    date: "",
    weapon: "",
    premise: "",
    victim_age: "",
    victim_sex: "",
    victim_descent: "",
  });

  const handleAdd = (e) => {
    e.preventDefault();
    onAdd(newCrimeReport);
    setNewCrimeReport({
      date: "",
      weapon: "",
      premise: "",
      victim_age: "",
      victim_sex: "",
      victim_descent: "",
    });
  };

  return (
    <div>
      <h5>Add Crime Report</h5>
      <form onSubmit={handleAdd}>
        <label>
          Date:
          <input
            type="text"
            value={newCrimeReport.date}
            onChange={(e) =>
              setNewCrimeReport({ ...newCrimeReport, date: e.target.value })
            }
          />
        </label>
        <label>
          Weapon:
          <input
            type="text"
            value={newCrimeReport.weapon}
            onChange={(e) =>
              setNewCrimeReport({ ...newCrimeReport, weapon: e.target.value })
            }
          />
        </label>
        <label>
          Premise:
          <input
            type="text"
            value={newCrimeReport.premise}
            onChange={(e) =>
              setNewCrimeReport({ ...newCrimeReport, premise: e.target.value })
            }
          />
        </label>
        <label>
          Victim Age:
          <input
            type="text"
            value={newCrimeReport.victim_age}
            onChange={(e) =>
              setNewCrimeReport({
                ...newCrimeReport,
                victim_age: e.target.value,
              })
            }
          />
        </label>
        <label>
          Victim Sex:
          <input
            type="text"
            value={newCrimeReport.victim_sex}
            onChange={(e) =>
              setNewCrimeReport({
                ...newCrimeReport,
                victim_sex: e.target.value,
              })
            }
          />
        </label>
        <label>
          Victim Descent:
          <input
            type="text"
            value={newCrimeReport.victim_descent}
            onChange={(e) =>
              setNewCrimeReport({
                ...newCrimeReport,
                victim_descent: e.target.value,
              })
            }
          />
        </label>
        <button type="submit">Add</button>
      </form>
    </div>
  );
}

export default AddCrimeReportForm;
