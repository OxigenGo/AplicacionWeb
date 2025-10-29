//-----------------------------------
//   Autor: Fédor Tikhomirov
//   Fecha: 27 de octubre de 2025
//   Esta fichero permite el envio del formulario y sus datos a la API
//-----------------------------------

const form = document.querySelector("form");
const messageDiv = document.createElement("div");
form.prepend(messageDiv);

async function handleEditUser(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm_password").value.trim();

    if (password !== confirmPassword) {
        messageDiv.textContent = "Las contraseñas no coinciden.";
        messageDiv.style.color = "red";
        return;
    }

    const payload = {
        username: username,
        email: email,
        password: password,
        profilePic: "" // Placeholder
    };

    try {
        const response = await fetch("/v1/users/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = `Usuario actualizado correctamente: ${data.usuario.username}`;
            messageDiv.style.color = "green";
        } else {
            if (data.detail) {
                if (Array.isArray(data.detail)) {
                    messageDiv.textContent = data.detail.map(d => d.msg).join(", ");
                } else {
                    messageDiv.textContent = data.detail;
                }
            } else {
                messageDiv.textContent = "Error al actualizar el usuario.";
            }
            messageDiv.style.color = "red";
        }
    } catch (error) {
        messageDiv.textContent = "Error de conexión con el servidor.";
        messageDiv.style.color = "red";
        console.error(error);
    }
}