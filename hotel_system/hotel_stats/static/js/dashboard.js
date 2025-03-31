document.addEventListener("DOMContentLoaded", function () {
    //console.log(document.getElementById("meals-data").textContent);
    const mealsData = JSON.parse(document.getElementById("meals-data").textContent);
    //console.log(mealsData);

    const labels = mealsData.map(data => data.meal);
    const values = mealsData.map(data => data.count);

    const mealsCtx = document.getElementById("mealsChart").getContext("2d");

    new Chart(mealsCtx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ["#FF6B6B", "#4D96FF",  "#FFD93D", "#6BCB77", "#FF9F45"],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            aspectRatio: 2,
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

    console.log("Selected Year:", selectedYear);

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
               //useMockReservationsData(year);
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
                //useMockAverageStayData(year);
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
        //console.log(data)

        const labels = data.map(entry => entry.month);
        const stays = data.map(entry => entry.avgStay);

        //console.log(labels)
        //console.log(stays)

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

    // Fetch data for default year (last one - default)
    fetchReservations(selectedYear);
    fetchAverageStay(selectedYear);

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
    const countriesList = document.querySelector('#topCountries ul');
    const countrySearchInput = document.querySelector('#countrySearch');

    const countriesData = JSON.parse(document.getElementById("countries-data").textContent);

    // Function to populate the country list
    function populateCountries(countries) {
        countriesList.innerHTML = '';  // Clear the list before populating

        countries.forEach((data, index) => {
            const li = document.createElement('li');
            li.textContent = `${index + 1}. ${data.country}: ${data.count} Reservations`;
            countriesList.appendChild(li);
        });

        // Setting max-height and enabling scrolling
        const maxHeight = 250;
        if (countriesList.scrollHeight > maxHeight) {
            countriesList.style.maxHeight = maxHeight + "px";
            countriesList.style.overflowY = "auto";
        }
    }

    // Search functionality
    countrySearchInput.addEventListener('input', function() {
        const searchTerm = countrySearchInput.value.toLowerCase();

        // Filter countries based on the search term (case-insensitive)
        const filteredCountries = countriesData.filter(data => 
            data.country.toLowerCase().includes(searchTerm)
        );

        // Populate the countries list with filtered data
        populateCountries(filteredCountries);
    });

    // Initially populate the list with all countries
    populateCountries(countriesData);
});
