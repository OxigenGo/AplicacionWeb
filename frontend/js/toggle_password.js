//-----------------------------------
//   © 2025 AirChecker. Todos los derechos reservados.
//-----------------------------------
//   Autor: Fédor Tikhomirov
//   Fecha: 2 de noviembre de 2025
//-----------------------------------
//   Fichero: toggle_password.js
//   Descripción: Este fichero permite la visualización de la contraseña
//-----------------------------------

const passwordInput = document.getElementById("password");
const confirmInput = document.getElementById("password-confirm");
const togglePassword = document.getElementById("toggle-password");
const toggleConfirm = document.getElementById("toggle-password-confirm");

const openeye = document.getElementById("open-eye");
const closeeye = document.getElementById("close-eye");
const openeyeconfirm = document.getElementById("open-eye-confirm");
const closeeyeconfirm = document.getElementById("close-eye-confirm");

// Función para alternar la visibilidad -- CHAPUZA EXTREMA ARREGLAR
function toggleVisibility(togglepaswd,input, icon) {
    if(togglepaswd == "normal"){
        if (input.type === "password") {
            input.type = "text";
            openeye.style.display = "none"
            closeeye.style.display = "block";
        } else {
            input.type = "password";
            openeye.style.display = "block"
            closeeye.style.display = "none";
        }
    } else {
        console.log("entra")
        if (input.type === "password") {
            input.type = "text";
            openeyeconfirm.style.display = "none"
            closeeyeconfirm.style.display = "block";
        } else {
            input.type = "password";
            openeyeconfirm.style.display = "block"
            closeeyeconfirm.style.display = "none";
        }
    }
}

// Añadir eventos de click
if (togglePassword) {
    togglePassword.addEventListener("click", () => toggleVisibility("normal",passwordInput, togglePassword));
}
if (toggleConfirm) {
    toggleConfirm.addEventListener("click", () => toggleVisibility("confirm",confirmInput, toggleConfirm));
}