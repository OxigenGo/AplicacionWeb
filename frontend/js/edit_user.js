//-----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
//-----------------------------------
//   Autor: Fédor Tikhomirov
//   Fecha: 27 de octubre de 2025
//-----------------------------------
//   Fichero: edit_user.js
//   Descripción: Este fichero permite el envio del formulario de edicion de usuario y sus datos a la API
//-----------------------------------

const form = document.getElementById("edit_user_form");
const messageDiv = document.createElement("div");
form.prepend(messageDiv);

async function handleEditUser(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const newPassword = document.getElementById("password").value.trim();
    const confirmNewPassword = document.getElementById("confirm-password").value.trim();
    const currentPassword = document.getElementById("current-password").value.trim();

    current_user_data = getCookie("user_data")
    if (!current_user_data) return
    const current_email = current_user_data.email

    try {
        const response = await fetch("/v1/users/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username_or_email: current_email,
                password: currentPassword
            })
        });

        if (!response.ok) {
            messageDiv.textContent = "Contraseña actual incorrecta.";
            messageDiv.style.color = "red";
            return;
        }

    } catch (error) {
        messageDiv.textContent = "Error de conexión con el servidor.";
        messageDiv.style.color = "red";
        console.error(error);
        return;
    }

    if (newPassword !== confirmNewPassword) {
        messageDiv.textContent = "Las contraseñas no coinciden.";
        messageDiv.style.color = "red";
        return;
    }

    const payload = {
        username,
        email,
        profilePic: ""
    };

    if (newPassword) payload.password = newPassword;

    try {
    const response = await fetch("/v1/users/update", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (response.ok) {
        messageDiv.textContent = `Usuario actualizado correctamente: ${data.usuario.username}`;
        messageDiv.style.color = "green";
    } else {
        if (data.detail) {
            messageDiv.textContent = Array.isArray(data.detail) ? 
                data.detail.map(d => d.msg).join(", ") :
                data.detail;
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

function fill_user_data() {
    const user = getCookie("user_data");
    if (!user) return;

    const registration_year = new Date(user.registration_date).getFullYear();

    document.getElementById("username").value = user.username || "";
    document.getElementById("email").value = user.email || "";
    document.getElementById("registration_date").textContent = `Usuario activo desde ${registration_year}`;
}



if (isUserLoggedIn() == false) window.location.href = "../login.html";
else { fill_user_data(); }

form.addEventListener("submit", handleEditUser);