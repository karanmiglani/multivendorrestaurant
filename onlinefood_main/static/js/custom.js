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
                $('#cart_counter').html(resp.cart_counter.cart_count)
                $('#qty-'+ food_id).html(resp.qty)
                // Subtotl and grand total tax
                applyCartAmount(resp.cart_amount.subTotal , resp.cart_amount.sgst , resp.cart_amount.cgst , resp.cart_amount.grandTotal)
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
                applyCartAmount(resp.cart_amount.subTotal , resp.cart_amount.sgst , resp.cart_amount.cgst , resp.cart_amount.grandTotal)
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
                applyCartAmount(resp.cart_amount.subTotal , resp.cart_amount.sgst , resp.cart_amount.cgst , resp.cart_amount.grandTotal)
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

    function applyCartAmount(subTotal , sgst , cgst , grandTotal){
        $('#subtotal').html(subTotal)
        $('#sgst').html(sgst)
        $('#cgst').html(cgst)
        $('#total').html(grandTotal)
    }
})

