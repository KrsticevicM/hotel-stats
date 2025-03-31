// add reservation form
document.getElementById("addReservationForm").addEventListener("submit", function(event) {
    event.preventDefault();
 
    // Capture form values
    const country = document.getElementById("country").value;
    const staysInWeekNightsInput = document.getElementById("stays_in_week_nights");
    const staysInWeekendNightsInput = document.getElementById("stays_in_weekend_nights");
    const arrivalDate = document.getElementById("arrivalDate").value;
    const hotelType = document.querySelector('input[name="hotelType"]:checked')?.value;
    const mealType = document.querySelector('input[name="meal"]:checked')?.value;
 
    // Validation check
    if (!country || !arrivalDate || !hotelType || !mealType || !staysInWeekNights || !staysInWeekendNights) {
        alert("Please fill in all fields before submitting!");
        return;
    }

    // Validate stays_in_week_nights and stays_in_weekend_nights
    if (!Number.isInteger(Number(staysInWeekNights)) || !Number.isInteger(Number(staysInWeekendNights))) {
        alert("Please enter valid integer values for the number of nights.");
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
        stays_in_week_nights: weekNights,
        stays_in_weekend_nights: weekendNights
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
            alert(`Reservation added successfully!`);
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


// Modify Reservation
document.getElementById("modifyReservationForm").addEventListener("submit", function(event) {
    event.preventDefault();
 
    const reservationID = document.getElementById("modifyReservationID").value.trim();
    const isCanceled = document.querySelector('input[name="isCanceled"]:checked')?.value;
    const arrivalDate = document.getElementById("modifyArrivalDate").value;
    const mealType = document.querySelector('input[name="modifyMeal"]:checked')?.value;
    const staysInWeekNights = document.getElementById("modifyStaysInWeek").value.trim();
    const staysInWeekendNights = document.getElementById("modifyStaysInWeekend").value.trim();
    
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    const formData = {
        id: reservationID, // Assuming reservationID is already set
        day: "",
        month: "", 
        year: "",
        meal: "",
        is_canceled: "",
        stays_in_week_nights: "",
        stays_in_weekend_nights: ""
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
        formData.meal = mealType;
    }
    if (isCanceled !== undefined) {
        formData.is_canceled = isCanceled;
    }

    if (stays_in_week_nights !== undefined){
        formData.stays_in_week_nights = staysInWeekNights;
    }

    if (stays_in_weekend_nights !== undefined){
        formData.stays_in_weekend_nights = staysInWeekendNights;
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