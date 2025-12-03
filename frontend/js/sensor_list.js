if (getUserRole() !== "Administrador") {
    if (document.referrer) {
        window.location.href = document.referrer;
    } else {
        window.location.href = "/login.html";
    }
}

// Función que devuelve el HTML de cada tarjeta
function TarjetaSensor(sensor) {
    return `
        <div>
            <h3>${sensor.UUID}</h3>
            <p><strong>Usuario:</strong> ${sensor.ASSOCIATED_USER}</p>
            <p><strong>Última actividad:</strong> ${sensor.LAST_ACTIVE}</p>
        </div>
    `;
}

// Función que carga sensores desde el endpoint
async function cargarSensores() {
    try {
        const response = await fetch("/v1/admin/sensors");
        const data = await response.json();

        const contenedor = document.getElementById("lista-sensores");
        contenedor.innerHTML = "";

        data.sensors.forEach(sensor => {
            contenedor.innerHTML += TarjetaSensor(sensor);
        });
    } catch (error) {
        console.error("Error al cargar sensores:", error);
    }
}

cargarSensores();