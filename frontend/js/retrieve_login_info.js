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
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const index = cookie.indexOf('=');
        if (index === -1) continue;

        const key = cookie.slice(0, index);
        let value = cookie.slice(index + 1);

        if (key === name) {
            if (value.startsWith('"') && value.endsWith('"')) {
                value = value.slice(1, -1);
            }

            try {
                const decoded = atob(value);
                return JSON.parse(decoded);
            } catch (e) {
                console.error("Error al decodificar cookie:", e);
                return null;
            }
        }
    }
    return null;
}


/**
 * Verifica si hay sesión iniciada
 */
function isUserLoggedIn() {
    return getCookie("user_data") !== null;
}
