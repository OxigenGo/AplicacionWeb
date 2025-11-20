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
 */
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

/**
 * Recupera los datos del usuario desde la cookie "user_data"
 */
function getLoginInfo() {
    try {
        let cookie = getCookie("user_data");
        if (!cookie) return null;

        if (cookie.startsWith('"') && cookie.endsWith('"')) {
            cookie = cookie.slice(1, -1);
        }

        cookie = cookie.replace(/\\054/g, ',');

        const userData = JSON.parse(cookie);

        if (userData && userData.id && userData.username && userData.email) {
            return userData;
        }

        return null;
    } catch (err) {
        console.error("Error al leer la cookie de usuario:", err);
        return null;
    }
}


/**
 * Verifica si hay sesión iniciada
 */
function isUserLoggedIn() {
    return getLoginInfo() !== null;
}
