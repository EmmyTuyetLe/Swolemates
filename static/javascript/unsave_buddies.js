'use strict';

let unsaveBuddyForms = document.querySelectorAll(".unsave_buddy_form")

for (let form of unsaveBuddyForms){
  form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    let buddyId = evt.target.id.split("_")[2]
  
    const formInputs = {
      buddy_id: buddyId,
      user_id: document.querySelector("#unsaver_id").value
    };
    fetch("/unsave_buddy.json", {
      method: "POST",
      body: JSON.stringify(formInputs),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(response => response.json())
      .then(responseJson => {
        console.log(responseJson);
        alert(responseJson.status);
        
      });
  });
}


