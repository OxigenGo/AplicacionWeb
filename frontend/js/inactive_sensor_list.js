/* 
    inactive_sensor_list.js
    ------------------------
    Módulo encargado de:
    - Renderizar tarjetas de sensores
    - Filtrar por inactividad
    - Filtrar por UUID
    - Filtrar por ID de usuario asociado
    - Ordenar resultados (más antiguo primero)
*/

/** Lista completa de sensores cargados desde el servidor */
let sensoresCargados = [];

/** Valor del filtro de inactividad en días (0 = sin filtro) */
let filtroDias = 0;

/* -------------------------------------------------------------------------- */
/*                               Funciones Utils                              */
/* -------------------------------------------------------------------------- */

/**
 * @brief Calcula cuánto tiempo ha pasado desde la fecha indicada.
 * @param fechaStr Fecha en formato ISO (string).
 * @return Texto del tipo: "hace 3 días", "hace 2 semanas", "hace 1 mes".
 */
function tiempoTranscurrido(fechaStr) {
    const fecha = new Date(fechaStr);
    const ahora = new Date();
    const diffMs = ahora - fecha;

    const dias = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const semanas = Math.floor(dias / 7);
    const meses = Math.floor(dias / 30);

    if (dias < 1) return "hoy";
    if (dias === 1) return "hace 1 día";
    if (dias < 7) return `hace ${dias} días`;
    if (semanas < 5) return `hace ${semanas} semanas`;
    return `hace ${meses} meses`;
}

/* -------------------------------------------------------------------------- */
/*                          Funciones de Renderizado                          */
/* -------------------------------------------------------------------------- */

/**
 * @brief Genera el HTML para una tarjeta de sensor.
 * @param sensor Objeto sensor (UUID, ASSOCIATED_USER, LAST_ACTIVE)
 * @return HTML con información formateada.
 */
function TarjetaSensor(sensor) {
    const tiempo = tiempoTranscurrido(sensor.LAST_ACTIVE);

    const fecha = new Date(sensor.LAST_ACTIVE).toLocaleString("es-ES", {
        dateStyle: "medium",
        timeStyle: "short"
    });

    return `
        <p>Id del sensor: ${sensor.UUID}</p>
        <p>ID Usuario asociado: ${sensor.ASSOCIATED_USER}</p>
        <p>Última actividad:<br>
            <strong>${tiempo}</strong> (${fecha})
        </p>
    `;
}

/**
 * @brief Renderiza una lista de sensores en pantalla.
 * @param sensors Lista de sensores filtrados o completos.
 */
function renderSensores(sensors) {
    const contenedor = document.getElementById("lista-sensores");
    contenedor.innerHTML = "";

    // Ordenar del más antiguo al más reciente
    sensors.sort((a, b) => new Date(a.LAST_ACTIVE) - new Date(b.LAST_ACTIVE));

    sensors.forEach(sensor => {
        const card = document.createElement("div");
        card.className = "sensor-card";
        card.innerHTML += TarjetaSensor(sensor);
        contenedor.appendChild(card);
    });
}

/* -------------------------------------------------------------------------- */
/*                            Funciones de Filtros                             */
/* -------------------------------------------------------------------------- */

/**
 * @brief Cambia el filtro de inactividad y vuelve a aplicar todos los filtros.
 * @param dias Cantidad mínima de días inactivo.
 */
function cambiarFiltroInactividad(dias) {
    filtroDias = dias;
    aplicarFiltros();
}

/**
 * @brief Aplica todos los filtros: UUID, usuario asociado y antigüedad.
 * Renderiza la lista resultante.
 */
function aplicarFiltros() {
    const uuidInput = document.getElementById("busqueda-uuid").value.trim();
    const usuarioInput = document.getElementById("busqueda-usuario").value.trim();

    const ahora = new Date();

    let filtrados = sensoresCargados.filter(sensor => {

        // --- Filtrar por UUID ---
        if (uuidInput && !String(sensor.UUID).includes(uuidInput)) {
            return false;
        }

        // --- Filtrar por ID Usuario asociado (NUMÉRICO) ---
        if (usuarioInput && !String(sensor.ASSOCIATED_USER).includes(usuarioInput)) {
            return false;
        }

        // --- Filtrar por días de inactividad ---
        if (filtroDias > 0) {
            const fecha = new Date(sensor.LAST_ACTIVE);
            const diffDias = Math.floor((ahora - fecha) / (1000 * 60 * 60 * 24));
            if (diffDias < filtroDias) return false;
        }

        return true;
    });

    renderSensores(filtrados);
}

/* -------------------------------------------------------------------------- */
/*                       Cargar Sensores desde el Backend                     */
/* -------------------------------------------------------------------------- */

/**
 * @brief Obtiene sensores desde el backend y los almacena para filtrado.
 */
async function cargarSensores() {
    try {
        const response = await fetch("/v1/data/admin/sensors");
        const data = await response.json();

        sensoresCargados = data.sensors;

        aplicarFiltros(); 

    } catch (error) {
        console.log("Error al cargar sensores:", error);
    }
}

//Chapuza
document.getElementById("day-one").addEventListener("click", function() {
    this.classList.toggle("activo");
});

document.getElementById("week-one").addEventListener("click", function() {
    this.classList.toggle("activo");
});

document.getElementById("month-one").addEventListener("click", function() {
    this.classList.toggle("activo");
});

document.getElementById("month-six").addEventListener("click", function() {
    this.classList.toggle("activo");
});

document.getElementById("show-all").addEventListener("click", function() {
    this.classList.toggle("activo");
});

//Función para actualizar el placeholder del input de búsqueda según el tamaño de la pantalla
function updatePlacholder() {
    const uuidInput = document.getElementById("busqueda-uuid");
    const usuarioInput = document.getElementById("busqueda-usuario");

    if (window.innerWidth < 650) {
        uuidInput.placeholder = "UUID";
        usuarioInput.placeholder = "Usuario";
    } else {
        uuidInput.placeholder = "Buscar por UUID";
        usuarioInput.placeholder = "Buscar por usuario";
    }
}



/* -------------------------------------------------------------------------- */
/*                               Ejecución Inicial                            */
/* -------------------------------------------------------------------------- */

// renderSensores(sensors_prueba); // datos de prueba mientras carga
cargarSensores();
//Para hacer la busqueda responsive
updatePlacholder();
window.addEventListener("resize", updatePlacholder);
