'use strict';

document.querySelector("#fav_location").addEventListener("click", evt => {
  evt.preventDefault();

  const formInputs = {
    location_id: document.querySelector("#location_id").value,
    user_id: document.querySelector("#user_id").value
  };

  console.log(formInputs);

  fetch("/fav_location.json", {
    method: "POST",
    body: JSON.stringify(formInputs),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(response => response.json())
    .then(responseJson => {
      console.log("******************")
      console.log(responseJson);
      alert(responseJson.status);
    });
});


