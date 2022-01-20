'use strict';

document.querySelector("#save_buddy_form").addEventListener("submit", evt => {
  evt.preventDefault();
  console.log("Clicked!!!!!!*******");

  const formInputs = {
    buddy_id: document.querySelector("#buddy_id").value,
    user_id: document.querySelector("#saver_id").value
  };

  console.log(formInputs);

  fetch("/save_buddy.json", {
    method: "POST",
    body: JSON.stringify(formInputs),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(response => response.json())
    .then(responseJson => {
      alert(responseJson.status);
    });
});

