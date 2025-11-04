//-----------------------------------
//   © 2025 Air Checker. Todos los derechos reservados.
//-----------------------------------
//   Autor: Fédor Tikhomirov
//   Fecha: 2 de noviembre de 2025
//-----------------------------------
//   Fichero: password_check.js
//   Descripción: Este fichero ayuda a mostrar si los criterios de la contraseña
//   se cumplen en tiempo real
//-----------------------------------

/**
 * Comprueba si la contraseña cumple los criterios:
 * - Al menos 8 caracteres
 * - Al menos una mayúscula
 * - Al menos un número
 * - Al menos un carácter especial
 */
function isPasswordSecure(password) {
    const regex = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+\-=\[\]{};:"'<>,.?/~`]).{8,}$/;
    return regex.test(password);
}

function showRemainingCriteria() {
    const passwordInput = document.getElementById("password");
    if (!passwordInput) return;

    const passwordCriteria = document.createElement("div");
    passwordCriteria.style.marginTop = "5px";
    passwordInput.parentNode.appendChild(passwordCriteria);

    function updateCriteria() {
        const value = passwordInput.value;
        if (!value) {
            passwordCriteria.innerHTML = "";
            return;
        }

        const criteria = [
            { check: value.length >= 8, text: "Mínimo 8 caracteres" },
            { check: /[A-Z]/.test(value), text: "Al menos una mayúscula" },
            { check: /[0-9]/.test(value), text: "Al menos un número" },
            { check: /[!@#$%^&*()_+\-=\[\]{};:"'<>,.?/~`]/.test(value), text: "Al menos un carácter especial" }
        ];

        passwordCriteria.innerHTML = criteria.map(c =>
            `<div style="line-height:1.4;">${c.check ? '✅' : '❌'} ${c.text}</div>`
        ).join('');
    }

    passwordInput.addEventListener("input", updateCriteria);
}

// Llamada directa
showRemainingCriteria();