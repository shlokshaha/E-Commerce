var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log("Product: ",productId, "Action:",action)
        console.log("USER:",user)
        if(user === 'AnonymousUser'){
            addCookieItem(productId,action)
        }else{
            updateUserOrder(productId,action)
        }
    })
}

/* cart(cookie) after parsing
    cart={
        1:{'quantity':4},
        2:{'quantity':6},
        3:{'quantity':1},
    }
*/

function addCookieItem(productId,action){             //for guest users adding items to cookie(cart)
    console.log("User not authenticated");

    if(action=='add'){
        if(cart[productId]==undefined){     //item not in cart
            cart[productId] = {'quantity':1}
        }else{                              //item already exists
            cart[productId]['quantity'] +=1
        }
    }

    if(action=='remove'){
        cart[productId]['quantity'] -=1
        if(cart[productId]['quantity']<=0){
            console.log("removed Item")
            delete cart[productId];      //delete the item from cart(cookie)
        }
    }
    console.log("cart:",cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"     //resetting the cookie cart
    location.reload()
}


function updateUserOrder(productId,action){                     //for authenticated users
    console.log("User is logged in... Sending Data...")

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId': productId,'action': action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}