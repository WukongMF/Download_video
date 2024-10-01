$(document).ready(function() {
    // Función para obtener el ID de YouTube desde la URL (esto puede seguir existiendo para mostrar la miniatura si lo deseas)
    function getYouTubeID(url) {
        const regex = /(?:https?:\/\/)?(?:www\.)?youtu(?:\.be\/|be\.com\/watch\?v=)([\w-]{11})/;
        const match = url.match(regex);
        return match ? match[1] : null;
    }

    // Mostrar la miniatura del video cuando el usuario ingresa una URL válida
    $('#url').on('input', function() {
        const url = $(this).val();
        const videoID = getYouTubeID(url);

        if (videoID) {
            // Genera la URL de la miniatura
            const thumbnailURL = `https://img.youtube.com/vi/${videoID}/0.jpg`;

            // Muestra la miniatura en el contenedor
            $('#thumbnail').attr('src', thumbnailURL).show();
        } else {
            // Oculta la miniatura si la URL no es válida
            $('#thumbnail').hide();
        }
    });

    // Descargar video
    $('#downloadBtn').click(function() {
        const url = $('#url').val();
        const quality = $('#quality').val();  // Calidad seleccionada manualmente
        const folder = $('#folder').val();  // Carpeta ingresada manualmente
        const filename = $('#filename').val();

        if (!url || !folder || !filename) {
            $('#message').text('Por favor, introduce una URL, selecciona una carpeta y un nombre de archivo').addClass('alert alert-danger');
            return;
        }

        $('#message').removeClass().text('Iniciando descarga...').addClass('alert alert-info');

        $.ajax({
            url: '/download',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ url: url, quality: quality, folder: folder, filename: filename }),  // Asegúrate de pasar la carpeta
            success: function(response) {
                if (response.status === 'success') {
                    $('#message').text(response.message).removeClass().addClass('alert alert-success');
                } else {
                    $('#message').text('Error: ' + response.message).removeClass().addClass('alert alert-danger');
                }
            },
            error: function() {
                $('#message').text('Error en el servidor').removeClass().addClass('alert alert-danger');
            }
        });
    });

    // Efecto de máquina de escribir dinámico
    function typeWriter(text, i, fnCallback) {
        if (i < (text.length)) {
            // Agrega el siguiente caracter al elemento HTML
            $('.typewriter').html(text.substring(0, i+1) + '<span aria-hidden="true"></span>');

            // Espera un poco y llama a la función nuevamente para el siguiente caracter
            setTimeout(function() {
                typeWriter(text, i + 1, fnCallback)
            }, 100);
        } else if (typeof fnCallback == 'function') {
            // Llamada al callback después de que todo el texto esté visible
            setTimeout(fnCallback, 700);
        }
    }

    // Inicia el efecto
    function startTextAnimation() {
        typeWriter("Descarga video", 0, function(){
            // Llama de nuevo para repetir el efecto
            startTextAnimation();
        });
    }

    // Inicia la animación al cargar la página
    startTextAnimation();
});
