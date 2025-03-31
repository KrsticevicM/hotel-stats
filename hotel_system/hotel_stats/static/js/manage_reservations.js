document.addEventListener("DOMContentLoaded", function () {
    // Parse the JSON data passed from the Django view
    const countriesData = JSON.parse(document.getElementById('countries-codes').textContent);
    //console.log(countriesData)
    
    // Get the select element for country
    const countrySelect = document.getElementById("country");

    // Check if countriesData is available and contains 'codes'
    if (countriesData && countriesData.codes) {
        // Loop through the countries and populate the dropdown
        countriesData.codes.forEach(country => {
            const option = document.createElement('option');
            option.value = country;  
            option.textContent = country;  
            countrySelect.appendChild(option);
        });
    } else {
        console.error("Countries data is missing or doesn't have 'codes' property.");
    }
});


// add reservation form
document.getElementById("addReservationForm").addEventListener("submit", function(event) {
    event.preventDefault();
 
    // Capture form values
    const country = document.getElementById("country").value;
    const staysInWeekNights = document.getElementById("stays_in_week_nights").value;
    const staysInWeekendNights = document.getElementById("stays_in_weekend_nights").value;
    const arrivalDate = document.getElementById("arrivalDate").value;
    const hotelType = document.querySelector('input[name="hotelType"]:checked')?.value;
    const mealType = document.querySelector('input[name="meal"]:checked')?.value;
 
    // Validation check
    if (!country || !arrivalDate || !hotelType || !mealType || !staysInWeekNights || !staysInWeekendNights) {
        alert("Please fill in all fields before submitting!");
        return;
    }

    const weekNights = parseInt(staysInWeekNights);
    const weekendNights = parseInt(staysInWeekendNights);

    if (weekNights < 0 || weekendNights < 0) {
        alert("The number of nights cannot be negative.");
        return;
    }

    const dateObj = new Date(arrivalDate);

    const day = dateObj.getDate();
    const monthIndex = dateObj.getMonth();
    const year = dateObj.getFullYear();

    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const monthName = monthNames[monthIndex];

    const formData = {
        country: country,
        day: day,
        month: monthName,
        year: year,
        hotelType: hotelType,
        mealType: mealType,
        weekNights: weekNights,
        weekendNights: weekendNights
    };

    fetch("/manage/add/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())  // Expecting a JSON response from backend
    .then(data => {
        //console.log("Backend Response:", data);
        if (data.success) {
            alert(`Reservation added successfully! Reservation ID: ${data.id}`);
            //console.log(data.id)
            document.getElementById("addReservationForm").reset();
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while submitting the reservation.");
    });
 
});

// Get Reservation
document.getElementById("getReservationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const reservationID = document.getElementById("getReservationID").value.trim();

    if (!reservationID) {
        alert("Please enter a Reservation ID.");
        return;
    }

    const requestData = { reservationID: reservationID };

    fetch("/manage/get/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        //console.log(response)
        return response.json()
    })
    .then(data => {
        console.log(data)
        if (data.success) {
            const reservation = data.data;
            const reservationDetailsDiv = document.getElementById("reservationDetails");

            reservationDetailsDiv.innerHTML = `
                <h4>Reservation Details</h4>
                <p><strong>Reservation ID:</strong> ${reservation.id}</p>
                <p><strong>Hotel Type:</strong> ${reservation.hotelType}</p>
                <p><strong>Country:</strong> ${reservation.country}</p>
                <p><strong>Arrival Date:</strong> ${reservation.arrivalDate}</p>
                <p><strong>Stays in Week Nights:</strong> ${reservation.staysInWeekNights}</p>
                <p><strong>Stays in Weekend Nights:</strong> ${reservation.staysInWeekendNights}</p>
                <p><strong>Meal Type:</strong> ${reservation.mealType}</p>
                <p><strong>Cancelation status:</strong> ${reservation.isCanceled}</p>
            `;
        } else {
            alert("No reservation found with the provided ID.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while fetching the reservation.");
    });
});




// Modify Reservation
document.getElementById("modifyReservationForm").addEventListener("submit", function(event) {
    event.preventDefault();
 
    const reservationID = document.getElementById("modifyReservationID").value.trim();
    const isCanceled = document.querySelector('input[name="isCanceled"]:checked')?.value;
    const arrivalDate = document.getElementById("modifyArrivalDate").value;
    const mealType = document.querySelector('input[name="meal"]:checked')?.value;
    const staysInWeekNights = document.getElementById("modifyStaysInWeek").value;
    const staysInWeekendNights = document.getElementById("modifyStaysInWeekend").value;
    
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    const formData = {
        id: reservationID, // Assuming reservationID is already set
        day: "",
        month: "", 
        year: "",
        mealType: "",
        is_canceled: "",
        weekNights: "",
        weekendNights: ""
    };

    // Check if arrivalDate is provided
    if (arrivalDate) {
        const dateObj = new Date(arrivalDate); // Parse the arrivalDate

        const day = dateObj.getDate(); // Get the day of the month
        const monthIndex = dateObj.getMonth(); // Get the month (0-based index)
        const year = dateObj.getFullYear(); // Get the full year

        const monthName = monthNames[monthIndex]; // Convert the month index to the full month name

        // Update formData with the parsed date information
        formData.day = day;
        formData.month = monthName;
        formData.year = year;
    }

    if (mealType !== undefined) {
        formData.mealType = mealType;
    }
    if (isCanceled !== undefined) {
        formData.is_canceled = isCanceled;
    }

    if (stays_in_week_nights !== undefined){
        formData.weekNights = staysInWeekNights;
    }

    if (stays_in_weekend_nights !== undefined){
        formData.weekendNights = staysInWeekendNights;
    }
 
    fetch("/manage/update/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())  // Expecting a JSON response from backend
    .then(data => {
        if (data.success) {
            alert(`Reservation updated successfully!`);
            document.getElementById("modifyReservationForm").reset();
        } else {
            alert(`Error: ${data.message}`);
            console.log(data.message)
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while submitting the reservation.");
    });
});
 


// Delete Reservation
document.getElementById("deleteReservationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const reservationID = document.getElementById("deleteReservationID").value.trim();
    console.log(reservationID);

    const requestData = {
        reservationID: reservationID
    };

    fetch("/manage/delete/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData) // Send JSON instead of SPARQL query
    })
    .then(response => response.json()) // Assume the backend responds with JSON
    .then(data => {
        console.log("Backend Response:", data);
        if (data.success) {
            alert("Reservation deleted successfully!");
            document.getElementById("deleteReservationForm").reset();
        } else {
            alert("Error deleting reservation.");
        }
    })
    .catch(error => console.error("Error:", error));
});