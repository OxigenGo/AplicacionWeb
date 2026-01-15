/* 
    incidencias_admin.js
    ------------------------
    Módulo encargado de:
    - Renderizar tarjetas de incidencias
*/

/* -------------------------------------------------------------------------- */
/*                       Cargar Incidencias desde el Backend                  */
/* -------------------------------------------------------------------------- */

/**
 * @brief Obtiene incidencias desde el backend.
 */
async function cargarIncidencias() {
    try {
        const response = await fetch("/v1/system/incidents", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const incidencias = await response.json();;

        renderIncidents(incidencias);

    } catch (error) {
        console.log("Error al cargar incidencias:", error);
    }
}

/* -------------------------------------------------------------------------- */
/*                          Funciones de Renderizado                          */
/* -------------------------------------------------------------------------- */

function tarjetaIncident(incident) {
    return `
            <h3>${incident.SUBJECT}</h3>
            <p>${incident.DESCRIPTION}</p>
    `;
}

function renderIncidents(incidents) {
    const container = document.getElementById("scroll-incidencias");
    container.innerHTML = "";

    incidents.forEach(incident => {
        const card = document.createElement("div");
        card.className = "incident-card";
        card.innerHTML += tarjetaIncident(incident);
        container.appendChild(card);
    });
}
