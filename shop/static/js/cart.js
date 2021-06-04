//To send cart addItem and remove item requests and update the corresponding listing cards
$(function(){
    $('body').on('click', '.addItemButton', function(){
    var pid;

    pid = $(this).attr("data-pid");
    $.ajax(
    {
        type:"GET",
        url: "/additem",
        data:{
                 pid: pid
        },
        success: function( data )
        {
            if(data.status == "Error"){
                alert(data.message);
                return;
            }
            if(data.status == "Success" && data.cart_qty == 1){
                $( '.controls #addButton_'+ pid ).remove();

                 //minus button
                 var minButton = document.createElement("button");
                 minButton.innerText = "-";
                 minButton.id = "minusButton_"+pid;
                 minButton.className = "minusItemButton btn btn-primary cart";
                 minButton.setAttribute('data-pid', pid);

                 //add button
                 var addButton = document.createElement("button");
                 addButton.innerText = "+";
                 addButton.id = "plusButton_"+pid;
                 addButton.className = "addItemButton btn btn-primary cart";
                 addButton.setAttribute('data-pid', pid);

                 //qty. span text
                 var spanText = document.createElement("span");
                 spanText.innerHTML = " "+data.cart_qty+" ";
                 spanText.id = "qtySpan_"+pid;

                //live stat update
                $('#pricepr_'+pid).text(data.cart_price.toFixed(2));
                $('#wght_'+pid).text(data.cart_weight.toFixed(1));

                //card buttons (+ -) of index and search page

                console.log($(this));
                $('#card_' + pid + ' .controls').append(minButton);
                $('#card_' + pid + ' .controls').append(spanText);
                $('#card_' + pid + ' .controls').append(addButton);

                //minus button
                var MminButton = document.createElement("button");
                MminButton.innerText = "-";
                MminButton.id = "minusButton_"+pid;
                MminButton.className = "minusItemButton btn btn-primary cart";
                MminButton.setAttribute('data-pid', pid);

                 //add button
                 var MaddButton = document.createElement("button");
                 MaddButton.innerText = "+";
                 MaddButton.id = "plusButton_"+pid;
                 MaddButton.className = "addItemButton btn btn-primary cart";
                 MaddButton.setAttribute('data-pid', pid);

                 //qty. span text
                 var MspanText = document.createElement("span");
                 MspanText.innerHTML = " "+data.cart_qty+" ";
                 MspanText.id = "qtySpan_"+pid;


                //Modal Body row creation
                var row = document.createElement("div");
                row.className = "row";
                row.id = '#row_' + pid;

                //Name row creation
                var nameTag = document.createElement("h6");
                nameTag.className = "col-sm-8";
                nameTag.innerText = $("#namepr"+pid).text();
                row.appendChild(nameTag);

                //row controls
                var modalControls = document.createElement("h6");
                modalControls.className = "col-sm modalControls";

                //appending row controls
                modalControls.append(MminButton);
                modalControls.append(MspanText);
                modalControls.append(MaddButton);

                row.appendChild(modalControls);

                // appending whole tree to Modal
                $("#cartModal .modal-body").append(row);
            }else {
                $('.controls #qtySpan_'+pid).text(' '+data.cart_qty+' ');
                $('.modal .modal-body #qtySpan_'+pid).text(' '+data.cart_qty+' ');
                $('#pricepr_'+pid).text(data.cart_price.toFixed(2));
                $('#wght_'+pid).text(data.cart_weight.toFixed(1));
            }

        }
     })
    });
    $('body').on('click', '.minusItemButton', function(){
    var pid;
    pid = $(this).attr("data-pid");
    $.ajax(
    {
        type:"GET",
        url: "/deleteitem",
        data:{
                 pid: pid
        },
        success: function( data )
        {
            if(data.status == "Error"){
                alert(data.message);
                return;
            }
            if(data.status == 'Success' && data.cart_qty == 0){
                 $( '.controls #minusButton_'+ pid ).remove();
                 $( '.controls #plusButton_'+ pid ).remove();
                 $( '.controls #qtySpan_'+ pid ).remove();
                 $( '.modal .modal-body' ).remove('#row_' + pid);
                 $( '.modal .modal-body #minusButton_'+ pid ).remove();
                 $( '.modal .modal-body #plusButton_'+ pid ).remove();
                 $( '.modal .modal-body #qtySpan_'+ pid ).remove();
                 $( '.modal .modal-body #row_' + pid +" h6" ).remove();
                 $( '.modal #row_' + pid ).remove();

                 var addButton = document.createElement("button");
                 addButton.innerText = "Add To Cart";
                 addButton.id = "addButton_"+pid;
                 addButton.className = "addItemButton btn btn-primary cart";
                 addButton.setAttribute('data-pid', pid);

                $('#card_' + pid + ' .controls').append(addButton);

                $('.card-body #pricepr_'+pid).text(data.cart_price.toFixed(2));
                $('.card-body #wght_'+pid).text(data.cart_weight.toFixed(1));

            }else{
                $('.controls #qtySpan_'+pid).text(' '+data.cart_qty+' ');
                $('.modal .modal-body #qtySpan_'+pid).text(' '+data.cart_qty+' ');
                $('.card-body #pricepr_'+pid).text(data.cart_price.toFixed(2));
                $('.card-body #wght_'+pid).text(data.cart_weight.toFixed(1));
            }
        }
     })
    });
});