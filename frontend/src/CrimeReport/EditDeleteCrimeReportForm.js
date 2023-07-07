import React, { useState } from "react";

function EditDeleteCrimeReportForm({ crimeReport, onUpdate, onDelete }) {
  const [editCrimeReport, setEditCrimeReport] = useState(crimeReport);

  const handleUpdate = (e) => {
    e.preventDefault();
    onUpdate(editCrimeReport);
  };

  return (
    <>
      <div>
        <div>
          <h6>Edit Crime Report</h6>
          <form onSubmit={handleUpdate}>
            <label>
              Date:
              <input
                type="text"
                value={editCrimeReport.date}
                onChange={(e) =>
                  setEditCrimeReport({
                    ...editCrimeReport,
                    date: e.target.value,
                  })
                }
              />
            </label>
            <label>
              Weapon:
              <input
                type="text"
                value={editCrimeReport.weapon}
                onChange={(e) =>
                  setEditCrimeReport({
                    ...editCrimeReport,
                    weapon: e.target.value,
                  })
                }
              />
            </label>
            <label>
              Premise:
              <input
                type="text"
                value={editCrimeReport.premise}
                onChange={(e) =>
                  setEditCrimeReport({
                    ...editCrimeReport,
                    premise: e.target.value,
                  })
                }
              />
            </label>
            <label>
              Victim Age:
              <input
                type="text"
                value={editCrimeReport.victim_age}
                onChange={(e) =>
                  setEditCrimeReport({
                    ...editCrimeReport,
                    victim_age: e.target.value,
                  })
                }
              />
            </label>
            <label>
              Victim Sex:
              <input
                type="text"
                value={editCrimeReport.victim_sex}
                onChange={(e) =>
                  setEditCrimeReport({
                    ...editCrimeReport,
                    victim_sex: e.target.value,
                  })
                }
              />
            </label>
            <label>
              Victim Descent:
              <input
                type="text"
                value={editCrimeReport.victim_descent}
                onChange={(e) =>
                  setEditCrimeReport({
                    ...editCrimeReport,
                    victim_descent: e.target.value,
                  })
                }
              />
            </label>
            <button type="submit">Update</button>
            <button onClick={onDelete}>Delete</button>
          </form>
        </div>
      </div>
    </>
  );
}

export default EditDeleteCrimeReportForm;
