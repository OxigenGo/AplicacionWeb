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

// Función para alternar la visibilidad
function toggleVisibility(input, icon) {
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "🙈";
    } else {
        input.type = "password";
        icon.textContent = "👁️";
    }
}

// Añadir eventos de click
if (togglePassword) {
    togglePassword.addEventListener("click", () => toggleVisibility(passwordInput, togglePassword));
}
if (toggleConfirm) {
    toggleConfirm.addEventListener("click", () => toggleVisibility(confirmInput, toggleConfirm));
}