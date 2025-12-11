/**
 * @brief Evalúa la calidad del aire a partir de 24 valores de O3 y da tips si hay picos peligrosos.
 * @param {Array<number>} hourlyValues Array de 24 valores de O3.
 * @param {string} elementId ID del elemento HTML donde mostrar el resultado.
 */
function evaluateAirQuality(hourlyValues, elementId) {
    if (!hourlyValues || hourlyValues.length === 0) return;

    const textElement = document.getElementById(elementId);
    if (!textElement) return;

    // Calcular la media de los valores
    const sum = hourlyValues.reduce((acc, val) => acc + val, 0);
    const average = sum / hourlyValues.length;

    let quality;
    if (average > 180) {
        quality = "Malo";
    } else if (average >= 120) {
        quality = "Mejorable";
    } else {
        quality = "Bueno";
    }

    // Detectar todas las horas con picos peligrosos
    const peakHours = hourlyValues
        .map((val, i) => ({ val, hour: i }))
        .filter(item => item.val > 180)
        .map(item => item.hour + ":00");

    // Crear tip único si hay picos
    let tipText = "";
    if (peakHours.length) {
        tipText = `pero recomendamos evitar los lugares en los que estuviste alrededor de las horas: ${peakHours.join(", ")}`;
    }

    textElement.textContent = `Calidad del aire: ${quality}` + (tipText ? ",  " + tipText : "");
}
