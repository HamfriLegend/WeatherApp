function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $('.forecast').click(function (){
        $('.forecast').removeClass('select-f');
        $(this).addClass('select-f');
        $(this).find('.wind-rain').slideDown();
        $('.forecast').not('.select-f').find('.wind-rain').slideUp();

        $(this).find('.degree').css({
            'flex-direction': 'row',
            'font-size': '6em',
        });

        $('.forecast').not('.select-f').find('.degree').css({
            'flex-direction': 'column-reverse',
            'font-size': '2em',
        });


        $(this).find('.day').slideDown();
        $(this).find('.day-short').slideUp();
        $(this).find('.location').slideDown();
        $(this).find('.night-temp').slideUp();


        $('.forecast').not('.select-f').find('.day').slideUp();
        $('.forecast').not('.select-f').find('.day-short').slideDown();
        $('.forecast').not('.select-f').find('.location').slideUp();
        $('.forecast').not('.select-f').find('.night-temp').slideDown();

        const id = '#'+$(this).attr('id')+'-day';
        $(".day-forecast").not(id).hide();
        $(id).show();

    });


    var $input = $('#city');
    var $suggestionsContainer = $('#suggestions-container');

    $input.click(function (){
        const citiesCookie = getCookie('city_search');
        const latsCookie = getCookie('lat_search');
        const lonsCookie = getCookie('lon_search');

        if (citiesCookie && latsCookie && lonsCookie) {
            const cities = JSON.parse(citiesCookie);
            const lats = JSON.parse(latsCookie);
            const lons = JSON.parse(lonsCookie);
            $suggestionsContainer.empty().show();
            cities.forEach((city, index) => {
            var suggestionItem = $('<div>')
                .addClass('autocomplete-suggestion')
                .html(`<div>${city}</div>`)
                .data('lon', lons[index])
                .data('lat', lats[index])
                .on('click', function () {
                    $input.val(city);
                    $('#lon').val($(this).data('lon'));
                    $('#lat').val($(this).data('lat'));
                    $suggestionsContainer.empty().hide();
                });
            $suggestionsContainer.append(suggestionItem);
        });
        }
    })



    $input.on('keypress', function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
        }
    });

    $input.on('input', function() {
                var query = $input.val();
                if (query.length < 3) {
                    $suggestionsContainer.hide();
                    return;
                }
                var url = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=29&language=ru&format=json`;

                $.ajax({
                    url: url,
                    method: 'GET',
                    success: function(data) {
                        $suggestionsContainer.empty().show();
                        data.results.forEach(function(suggestion) {
                            var info = '';
                            if (suggestion.country) info = suggestion.country;
                            if (suggestion.admin1) info += ' ' + suggestion.admin1;
                            if (suggestion.admin2) info += ' ' + suggestion.admin2;
                            if (suggestion.admin3) info += ' ' + suggestion.admin3;

                            var suggestionItem = $('<div>')
                            .addClass('autocomplete-suggestion')
                            .html(`
                                <div>
                                    ${suggestion.name}
                                    <div>
                                        <sub>${info}</sub>
                                    </div>
                                </div>
                            `)
                            .data('lon', suggestion.longitude)
                            .data('lat', suggestion.latitude)
                            .on('click', function() {
                                $input.val(suggestion.name);
                                $('#lon').val($(this).data('lon'));
                                $('#lat').val($(this).data('lat'));
                                $suggestionsContainer.empty().hide();
                            });
                        $suggestionsContainer.append(suggestionItem);});
                    }
                });
            });

            // Скрыть подсказки при клике вне поля ввода
        $(document).on('click', function(event) {
            if (!$(event.target).closest('#city').length) {
                $suggestionsContainer.empty().hide();
            }
        });



});
