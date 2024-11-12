<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pint Glass Visualization with D3.js</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <svg width="600" height="400"></svg>
    <script>
        const svg = d3.select("svg");
        const pintWidth = 40; // Width of the pint glass
        const gap = 50; // Gap between glasses
        
        // Create X scale
        const xScale = d3.scaleBand()
            .range([0, (pintWidth + gap) * 5]) // Adjust based on number of data entries
            .padding(0.1);

        // Create Y scale
        const yScale = d3.scaleLinear()
            .range([300, 0]); // Always set the range at the start

        // Load CSV data
        d3.csv("data.csv").then(data => {
            // Convert volume strings into numbers
            data.forEach(d => {
                d.volume = +d.volume; // Convert to number
            });

            // Setup the xScale domain based on labels
            xScale.domain(data.map(d => d.label));
            yScale.domain([0, d3.max(data, d => d.volume)]); // Initial Y scale domain
            
            // Create Y-axis
            const yAxis = d3.axisLeft(yScale);
            svg.append("g")
                .attr("class", "y-axis")
                .attr("transform", "translate(100, 50)")
                .call(yAxis);

            // Function to update the visualization
            function update() {
                // Update the Y scale domain based on current data
                yScale.domain([0, d3.max(data, d => d.volume)]); // Using max volume from CSV

                // Clear previous pint glasses
                svg.selectAll("path").remove();
                svg.selectAll("text.label").remove();

                // Draw each pint glass
                svg.selectAll("path")
                    .data(data)
                    .enter()
                    .append("path")
                    .attr("transform", (d, i) => `translate(${xScale(d.label) + 100}, 350)`)
                    .attr("d", (d) => {
                        const height = 350 - yScale(d.volume); // Calculate height based on scale
                        // Improving pint glass shape
                        return `
                            M -10, 0 
                            L -10, -${height} 
                            Q 0, -${height - 10} 10, -${height}
                            L 10, 0 
                            Q 10, 10 0, 0 
                            L -10, 0 
                            Z
                        `;
                    })
                    .attr("fill", "tan")
                    .attr("stroke", "black");

                // Add labels below each glass
                svg.selectAll("text.label")
                    .data(data)
                    .enter()
                    .append("text")
                    .attr("class", "label")
                    .attr("x", (d) => xScale(d.label) + 100 + pintWidth / 2)
                    .attr("y", 20) // Adjust text position
                    .attr("text-anchor", "middle")
                    .text(d => d.label);
                
                // Remove and update the Y-axis
                svg.select(".y-axis")
                    .call(yAxis); // Update Y-axis
            }

            // Initial rendering
            update();

            // Set interval to update every 500ms
            setInterval(() => {
                // Simulate data update (optional)
                data.forEach(d => {
                    d.volume = Math.floor(Math.random() * 6); // Simulating new volume each time
                });
                update();
            }, 500);
        });
    </script>
</body>
</html>
