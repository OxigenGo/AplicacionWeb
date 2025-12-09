// Función para obtener la ubicación del usuario
function getUserLocation(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => callback(position.coords.latitude, position.coords.longitude),
            (error) => {
                console.warn('No se pudo obtener la ubicación del usuario:', error.message);
                callback(null, null); // devolvemos null si falla
            }
        );
    } else {
        console.warn('Geolocalización no soportada por este navegador');
        callback(null, null);
    }
}

// Función para crear el mapa base
function createMap(lat, lon, zoomFallback = 2) {
    // Si no hay lat/lon válidos, centramos en [0,0] con zoom global
    const map = L.map('map').setView(
        (lat !== null && lon !== null) ? [lat, lon] : [0, 0],
        (lat !== null && lon !== null) ? 13 : zoomFallback
    );

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Solo añadir marcador si lat/lon válidos
    if (lat !== null && lon !== null) {
        L.circle([lat, lon], { radius: 10, color: 'blue' })
            .addTo(map)
            .bindPopup('Tu ubicación actual')
            .openPopup();
    }

    return map;
}

// Función para obtener mediciones desde el backend filtrando por fecha y tipo de gas
async function fetchReadings(dateStr, gasType = null) {
    const body = { datetime: dateStr };
    if (gasType) body.gas_type = gasType;

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

// Función para crear heatmap a partir de mediciones
function addHeatmap(map, mediciones) {
    const maxCO2 = 450; // valor máximo esperado para normalizar
    const heatPoints = mediciones.map(med => {
        try {
            const geo = JSON.parse(med.POSITION);
            if (geo.type !== "Point") return null;
            const [lon, lat] = geo.coordinates;
            return [lat, lon, med.GAS_VALUE / maxCO2]; // normalizado
        } catch (e) {
            return null;
        }
    }).filter(p => p !== null);

    if (heatPoints.length === 0) return;

    L.heatLayer(heatPoints, {
        radius: 25,
        blur: 20,
        maxZoom: 17,
        gradient: {
            0.0: 'green',
            0.85: 'yellow',
            0.95: 'orange',
            1.0: 'red'
        }
    }).addTo(map);

    if (map.getZoom() === 2) {
        const latLngs = heatPoints.map(p => [p[0], p[1]]);
        map.fitBounds(latLngs);
    }
}

// Función principal para inicializar mapa con filtros
async function generateMap({ dateStr, gasType = null }) {
    getUserLocation(async (userLat, userLon) => {
        const map = createMap(userLat, userLon);
        try {
            const mediciones = await fetchReadings(dateStr, gasType);
            addHeatmap(map, mediciones);
        } catch (err) {
            console.error('Error al cargar mediciones:', err);
        }
    });
}

// Llamada con la fecha de hoy
const today = new Date();
const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0');
const dd = String(today.getDate()).padStart(2, '0');
const dateStr = `${yyyy}-${mm}-${dd}`;
generateMap({ dateStr: dateStr, gasType: 'CO2' });