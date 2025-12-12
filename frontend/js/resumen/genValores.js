/**
 * @file genValores.js
 * @brief Genera valores ficticios de O3 más realistas siguiendo los umbrales.
 */

/**
 * @brief Genera 24 valores de O3 para cada hora del día.
 * @return {Array<number>} Array de 24 valores de O3.
 */
function generateFictitiousO3Values() {
    const values = [];

    for (let i = 0; i < 24; i++) {
        let val;
        const rand = Math.random();

        if (rand < 0.05) {
            // Caso peligroso >180 (5%)
            val = 180 + Math.random()*30; // un poco de variación
        } else if (rand < 0.30) {
            // Caso moderado 120-180 (25%)
            val = 120 + Math.random()*60;
        } else {
            // Caso bueno <120 (70%)
            val = 50 + Math.random()*70; // 50-120, más realista
        }

        values.push(Math.round(val*100)/100); // Redondeo a 2 decimales
    }

    return values;
}

/**
 * @brief Configura el botón para generar valores ficticios de O3.
 * @param {string} buttonId ID del botón HTML.
 */
function setupFictitiousButton(buttonId) {
    const button = document.getElementById(buttonId);
    if (!button) return;

    button.addEventListener('click', () => {
        const values = generateFictitiousO3Values();
        updateChart(values);
        evaluateAirQuality(values, 'airQualityText'); // actualizar texto
    });
}
