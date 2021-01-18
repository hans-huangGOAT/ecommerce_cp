var updateBtns = document.getElementsByClassName("update_item")

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        let action = this.dataset.action
        let product_id = this.dataset.product
        console.log("ppp")

        if (user === 'AnonymousUser') {
            addCookieItem(product_id, action)
        } else {
            updateOrderItem(action, product_id)
        }
    })
}

function addCookieItem(product_id, action) {
    console.log("user is not authenticated")

    if (action == 'add') {
        if (cart[product_id] == undefined) {
            cart[product_id] = {'quantity': 1}
        } else {
            cart[product_id]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[product_id]['quantity'] -= 1

        if (cart[product_id]['quantity'] <= 0) {
            console.log("Remove Item")
            delete cart[product_id]
        }
    }
    console.log("Cart:", cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()

}


function updateOrderItem(action, product_id) {
    let url = '/update_item/'

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': product_id,
            'action': action,
        })
    })
        .then(response => {
            return response.json()
        })
        .then(data => {
            console.log("Success: " + data)
            location.reload();
        })
}