'use strict';

document.querySelector("#send_message_form").addEventListener("submit", evt => {
  evt.preventDefault();
  console.log("Clicked!!!!!!*******");

  const formInputs = {
    buddy_id: document.querySelector("#buddy_id").value,
    user_id: document.querySelector("#sender_id").value,
    message_content: document.querySelector("#message_text").value
  };

  console.log(formInputs);

  fetch("/send_message.json", {
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
