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

document.addEventListener("DOMContentLoaded", function () {
  fetchHighCancellationRisk();
});

function fetchHighCancellationRisk() {
  fetch('/api/high-risk-bookings/')
    .then(response => response.json())
    .then(data => {
      document.getElementById('high-risk-count').innerHTML = `Number of total reservations: <strong>${data.high_risk_count}</strong>`;
      document.getElementById('high-risk-percentage').innerHTML = `Percentage: <strong>${data.high_risk_percentage}%</strong> of upcoming reservations`;


      const list = document.getElementById('high-risk-list');
      list.innerHTML = ""; // clear existing
      data.high_risk_bookings.forEach(booking => {
        const item = document.createElement('li');
        item.textContent = `${booking.reservation_id} - ${booking.guest_name}`;
        list.appendChild(item);
      });
    })
    .catch(error => {
      console.error('Error fetching high cancellation risk data:', error);
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const countriesList = document.querySelector('#topCountries ul');
    const countrySearchInput = document.querySelector('#countrySearch');

    const countriesData = JSON.parse(document.getElementById("countries-data").textContent);
    
    // Function to populate the country list
    function populateCountries(countries) {
        countriesList.innerHTML = '';  // Clear the list

        countries.forEach((data, index) => {
            const li = document.createElement('li');
            li.title = 'Click to get data about this country'; 
            li.textContent = `${index + 1}. ${data.country}: ${data.count} Reservations`;

            // Add click listener to fetch and display statistics
            li.addEventListener('click', () => {
                console.log(`Clicked on ${data.country}`); 
                fetchCountryStats(data.country);
            });

            countriesList.appendChild(li);
        });

        // Scroll setup
        const maxHeight = 250;
        if (countriesList.scrollHeight > maxHeight) {
            countriesList.style.maxHeight = maxHeight + "px";
            countriesList.style.overflowY = "auto";
        }
    }

    function formatPopulation(pop) {
        if (!pop) return 'N/A';

        // If population is a string, convert to number
        const num = typeof pop === 'string' ? Number(pop.replace(/[^\d]/g, '')) : pop;

        if (isNaN(num)) return pop; // fallback: return original if not a number

        // Format with commas 
        return num.toLocaleString('en-US');
    }
    function truncateText(text, maxLength = 200) {
        if (!text) return 'N/A';
        if (text.length <= maxLength) return text;
        return text.slice(0, maxLength) + '...';
    }

    function fetchCountryStats(countryName) {
    fetch(`/additional/get/?country_name=${encodeURIComponent(countryName)}`)
        .then(response => response.json())
        .then(data => {
            const statsContainer = document.getElementById("countryStats");

            // Keep the existing h3, update or add details below it
            let detailsHtml = `
                <p><strong>Country:</strong> ${countryName}</p>
                <p><strong>Capital:</strong> ${data.Capital || 'N/A'}</p>
                <p><strong>Population:</strong> ${formatPopulation(data.Population)}</p>
                <p><strong>Language:</strong> ${data.Language || 'N/A'}</p>
                <p><strong>Currency:</strong> ${data.Currency || 'N/A'}</p>
                <p><strong>Abstract:</strong> <span id="abstract">${truncateText(data.Abstract)}</span> ${data.Abstract.length > 150 ? '<a href="#" id="readMore">Read more</a>' : ''}</p>
            `;

            // Find the existing <h3> inside the container
            const h3 = statsContainer.querySelector('h3');

            // Replace container's innerHTML but keep h3 at top
            statsContainer.innerHTML = '';
            if (h3) statsContainer.appendChild(h3);
            statsContainer.insertAdjacentHTML('beforeend', detailsHtml);

            const readMoreLink = document.getElementById('readMore');
            if (readMoreLink) {
                readMoreLink.addEventListener('click', function(e) {
                    e.preventDefault();
                    document.getElementById('abstract').textContent = data.Abstract;
                    this.style.display = 'none';
                });
            }
        })
        .catch(error => {
            alert("Failed to fetch country data.");
            console.error(error);
        });
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

document.addEventListener("DOMContentLoaded", function () {
    const familyBookingsCtx = document.getElementById("familyBookingsChart").getContext("2d");
    let familyBookingsChart;

    // Fetch family booking data
    function fetchFamilyBookings(year) {
        fetch(`/api/family-bookings/?year=${year}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("API not available, using mock data...");
                }
                return response.json();
            })
            .then(data => updateFamilyBookingsChart(data))
            .catch(error => {
                console.warn(error.message);
                // You can add mock data fallback here
            });
    }

    // Update the Family Bookings chart
    function updateFamilyBookingsChart(data) {
        const labels = data.map(entry => entry.month);
        const counts = data.map(entry => entry.count);

        if (familyBookingsChart) {
            familyBookingsChart.data.labels = labels;
            familyBookingsChart.data.datasets[0].data = counts;
            familyBookingsChart.update();
        } else {
            familyBookingsChart = new Chart(familyBookingsCtx, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Family Bookings",
                        data: counts,
                        backgroundColor: "rgba(255, 99, 132, 0.6)",
                        borderColor: "rgba(255, 99, 132, 1)",
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

    // Initial fetch for the default year
    fetchFamilyBookings(selectedYear);

    // Event listener for year filter dropdown (Family Bookings)
    document.getElementById("yearFilterFamily").addEventListener("change", function () {
        const selectedYear = this.value;
        fetchFamilyBookings(selectedYear);
    });
});

document.addEventListener("DOMContentLoaded", function () {
  fetchHighCancellationRisk();
  fetchLoyalGuests();
});

function fetchLoyalGuests() {
  fetch('/api/loyal-guests-this-month/')
    .then(response => response.json())
    .then(data => {
      document.getElementById('loyal-guest-count').innerHTML = `Number of loyal guests: <strong>${data.loyal_guest_count}</strong>`;
      document.getElementById('loyal-guest-percent').innerHTML = `Repeat guests: <strong>${data.repeat_percentage}%</strong> | New guests: <strong>${data.new_percentage}%</strong>`;

      const list = document.getElementById('loyal-guest-list');
      list.innerHTML = ""; // clear existing
      data.loyal_guests.forEach(guest => {
        const item = document.createElement('li');
        item.textContent = `${guest.reservation_id} - ${guest.guest_name}`;
        list.appendChild(item);
      });
    })
    .catch(error => {
      console.error('Error fetching loyal guests data:', error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const vipYearSelect = document.getElementById("vipYearSelect");
  const vipStatsSummary = document.getElementById("vipStatsSummary"); // optional, create this div in HTML if you want summary text
  const ctx = document.getElementById("vipRevenueChart").getContext("2d");

  let vipData = null;
  let vipChart = null;

  // Fetch mock data from backend
  fetch('api/vip-bookings/')  // Adjust URL to your Django endpoint
    .then((res) => res.json())
    .then((data) => {
      vipData = data;
      populateYearSelect(data.years);
      updateVipCard("all"); // Default to all years
    })
    .catch((err) => console.error("Failed to fetch VIP data:", err));

  function populateYearSelect(years) {
    // Add 'All Years' option first
    const allOption = document.createElement("option");
    allOption.value = "all";
    allOption.textContent = "All Years";
    vipYearSelect.appendChild(allOption);

    years.forEach((year) => {
      const option = document.createElement("option");
      option.value = year;
      option.textContent = year;
      vipYearSelect.appendChild(option);
    });

    vipYearSelect.value = "all";
    vipYearSelect.addEventListener("change", () => {
      updateVipCard(vipYearSelect.value);
    });
  }

  function updateVipCard(year) {
    if (!vipData) return;

    const bookings = vipData.top_revenue_bookings[year] || [];
    if (bookings.length === 0) {
      if (vipStatsSummary) vipStatsSummary.textContent = "No bookings for selected year.";
      if (vipChart) vipChart.destroy();
      return;
    }

    // Sort bookings by total_revenue descending
    bookings.sort((a, b) => b.total_revenue - a.total_revenue);

    // Update summary stats (optional)
    if (vipStatsSummary) {
      const totalBookings = bookings.length;
      const avgAdr = (bookings.reduce((sum, b) => sum + b.adr, 0) / totalBookings).toFixed(2);
      vipStatsSummary.textContent = `Total VIP Bookings: ${totalBookings} | Average ADR: $${avgAdr}`;
    }

    // Prepare data for Chart.js horizontal bar
    const labels = bookings.map((b) => `${b.guest_name} (${b.reservation_id})`);
    const revenues = bookings.map((b) => b.total_revenue);

    // Create or update chart
    if (vipChart) {
      vipChart.data.labels = labels;
      vipChart.data.datasets[0].data = revenues;
      vipChart.update();
    } else {
      vipChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Total Revenue ($)",
              data: revenues,
              backgroundColor: "rgba(44, 62, 80, 0.7)",
            },
          ],
        },
        options: {
          indexAxis: "y",
          responsive: true,
          scales: {
            x: { beginAtZero: true },
          },
          plugins: {
            legend: { display: false },
            tooltip: { enabled: true },
          },
        },
      });
    }
  }
});





