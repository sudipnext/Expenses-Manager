const usernameField = document.querySelector("#usernameField");
const feedbackField = document.querySelector("#invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedback = document.querySelector("#email_feedback");
const showPasswordToggle = document.querySelector(".ShowPasswordToggle");
const passwordField = document.querySelector("#passwordField");
const myButton = document.querySelector("#my-button");

showPasswordToggle.addEventListener("click", (e) => {
  if (showPasswordToggle.textContent === "SHOW") {
    showPasswordToggle.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    passwordField.setAttribute("type", "password");
    showPasswordToggle.textContent = "SHOW";
  }
});

emailField.addEventListener("keyup", (e) => {
  const emailData = e.target.value;
  emailField.classList.remove("is-invalid");
  emailField.classList.remove("is-valid");
  emailFeedback.style.display = "none";

  if (emailData.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailData }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.email_error) {
          myButton.setAttribute("aria-disabled", true);
          emailField.classList.add("is-invalid");
          emailFeedback.style.display = "block";
          emailFeedback.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          myButton.removeAttribute("disabled");
          emailField.classList.add("is-valid");
        }
      });
  }
});

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;
  usernameField.classList.remove("is-invalid");
  usernameField.classList.remove("is-valid");

  feedbackField.style.display = "none";

  console.log(usernameVal);
  if (usernameVal.length > 0) {
    fetch("/authentication/validate-username", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        if (data.username_error) {
          myButton.setAttribute("disabled", true);

          usernameField.classList.add("is-invalid");
          feedbackField.style.display = "block";
          feedbackField.innerHTML = `<p>${data.username_error}</p>`;
        } else {
          myButton.removeAttribute("disabled");

          usernameField.classList.add("is-valid");
        }
      });
  }
});
