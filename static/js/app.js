const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');
const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
const datosRegistro = new Array();
const login = document.getElementById('login');

const expresiones = {
	usuarioycontra: /^[a-zA-Z0-9_-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombreyapellidos: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
}

const campos = {
	usuario: false,
	nombre: false,
	apellidos: false,
	password: false,
}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "usuario":
			validarCampo(expresiones.usuarioycontra, e.target, 'usuario');
		break;
		case "nombre":
			validarCampo(expresiones.nombreyapellidos, e.target, 'nombre');
		break;
		case "apellidos":
			validarCampo(expresiones.nombreyapellidos, e.target, 'apellidos');
		break;
		case "password":
			validarCampo(expresiones.usuarioycontra, e.target, 'password');
		break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		// Si esta bien
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i.formulario__validacion-estado`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i.formulario__validacion-estado`).classList.remove('fa-times-circle');
		datosRegistro[campo] = input.value;
		campos[campo] = true;
	} else if (input.value !== '' && !(expresion.test(input.value))) {
		var wrapper = document.createElement('div'); 
		wrapper.innerHTML = '<div class="alert alert-warning alert-dismissible" role="alert">' + 'Carácteres no permitidos' + '<button type="button" id="btn-close" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' + '</div>';
		alertPlaceholder.append(wrapper);
		document.querySelector(`#grupo__${campo} i.formulario__validacion-estado`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i.formulario__validacion-estado`).classList.remove('fa-check-circle');
		campos[campo] = false;
	} 
	else {
		// Si esta mal
		document.querySelector(`#grupo__${campo} i.formulario__validacion-estado`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i.formulario__validacion-estado`).classList.remove('fa-check-circle');
		campos[campo] = false;
	}
}

inputs.forEach((input) => {
	input.addEventListener('blur', validarFormulario);
});

formulario.addEventListener('submit', (e) => {
	e.preventDefault();
	if(campos.usuario && campos.nombre && campos.password && campos.apellidos){
		formulario.reset();
		// Te lleva a la pagina principal porque no hay base de datos para registrar ni comprobar datos xd
		let wrapper = document.createElement('div');
		wrapper.innerHTML = '<div class="alert alert-success alert-dismissible" role="alert">' + 'Bienvenido: ' + datosRegistro.usuario + '<button type="button" id="btn-close" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +'</div>';
		alertPlaceholder.append(wrapper);
		setTimeout( function() { window.location.href = "programas" }, 3000 );
	}
});

login.addEventListener('click', (e) => {
	e.preventDefault();
	if(campos.usuario && campos.password){
		formulario.reset();
		// Te lleva a la pagina principal porque no hay base de datos para registrar ni comprobar datos
		let wrapper = document.createElement('div');
		wrapper.innerHTML = '<div class="alert alert-success alert-dismissible" role="alert">' + 'Bienvenido: ' + datosRegistro.usuario + '<button type="button" id="btn-close" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +'</div>';
		alertPlaceholder.append(wrapper);
		setTimeout( function() { window.location.href = "programas" }, 3000 );
	}
});