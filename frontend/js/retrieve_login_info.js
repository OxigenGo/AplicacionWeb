//-----------------------------------
//   © 2025 AirChecker. Todos los derechos reservados.
//-----------------------------------
//   Autor: Fédor Tikhomirov
//   Fecha: 2 de noviembre de 2025
//-----------------------------------
//   Fichero: retrieve_login_info.js
//   Descripción: Funciones auxiliares para recuperar la cookie con los datos de inicio de sesión
//-----------------------------------

/**
 * Obtiene el valor de una cookie por nombre
 * @param {string} name - Nombre de la cookie
 * @returns {string|null} - Valor de la cookie o null si no existe
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Recupera y analiza los datos del usuario desde la cookie "user_data"
 * @returns {object|null} - Objeto con { id, username, email } o null si no existe / es inválido
 */
function getLoginInfo() {
    try {
        const cookie = getCookie("user_data");
        if (!cookie) return null;

        const userData = JSON.parse(cookie);

        if (userData && userData.id && userData.username && userData.email) {
            return userData;
        }

        return null; // En caso de malformación o fallo
    } catch (err) {
        console.error("Error al leer la cookie de usuario:", err);
        return null;
    }
}

/**
 * Verifica si hay una sesión iniciada
 * @returns {boolean} - true si hay cookie válida, false si no
 */
function isUserLoggedIn() {
    return getLoginInfo() !== null;
}

// Exportar funciones
export { getCookie, getLoginInfo, isUserLoggedIn };