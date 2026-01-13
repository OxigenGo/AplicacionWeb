/**
 * @file gen_map.js
 * @brief Funciones para recibir datos y generar el mapa
 * @copyright Copyright (c) 2025, OxiGo.
 * @date 2025-12-10
 * @author Fedor Tikhomirov
 */


/**
 * @brief Obtiene la ubicación actual del usuario mediante geolocalización.
 * 
 * @param {function} callback Función que recibe (lat, lon). Si falla, recibe (null, null).
 */
function getUserLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => callback(position.coords.latitude, position.coords.longitude),
            (error) => {
                console.warn('No se pudo obtener la ubicación del usuario:', error.message);
                callback(null, null);
            }
        );
    } else {
        console.warn('Geolocalización no soportada por este navegador');
        callback(null, null);
    }
}


/**
 * @brief Crea el mapa base centrado en la posición del usuario o en [0,0].
 * 
 * @param {number|null} lat Latitud del usuario, o null si desconocida.
 * @param {number|null} lon Longitud del usuario, o null si desconocida.
 * @param {number} zoomFallback Zoom usado si no hay ubicación válida. 2 por defecto
 * @return {object} Instancia del mapa Leaflet creada.
 */

function createMap(lat, lon, zoomFallback = 2) {
    const map = L.map('map').setView(
        (lat !== null && lon !== null) ? [lat, lon] : [0, 0],
        (lat !== null && lon !== null) ? 13 : zoomFallback
    );

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    if (lat !== null && lon !== null) {
        L.circle([lat, lon], { radius: 10, color: 'blue' })
            .addTo(map)
            .bindPopup('Tu ubicación actual')
            .openPopup();
    }

    return map;
}


/**
 * @brief Obtiene mediciones del backend filtrando por fecha y tipo de gas.
 * @param {string} dateStr Fecha en formato 'YYYY-MM-DD'.
 * @param {string} gasType Tipo de gas a filtrar (O3, CO, NO2, SO2).
 * @returns {Promise<Array>} Lista de mediciones.
 * @throws {Error} Si hay error HTTP o en la respuesta.
 */
async function fetchReadings(dateStr, gasType) {
    if (!gasType || typeof gasType !== 'string') {
        throw new Error("Debe proporcionar un gasType válido como string");
    }

    const body = { 
        datetime: dateStr,
        gasType: gasType
    };

    const response = await fetch(`/v1/data/map_readings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });

    if (!response.ok) throw new Error(`HTTP error ${response.status}`);

    const data = await response.json();
    if (data.status !== 'ok' || !data.mediciones) return [];

    return data.mediciones;
}


let mapInstance = null;
let heatLayer = null;

/**
 * @brief Genera el mapa y carga mediciones filtradas por fecha y gas.
 * @param {object} params 
 * @param {string} params.dateStr Fecha en formato YYYY-MM-DD.
 * @param {string|null} params.gasType Tipo de gas.
 */
async function generateMap({ dateStr, gasType = null }) {
    getUserLocation(async (userLat, userLon) => {
        if (!mapInstance) {
            mapInstance = createMap(userLat, userLon);
        }

        if (heatLayer) {
            heatLayer.remove();
            heatLayer = null;
        }

        try {
            const mediciones = await fetchReadings(dateStr, gasType);
            heatLayer = addHeatmap(mapInstance, mediciones, gasType);
        } catch (err) {
            console.error('Error al cargar mediciones:', err);
        }
    });
}


/**
 * @brief Añade un heatmap al mapa y devuelve la capa creada.
 * @param {object} map Instancia del mapa Leaflet.
 * @param {Array} mediciones Lista de mediciones.
 * @param {string} gasType Tipo de gas para normalización.
 * @returns {object|null} Capa de heatmap añadida o null si no hay puntos.
 */
function addHeatmap(map, mediciones, gasType) {
    const maxValues = { o3: 300, co: 50, no2: 200, so2: 150 };
    const maxValue = maxValues[gasType] || 100;

    const BASE_ZOOM = 7;   // the zoom where values look correct

    function getZoomScale() {
        const z = map.getZoom();
        return Math.pow(2, 2 * (z - BASE_ZOOM));
    }

    function buildPoints() {
        const scale = getZoomScale();

        return mediciones.map(med => {
            try {
                const geo = JSON.parse(med.POSITION);
                if (geo.type !== "Point") return null;
                const [lon, lat] = geo.coordinates;

                return [
                    lat,
                    lon,
                    (med.GAS_VALUE / maxValue) / scale
                ];
            } catch {
                return null;
            }
        }).filter(p => p !== null);
    }

    let heatPoints = buildPoints();
    if (heatPoints.length === 0) return null;

    const layer = L.heatLayer(heatPoints, {
        radius: 75,
        blur: 50,
        maxZoom: 20,
        gradient: { 0.0: 'green', 0.5: 'yellow', 1.0: 'red' }
    }).addTo(map);

    map.on('zoomend', () => {
        layer.setLatLngs(buildPoints());
    });

    if (map.getZoom() === 2) {
        const latLngs = heatPoints.map(p => [p[0], p[1]]);
        map.fitBounds(latLngs);
    }

    return layer;
}
