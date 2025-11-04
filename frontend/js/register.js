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

//HandleRegister se encarga de enviar los datos del formulario a la API
async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("password-confirm").value;
    const termsChecked = document.getElementById("terms").checked;

    if (password !== confirm_password) {
        messageDiv.textContent = "Las contraseñas no coinciden.";
        messageDiv.style.color = "red";
        return;
    }

    if (!isPasswordSecure(password)) {
        messageDiv.textContent = "La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un carácter especial.";
        messageDiv.style.color = "red";
        return;
    }

    if (!termsChecked) {
        messageDiv.textContent = "Debes aceptar los términos y condiciones.";
        messageDiv.style.color = "red";
        return;
    }

    //Envía los datos a la API
    try {
        const response = await fetch("v1/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        //Si el registro es exitoso
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
        //Si hay un error de conexión
    } catch (error) {
        messageDiv.textContent = "Error de conexión con el servidor.";
        messageDiv.style.color = "red";
        console.error(error);
    }
}

//Al hacer el submit ejecuta la función de registro
form.addEventListener("submit", handleRegister);