def get_template() -> str:
    HTML_TEMPLATE = """<!DOCTYPE html>
  <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Test Report</title>
      <style>
        /* Add your styles here */
        body {{
          margin: 0;
          font-family: Arial, sans-serif;
          display: flex;
          flex-direction: column;
          height: 100vh;
        }}
        .menu-bar {{
          background: #333;
          color: white;
          padding: 10px;
          display: flex;
          justify-content: space-between;
        }}
        .menu-bar .menu {{
          display: flex;
          gap: 20px;
        }}
        .menu-bar .menu a {{
          color: white;
          text-decoration: none;
          cursor: pointer;
        }}
        .container {{
          display: flex;
          flex-grow: 1;
          overflow: hidden;
        }}
        .test-cases {{
          flex: 1;
          background: #f4f4f4;
          padding: 10px;
          overflow-y: auto;
          border-right: 1px solid #ddd;
        }}
        .test-case {{
          padding: 10px;
          margin-bottom: 5px;
          border: 1px solid #ccc;
          border-radius: 5px;
          cursor: pointer;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }}
        .test-case.pass {{
          background-color: #d4edda;
        }}
        .test-case.fail {{
          background-color: #f8d7da;
        }}
        .test-case.skip {{
          background-color: #ffeeba;
        }}
        .test-case.active {{
          border: 2px solid #333;
        }}
        .test-steps {{
          flex: 2;
          padding: 10px;
          overflow-y: auto;
        }}
        .popup-overlay {{
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(0, 0, 0, 0.5);
          display: none;
          z-index: 1000;
        }}
        .popup {{
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background: white;
          padding: 20px;
          border-radius: 5px;
          max-width: 80%;
          max-height: 80%;
          overflow: auto;
          z-index: 1001;
        }}
        .close-popup {{
          float: right;
          background: red;
          color: white;
          border: none;
          padding: 5px 10px;
          cursor: pointer;
        }}
        .close-popup.hidden {{
          display: none;
        }}
        .summary {{
          display: none;
          flex-direction: column;
          padding: 10px;
        }}
      </style>
    </head>
    <body>
      <div class="menu-bar">
        <div class="menu">
          <a href="#" id="testcases-link" onclick="showTestCases()">Test Cases</a>
          <a href="#" id="summary-link" onclick="showSummary()">Summary</a>
        </div>
      </div>

      <div class="container" id="testcases-container">
        <!-- Left Side Test Cases -->
        <div class="test-cases" id="test-cases">
          {test_cases}
        </div>

        <!-- Right Side Test Steps -->
        <div class="test-steps" id="test-steps"></div>
      </div>

      <!-- Summary Section -->
      <div class="summary" id="summary-container">
        <h2>Summary</h2>
        <canvas id="summary-chart" style="width: 200px; height: 200px"></canvas>
      </div>

      <!-- Popup -->
      <div class="popup-overlay" id="popup-overlay" onclick="closePopup()"></div>
      <div class="popup" id="popup">
        <button
          class="close-popup hidden"
          id="close-popup"
          onclick="closePopup()"
        >
          X
        </button>
        <div id="popup-content"></div>
      </div>

      <script>
        const testStepsData = {test_steps_data};
        const testStatusCount = {test_status_count};

        window.onload = () => {{
          const firstTestCase = document.querySelector(".test-case");
          showTestSteps("Test Case 1", firstTestCase);
        }};

        function showTestSteps(testCaseName, element) {{
          document.querySelectorAll(".test-case").forEach((testCase) => {{
            testCase.classList.remove("active");
          }});
          element.classList.add("active");

          const steps = testStepsData[testCaseName] || ["No steps available."];
          const stepDiv = document.getElementById("test-steps");
          stepDiv.innerHTML =
            `<h2>${{testCaseName}}</h2>` +
            steps.map((step) => `<div class="test-step">${{step}}</div>`).join("");
        }}

        function openPopup(fileName) {{
          const popupContent = document.getElementById("popup-content");
          popupContent.innerHTML = `<h3>Table: ${{fileName}}</h3><p>Dummy content for ${{fileName}}</p>`;
          document.getElementById("popup-overlay").style.display = "block";
          document.getElementById("popup").style.display = "block";
          document.getElementById("close-popup").classList.remove("hidden");
        }}

        function closePopup() {{
          document.getElementById("popup-overlay").style.display = "none";
          document.getElementById("popup").style.display = "none";
          document.getElementById("close-popup").classList.add("hidden");
        }}

        function showTestCases() {{
          document.getElementById("testcases-container").style.display = "flex";
          document.getElementById("summary-container").style.display = "none";
        }}

        function showSummary() {{
          document.getElementById("testcases-container").style.display = "none";
          document.getElementById("summary-container").style.display = "flex";
          renderChart();
        }}

        function renderChart() {{
          const ctx = document.getElementById("summary-chart").getContext("2d");
          new Chart(ctx, {{
            type: "pie",
            data: {{
              labels: ["Pass", "Fail", "Skip"],
              datasets: [
                {{
                  data: [
                    testStatusCount.pass,
                    testStatusCount.fail,
                    testStatusCount.skip,
                  ],
                  backgroundColor: ["#28a745", "#dc3545", "#ffc107"],
                }},
              ],
            }},
            options: {{
              responsive: false,
              maintainAspectRatio: false,
            }},
          }});
        }}
      </script>

      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </body>
  </html>
  """
    return HTML_TEMPLATE
