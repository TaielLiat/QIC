var vacio = "None";
var disponible = "disponible";
var ocupado = "ocupado";
var no_disponible = "no disponible";
var clientes = document.querySelectorAll(".cliente");
var seña = document.querySelectorAll(".seña");
var estado = document.querySelectorAll(".cartauwu");
var vacios = document.getElementsByTagName("dato");




Array.from(clientes).forEach(e => {
    if (e.textContent.includes(vacio)) {
        e.textContent = "";
    }
})

Array.from(seña).forEach(e => {
    if (e.textContent.includes(vacio)) {
        e.textContent = "";
        e.setAttribute('style', 'margin-bottom: 35%');
    }
})

Array.from(estado).forEach(e => {
    if (e.textContent.includes(no_disponible)) {
        e.classList.add('mesa-no-disponible');
        e.classList.add('cartuwu');
    } else if (e.textContent.includes(disponible)) {
        e.classList.add('mesa-libre');
        e.classList.add('cartuwu');
    } else if (e.textContent.includes(ocupado)) {
        e.classList.add('mesa-ocupada');
    }
})

Array.from(vacios).forEach(e => {
    if (e.textContent.includes("None")) {
        e.textContent = "-";
    }
})

function confirmar() {
    alert('¿Estás seguro de que deseas crear una nueva mesa?');
}

function cambiarEstado() {
    checkbox = document.getElementById("estado");
    valor = document.getElementById("estado_mesa");
    if (checkbox.checked) {
        checkbox.textContent = "Disponible";
        valor.value = "disponible";
        checkbox.checked = false;
    } else {
        checkbox.textContent = "Ocupado"
        valor.value = "ocupado";
        checkbox.checked = true;
    }
}

function verContrasenia() {
    var tipo = document.getElementById("pass");
    if (tipo.type == "password") {
        tipo.type = "text";
    } else {
        tipo.type = "password";
    }
}

function openCreationForm() {
    document.getElementById("crear_mesa").style.display = "block";
}

function closeCreationForm() {
    document.getElementById("crear_mesa").style.display = "none";
}

function getMesas() {
    var cantidad_mesas;
    var list = document.getElementsByClassName("card-title");
    for (var i = 1; i <= list.length; i++) {
        cantidad_mesas = i;
    }
    console.log(cantidad_mesas);
    document.getElementById("creacion_mesa").value = (cantidad_mesas + 1);
    document.getElementById("creacion_mesa").innerHTML = (cantidad_mesas + 1);
}

function openModifyForm() {
    document.getElementById("editar_mesa").style.display = "block";
}

function closeModifyForm() {
    document.getElementById("editar_mesa").style.display = "none";
}

function openDeleteForm() {
    document.getElementById("borrar_mesa").style.display = "block";
}

function closeDeleteForm() {
    document.getElementById("borrar_mesa").style.display = "none";
}

let options
let i = 1;
while (i <= 50) {
    options += "<option>" + i + "<option>";
    i++;
}
document.getElementById("loop").innerHTML = options;

/* SEARCH
const searchInput = document.querySelector("[busqueda-datos]").style.display = "background-color: red"

let empleados = document.querySelectorAll("nombre")
searchInput.addEventListener("input", e => {
    const value = e.target.value.toLowerCase()
    empleados.forEach(empleado => {
        const visible =
            empleado.toLowerCase().includes(value)
        document.querySelector("[lista-datos]").style.display = "none";
        empleado.element.classList.toggle("hide", !visible)
    })
})

FORMATEAR MONEDA LOCAL 
onBlur="toFinalNumberFormat(this)"
function toFinalNumberFormat(controlToCheck) {
    var enteredNumber = '' + controlToCheck.value;
    enteredNumber = enteredNumber.replace(/[^0-9\.]+/g, '');
    controlToCheck.value = Number(enteredNumber).toLocaleString('es-AR', { style: 'currency', currency: 'ARS' });
}

*/