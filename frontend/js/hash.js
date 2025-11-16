// -----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
// -----------------------------------
//   Autor: Fedor Tikhomirov
//   Fecha: 16 de noviembre 2025
// -----------------------------------
//  Fichero: hash.js
//  Descripción: Funcion auxiliar para hashear contraseñas en el cliente
// -----------------------------------

async function hashPassword(password) {
    // Coste estándar recomendado para frontend
    const saltRounds = 10;

    // Genera el hash
    const hash = await bcrypt.hash(password, saltRounds);

    return hash;
}
