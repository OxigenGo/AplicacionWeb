//-----------------------------------
//   © 2025 RRVV Systems. Todos los derechos reservados.
//-----------------------------------
//   Autor: Adrián Jáuregui Felipe
//   Fecha: 28 de octubre de 2025
//-----------------------------------
//   Fichero: register.js
//   Descripción: Este fichero envia los datos de registro a la API
//-----------------------------------

const form = document.getElementById("register-form");
const messageDiv = document.getElementById("register_message");

async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("password-confirm").value;

    if (password !== confirm_password) {
        // TODO: Mostrar mensaje de error
        return;
    }

    try {
        const response = await fetch("v1/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = `¡Registro exitoso, ${data.usuario.username}!`;
            messageDiv.style.color = "black";
            //TODO - Redirigir a página de registro exitoso
        } else {
            //Si el registro falla
            if (data.detail) {
                //Si hay varios errores, los une en un string y los muestra
                if (Array.isArray(data.detail)) {
                    messageDiv.textContent = data.detail.map(d => d.msg).join(", ");
                } else {
                    //Si solo hay un error, lo muestra directamente
                    messageDiv.textContent = data.detail;
                }
            } else {
                messageDiv.textContent = "Error al registrar usuario";
            }
        }
    } catch (error) {
        messageDiv.textContent = "Error de conexión con el servidor.";
        messageDiv.style.color = "red";
        console.error(error);
    }
}

//Al hacer el submit ejecuta la función de registro
form.addEventListener("submit", handleRegister);