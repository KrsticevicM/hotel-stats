document.addEventListener("DOMContentLoaded", function() {
    // Example mock data (replace with data from GraphDB)
    const stayData = [
        { month: 'January', nights: 5 },
        { month: 'February', nights: 4 },
        { month: 'March', nights: 6 },
    ];

    const cancellationData = [
        { month: 'January', count: 30 },
        { month: 'February', count: 20 },
        { month: 'March', count: 25 },
    ];

    const countriesData = [
        { country: 'Portugal', count: 150 },
        { country: 'United Kingdom', count: 120 },
        { country: 'France', count: 100 },
    ];

    // Populating "Average Stay per Month"
    const averageStayList = document.querySelector('#averageStay ul');
    stayData.forEach(data => {
        const li = document.createElement('li');
        li.textContent = `${data.month}: ${data.nights} nights`;
        averageStayList.appendChild(li);
    });

    // Populating "Cancellations per Month"
    const cancellationsList = document.querySelector('#cancellationsByMonth ul');
    cancellationData.forEach(data => {
        const li = document.createElement('li');
        li.textContent = `${data.month}: ${data.count} Cancellations`;
        cancellationsList.appendChild(li);
    });

    // Populating "Top Countries"
    const countriesList = document.querySelector('#topCountries ul');
    countriesData.forEach(data => {
        const li = document.createElement('li');
        li.textContent = `${data.country}: ${data.count} Reservations`;
        countriesList.appendChild(li);
    });
});

// Reservations by month
document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("reservationsChart").getContext("2d");
    let reservationsChart;

    function fetchReservations(year) {
        fetch(`/api/reservations/?year=${year}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("API not available, using mock data...");
                }
                return response.json();
            })
            .then(data => updateChart(data))
            .catch(error => {
                console.warn(error.message);
                useMockData(year);
            });
    }

    function updateChart(data) {
        const labels = data.map(entry => entry.month);
        const counts = data.map(entry => entry.count);

        if (reservationsChart) {
            reservationsChart.data.labels = labels;
            reservationsChart.data.datasets[0].data = counts;
            reservationsChart.update();
        } else {
            reservationsChart = new Chart(ctx, {
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
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }
    }

    function useMockData(year) {
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
        updateChart(data);
    }

    // Fetch data for the default year (2024)
    fetchReservations("2024");

    // Event listener for year filter dropdown
    document.getElementById("yearFilter").addEventListener("change", function () {
        fetchReservations(this.value);
    });
});
