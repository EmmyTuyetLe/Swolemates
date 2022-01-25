'use strict';
console.log('hellllooooooooo')
let sendMessageForms = document.querySelectorAll(".send_message_form")
console.log('TEST 1');

for (let form of sendMessageForms){
  form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    console.log('TEST 2')


    let buddyId = evt.target.id.split("_")[2]
    console.log("*********", buddyId);
  
    const formInputs = {
      buddy_id: document.querySelector(`#buddy_id_${buddyId}`).value,
      user_id: document.querySelector("#sender_id").value,
      message_content: document.querySelector("#message_text").value
    };

    console.log('TEST 3')


    console.log(formInputs)
    fetch("/send_message.json", {
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


