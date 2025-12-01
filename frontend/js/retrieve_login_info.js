/**-----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
//-----------------------------------
//   @file retrieve_login_info.js
//   @author Fédor Tikhomirov
//   @date 2025-11-02
//   @brief Funciones auxiliares para recuperar la cookie con los datos de inicio de sesión.
//-----------------------------------

/**
 * @brief Obtiene el valor de una cookie por su nombre.
 *
 * Busca entre todas las cookies del navegador y devuelve el valor decodificado
 * y parseado como JSON si existe.
 *
 * @param {string} name Nombre de la cookie a buscar.
 * @return {Object|null} Contenido de la cookie como objeto JSON, o null si no existe o no pudo decodificarse.
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
 * @brief Verifica si la sesión del usuario está iniciada.
 *
 * Comprueba si existe una cookie válida llamada `user_data`.
 *
 * @return {boolean} true si existe la cookie, false en caso contrario.
 */
function isUserLoggedIn() {
    return getCookie("user_data") !== null;
}

/**
 * @brief Obtiene el rol del usuario desde la cookie.
 *
 * Extrae el campo `role` dentro de la cookie `user_data` y verifica
 * si es "Usuario" o "Administrador".
 *
 * @return {string|null} El rol del usuario ("Usuario", "Administrador") o null si no existe o no es válido.
 */
function getUserRole() {
    const data = getCookie("user_data");

    if (!data || !data.role) return null;

    const role = data.role;

    if (role === "Usuario" || role === "Administrador") {
        return role;
    }

    return null;
}
