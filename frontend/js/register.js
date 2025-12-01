//-----------------------------------
//   © 2025 OxiGo. Todos los derechos reservados.
//-----------------------------------
//   Autor: Adrián Jáuregui Felipe
//   Fecha: 28 de octubre de 2025
//-----------------------------------
//   Fichero: register.js
//   Descripción: Este fichero envia los datos de registro a la API
//-----------------------------------

const form = document.getElementById("registerForm");
const messageDiv = document.getElementById("error-message-form");
const closebutton = document.getElementById("close-error");
const codeMessage = document.getElementById("body-code");

let registeredEmail = null;

//const number_inputs = 5;

//HandleRegister se encarga de enviar los datos del formulario a la API
async function handleRegister(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirm_password = document.getElementById("password-confirm").value;
    const termsChecked = document.getElementById("checkbox-terms").checked;

//----------------- Validaciones de los datos del formulario -----------------
    if (!username || !email || !password || !confirm_password) {
        console.log("Entra")
        showError("Por favor, completa todos los campos.");
        return;
    }

    if (password !== confirm_password) {
        showError("Las contraseñas no coinciden.");
        return;
    }

    if (!isPasswordSecure(password)) {
        showError("La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un carácter especial.");
        return;
    }

    if (!termsChecked) {
        showError("Debes aceptar los términos y condiciones.");
        return;
    }
//-----------------------------------------------------------------------------

    //Envía los datos a la API
    try {

        const response = await fetch("/v2/register/request", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        //Si el registro es exitoso
        if (response.ok) {
            registeredEmail = email;
            codeMessage.style.display = "flex";

            //No se si hay que pasar por aqui para poner el codigo sin que guarde el usuario en la BBDD o eso se puede cortar o eliminar de alguna manera
            //TODO - Redirigir a página de registro exitoso
        } else {
            //Si el registro falla
            if (data.detail) {
                //Si hay varios errores, los une en un string y los muestra
                if (Array.isArray(data.detail)) {
                    messageDiv.textContent = data.detail.map(d => d.msg).join(", ");
                } else {
                    //Si solo hay un error, lo muestra directamente
                    messageDiv.textContent = data.detail;
                }
            } else {
                messageDiv.textContent = "Error al registrar usuario";
            }
        }
        //Si hay un error de conexión
    } catch (error) {
        messageDiv.textContent = "Error de conexión con el servidor.";
        messageDiv.style.color = "red";
        console.error(error);
    }

}

//---------------------EventListener de los inputs (Codigo de verificacion)-----------------------------------------------//
//Al cargar la página añade un eventListener para recoger todos los inputs del codigo de verificacion
document.addEventListener('DOMContentLoaded', () => {
    // Coge todos los inputs con la clase .code-input
    const inputs = document.querySelectorAll('.code-input');
    const errorCodeDiv = document.getElementById("code-error"); 

    //Guarda en la variable inputs todos los inputs y sus valores de la pagina
    inputs.forEach((input, index) => {
        //Añade un eventlistener para que escuche al escribir en el input
        input.addEventListener('input', async () => {

            //Se asegura de que solo se pongan numeros
            input.value = input.value.replace(/[^0-9]/g, '');

            //Pasa al siguiente input si el actual está lleno
            if (input.value.length === 1) {

            // Busca el siguiente input en la lista
            const nextInput = inputs[index + 1];
            if (nextInput) {
                nextInput.focus(); // Mueve el cursor al siguiente input
            }
            }

            if(index == inputs.length - 1){
                const code = getFullCode(inputs);
                if(code.length !== 6){
                    errorCodeDiv.textContent = "Por favor, no has introducido el código bien";
                    return;
                }
                try{
                    const response = await fetch("/v2/register/verify", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json" 
                        },
                        body: JSON.stringify({ email: registeredEmail, code})
                    });

                    const result = await response.json();
                    if(response.ok){
                        window.location.href = "../login.html";
                    } else { 
                        errorCodeDiv.textContent = result.message || "El código es incorrecto.";
                    }
                } catch(error){
                    console.log("Error al verificar el código " + error);
                    errorCodeDiv.textContent = 'Error de conexión. Inténtelo de nuevo.'
                }
            }
        });

        // Añade un eventlistener para escuchar si la tecla Backspace ha sido pulsada
        input.addEventListener('keydown', (e) => {
            // Si se presiona Backspace y el campo está vacío
            if (e.key === 'Backspace' && input.value === '') {
        
                // Busca el input anterior
                const prevInput = inputs[index - 1];
                if (prevInput) {
                    prevInput.focus(); // Mueve el cursor al input anterior
                }
            }
        });
    });
});
//----------------------------------------------------------------------------------------------------

//Muestra el contenedor de error con el mensaje pasado
function showError(message){
    messageDiv.textContent = message;
}

function getFullCode(inputs){
    let code = '';
    inputs.forEach(input => {
        code += input.value;
    })
    return code;
}

if(isUserLoggedIn() == true){
    window.location.href = "../edit_user.html"
}

//Al hacer el submit ejecuta la función de registro
form.addEventListener("submit", handleRegister);