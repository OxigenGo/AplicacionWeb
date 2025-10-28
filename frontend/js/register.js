//-----------------------------------
//   Autor: Adrián Jáuregui
//   Fecha: 28 de octubre de 2025
//-----------------------------------

const form = document.getElementById("register_form");
const messageDiv = document.getElementById("register_message");

async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("password-confirm").value;

    try {
        const respones = await fetch("v1/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password, confirm_password })
        });

        const data = await respones.json();

        if (respones.ok) {
            messageDiv.textContent = `¡Registro exitoso, ${data.usuario.username}!`;
            messageDiv.style.color = "black";
            //TODO - Redirigir a página de registro exitoso
        } else {
            //Si el registro falla
            if (data.detail) {
                if (Array.isArray(data.detail)) {
                    messageDiv.textContent = data.detail.map(d => d.msg).join(", ");
                } else {
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