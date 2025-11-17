//-----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
//-----------------------------------
//   Autor: Fédor Tikhomirov
//   Fecha: 27 de octubre de 2025
//-----------------------------------
//   Fichero: login.js
//   Descripción: Este fichero permite el envío de los datos de inicio de sesión a la API
//-----------------------------------

const form = document.getElementById("login_form");
const messageDiv = document.getElementById("login_message");

async function handleLogin(event) {
    event.preventDefault();

    // Obtiene datos de las entradas
    const username_or_email = document.getElementById("username_or_email").value;
    const password = document.getElementById("password").value;

    try {
        // Envia POST al endpoint de login
        const response = await fetch("/v1/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username_or_email, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = `¡Bienvenido, ${data.usuario.username}!`;
            messageDiv.style.color = "green";
            //TODO - Redirigir a siguiente página
            
        } else {
            // Login fallido
            if (data.detail) {
                // FastAPI puede devolver el "detail" como string o array si son varios
                if (Array.isArray(data.detail)) {
                    messageDiv.textContent = data.detail.map(d => d.msg).join(", ");
                } else {
                    messageDiv.textContent = data.detail;
                }
            } else {
                messageDiv.textContent = "Error al iniciar sesión";
            }
            messageDiv.style.color = "red";
        }
    } catch (error) {
        messageDiv.textContent = "Error de conexión con el servidor.";
        messageDiv.style.color = "red";
        console.error(error);
    }
}

// Asocia la función al submit del login
form.addEventListener("submit", handleLogin);
