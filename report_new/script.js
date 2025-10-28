function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.getElementById(tabName).classList.remove('hidden');
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
}

function drawPieChart(passed, failed) {
    const canvas = document.getElementById('pieChart');
    const ctx = canvas.getContext('2d');
    const total = passed + failed;
    
    if (total === 0) return;
    
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;
    
    const passAngle = (passed / total) * 2 * Math.PI;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw pass slice
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, 0, passAngle);
    ctx.closePath();
    ctx.fillStyle = '#2e7d32';
    ctx.fill();
    
    // Draw fail slice
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, passAngle, 2 * Math.PI);
    ctx.closePath();
    ctx.fillStyle = '#d32f2f';
    ctx.fill();
}

document.addEventListener('DOMContentLoaded', function() {
    showTab('summary');
});
