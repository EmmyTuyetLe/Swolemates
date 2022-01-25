'use strict';

let forms = document.querySelectorAll(".unsave_buddy_form")

for (let form of forms){
  form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    let buddyId = evt.target.id.split("_")[2]
    console.log(buddyId);
  
    const formInputs = {
      buddy_id: document.querySelector(`#buddy_id_${buddyId}`).value,
      user_id: document.querySelector("#unsaver_id").value
    };

    console.log(formInputs)
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


