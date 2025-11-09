const signupForm = document.getElementById("signupForm");
const username = document.getElementById("fname");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");
const dob = document.getElementById("dob");
const phone = document.getElementById("pnum");

const userError = document.getElementById("userError");
const passError = document.getElementById("passError");
const confirmPassError = document.getElementById("confirmPassError");
const phoneError = document.getElementById("phoneError");
const dobError = document.getElementById("dobError");

const vikingBtn = document.getElementById("vikingGen");
const vikingNameDisplay = document.getElementById("vikingName");

const vikingNames = [
    "Erik the Bold","Astrid the Fearless", "Bjorn Ironside","Freya Flamehair", "Ragnar Stormborn","Leif the Wanderer","Ingrid Wolf-Eye","Thorvald Thunderfist",
    "Sigrid the Unshaken", "Haldor the Ironclad", "Eydis Frostborn", "Sten Skullsplitter", "Solveig the Wise", "Ulf the Silent",
    "Kjell Bearheart","Gunnhild Sea-Blessed","Ivar the Restless","Thora Iceblade","Vidar Shieldbreaker","Brynhild the Swift","Magnus Axehand",
    "Helga Moonshadow", "Olaf Deepvoice", "Runa Fireborn", "Torsten Nightwolf"
];

function generateVikingName() {
    const index = Math.floor(Math.random() * vikingNames.length);
    const name = vikingNames[index];
    vikingNameDisplay.textContent = `Your Viking name: ${name}`;
}

vikingBtn.addEventListener("click", generateVikingName);

function isValidUsername(name) {
  return /^[a-zA-Z]+$/.test(name);
}

function isStrongPassword(pass) {
  const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$/;
  return pattern.test(pass);
}

function checkConfirmPassword() {
  if (confirmPassword.value !== password.value) {
    confirmPassError.textContent = "Passwords do not match.";
    return false;
  } else {
    confirmPassError.textContent = "";
    return true;
  }
}
