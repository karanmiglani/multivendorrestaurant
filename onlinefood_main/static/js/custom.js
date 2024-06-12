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
    if(sessionStorage.getItem('current_location')){
        document.getElementById('current-location').value = sessionStorage.getItem('current_location')
    }
    function getCurrentLocation(){
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(async (pos)=>{
                var lat = pos.coords.latitude
                var long = pos.coords.longitude
                var apiKey = 'ge-50873fc6f0890c2d'
                console.log(lat , long)
                // var resp = await fetch('https://geocode.maps.co/reverse?lat='+lat+'&lon='+long+'&api_key=66680eeff0e9f808416099ubc5bf11d')
                const url = `https://api.geocode.earth/v1/reverse?api_key=${apiKey}&point.lat=${lat}&point.lon=${long}`;
                var resp = await fetch(url)
                var resp = await resp.json()
                var current_location = resp.features[0].properties.label
                document.getElementById('current-location').value = current_location
                sessionStorage.setItem('current_location',current_location)
                window.location =  '?lat='+lat+'&long='+long
            })
        }
    }
    $('#foodbakery_radius_location_open').on('click', (e)=> {
        e.preventDefault()
        getCurrentLocation()
    })
    $('#current-address-autocomplete').on('select',(e)=> {
        e.preventDefault()
        document.getElementById('current_id_address').value = e.detail.properties.label
        document.getElementById('current_id_lat').value = e.detail.geometry.coordinates[1]
        document.getElementById('current_id_long').value = e.detail.geometry.coordinates[0]
    })

    $('#search-auto').on('select',(e)=> {
        e.preventDefault()
        document.getElementById('search-id-address').value = e.detail.properties.label
        document.getElementById('search-id-latitude').value = e.detail.geometry.coordinates[1]
        document.getElementById('search-id-longitude').value = e.detail.geometry.coordinates[0]
    })


    $('#profile-auto').on('select' ,(event)=> {
        document.getElementById('id_country').value = event.detail.properties.country
        document.getElementById('id_state').value = event.detail.properties.region
        document.getElementById('id_city').value = event.detail.properties.locality
        if(event.detail.properties.postalcode){
            document.getElementById('id_pincode').value = event.detail.properties.postalcode
        }else{
            document.getElementById('id_pincode').value = ''
        }
        document.getElementById('id_address').value = event.detail.properties.label
        document.getElementById('id_latitude').value = event.detail.geometry.coordinates[1]
        document.getElementById('id_longitude').value = event.detail.geometry.coordinates[0]
    })




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

$('#place-order').on('click' , (e)=> {
    // e.preventDefault()
    var paymentMethod = $("input[name='payment_method']:checked").val()
    if(!paymentMethod){
        document.getElementById('payment-method-error').style.display = 'block'
        document.getElementById('payment-method-error').innerHTML = '<b>Select Payment Method</b>'
        return false
    }else{
       var conf = confirm('You have selected '+ paymentMethod + ' as your preffered payment method.\n Click Ok to continue')
       if(conf){
        return true
       }else{
        return false
       }
    }
    
})

$("input[name='payment_method']").on('change' , (e) => {
    document.getElementById('payment-method-error').style.display = 'none'
})


})