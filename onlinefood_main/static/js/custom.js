// let autocomplete;

// function initAutoComplete(){
// autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById('id_address'),
//     {
//         types: ['geocode', 'establishment'],
//         //default in this app is "IN" - add your country code
//         componentRestrictions: {'country': ['in']},
//     })
// // function to specify what should happen when the prediction is clicked
// autocomplete.addListener('place_changed', onPlaceChanged);
// }

// function onPlaceChanged (){
//     var place = autocomplete.getPlace();

//     // User did not select the prediction. Reset the input field or alert()
//     if (!place.geometry){
//         document.getElementById('id_address').placeholder = "Start typing...";
//     }
//     else{
//         console.log('place name=>', place.name)
//     }
//     // get the address components and assign them to the fields
// }




$(document).ready(function(){
    $('.add-to-cart').on('click',function(e){
        e.preventDefault();
       food_id = $(this).attr('data-id')
       url = $(this).attr('data-url')
       data  = {
        food_id : food_id
       }
       $.ajax({
        type : 'GET',
        url : url,
        data : data,
        success : function(resp){
            if(resp.status == 200){
                console.log(resp)
                $('#cart_counter').html(resp.cart_counter.cart_count)
                $('#qty-'+ food_id).html(resp.qty)
                // Subtotl and grand total tax
                applyCartAmount(resp.cart_amount.subTotal ,  resp.cart_amount.tax_dict , resp.cart_amount.grandTotal)
                Swal.fire({
                    title: 'Success!',
                    text: resp.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                });
            }else if(resp.status == 404){
                Swal.fire({
                    title: 'Error!',
                    text: resp.message,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }else{
                Swal.fire({
                    title: 'Error!',
                    text: "server error",
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }

        },
        error:function(e){
            console.log(e.responseText)
            
        }
       })
    })

    // Place the cart item qty on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        console.log(qty)
        $('#' + the_id).html(qty)
    })

    $('.decrease-from-cart').on('click',function(){
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        cart_id = $(this).attr('id')
        data = {
            food_id :food_id
        }
        $.ajax({
            type : "GET",
            url : url,
            data : data,
            success:function(resp){
               if(resp.status ==  200){
                $('#cart_counter').html(resp.cart_counter.cart_count)
                $('#qty-'+ food_id).html(resp.qty)
                applyCartAmount(resp.cart_amount.subTotal ,  resp.cart_amount.tax_dict , resp.cart_amount.grandTotal)
                if(window.location.pathname == '/marketplace/cart/'){
                    
                    removeCartItem(resp.qty , cart_id)
                    checkEmptyCart()
                    
                }
                
                Swal.fire({title: 'Success!',text: resp.message,icon: 'success',confirmButtonText: 'OK'});
               }else if(resp.status == 204){Swal.fire({title: 'Oops!😲',text: resp.message,icon: 'warning',confirmButtonText: 'OK'});}
                else if(resp.status == 404){Swal.fire({title: 'Error!😵',text: resp.message,icon: 'error',confirmButtonText: 'OK'});}
                else if(resp.status == 400){Swal.fire({title: 'Error!😵',text: resp.message,icon: 'error',confirmButtonText: 'OK'});}
                else if(resp.status == 401){Swal.fire({title: 'Error!😵',text: resp.message,icon: 'error',confirmButtonText: 'OK'});}
                else{
                    console.log('Server error')
                }
            },
            error:function(e){
                console.log(e.responseText)
            }
        })
    })

    $('.delete-cart-item').on('click',function(){
        cart_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        data = {
            cart_id : cart_id
        }
        $.ajax({
            type : "GET",
            url : url,
            data : data,
            success:function(resp){
               if(resp.status ==  200){
                $('#cart_counter').html(resp.cart_counter.cart_count)
                removeCartItem(0 , cart_id)
                checkEmptyCart()
                applyCartAmount(resp.cart_amount.subTotal ,  resp.cart_amount.tax_dict , resp.cart_amount.grandTotal)
                Swal.fire({title: 'Success!',text: resp.message,icon: 'success',confirmButtonText: 'OK'});
               }else if(resp.status == 204){Swal.fire({title: 'Oops!😲',text: resp.message,icon: 'warning',confirmButtonText: 'OK'});}
                else if(resp.status == 404){Swal.fire({title: 'Error!😵',text: resp.message,icon: 'error',confirmButtonText: 'OK'});}
                else if(resp.status == 400){Swal.fire({title: 'Error!😵',text: resp.message,icon: 'error',confirmButtonText: 'OK'});}
                else if(resp.status == 401){Swal.fire({title: 'Error!😵',text: resp.message,icon: 'error',confirmButtonText: 'OK'});}
                else{
                    console.log('Server error')
                }
            },
            error:function(e){
                console.log(e.responseText)
            }
        })
    })


    // delete cart item if the qty is 0
    function removeCartItem(cartItemQty , cart_id){
        if(cartItemQty <= 0){
            // remove cart item elemet
            document.getElementById('cart-item-'+cart_id).remove()
        }
    }

    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter <= 0){
            document.getElementById('empty-cart').style.display = 'block'
        }
    }

    function applyCartAmount(subTotal , tax_dict , grandTotal){
        $('#subtotal').html(subTotal)
        $('#total').html(grandTotal)
        for(key1 in tax_dict){
            for(key2 in tax_dict[key1]){
                $('#tax-'+key1).html(tax_dict[key1][key2])
            }
        }
    }

    $('.add_hour').on('click' , function(e){
        e.preventDefault()
       var day = document.getElementById('id_day').value
       var from_hours = document.getElementById('id_from_hours').value
       var to_hours = document.getElementById('id_to_hours').value
       var is_closed = document.getElementById('id_is_closed').checked
       var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
       var url = $(this).attr('data-url')
       console.log(day , from_hours , to_hours , is_closed , csrf_token , url)
       data = {
        day : day,
        from_hours : from_hours,
        to_hours : to_hours,
        is_closed : is_closed,
        csrfmiddlewaretoken : csrf_token
       }
        if(is_closed){
            is_closed = 'True'
            condition = "day !=''"
        }else{
            is_closed = 'False'
            condition = "day!='' && from_hours !='' && to_hours != ''"
        }

        if(eval(condition)){
            $.ajax({
                type : 'POST',
                url : url ,
                data : data,
                success:function(resp){
                    console.log(resp)
                    if(resp.status == 200){
                        var baseRemoveUrl = $('.opening_hours').attr('data-remove-url');
                        baseRemoveUrl = baseRemoveUrl.replace('0', resp.id);
                        if(resp.is_closed == 1){
                            html = '<tr id="hour-' + resp.id +'"><td><b>'+resp.day+'</b></td><td>Closed</td><td><a href="'+ baseRemoveUrl +'" class="remove_hour" ">Remove</a></td> </tr>'
                        }else{
                            html = '<tr id="hour-' + resp.id +'"><td><b>'+resp.day+'</b></td><td>'+resp.from_hours+' - '+resp.to_hours+'</td><td><a href="'+ baseRemoveUrl+'" class="remove_hour">Remove</a></td> </tr>'
                        }
                        $('.opening_hours').append(html)
                        document.getElementById('opening_hours').reset()
                    }else{
                        Swal.fire({title: 'Error!😵',text: resp.message,icon: 'error',confirmButtonText: 'OK'});
                    }
                },
                error:function(e){
                    console.log(e.responseText)
                }
            })
        }
    })



})

