/* 
    incidencias_admin.js
    ------------------------
    Módulo encargado de:
    - Renderizar tarjetas de incidencias
*/

//Variables Globales
let incidenciasCargadas = [];
let incidenciaSeleccionada = null;

//Text Content Elements
const titulo = document.getElementById("title");
const createDate = document.getElementById("create-date");
const updateDate = document.getElementById("update-date");
const descripcion = document.getElementById("description");
const estado = document.getElementById("status");

//Botones
const botonSolucionar = document.getElementById("sol-button");
const botonRechazar = document.getElementById("reject-button");


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
        cargarIncidenciasDetalles(incidencias[0]);

    } catch (error) {
        console.log("Error al cargar incidencias:", error);
    }
}

/* -------------------------------------------------------------------------- */
/*                          Funciones de Renderizado                          */
/* -------------------------------------------------------------------------- */

/**
 * @brief Hace una tarjeta del scrollbar con el titulo y una previsualizacion de la descripción.
 */
function tarjetaIncident(incident) {
    return `
            <h3>${incident.SUBJECT}</h3>
            <p>${incident.DESCRIPTION}</p>
    `;
}

/**
 * @brief Renderiza las tarjetas de incidencias y pone un evento click para actualizar la tarjeta grande.
 */
function renderIncidents(incidents) {
    const container = document.getElementById("scroll-incidencias");
    container.innerHTML = "";

    incidents.forEach(incident => {
        const card = document.createElement("div");
        card.className = "incident-card";
        card.innerHTML += tarjetaIncident(incident);
        container.appendChild(card);

        card.addEventListener("click", function() {
            document.querySelectorAll('.incident-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            incidenciaSeleccionada = incident;
            cargarIncidenciasDetalles(incidenciaSeleccionada);
        });
    });
}

/**
 * @brief Carga los detalles de la incidencia seleccionada en la tarjeta grande.
 */
function cargarIncidenciasDetalles(incident) {
    titulo.textContent = incident.SUBJECT;
    descripcion.textContent = incident.DESCRIPTION;
    estado.textContent = incident.STATE;
    createDate.textContent = incident.CREATED_AT;
    updateDate.textContent = incident.UPDATED_AT;
}

/* -------------------------------------------------------------------------- */
/*                     Funcion de Cambio de estado                          */
/* -------------------------------------------------------------------------- */

async function cambiarState(state){
    try {
        const response = await fetch("/v1/system/incidents/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                INCIDENT_ID: incidenciaSeleccionada.ID,
                STATE: state ? "Solucionada" : "Rechazada"
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const incidencias = await response.json();;

        cargarIncidenciasDetalles(incidenciaSeleccionada);

    } catch (error) {
        console.log("Error al cargar incidencias:", error);
    }
}

//Inicializacion de pagina
cargarIncidencias();

