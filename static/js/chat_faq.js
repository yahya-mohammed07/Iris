const menu = document.querySelector("#menu-icon");
const navbar = document.querySelector(".navbar");
menu.onclick = () => {
  menu.classList.toggle("bx-x"); // toggle menu icon to x
  navbar.classList.toggle("open"); // toggle navbar to open
};

const msgerForm = document.querySelector(".msger-inputarea");
const msgerInput = document.querySelector(".msger-input");
const msgerChat = document.querySelector(".msger-chat");

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "/static/images/robot-face-svgrepo-com.svg";
const PERSON_IMG = "";
const BOT_NAME = "    Iris";
const PERSON_NAME = "";

msgerForm.addEventListener("submit", function (event) {
  event.preventDefault(); // prevent form from submitting
  const msgText = msgerInput.value;
  if (!msgText) {
    // if message is empty
    return;
  }
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText); // send message to chatbot
  msgerInput.value = "";
  botResponse(msgText); // send message to chatbot
});

function appendMessage(name, img, side, text, typing = false) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>
      <div class="msg-bubble${typing ? " typing" : ""}">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>
        <div class="msg-text"></div>
      </div>
    </div>
  `; // create message html element with name, image, side, text, and typing status

  msgerChat.insertAdjacentHTML("beforeend", msgHTML); // add message to chat box

  if (typing) { // if typing
    const msgBubble = msgerChat.lastElementChild;
    const msgText = msgBubble.querySelector(".msg-text");
    const typingDelay = 50;

    for (let i = 0; i < text.length; i++) {
      setTimeout(() => {
        msgText.innerHTML += text.charAt(i);
        msgerChat.scrollTop += 50;
      }, typingDelay * i);
    }
  } else {
    const msgBubble = msgerChat.lastElementChild;
    const msgText = msgBubble.querySelector(".msg-text");
    msgText.innerHTML = text;
    msgerChat.scrollTop += 500;
  }
}

function botResponse(rawText) {
  // Check if previous message was a typing message
  const isTypingMessage =
    msgerChat.lastElementChild?.querySelector(".msg-bubble.typing") != null;

  // Show bot "typing" message
  appendMessage(BOT_NAME, BOT_IMG, "left", "Thinking...", true);

  // Bot Response
  setTimeout(() => {
    fetch(`/get?msg=${encodeURIComponent(rawText)}`)
      .then( (response) => {
        // response is a Response instance.
        return response.text(); // return the response text
      })
      .then( (data) => {
        // data is a string
        // Remove "typing" message and show bot's response
        removeMessage(msgerChat.lastElementChild.querySelector(".msg-bubble"));
        appendMessage(BOT_NAME, BOT_IMG, "left", data, !isTypingMessage);

        // Add regenerate button
        const regenerateButton = document.createElement("button");
        regenerateButton.innerHTML = `<i class="fas fa-sync"></i>`;
        regenerateButton.addEventListener("click", () => {
          botResponse(rawText); // send message to chatbot again
        });

        msgerChat.lastElementChild.appendChild(regenerateButton);

        msgerChat.lastElementChild.appendChild(regenerateButton);
      })
      .catch( (error) => {
        console.error(error);
      });
  }, 1000);
}

function removeMessage(message) {
  message.parentNode.parentNode.removeChild(message.parentNode);
}

// Utils
function get(selector, root = document) {
  // get element by selector
  return root.querySelector(selector); // return the first element that matches the specified selector
}

function formatDate(date) {
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`; // 10:30
}

let modal = document.getElementById("myModal");
let btn = document.getElementById("myBtn");
let span = document.getElementsByClassName("close")[0];

btn.onclick = function () {
  modal.style.display = "block";
};

span.onclick = function () {
  modal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

const textCounter = (field, field2, maxlimit) => {
  let countfield = document.querySelector(field2);
  if (field.value.length > maxlimit) {
    return false; // stop when max reached
  } else {
    countfield.value = maxlimit - field.value.length;
  }
};