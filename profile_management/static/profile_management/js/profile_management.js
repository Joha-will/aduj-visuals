// CountryField js

let countrySelected = $('#id_default_country').val();
if (!countrySelected) {
    $('#id_default_country').css('color', '#CFCFCF');
}

$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#CFCFCF');
    } else {
        $(this).css('color', 'black');
    }
});