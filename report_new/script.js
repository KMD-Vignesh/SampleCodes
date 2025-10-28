function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabName).classList.remove('hidden');
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
}

function selectTestcase(testId, testName, author, description, status, validation) {
    document.querySelectorAll('.testcase-item').forEach(item => item.classList.remove('active'));
    document.getElementById('item-' + testId).classList.add('active');
    
    const statusClass = status.toLowerCase() === 'pass' ? 'pass' : 'fail';
    document.getElementById('testcase-details').innerHTML = `
        <div class="detail-row">
            <div class="detail-label">Test Case ID</div>
            <div class="detail-value">${testId}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Test Case Name</div>
            <div class="detail-value">${testName}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Author</div>
            <div class="detail-value">${author}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Description</div>
            <div class="detail-value">${description}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Status</div>
            <div class="detail-value"><span class="status-badge ${statusClass}">${status.toUpperCase()}</span></div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Validation Parameter</div>
            <div class="detail-value">${validation}</div>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', function() {
    showTab('summary');
});
