const ctx = document.getElementById('myChart').getContext('2d');

const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Half Pints Available',
            data: [],
            backgroundColor: 'hsl(45, 100%, 80%)', // Use a single color for all bars
            borderWidth: 4,
            borderColor: 'black' // Border for visibility
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            beforeDraw: (chart) => {
                const ctx = chart.ctx;
                const meta = chart.getDatasetMeta(0);
                
                // Clear the canvas before redrawing
                ctx.clearRect(0, 0, chart.width, chart.height);
                
                // Draw each bar as a pint glass
                meta.data.forEach((bar, index) => {
                    const { x, y } = bar.getProps(['x', 'y'], true);
                    const width = bar.width - 1; // Adjust the width for rounding
                    const height = bar.getProps('height', true);
                    
                    ctx.fillStyle = 'hsl(220, 40%, 100%)'; // Pint glass color

                    // Draw the pint glass
                    ctx.beginPath();
                    // Round the top
                    ctx.moveTo(x - width / 2, y - height);
                    ctx.lineTo(x + width / 2, y - height);
                    ctx.quadraticCurveTo(x + width / 2, y - height + 10, x + width / 4, y - height + 10); // Round right top
                    ctx.lineTo(x - width / 4, y - height + 10); // Create the right edge of the rounded top
                    ctx.quadraticCurveTo(x - width / 2, y - height + 10, x - width / 2, y - height); // Round left top
                    ctx.closePath(); // Close the top shape
                    ctx.fill(); // Fill the top

                    // Draw the body of the pint glass
                    ctx.fillRect(x - width / 2, y - height, width, height);
                });
            },
        },
    }
});

// CONFIGS
Chart.defaults.font.size = 16;
Chart.defaults.font.weight = 'bolder';
Chart.defaults.color = '#000';

// Function to fetch CSV data and update the chart
async function fetchData() {
    const timestamp = new Date().getTime(); // Unique timestamp for cache busting
    const response = await fetch(`data.csv?t=${timestamp}`); 
    const data = await response.text();

    const rows = data.split('\n').slice(1).filter(row => row.trim() !== ''); // Remove empty rows
    const labels = [];
    const values = [];

    rows.forEach(row => {
        const cols = row.split(',');
        if (cols.length < 2) return;
        labels.push(cols[0]);
        values.push(parseInt(cols[1]));
    });

    // Update chart data
    myChart.data.labels = labels;
    myChart.data.datasets[0].data = values;
    myChart.update();
}

// Fetch data every 500 ms
setInterval(fetchData, 500);
