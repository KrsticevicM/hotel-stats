document.addEventListener("DOMContentLoaded", function () {
    const mealsCtx = document.getElementById("mealsChart").getContext("2d");

    // Mock data for Most Popular Meals
    const mealsData = [
        { meal: "Breakfast", count: 500 },
        { meal: "Half-board", count: 300 },
        { meal: "Full-board", count: 200 },
    ];

    // Extract labels and values
    const labels = mealsData.map(data => data.meal);
    const values = mealsData.map(data => data.count);

    // Render Pie Chart
    new Chart(mealsCtx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: false,
            plugins: {
                legend: { position: "right" }
            }
        }
    });
});


// Reservations by month
document.addEventListener("DOMContentLoaded", function () {
    const reservationsCtx = document.getElementById("reservationsChart").getContext("2d");
    const averageStayCtx = document.getElementById("averageStayChart").getContext("2d");

    let reservationsChart, averageStayChart;

    // Fetch reservations data for a specific year
    function fetchReservations(year) {
        fetch(`/api/reservations/?year=${year}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("API not available, using mock data...");
                }
                return response.json();
            })
            .then(data => updateReservationsChart(data))
            .catch(error => {
                console.warn(error.message);
                useMockReservationsData(year);
            });
    }

    // Fetch average stay data for a specific year
    function fetchAverageStay(year) {
        fetch(`/api/average-stay/?year=${year}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("API not available, using mock data...");
                }
                return response.json();
            })
            .then(data => updateAverageStayChart(data))
            .catch(error => {
                console.warn(error.message);
                useMockAverageStayData(year);
            });
    }

    // Update the Reservations chart
    function updateReservationsChart(data) {
        const labels = data.map(entry => entry.month);
        const counts = data.map(entry => entry.count);

        if (reservationsChart) {
            reservationsChart.data.labels = labels;
            reservationsChart.data.datasets[0].data = counts;
            reservationsChart.update();
        } else {
            reservationsChart = new Chart(reservationsCtx, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Reservations per Month",
                        data: counts,
                        backgroundColor: "rgba(54, 162, 235, 0.6)",
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: { y: { beginAtZero: true } }
                }
            });
        }
    }

    // Update the Average Stay chart
    function updateAverageStayChart(data) {
        const labels = data.map(entry => entry.month);
        const stays = data.map(entry => entry.avgStay);

        if (averageStayChart) {
            averageStayChart.data.labels = labels;
            averageStayChart.data.datasets[0].data = stays;
            averageStayChart.update();
        } else {
            averageStayChart = new Chart(averageStayCtx, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Average Stay per Night",
                        data: stays,
                        backgroundColor: "rgba(75, 192, 192, 0.6)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: { y: { beginAtZero: true } }
                }
            });
        }
    }

    // Use mock data for Reservations chart (when the API fails)
    function useMockReservationsData(year) {
        const mockData = {
            "2023": [
                { month: "January", count: 120 },
                { month: "February", count: 95 },
                { month: "March", count: 110 },
                { month: "April", count: 130 },
                { month: "May", count: 150 },
                { month: "June", count: 170 }
            ],
            "2024": [
                { month: "January", count: 100 },
                { month: "February", count: 85 },
                { month: "March", count: 90 },
                { month: "April", count: 140 },
                { month: "May", count: 160 },
                { month: "June", count: 180 }
            ]
        };

        const data = mockData[year] || mockData["2024"]; // Default to 2024 mock data
        updateReservationsChart(data);
    }

    // Use mock data for Average Stay chart (when the API fails)
    function useMockAverageStayData(year) {
        const mockData = {
            "2023": [
                { month: "January", avgStay: 5 },
                { month: "February", avgStay: 4.5 },
                { month: "March", avgStay: 6 },
                { month: "April", avgStay: 5.2 },
                { month: "May", avgStay: 5.7 },
                { month: "June", avgStay: 6.1 }
            ],
            "2024": [
                { month: "January", avgStay: 7 },
                { month: "February", avgStay: 5.5 },
                { month: "March", avgStay: 6.2 },
                { month: "April", avgStay: 6.1 },
                { month: "May", avgStay: 6.8 },
                { month: "June", avgStay: 7.3 }
            ]
        };

        const data = mockData[year] || mockData["2024"];
        updateAverageStayChart(data);
    }

    // Fetch data for default year (2024)
    fetchReservations("2024");
    fetchAverageStay("2024");

    // Event listener for year filter dropdown (Reservations per Month)
    document.getElementById("yearFilterRes").addEventListener("change", function () {
        const selectedYear = this.value;
        fetchReservations(selectedYear); // Only update reservations chart
    });

    // Event listener for year filter dropdown (Average Stay per Month)
    document.getElementById("yearFilterAvgStay").addEventListener("change", function () {
        const selectedYear = this.value;
        fetchAverageStay(selectedYear); // Only update average stay chart
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Example mock data (replace with data from GraphDB)
    const countriesData = [
        { country: 'Portugal', count: 150 },
        { country: 'United Kingdom', count: 120 },
        { country: 'France', count: 100 },
        { country: 'Spain', count: 80 },
        { country: 'Italy', count: 70 },
        { country: 'Germany', count: 60 },
        { country: 'United States', count: 50 },
        { country: 'Canada', count: 45 },
        { country: 'Australia', count: 40 },
        { country: 'Brazil', count: 35 },
        { country: 'India', count: 30 },
        { country: 'Mexico', count: 25 },
        { country: 'Japan', count: 20 },
        { country: 'China', count: 15 },
        { country: 'Russia', count: 10 },
        { country: 'South Africa', count: 5 },
        { country: 'Argentina', count: 5 },
        { country: 'Colombia', count: 5 },
        { country: 'Nigeria', count: 3 },
        { country: 'Egypt', count: 2 },
    ];

    // Populating "Top Countries"
    const countriesList = document.querySelector('#topCountries ul'); // Correct selector for ul
    console.log(countriesList); // Make sure it's selecting the ul

    countriesData.forEach((data, index) => {
        const li = document.createElement('li');
        li.textContent = `${index + 1}. ${data.country}: ${data.count} Reservations`;
        countriesList.appendChild(li);
    });

    // Setting max-height and enabling scrolling
    var maxHeight = 250;  // Define the max height for the scrollable area
    if (countriesList.scrollHeight > maxHeight) {
        countriesList.style.maxHeight = maxHeight + "px";  // Apply the max height
        countriesList.style.overflowY = "auto";  // Enable vertical scrolling
    }
});
