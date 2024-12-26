def get_template() -> str:
    template_content = (
        """<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <title>Test Report</title>
        """
        + get_styles()
        + """
      </head>
      <body>"""
        + get_menu_bar()
        + get_test_case_section()
        + get_summary_section()
        + get_popup_section()
        + get_script_content()
        + """</body>
    </html>
    """
    )
    return template_content


def get_test_case_section() -> str:
    testcas_section_content = """
      <div class="container" id="testcases-container">
        <!-- Left Side Test Cases -->
        <div class="test-cases" id="test-cases">
        {test_cases}
        </div>
        <!-- Right Side Test Steps -->
        <div class="test-steps" id="test-steps"></div>
      </div>
    """
    return testcas_section_content


def get_summary_section() -> str:
    summary_section_content = """
        <!-- Summary Section -->
        <div class="summary" id="summary-container">
          <h2>Summary</h2>
          <canvas id="summary-chart" style="width: 200px; height: 200px"></canvas>
        </div>
    """
    return summary_section_content


def get_popup_section() -> str:
    popup_section_content = """
      <!-- Popup -->
      <div class="popup-overlay" id="popup-overlay" onclick="closePopup()"></div>
      <div class="popup hidden" id="popup">
      <button
      class="close-popup hidden"
      id="close-popup"
      onclick="closePopup()"
      >
      X
      </button>
      <div id="popup-content"></div>
      </div>
    """
    return popup_section_content


def get_menu_bar() -> str:
    menu_bar_content = """
      <div class="menu-bar">
      <div class="menu">
      <a href="#" id="testcases-link" onclick="showTestCases()">Test Cases</a>
      <a href="#" id="summary-link" onclick="showSummary()">Summary</a>
      </div>
      </div>
    """
    return menu_bar_content


def get_script_content() -> str:
    script_content = """
        <script>
          const testStepsData = {test_steps_data};
          const testStatusCount = {test_status_count};

          window.onload = () => {{
            const firstTestCase = document.querySelector(".test-case");
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
            popupContent.innerHTML = `${{fileName}}`;
            document.getElementById("popup-overlay").style.display = "block";
            document.getElementById("popup").style.display = "block";
            document.getElementById("close-popup").classList.remove("hidden");
          }}

          function openPopup2(testCaseId, fileName) {{
            const popupContent = document.getElementById("popup-content");
            if (testStepsData[testCaseId] && testStepsData[testCaseId][fileName]) {{
              const tableHTML = testStepsData[testCaseId][fileName];
              popupContent.innerHTML = tableHTML;
              document.getElementById("popup-overlay").style.display = "block";
              document.getElementById("popup").style.display = "block";
              document.getElementById("close-popup").classList.remove("hidden");
            }} else {{
              popupContent.innerHTML = `<p>Error: No data found for Test Case "${{testCaseId}}" and File "${{fileName}}".</p>`;
              document.getElementById("popup-overlay").style.display = "block";
              document.getElementById("popup").style.display = "block";
            }}
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
    """
    return script_content


def get_styles() -> str:
    style_content = """<style>
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
      .popup.hidden {{
        display: none;
      }}
      .close-popup {{
        display: flex;
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
    """
    return style_content
