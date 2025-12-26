//-----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
//-----------------------------------
//   Autor: Adrián Jáuregui
//   Fecha: 26 de diciembre de 2025
//-----------------------------------
//   Fichero: index.js
//   Descripción: Este fichero maneja el cambio de boton
//-----------------------------------

const buttons = document.getElementById("session-buttons");
const username = getUsername();

//Algoritmo para cambiar los botones del header
if(isUserLoggedIn()){
    buttons.innerHTML =
        `<button class="profile-button">${username}</button>`;
} else {
    buttons.innerHTML =
        `<a href="./registro.html" class="register-button">Registro</a>
        <a href="./login.html" class="login-button">Iniciar Sesión</a>`;
}