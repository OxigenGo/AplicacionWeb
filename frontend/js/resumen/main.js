document.addEventListener("DOMContentLoaded", () => {
    // Inicializar gráfica vacía con 24 horas
    initChart('medicionesChart');

    // Hacer POST al endpoint para obtener mediciones
    fetch('/v1/data/today', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: getUserId() }) // Cambiar según usuario
    })
    .then(response => response.json())
    .then(data => {
        if (data && Array.isArray(data.mediciones)) {
            const hourlyO3 = Array(24).fill(0); // 24 horas

            // Procesar solo O3
            data.mediciones.forEach(m => {
                if (m.GAS_TYPE === "O3") {
                    const date = new Date(m.DATE);
                    const hour = date.getHours();
                    hourlyO3[hour] = m.GAS_VALUE;
                }
            });

            // Actualizar la gráfica
            updateChart(hourlyO3);
            evaluateAirQuality(hourlyO3, 'airQualityText');

        } else {
            console.warn("No se recibieron mediciones del endpoint.");
        }
    })
    .catch(error => console.error("Error al obtener las mediciones:", error));

    // Botón para generar valores ficticios
    setupFictitiousButton('generarFicticios');
});
