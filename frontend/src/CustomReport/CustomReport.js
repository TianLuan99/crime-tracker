import React, { useState, useEffect } from "react";
import axios from "axios";
import Chart from "chart.js/auto";
import "./CustomReport.css";

const CustomReport = () => {
  const [crimeData, setCrimeData] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const API_BASE_URL = "https://crime-tracker-backend-dot-cs411-pt1-crimetracker.uc.r.appspot.com/";

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        `${API_BASE_URL}/query/generate_report`,
        {
          start_date: startDate,
          end_date: endDate,
        }
      );
      setCrimeData(response.data);
    } catch (error) {
      console.error("Error when get report:", error);
    }
  };

  useEffect(() => {
    let chart1, chart2, chart3;

    if (crimeData.length > 0) {
      const ctx = document.getElementById("crimeChart");
      const patrolDivision = crimeData.map((item) => item.patrol_division);
      const totalCrimes = crimeData.map((item) => item.total_crimes);

      chart1 = new Chart(ctx, {
        type: "bar",
        data: {
          labels: patrolDivision,
          datasets: [
            {
              label: "Crime Count",
              data: totalCrimes,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                },
              },
            ],
          },
        },
      });

      const weaponCount = crimeData.map((item) => item.weapon_count);
      const ctx2 = document.getElementById("weaponCountChart");

      chart2 = new Chart(ctx2, {
        type: "bar",
        data: {
          labels: patrolDivision,
          datasets: [
            {
              label: "Weapon Count",
              data: weaponCount,
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            yAxes: [
              {
                ticks: {
                  beginAtZero: true,
                },
              },
            ],
          },
        },
      });

      const mostCommonCrimeTypes = crimeData.map(
        (item) => item.most_common_crime_description
      );
      const uniqueCrimeTypes = [...new Set(mostCommonCrimeTypes)];
      const crimeTypeCounts = uniqueCrimeTypes.map(
        (type) => mostCommonCrimeTypes.filter((crime) => crime === type).length
      );

      const ctx3 = document.getElementById("mostCommonCrimeTypesChart");

      chart3 = new Chart(ctx3, {
        type: "pie",
        data: {
          labels: uniqueCrimeTypes,
          datasets: [
            {
              data: crimeTypeCounts,
              backgroundColor: [
                "rgba(255, 99, 132, 0.5)",
                "rgba(54, 162, 235, 0.5)",
                "rgba(255, 206, 86, 0.5)",
                "rgba(75, 192, 192, 0.5)",
                "rgba(153, 102, 255, 0.5)",
                "rgba(255, 159, 64, 0.5)",
                "rgba(101, 137, 164, 0.5)",
              ],
              borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
                "rgba(255, 159, 64, 1)",
                "rgba(101, 137, 164, 1)",
              ],
              borderWidth: 1,
            },
          ],
        },
      });
    }

    return () => {
      if (chart1) {
        chart1.destroy();
      }
      if (chart2) {
        chart2.destroy();
      }
      if (chart3) {
        chart3.destroy();
      }
    };
  }, [crimeData]);

  return (
    <div className="container">
      <h1>Create Your Own Report</h1>
      <form className="report-form" onSubmit={handleSubmit}>
        <label className="date-label">
          From:
          <input
            type="date"
            className="date-input"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>
        <label className="date-label">
          To:
          <input
            type="date"
            className="date-input"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
        <button className="submit-button" type="submit">
          Generate Your Report
        </button>
      </form>
      <div className="charts">
        <div className="chart">
          <h2>Crime Count</h2>
          <canvas id="crimeChart"></canvas>
        </div>
        <div className="chart">
          <h2>Weapon Count</h2>
          <canvas id="weaponCountChart"></canvas>
        </div>
        <div className="chart">
          <h2>Most Common Crime Types</h2>
          <canvas id="mostCommonCrimeTypesChart"></canvas>
        </div>
      </div>
    </div>
  );
};

export default CustomReport;
