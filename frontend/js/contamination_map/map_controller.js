/**
 * @file map_controller.js
 * @brief Funciones con controles de mapa, como filtro por fecha y gas
 * @copyright Copyright (c) 2025, OxiGo.
 * @date 2025-12-10
 * @author Fedor Tikhomirov
 */


/**
 * @brief Obtiene la fecha seleccionada del selector de fecha.
 * @returns {string} Fecha en formato YYYY-MM-DD.
 */
function getSelectedDate() {
    const dateInput = document.getElementById('date-selector');
    return dateInput ? dateInput.value : null;
}


/**
 * @brief Obtiene el tipo de gas seleccionado del selector de gases.
 * @returns {string|null} Tipo de gas seleccionado o null si no hay selección.
 */
function getSelectedGas() {
    const gasSelect = document.getElementById('gas-selector');
    return gasSelect ? gasSelect.value : null;
}


/**
 * @brief Inicializa los selectores de fecha y gas con valores por defecto.
 */
function initializeSelectors() {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const dateInput = document.getElementById('date-selector');
    if (dateInput) dateInput.value = `${yyyy}-${mm}-${dd}`;

    const gasSelect = document.getElementById('gas-selector');
    if (gasSelect) gasSelect.value = 'general';
}


/**
 * @brief Regenera el mapa con los filtros actuales de fecha y gas.
 */
function updateMap() {
    const dateStr = getSelectedDate();
    const gasType = getSelectedGas();
    if (!dateStr || !gasType) {
        console.warn('Fecha o tipo de gas no seleccionados');
        return;
    }

    generateMap({ dateStr, gasType });
}


/**
 * @brief Configura los eventos de los selectores para actualizar el mapa al cambiar.
 */
function setupSelectorEvents() {
    const dateInput = document.getElementById('date-selector');
    const gasSelect = document.getElementById('gas-selector');

    if (dateInput) dateInput.addEventListener('change', updateMap);
    if (gasSelect) gasSelect.addEventListener('change', updateMap);
}

function applyRoleRestrictions() {
    const role = getUserRole();
    const dateInput = document.getElementById('date-selector');

    if (dateInput && role != "Administrador") {
        dateInput.style.display = "none";
    }
}

/**
 * @brief Inicializa el módulo de control del mapa.
 */
function initMapController() {
    initializeSelectors();
    applyRoleRestrictions();
    setupSelectorEvents();
    updateMap();
}

// Inicialización automática
initMapController();