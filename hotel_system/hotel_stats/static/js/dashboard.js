// Reservations per Month Histogram
var ctx = document.getElementById('reservationsChart').getContext('2d');
var reservationsChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['January', 'February', 'March'],  // Replace with dynamic data
        datasets: [{
            label: 'Reservations per Month',
            data: [120, 130, 110],  // Replace with dynamic data
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


var map = L.map('worldMap').setView([20, 0], 2);  // Default view (latitude, longitude, zoom level)

// Add Mapbox tile layer (you can use your own tile service)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Example: Adding markers for top countries (Replace with dynamic data)
var countries = [
    { country: 'USA', lat: 37.0902, lon: -95.7129, reservations: 500 },
    { country: 'UK', lat: 51.5074, lon: -0.1278, reservations: 300 },
    { country: 'Germany', lat: 51.1657, lon: 10.4515, reservations: 250 }
];

countries.forEach(function(country) {
    L.marker([country.lat, country.lon])
        .addTo(map)
        .bindPopup("<b>" + country.country + "</b><br>Reservations: " + country.reservations);
});

