//-----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
//-----------------------------------
//   Autor: Adrián Jáuregui
//   Fecha: 10 de diciembre de 2025
//-----------------------------------
//   Fichero: incidencias_client.js
//   Descripción: Este fichero permite el envío de los datos de incidencias a la API
//-----------------------------------

const form = document.getElementById("incidencias_form");

async function handleIncidencias(event) {
    event.preventDefault();

    // Obtiene datos de las entradas
    const asunto = document.getElementById("asunto-label").value;
    const description = document.getElementById("descripcion-label").value;

    try {
        // Envia POST al endpoint de login
        const response = await fetch("/incidents/create", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username_or_email, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = `¡Incidencia enviada correctamente!`;
            messageDiv.style.color = "green";
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
form.addEventListener("submit", handleIncidencias);
