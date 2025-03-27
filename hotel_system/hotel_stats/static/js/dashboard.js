document.addEventListener("DOMContentLoaded", function() {
    // Example mock data (replace with data from GraphDB)
    const stayData = [
        { month: 'January', nights: 5 },
        { month: 'February', nights: 4 },
        { month: 'March', nights: 6 },
    ];

    const reservationData = [
        { month: 'January', count: 120 },
        { month: 'February', count: 95 },
        { month: 'March', count: 110 },
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

    // Populating "Reservations by Month"
    const reservationsList = document.querySelector('#reservationsByMonth ul');
    reservationData.forEach(data => {
        const li = document.createElement('li');
        li.textContent = `${data.month}: ${data.count} Reservations`;
        reservationsList.appendChild(li);
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
