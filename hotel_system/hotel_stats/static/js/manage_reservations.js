document.getElementById("addReservationForm").addEventListener("submit", function(event) {
   event.preventDefault(); // Prevent actual form submission

   // Capture form values
   const name = document.getElementById("name").value.trim();
   const email = document.getElementById("email").value.trim();
   const country = document.getElementById("country").value.trim();
   const arrivalDate = document.getElementById("arrivalDate").value;

   // Get selected hotel type
   const hotelType = document.querySelector('input[name="hotelType"]:checked')?.value;
   
   // Get selected meal type
   const mealType = document.querySelector('input[name="meal"]:checked')?.value;

   // Validation check
   if (!name || !email || !country || !arrivalDate || !hotelType || !mealType) {
       alert("Please fill in all fields before submitting!");
       return; // Stop execution if validation fails
   }

   // Mock reservation ID generation
   const reservationID = "RES-" + Math.floor(1000 + Math.random() * 9000);

   // Mock SPARQL INSERT Query
   const sparqlQuery = `
       PREFIX ex: <http://example.com/hotel#> 
       INSERT DATA {
           ex:${reservationID} a ex:Reservation ;
               ex:name "${name}" ;
               ex:email "${email}" ;
               ex:hotelType "${hotelType}" ;
               ex:country "${country}" ;
               ex:arrivalDate "${arrivalDate}" ;
               ex:mealType "${mealType}" .
       }
   `;

   console.log("Mock SPARQL Query (To be sent to GraphDB):");
   console.log(sparqlQuery);

   // Simulate adding to the database (Mock)
   console.log("Reservation Added Successfully!");
   alert(`Reservation ${reservationID} added for ${name}!`);

   // Reset form after successful submission
   document.getElementById("addReservationForm").reset();
});

// Modify Reservation functionality
document.getElementById("modifyReservationForm").addEventListener("submit", function(event) {
   event.preventDefault();
   console.log("Modify Reservation Form Submitted!");

   // Get form values
   const reservationID = document.getElementById("modifyReservationID").value.trim();
   const name = document.getElementById("modifyName").value.trim();
   const email = document.getElementById("modifyEmail").value.trim();
   const country = document.getElementById("modifyCountry").value.trim();
   const arrivalDate = document.getElementById("modifyArrivalDate").value;
   
   // Get selected hotel type and meal type
   const hotelType = document.querySelector('input[name="modifyHotelType"]:checked');
   const mealType = document.querySelector('input[name="modifyMeal"]:checked');

   // Mock database check
   const existingReservations = ["RES-1234", "RES-5678"];
   if (!existingReservations.includes(reservationID)) {
       alert("Reservation ID does not exist!");
       return;
   }

   console.log("Modifying Reservation:");
   console.log({
       reservationID, name, email, country, arrivalDate,
       hotelType: hotelType ? hotelType.value : "Unchanged",
       mealType: mealType ? mealType.value : "Unchanged"
   });

   alert("Reservation modified successfully!");

   // Reset form
   document.getElementById("modifyReservationForm").reset();
});

// Delete Reservation Form Submission
document.getElementById("deleteReservationForm").addEventListener("submit", function(event) {
   event.preventDefault();
   console.log("Delete Reservation Form Submitted!");

   // Get reservation ID
   const reservationID = document.getElementById("deleteReservationID").value.trim();

   // Mock database check
   const existingReservations = ["RES-1234", "RES-5678"];
   if (!existingReservations.includes(reservationID)) {
       alert("Reservation ID does not exist!");
       return;
   }

   console.log("Deleting Reservation ID:", reservationID);
   alert("Reservation deleted successfully!");

   // Reset form
   document.getElementById("deleteReservationForm").reset();
});