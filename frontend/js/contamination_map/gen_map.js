/**
 * @file gen_map.js
 * @brief Funciones para recibir datos y generar el mapa
 */

const OFFICIAL_STATIONS = [
    { name: "Prat de Cabanes", lat: 40.136944, lon: 0.165556 },
    { name: "Aras de los Olmos", lat: 39.950278, lon: -1.108889 },
    { name: "Valencia", lat: 39.472222, lon: -0.422500 },
    { name: "Denia", lat: 38.821944, lon: 0.035833 },
    { name: "Torrevieja", lat: 38.008333, lon: -0.658611 }
];

let mapInstance = null;
let heatLayer = null;
let officialLayer = null;

/* ================= GEOLOCALIZACIÓN ================= */

function getUserLocation(callback) {
    if (!navigator.geolocation) {
        callback(null, null);
        return;
    }

    navigator.geolocation.getCurrentPosition(
        pos => callback(pos.coords.latitude, pos.coords.longitude),
        () => callback(null, null)
    );
}

/* ================= MAPA ================= */

function createMap(lat, lon, zoomFallback = 6) {
    const map = L.map('map').setView(
        (lat !== null && lon !== null) ? [lat, lon] : [39.5, -0.5],
        (lat !== null && lon !== null) ? 11 : zoomFallback
    );

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap & CARTO',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    return map;
}

/* ================= BACKEND HEATMAP ================= */

async function fetchReadings(dateStr, gasType) {

    if (gasType !== "general") {
        const response = await fetch(`/v1/data/map_readings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ datetime: dateStr, gasType })
        });

        if (!response.ok) throw new Error("HTTP " + response.status);
        const data = await response.json();
        return data.mediciones || [];
    }

    // MODO GENERAL: pedir todos los gases por separado
    const gases = ["o3", "no2", "so2", "co"];
    const results = {};

    for (const g of gases) {
        const resp = await fetch(`/v1/data/map_readings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ datetime: dateStr, gasType: g })
        });

        if (!resp.ok) continue;

        const json = await resp.json();
        for (const m of (json.mediciones || [])) {
            // usamos la posición como clave
            if (!results[m.POSITION]) results[m.POSITION] = {};
            results[m.POSITION][g] = m.GAS_VALUE;
        }
    }

    // Convertimos a estructura unificada
    return Object.entries(results).map(([pos, vals]) => ({
        POSITION: pos,
        o3: vals.o3 || 0,
        no2: vals.no2 || 0,
        so2: vals.so2 || 0,
        co: vals.co || 0
    }));
}


/* ================= OPEN-METEO (igual que Java) ================= */

async function fetchOfficialStationData(st) {
    const url =
        `https://air-quality-api.open-meteo.com/v1/air-quality` +
        `?latitude=${st.lat}&longitude=${st.lon}` +
        `&current=nitrogen_dioxide,ozone,sulphur_dioxide,carbon_monoxide`;

    const resp = await fetch(url);
    if (!resp.ok) throw new Error("Open-Meteo error");

    const json = await resp.json();
    if (!json.current) return null;

    return {
        name: st.name,
        lat: st.lat,
        lon: st.lon,
        o3: json.current.ozone || 0,
        no2: json.current.nitrogen_dioxide || 0,
        so2: json.current.sulphur_dioxide || 0,
        co: json.current.carbon_monoxide || 0
    };
}

/* ================= COLOR POR GAS ================= */

function getColorForGasCategory(category) {
    if (category === "Bueno") return "green";
    if (category === "Regular") return "orange";
    return "red";
}


/* ================= ESTACIONES OFICIALES ================= */

async function loadOfficialStations(map, gasType) {
    officialLayer.clearLayers();

    for (const st of OFFICIAL_STATIONS) {
        try {
            const data = await fetchOfficialStationData(st);
            if (!data) continue;

            let category;

            if (gasType === "general") {
                category = classifyGeneral(data);
            } else {
                category = classifyGas(data[gasType], gasType);
            }

            const popup = `
                <b>${data.name}</b><br>
                O₃: ${classifyGas(data.o3, "o3")}<br>
                NO₂: ${classifyGas(data.no2, "no2")}<br>
                CO: ${classifyGas(data.co, "co")}<br>
                SO₂: ${classifyGas(data.so2, "so2")}
            `;

            L.circleMarker([data.lat, data.lon], {
                radius: 10,
                color: "blue",
                weight: 2,
                fillColor: color,
                fillOpacity: 0.85
            })
                .bindPopup(popup)
                .addTo(officialLayer);

        } catch (e) {
            console.warn("Error estación", st.name, e);
        }
    }
}


/* ================= HEATMAP CONSERVATIVO ================= */

function addHeatmap(map, mediciones, gasType) {
    const maxValues = { o3: 300, co: 50, no2: 200, so2: 150 };
    const maxValue = maxValues[gasType] || 100;
    const BASE_ZOOM = 3;

    function scale() {
        return Math.pow(2, 2 * (map.getZoom() - BASE_ZOOM));
    }

    function build() {
        const s = scale();
        return mediciones.map(m => {
            try {
                const geo = JSON.parse(m.POSITION);
                const [lon, lat] = geo.coordinates;

                let intensity;

                if (gasType === "general") {
                    const cats = [
                        classifyGas(m.o3, "o3"),
                        classifyGas(m.no2, "no2"),
                        classifyGas(m.so2, "so2"),
                        classifyGas(m.co, "co")
                    ];

                    if (cats.includes("Malo")) intensity = 1;
                    else if (cats.includes("Regular")) intensity = 0.6;
                    else intensity = 0.3;
                } else {
                    intensity = m.GAS_VALUE / maxValue;
                }

                return [lat, lon, intensity / s];

            } catch {
                return null;
            }
        }).filter(p => p);
    }

    const layer = L.heatLayer(build(), {
        radius: 75,
        blur: 50,
        gradient: { 0: "green", 0.5: "yellow", 1: "red" }
    }).addTo(map);

    map.on("zoomend", () => layer.setLatLngs(build()));
    return layer;
}

function classifyGas(value, gas) {
    const limits = {
        o3: [60, 120],
        no2: [50, 100],
        so2: [40, 80],
        co: [5, 10]
    };

    const [good, bad] = limits[gas] || [50, 100];

    if (value < good) return "Bueno";
    if (value < bad) return "Regular";
    return "Malo";
}

function classifyGeneral(data) {
    const gases = ["o3", "no2", "so2", "co"];
    let hasRegular = false;

    for (const g of gases) {
        const cat = classifyGas(data[g], g);
        if (cat === "Malo") return "Malo";
        if (cat === "Regular") hasRegular = true;
    }

    return hasRegular ? "Regular" : "Bueno";
}


/* ================= MAIN ================= */

async function generateMap({ dateStr, gasType }) {
    getUserLocation(async (lat, lon) => {
        if (!mapInstance) {
            mapInstance = createMap(lat, lon);
        }

        if (!officialLayer) {
            officialLayer = L.layerGroup().addTo(mapInstance);
        }

        officialLayer.clearLayers();

        if (heatLayer) {
            mapInstance.removeLayer(heatLayer);
        }

        await loadOfficialStations(mapInstance, gasType);

        const data = await fetchReadings(dateStr, gasType);
        heatLayer = addHeatmap(mapInstance, data, gasType);
    });
}