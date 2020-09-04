(function($) {
    $(document).ready(function(){
        //alert('yes');
    });
})(django.jQuery);

var $ = django.jQuery.noConflict();

function part_changed(mutation,quantity_tag)
{
    $.ajax({
        url: 'http://127.0.0.1:8000/stock/get_quantity/',
        method: 'GET',
        data: {
            id: mutation.target.getAttribute('title'),
        },
        success: function(result){
            quantity_tag.innerHTML = result.quantity;
            observer.observe(targetNode, observerOptions);
        }
    });
};

//alert('yes');

let observer = new MutationObserver(callback);
targetNode = document.getElementById('InventoryPart_sup_part-group');
observerOptions = {
    attribute: true,
    attributeOldValue: true,
    subtree: true,
    attributeFilter: ['title',],
    characterData: true,
  };
function callback(mutations) {
    //alert('hoohooo');
    for (let mutation of mutations) {
        if (mutation.type === 'attributes') { 
            //alert(mutation.target);
            if (mutation.oldValue != mutation.target.getAttribute('title')){
                targetSiblings = mutation.target.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.children
                for (i = 0; i < targetSiblings.length; i++) {
                    if (targetSiblings[i].getAttribute('class') == 'field-stock' ) {
                        c = targetSiblings[i].children;
                        for (j=0;j<c.length;j++) {
                            //alert(c[j].getAttribute('class'))
                            if (c[j].getAttribute('class') == 'stock_tag') {
                                //alert('ok');
                                quantity_tag = c[j];
                                //alert(unit_tag);
                            };
                        };
                    };
                  };
                observer.disconnect();
                part_changed(mutation,quantity_tag);
            };
            //alert(mutation.target);
        };
    };
    //observer.disconnect();
};

observer.observe(targetNode, observerOptions);