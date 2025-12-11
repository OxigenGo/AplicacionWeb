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

/**
 * @brief Obtiene el ID del usuario desde la cookie `user_data`.
 *
 * @return {number|string|null} El ID del usuario o null si no existe.
 */
function getUserId() {
    const data = getCookie("user_data");
    if (!data || !data.id) return null;
    return data.id;
}

/**
 * @brief Obtiene el nombre de usuario desde la cookie `user_data`.
 *
 * @return {string|null} El nombre de usuario o null si no existe.
 */
function getUsername() {
    const data = getCookie("user_data");
    if (!data || !data.username) return null;
    return data.username;
}

/**
 * @brief Cierra la sesión del usuario.
 *
 * Envía una petición al backend para borrar la cookie y recarga la página.
 */
async function logout() {
    try {
        const response = await fetch("/v1/users/logout", {
            method: "POST"
        });

        if (response.ok) {
            window.location.href = "/index.html"; // Redirigir al inicio
        } else {
            console.error("Error al cerrar sesión");
        }
    } catch (error) {
        console.error("Error de red al cerrar sesión:", error);
    }
}

/**
 * @brief Actualiza los botones del header según el estado de sesión.
 */
function updateHeader() {
    const sesionButtons = document.querySelector(".sesion-buttons");
    if (!sesionButtons) return;

    if (isUserLoggedIn()) {
        // Usuario logueado: Mostrar botón de Cerrar Sesión
        sesionButtons.innerHTML = `
            <button onclick="logout()" class="login-button" style="cursor: pointer;">Cerrar Sesión</button>
        `;
        
        // Opcional: Si quieres mantener el botón de perfil o añadirlo
        // const username = getUsername();
        // if (username) {
        //    // Añadir lógica para mostrar nombre de usuario si se desea
        // }

    } else {
        // Usuario no logueado: Mostrar Registro e Iniciar Sesión (estado original)
        sesionButtons.innerHTML = `
            <a href="./registro.html" class="register-button">Registro</a>
            <a href="./login.html" class="login-button">Iniciar Sesión</a>
        `;
    }
}

// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", updateHeader);
