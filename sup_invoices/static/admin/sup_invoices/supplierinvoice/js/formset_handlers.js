//document.querySelector('select[name="myselect2name"]').onchange=function() {
//    console.log("myselect2name changed");
//  };

(function($) {
    $(document).ready(function(){
        //alert('wow');
        //$('body').on('change', '.select2-selection', function() {
        //    alert('hey');
        /*
        $("#supplierinvoiceparts_set-group").on('DOMSubtreeModified', function() {
            //alert($(this).text());
            if ($('#select2-id_supplierinvoiceparts_set-0-part-container').text() != ''){
                //alert($(this).text());
                part_changed($(this).text());
            }
        });*/
    });
    //function part_changed(part){
    //    $('.unit_tag').html() = 'clicked';
    //};
})(django.jQuery);


var $ = django.jQuery.noConflict();

function part_changed(mutation,unit_tag)
{
    //alert(part);
    //document.getElementById('unit_tag').innerHTML = part;
    /*$.ajax({
        url: 'http://127.0.0.1:8000/admin/sup_invoices/supplierinvoice/add/?ids=',
        type: 'POST',
        data: '1_2',
        traditional: true,
        dataType: 'html',
        success: function(result){
            $('#unit_tag').append(result);
            }
    });*/
    $.ajax({
        url: 'http://127.0.0.1:8000/sup_invoices/get_units/',
        method: 'GET',
        data: {
            id: mutation.target.getAttribute('title'),
        },
        success: function(result){
            alert(result.unit);
            unit_tag.innerHTML = result.unit;
            observer.observe(targetNode, observerOptions);
        }
    });
};

let observer = new MutationObserver(callback);
targetNode = document.getElementById('supplierinvoiceparts_set-group');
observerOptions = {
    attribute: true,
    attributeOldValue: true,
    subtree: true,
    attributeFilter: ['title',],
  };
function callback(mutations) {
    for (let mutation of mutations) {
        if (mutation.type === 'attributes') { 
            if (mutation.oldValue != mutation.target.getAttribute('title')){
                alert(mutation.target.getAttribute('id'));
                targetSiblings = mutation.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.children
                for (i = 0; i < targetSiblings.length; i++) {
                    if (targetSiblings[i].getAttribute('class') == 'field-unit' ) {
                        c = targetSiblings[i].children;
                        for (j=0;j<c.length;j++) {
                            alert(c[j].getAttribute('class'))
                            if (c[j].getAttribute('class') == 'unit_tag') {
                                //alert('ok');
                                unit_tag = c[j];
                                alert(unit_tag);
                            };
                        };
                    };
                  };
                observer.disconnect();
                part_changed(mutation,unit_tag);
            };
            //alert(mutation.target);
        };
    };
    //observer.disconnect();
};

observer.observe(targetNode, observerOptions);