/* 
    rewards.js
    ------------------------
    Módulo encargado de:
    - Renderizar tarjetas de recompensas
    - Filtrar por reclamadas o no
*/

/** Lista completa de recompensas cargadas desde el servidor */
let recompensasCargadas = [];

/** Valor del filtro de reclamadas o no (0 = sin filtro) */
let filtro = 0;

/* -------------------------------------------------------------------------- */
/*                               Funciones Utils                              */
/* -------------------------------------------------------------------------- */

function isClaimed(recompensas) {
    recompensas.forEach(recompensa => {
        if (recompensa.STATE === "CLAIMED") {
            return true
        } else {
            return false;
        }
    });
}

function claimReward(rewardId) {
    try{
        fetch("/v1/rewards/claim", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ reward_id: rewardId, user_id: getUserId() })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        aplicarFiltros();

    } catch (error) {
        console.log("Error al cargar recompensas:", error);
    }
}

/* -------------------------------------------------------------------------- */
/*                          Funciones de Renderizado                          */
/* -------------------------------------------------------------------------- */

/**
 * @brief Genera el HTML para una tarjeta de recompensa.
 * @param recompensa Objeto recompensa (ID, ASSOCIATED_USER, STATE)
 * @return HTML con información formateada.
 */
function tarjetaRecompensa(recompensa, reward_state) {
    if(reward_state) {
        return `
        <div class="reward-info" id="claimed-reward">
            <p>Id de la recompensa: ${recompensa.ID}</p>
            <p>Estado: <strong>${recompensa.STATE}</strong></p>
        </div>
        <div class="reward-description">
            <p>Descripcion: ${recompensa.DESCRIPTION}</p>
        </div>
        `;
    }else{
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
    //Hacer que en vez de que salga el id del usuario salga el nombre.
}

/**
 * @brief Renderiza una lista de recompensas en pantalla.
 * @param recompensas Lista de recompensas filtradas o completas.
 */
function renderRecompensas(recompensas) {
    const contenedor = document.getElementById("lista-reward");
    contenedor.innerHTML = "";


    recompensas.forEach(recompensa => {
        const reward_state = isClaimed(recompensa);
        const card = document.createElement("div");
        card.className = "reward-card";
        card.innerHTML += tarjetaRecompensa(recompensa, reward_state);
        contenedor.appendChild(card);
    });
}

/* -------------------------------------------------------------------------- */
/*                            Funciones de Filtros                             */
/* -------------------------------------------------------------------------- */

/**
 * @brief Cambia el filtro de inactividad y vuelve a aplicar todos los filtros.
 * @param dias Cantidad mínima de días inactivo.
 */
function cambiarFiltroReward(reclamo) {
    filtro = reclamo;
    aplicarFiltros();
}

/**
 * @brief Aplica todos los filtros: UUID, usuario asociado y antigüedad.
 * Renderiza la lista resultante.
 */
function aplicarFiltros() {

    let filtrados = recompensasCargadas.filter(recompensa => {
        // --- Filtrar por reclamo ---
        if (filtro > 0) {
            if (filtro === 1 && recompensa.STATE == "CLAIMED") return false;
            if (filtro === 2 && recompensa.STATE == "UNCLAIMED") return false;
        }

        return true;
    });

    renderRecompensas(filtrados);
}

/* -------------------------------------------------------------------------- */
/*                       Cargar Recompensas desde el Backend                  */
/* -------------------------------------------------------------------------- */

/**
 * @brief Obtiene recompensas desde el backend y las almacena para filtrado.
 */
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


//Chapuza
document.getElementById("reclamadas").addEventListener("click", function() {
    this.classList.toggle("activo");
});

document.getElementById("no-reclamadas").addEventListener("click", function() {
    this.classList.toggle("activo");
});


/* -------------------------------------------------------------------------- */
/*                               Ejecución Inicial                            */
/* -------------------------------------------------------------------------- */

// renderRecompensa(reward_prueba); // datos de prueba mientras carga
cargarRecompensas();
