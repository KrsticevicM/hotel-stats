// add reservation form
document.getElementById("addReservationForm").addEventListener("submit", function(event) {
   event.preventDefault();

   // Capture form values
   const name = document.getElementById("name").value.trim();
   const email = document.getElementById("email").value.trim();
   const country = document.getElementById("country").value.trim();
   const arrivalDate = document.getElementById("arrivalDate").value;
   const hotelType = document.querySelector('input[name="hotelType"]:checked')?.value;
   const mealType = document.querySelector('input[name="meal"]:checked')?.value;

   // Validation check
   if (!name || !email || !country || !arrivalDate || !hotelType || !mealType) {
       alert("Please fill in all fields before submitting!");
       return;
   }

   // Mock reservation ID generation
   const reservationID = "RES-" + Math.floor(1000 + Math.random() * 9000);

   // SPARQL INSERT Query - fill in KG
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

   fetch("http://your-backend-endpoint", {
       method: "POST",
       headers: { "Content-Type": "application/sparql-update" },
       body: sparqlQuery
   })
   .then(response => response.text())
   .then(data => {
       console.log("SPARQL Insert Response:", data);
       alert(`Reservation ${reservationID} added successfully!`);
       document.getElementById("addReservationForm").reset();
   })
   .catch(error => console.error("Error:", error));
});

// Modify Reservation
document.getElementById("modifyReservationForm").addEventListener("submit", function(event) {
   event.preventDefault();

   const reservationID = document.getElementById("modifyReservationID").value.trim();
   const name = document.getElementById("modifyName").value.trim();
   const email = document.getElementById("modifyEmail").value.trim();
   const country = document.getElementById("modifyCountry").value.trim();
   const arrivalDate = document.getElementById("modifyArrivalDate").value;
   const hotelType = document.querySelector('input[name="modifyHotelType"]:checked')?.value;
   const mealType = document.querySelector('input[name="modifyMeal"]:checked')?.value;

   // Check if reservation exists fill in KG
   const checkReservationQuery = `
       PREFIX ex: <http://example.com/hotel#>
       ASK WHERE { ex:${reservationID} a ex:Reservation . }
   `;

   fetch("http://your-backend-endpoint", {
       method: "POST",
       headers: { "Content-Type": "application/sparql-query" },
       body: checkReservationQuery
   })
   .then(response => response.text())
   .then(data => {
       if (data.includes("false")) {
           alert("Reservation ID does not exist!");
           return;
       }
       
       // SPARQL DELETE/INSERT Query
       let updateQuery = `PREFIX ex: <http://example.com/hotel#> DELETE { ex:${reservationID} ?p ?o } INSERT { `;
       if (name) updateQuery += `ex:${reservationID} ex:name "${name}" . `;
       if (email) updateQuery += `ex:${reservationID} ex:email "${email}" . `;
       if (country) updateQuery += `ex:${reservationID} ex:country "${country}" . `;
       if (arrivalDate) updateQuery += `ex:${reservationID} ex:arrivalDate "${arrivalDate}" . `;
       if (hotelType) updateQuery += `ex:${reservationID} ex:hotelType "${hotelType}" . `;
       if (mealType) updateQuery += `ex:${reservationID} ex:mealType "${mealType}" . `;
       updateQuery += `} WHERE { ex:${reservationID} ?p ?o }`;

       return fetch("http://your-backend-endpoint", {
           method: "POST",
           headers: { "Content-Type": "application/sparql-update" },
           body: updateQuery
       });
   })
   .then(response => response.text())
   .then(data => {
       console.log("SPARQL Update Response:", data);
       alert("Reservation modified successfully!");
       document.getElementById("modifyReservationForm").reset();
   })
   .catch(error => console.error("Error:", error));
});

// Delete Reservation
document.getElementById("deleteReservationForm").addEventListener("submit", function(event) {
   event.preventDefault();

   const reservationID = document.getElementById("deleteReservationID").value.trim();
   
   // fill in KG
   const deleteQuery = `
       PREFIX ex: <http://example.com/hotel#>
       DELETE WHERE { ex:${reservationID} ?p ?o . }
   `;

   fetch("http://your-backend-endpoint", {
       method: "POST",
       headers: { "Content-Type": "application/sparql-update" },
       body: deleteQuery
   })
   .then(response => response.text())
   .then(data => {
       console.log("SPARQL Delete Response:", data);
       alert("Reservation deleted successfully!");
       document.getElementById("deleteReservationForm").reset();
   })
   .catch(error => console.error("Error:", error));
});