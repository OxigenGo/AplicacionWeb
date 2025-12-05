/*if (getUserRole() !== "Administrador") {
    if (document.referrer) {
        window.location.href = document.referrer;
    } else {
        window.location.href = "/login.html";
    }
}*/

const sensors_prueba= [
    {UUID: 1,ASSOCIATED_USER: "Usuario1",LAST_ACTIVE: "2023-01-15"},
    {UUID: 1,ASSOCIATED_USER: "Usuario1",LAST_ACTIVE: "2023-01-15"},
    {UUID: 1,ASSOCIATED_USER: "Usuario1",LAST_ACTIVE: "2023-01-15"},
    {UUID: 1,ASSOCIATED_USER: "Usuario1",LAST_ACTIVE: "2023-01-15"},
    {UUID: 1,ASSOCIATED_USER: "Usuario1",LAST_ACTIVE: "2023-01-15"},
    {UUID: 1,ASSOCIATED_USER: "Usuario1",LAST_ACTIVE: "2023-01-15"},
]

function prueba_etiquetas(sensors){
    console.log(document);
    const contenedor = document.getElementById("lista-sensores");

    contenedor.innerHTML = "";

    sensors.forEach(sensor => {
        const card = document.createElement("div");
        card.className = "sensor-card";
        card.innerHTML += TarjetaSensor(sensor);
        contenedor.appendChild(card);
    });
}

// Función que devuelve el HTML de cada tarjeta
function TarjetaSensor(sensor) {
    return `
        <p>Id del sensor: ${sensor.UUID}</p>
        <p>Usuario asociado:${sensor.ASSOCIATED_USER}</p>
        <p>Ultima actividad: <br>${sensor.LAST_ACTIVE}</p>
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
            const card = document.createElement("div");
            card.className = "sensor-card";
            card.innerHTML += TarjetaSensor(sensor);
            contenedor.appendChild(card);
        });
    } catch (error) {
        console.error("Error al cargar sensores:", error);
    }
}

prueba_etiquetas(sensors_prueba);
//cargarSensores();