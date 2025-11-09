document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const email = document.getElementById("loginEmail");
  const password = document.getElementById("loginPassword");
  const loginError = document.getElementById("loginError");

  loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    loginError.textContent = "";

    if (email.value === "viking@legacy.com" && password.value === "valhalla123") {
      alert("Login successful! Welcome to the camp.");
      loginForm.reset();
    } else {
      loginError.textContent = "Invalid email or password. Try again.";
      email.classList.add("invalid");
      password.classList.add("invalid");
    }
  });
});
