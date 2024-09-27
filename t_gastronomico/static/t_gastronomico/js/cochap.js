$('.star-rating .fa').hover(
    // Manejar el evento de pasar el mouse
    function () {
        var rating = $(this).data('rating');
        $(this).parent().children('.fa').each(function (index) {
            if (index < rating) {
                $(this).removeClass('text-muted fa-star').addClass('text-warning fa-star');
            } else {
                $(this).removeClass('text-warning fa-star').addClass('text-muted fa-star');
            }
        });
    },
    // Manejar el evento de salir del mouse
    function () {
        var rating = $(this).parent().children('input.rating-value').val();
        $(this).parent().children('.fa').each(function (index) {
            if (index < rating) {
                $(this).removeClass('text-muted fa-star').addClass('text-warning fa-star');
            } else {
                $(this).removeClass('text-warning fa-star').addClass('text-muted fa-star');
            }
        });
    }
);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$('.star-rating .fa').click(function () {
    var rating = $(this).data('rating');
    console.log('rating:', rating);
    var turista_id = $(this).parent().find('.turista-id').val();
    console.log('turista_id:', turista_id);
    var plato_id = $(this).parent().find('.plato-id').val();
    var restaurante_id = $(this).parent().find('.restaurante-id').val();

    $(this).parent().find('input.rating-value').val(rating);
    $(this).parent().find('input.turista-id').val(turista_id);
    $(this).parent().find('input.plato-id').val(plato_id);
    $(this).parent().find('input.restaurante-id').val(restaurante_id);

    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/calificacion/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            rating: rating,
            turista_id: turista_id,
            plato_id: plato_id,
            restaurante_id: restaurante_id
        },
        success: function (response) {
            console.log('Calificación guardada exitosamente');
            console.log(response);
        },
        error: function (error) {
            console.error('Error al guardar la calificación:', error);
        }
    });
});


function cargarCalificacionesTurista() {
    var turista_id = $(this).parent().find('.turista-id').val();

    $.ajax({
        url: '/obtener_calificaciones/',
        type: 'GET',
        data: {
            turista_id: turista_id
        },
        success: function(response) {
            console.log('Calificaciones del turista cargadas correctamente:', response);
        },
        error: function(error) {
            console.error('Error al cargar las calificaciones del turista:', error);
        }
    });
}

$(document).ready(function() {
    cargarCalificacionesTurista();
});


$(document).ready(function() {
    $('#comentarioForm').on('submit', function(event) {
        event.preventDefault();

        $.ajax({
             url: $(this).data('url-agregar-resena'),
             type: 'POST',
             data: $(this).serialize(),
             success: function(response) {
                 console.log(response);
                 if (response && response.turista) {
                     var nombre = response.turista.nombre;
                     var foto = response.turista.Tfoto;
                     // Aquí puedes manejar la respuesta del servidor
                     // Por ejemplo, puedes agregar el nuevo comentario a la lista de comentarios
                     var nuevoComentario = '<div class="row mb-3">' +
                        '<div class="col-2">' +
                        '<img class="rounded-circle" src="' + foto + '" alt="' + nombre + '" width="64">' +
                        '</div>' +
                        '<div class="col-2">' +
                        '<h5 class="mt-0">' + nombre + '</h5>' +
                        '<p class="text-muted">' + response.fecha + '</p>' +
                        '</div>' +
                        '<div class="col-6">' +
                        '<p>' + response.comentario + '</p>' +
                        '</div>' +
                        '</div>';

                     // Agrega el nuevo comentario a la lista de comentarios
                     $('#listaComentarios').prepend(nuevoComentario);
                     $('#comentario').val('');

                 } else {
                     console.log('Los datos devueltos por el servidor no tienen la estructura esperada');
                 }
             },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    });
});

    







    

