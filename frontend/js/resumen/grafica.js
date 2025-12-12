let medicionesChart = null;

/**
 * @brief Inicializa la gráfica de barras con líneas de umbral.
 * @param {string} canvasId ID del canvas HTML.
 */
function initChart(canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const labels = Array.from({length:24}, (_,i) => i + ':00'); // 24 horas
    const emptyData = Array(24).fill(0);

    medicionesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'O3 (µg/m³)',
                    data: emptyData,
                    backgroundColor: emptyData.map(val => getBarColor(val)),
                    borderColor: emptyData.map(val => getBarColor(val)),
                    borderWidth: 1
                },
                {
                    label: 'Umbral moderado',
                    data: Array(24).fill(120),
                    type: 'line',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 0
                },
                {
                    label: 'Umbral peligro',
                    data: Array(24).fill(180),
                    type: 'line',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 2,
                    fill: false,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'O3 (µg/m³)' } }
            }
        }
    });
}

/**
 * @brief Determina el color de la barra según el valor de O3.
 * @param {number} value Valor de O3
 * @return {string} Color en rgba
 */
function getBarColor(value) {
    if (value < 120) return 'rgba(0, 200, 0, 0.7)';       // Verde
    else if (value < 180) return 'rgba(255, 206, 86, 0.7)'; // Amarillo
    else return 'rgba(255, 99, 132, 0.7)';               // Rojo
}

/**
 * @brief Actualiza la gráfica con nuevos valores de O3 y colores según umbral.
 * @param {Array<number>} hourlyValues Array de 24 valores de O3.
 */
function updateChart(hourlyValues) {
    if (!medicionesChart) {
        console.error("La gráfica no ha sido inicializada.");
        return;
    }
    if (!medicionesChart.data.datasets || medicionesChart.data.datasets.length === 0) {
        console.error("La gráfica no tiene datasets definidos.");
        return;
    }
    if (hourlyValues.length !== 24) {
        console.warn("Se esperan 24 valores para actualizar la gráfica");
    }

    // Actualizar datos y colores de las barras
    medicionesChart.data.datasets[0].data = hourlyValues;
    medicionesChart.data.datasets[0].backgroundColor = hourlyValues.map(getBarColor);
    medicionesChart.data.datasets[0].borderColor = hourlyValues.map(getBarColor);

    medicionesChart.update();
}
