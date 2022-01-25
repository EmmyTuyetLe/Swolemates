'use strict';

let saveBuddyForms = document.querySelectorAll(".save_buddy_form")

for (let form of saveBuddyForms){
  console.log(form);
  form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    let buddyId = evt.target.id.split("_")[2]
  
    const formInputs = {
      buddy_id: document.querySelector(`#buddy_id_${buddyId}`).value,
      user_id: document.querySelector("#saver_id").value
    };

    console.log(formInputs)
    fetch("/save_buddy.json", {
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


