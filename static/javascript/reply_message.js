'use strict';
let replyMessageForms = document.querySelectorAll(".reply_message_form")
console.log('*********TEST 1');

for (let form of replyMessageForms){
  form.addEventListener("submit", (evt) => {
    evt.preventDefault();

    let buddyId = evt.target.id.split("_")[2]
  
    const formInputs = {
      buddy_id: document.querySelector(`#buddy_id_${buddyId}`).value,
      user_id: document.querySelector("#sender_id").value,
      message_content: document.querySelector(`#message_text_${buddyId}`).value
    };

    console.log('TEST 3')


    console.log(formInputs)
    fetch("/reply_message.json", {
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


