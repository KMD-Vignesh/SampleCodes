
window.onload = () => {
  const firstTestCase = document.querySelector(".test-case");
};

function showTestSteps(testCaseName, element) {
  document.querySelectorAll(".test-case").forEach((testCase) => {
    testCase.classList.remove("active");
  });
  element.classList.add("active");

  const steps = testStepsData[testCaseName] || ["No steps available."];
  const stepDiv = document.getElementById("test-steps");
  stepDiv.innerHTML =
    `<h2 class="case-head">${testCaseName}</h2>` +
    steps.map((step) => `<div class="test-step">${step}</div>`).join("");
}

function openPopup(fileName) {
  const popupContent = document.getElementById("popup-content");
  popupContent.innerHTML = `${fileName}`;
  document.getElementById("popup-overlay").style.display = "block";
  document.getElementById("popup").style.display = "block";
  document.getElementById("close-popup").classList.remove("hidden");
}

function openPopup2(testCaseId, fileName) {
  const popupContent = document.getElementById("popup-content");
  if (testStepsData[testCaseId] && testStepsData[testCaseId][fileName]) {
    const tableHTML = testStepsData[testCaseId][fileName];
    popupContent.innerHTML = tableHTML;
    document.getElementById("popup-overlay").style.display = "block";
    document.getElementById("popup").style.display = "block";
    document.getElementById("close-popup").classList.remove("hidden");
  } else {
    popupContent.innerHTML = `<p>Error: No data found for Test Case "${testCaseId}" and File "${fileName}".</p>`;
    document.getElementById("popup-overlay").style.display = "block";
    document.getElementById("popup").style.display = "block";
  }
}

function closePopup() {
  document.getElementById("popup-overlay").style.display = "none";
  document.getElementById("popup").style.display = "none";
  document.getElementById("close-popup").classList.add("hidden");
}

function showTestCases() {
  document.getElementById("testcases-container").style.display = "flex";
  document.getElementById("summary-container").style.display = "none";
  document.getElementById('status-filter').disabled = false;
  document.getElementById('search-box').disabled = false;
}

function showSummary() {
  document.getElementById("testcases-container").style.display = "none";
  document.getElementById("summary-container").style.display = "flex";
  document.getElementById('status-filter').disabled = true;
  document.getElementById('search-box').disabled = true;
  renderChart();
}

function renderChart() {
  const ctx = document.getElementById("summary-chart").getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Pass", "Fail", "Skip"],
      datasets: [
        {
          data: [
            testStatusCount.pass,
            testStatusCount.fail,
            testStatusCount.skip,
          ],
          backgroundColor: ["#28a745", "#dc3545", "#ffc107"],
        },
      ],
    },
    options: {
      responsive: false,
      maintainAspectRatio: false,
    },
  });
}

function filterTestCases() {
  const statusFilter = document.getElementById("status-filter").value;
  const searchBox = document.getElementById("search-box").value.toLowerCase();
  const testCases = document.querySelectorAll(".test-case");

  testCases.forEach(testCase => {
    const status = testCase.classList.contains("pass") ? "pass" :
                   testCase.classList.contains("fail") ? "fail" :
                   testCase.classList.contains("skip") ? "skip" : "";

    const name = testCase.textContent.toLowerCase();

    const matchesStatus = (statusFilter === "all" || status === statusFilter);
    const matchesName = name.includes(searchBox);

    if (matchesStatus && matchesName) {
      testCase.style.display = "";
    } else {
      testCase.style.display = "none";
    }
  });
}
