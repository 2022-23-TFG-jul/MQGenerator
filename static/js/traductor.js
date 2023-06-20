$(document).ready(function() {
    // Obtener el idioma almacenado en localStorage o establecer el idioma predeterminado como 'es'
    var idioma = localStorage.getItem('idioma') || 'es';
    // Función para cambiar el idioma
    function cambiarIdioma(idioma) {
        $.getJSON('/static/lang/' + idioma + '.json', function(data) {
            $('[data-i18n]').each(function() {
                var clave = $(this).attr('data-i18n');
            $(this).text(data[clave]);
            });
        });
        // Cambiar la imagen de ejemplo según el idioma seleccionado
        if (idioma === 'es') {
            $('#imagenEjemplo').attr('src', 'static/img/EjemploTabla.png');
            $('#imagenEjemploV').attr('src', 'static/img/EjemploValor.jpg');
            $('#imagenEjemploP').attr('src', 'static/img/EjemploPrograma.png');
        } else if (idioma === 'en') {
            $('#imagenEjemplo').attr('src', 'static/img/ExampleTabla.png');
            $('#imagenEjemploV').attr('src', 'static/img/ExampleValor.png');
            $('#imagenEjemploP').attr('src', 'static/img/ExamplePrograma.png');
        }
    } 
    // Asignar el idioma seleccionado al cargar la página
    cambiarIdioma(idioma); 
    // Manejar el evento de clic en el botón de idioma español
    $('#espana').click(function() {
        idioma = 'es';
        localStorage.setItem('idioma', idioma);
        cambiarIdioma(idioma);
    });  
    // Manejar el evento de clic en el botón de idioma inglés
    $('#ingles').click(function() {
        idioma = 'en';
        localStorage.setItem('idioma', idioma);
        cambiarIdioma(idioma);
    });
});
  