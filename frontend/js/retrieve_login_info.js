//-----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
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
    console.log(value);
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        let raw = parts.pop().split(';').shift();

        if (raw.startsWith('"') && raw.endsWith('"')) {
            raw = raw.slice(1, -1);
        }

        try {
            const decoded = atob(raw);
            return JSON.parse(decoded);
        } catch (e) {
            console.error("Error al decodificar cookie:", e);
            return raw;
        }
    }
    return null;
}



/**
 * Recupera los datos del usuario desde la cookie "user_data"
 */
function getLoginInfo() {
    try {
        const cookie = getCookie("user_data");
        if (!cookie){
            console.error("No hay cookie user_data")
            return null;
        }
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
