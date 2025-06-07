async function submitQuery() {
    const text = document.getElementById('queryInput').value;
    const res = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    const data = await res.json();
    document.getElementById('output').textContent = data.fhir_request;
    updateTable(data.patients);
    updateChart(data.patients);
}

document.getElementById('submitBtn').addEventListener('click', submitQuery);

function updateTable(patients) {
    const tbody = document.querySelector('#resultTable tbody');
    tbody.innerHTML = '';
    patients.forEach(p => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${p.name}</td><td>${p.age}</td><td>${p.gender}</td><td>${p.condition}</td>`;
        tbody.appendChild(row);
    });
}

let chart;
function updateChart(patients) {
    const ctx = document.getElementById('chart').getContext('2d');
    const labels = patients.map(p => p.name);
    const ages = patients.map(p => p.age);
    if (chart) {
        chart.destroy();
    }
    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Age',
                data: ages,
                backgroundColor: 'rgba(0,255,0,0.5)'
            }]
        }
    });
}