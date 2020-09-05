
(function($) {
    $(document).ready(function(){
        alert('docready');
        $('#id_labour_guide').change(function(){
            alert($('#id_labour_guide'));
            value = $('#id_labour_guide').val();
            alert(value);
            hours_changed(value);
        });
    });
})(django.jQuery);


var $ = django.jQuery.noConflict();

function hours_changed(mutation)
{
    $.ajax({
        url: '/workorders/get_defaults/',
        method: 'GET',
        data: {
            'value': value,
        },
        success: function(result){
            alert(result);
            //alert(result.labour);
            $('#id_labour_charged').val(result.labour);
            $('#id_hours_charged').val(result.hours);
        }
    });
};
