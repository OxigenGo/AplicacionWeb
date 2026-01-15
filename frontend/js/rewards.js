/* 
    rewards.js
    ------------------------
    Módulo encargado de:
    - Renderizar tarjetas de recompensas
    - Filtrar por reclamadas o no
*/

/** Lista completa de recompensas cargadas desde el servidor */
let recompensasCargadas = [];

/** Valor del filtro de reclamadas o no (0 = sin filtro, 1 = solo reclamadas, 2 = solo no reclamadas) */
let filtro = 0;

/* -------------------------------------------------------------------------- */
/*                               Funciones Utils                              */
/* -------------------------------------------------------------------------- */

function isClaimed(recompensa) {
    return recompensa.STATE === "CLAIMED";
}

async function claimReward(rewardId) {
    try {
        const response = await fetch("/v1/rewards/claim", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ 
                reward_id: rewardId, 
                user_id: getUserId() 
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Recargar recompensas después de reclamar
        await cargarRecompensas();

    } catch (error) {
        console.log("Error al reclamar recompensa:", error);
    }
}

/* -------------------------------------------------------------------------- */
/*                          Funciones de Renderizado                          */
/* -------------------------------------------------------------------------- */

/**
 * @brief Genera el HTML para una tarjeta de recompensa.
 * @param recompensa Objeto recompensa (ID, ASSOCIATED_USER, STATE, DESCRIPTION)
 * @param reward_state true si está reclamada
 */
function tarjetaRecompensa(recompensa, reward_state) {
    if (reward_state) {
        return `
        <div class="reward-info" id="claimed-reward">
            <p>Id de la recompensa: ${recompensa.ID}</p>
            <p>Estado: <strong>${recompensa.STATE}</strong></p>
        </div>
        <div class="reward-description">
            <p>Descripcion: ${recompensa.DESCRIPTION}</p>
        </div>
        `;
    } else {
        return `
        <div class="reward-info" id="unclaimed-reward">
            <p>Id de la recompensa: ${recompensa.ID}</p>
            <p>Estado: <strong>${recompensa.STATE}</strong></p>
        </div>
        <div class="reward-description">
            <p>Descripcion: ${recompensa.DESCRIPTION}</p>
        </div>
        <button class="claim-button" onclick="claimReward('${recompensa.ID}')">Reclamar</button>
        `;
    }
}

/**
 * @brief Renderiza una lista de recompensas en pantalla.
 */
function renderRecompensas(recompensas) {
    const contenedor = document.getElementById("lista-reward");
    contenedor.innerHTML = "";

    recompensas.forEach(recompensa => {
        const reward_state = isClaimed(recompensa);
        const card = document.createElement("div");
        card.className = "reward-card";
        card.innerHTML = tarjetaRecompensa(recompensa, reward_state);
        contenedor.appendChild(card);
    });
}

/* -------------------------------------------------------------------------- */
/*                            Funciones de Filtros                             */
/* -------------------------------------------------------------------------- */

function cambiarFiltroReward(reclamo) {
    filtro = reclamo;
    aplicarFiltros();
}

function aplicarFiltros() {
    let filtrados = recompensasCargadas.filter(recompensa => {
        if (filtro === 1 && recompensa.STATE !== "CLAIMED") return false;
        if (filtro === 2 && recompensa.STATE !== "UNCLAIMED") return false;
        return true;
    });

    renderRecompensas(filtrados);
}

/* -------------------------------------------------------------------------- */
/*                       Cargar Recompensas desde el Backend                  */
/* -------------------------------------------------------------------------- */

async function cargarRecompensas() {
    try {
        const response = await fetch("/v1/rewards", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ user_id: getUserId() })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        recompensasCargadas = data.rewards;

        aplicarFiltros();

    } catch (error) {
        console.log("Error al cargar recompensas:", error);
    }
}

/* -------------------------------------------------------------------------- */
/*                               Eventos UI                                   */
/* -------------------------------------------------------------------------- */

document.getElementById("reclamadas").addEventListener("click", function () {
    cambiarFiltroReward(1);
});

document.getElementById("no-reclamadas").addEventListener("click", function () {
    cambiarFiltroReward(2);
});

/* -------------------------------------------------------------------------- */
/*                               Ejecución Inicial                            */
/* -------------------------------------------------------------------------- */

cargarRecompensas();
