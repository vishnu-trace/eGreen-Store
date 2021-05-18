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
                 $( '#addButton_'+ pid ).remove();

                 var minButton = document.createElement("button");
                 minButton.innerText = "-";
                 minButton.id = "minusButton_"+pid;
                 minButton.className = "minusItemButton btn btn-primary cart";
                 minButton.setAttribute('data-pid', pid);

                 var addButton = document.createElement("button");
                 addButton.innerText = "+";
                 addButton.id = "plusButton_"+pid;
                 addButton.className = "addItemButton btn btn-primary cart";
                 addButton.setAttribute('data-pid', pid);

                 var spanText = document.createElement("span");
                 spanText.innerHTML = " "+data.cart_qty+" ";
                 spanText.id = "qtySpan_"+pid;

                var spanpr = document.getElementById('pricepr_' + pid);
                spanpr.innerHTML = " "+data.cart_price.toFixed(2)+" ";
                var spanwght = document.getElementById('wght_' + pid);
                spanwght.innerHTML = " "+data.cart_weight.toFixed(2)+" ";

                 var div = document.getElementById('card_'+ pid);
                 div.appendChild(minButton);
                 div.appendChild(spanText);
                 div.appendChild(addButton);
            }else {
                console.log(data);
                var spanqty = document.getElementById('qtySpan_' + pid);
                spanqty.innerHTML = " "+data.cart_qty+" ";
                var spanpr = document.getElementById('pricepr_' + pid);
                spanpr.innerHTML = " "+data.cart_price.toFixed(2)+" ";
                var spanwght = document.getElementById('wght_' + pid);
                spanwght.innerHTML = " "+data.cart_weight.toFixed(1)+" ";
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
                 $( '#minusButton_'+ pid ).remove();
                 $( '#plusButton_'+ pid ).remove();
                 $( '#qtySpan_'+ pid ).remove();

                 var addButton = document.createElement("button");
                 addButton.innerText = "Add To Cart";
                 addButton.id = "addButton_"+pid;
                 addButton.className = "addItemButton btn btn-primary cart";
                 addButton.setAttribute('data-pid', pid);

                 var div = document.getElementById('card_'+ pid);
                 div.appendChild(addButton);

                var spanpr = document.getElementById('pricepr_' + pid);
                spanpr.innerHTML = " "+data.cart_price.toFixed(2)+" ";
                var spanwght = document.getElementById('wght_' + pid);
                spanwght.innerHTML = " "+data.cart_weight.toFixed(1)+" ";

            }else{
                var spanqty = document.getElementById('qtySpan_' + pid);
                spanqty.innerHTML = " "+data.cart_qty+" ";
                var spanpr = document.getElementById('pricepr_' + pid);
                spanpr.innerHTML = " "+data.cart_price.toFixed(2)+" ";
                var spanwght = document.getElementById('wght_' + pid);
                spanwght.innerHTML = " "+data.cart_weight.toFixed(1)+" ";
            }
        }
     })
    });
});