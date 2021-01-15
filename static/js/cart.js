var updateBtns = document.getElementsByClassName("update_item")

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", function () {
        let action = this.dataset.action
        let product_id = this.dataset.product
        console.log("ppp")

        updateOrderItem(action, product_id)
    })
}


function updateOrderItem(action, product_id) {
    let url = '/update_item/'

    fetch(url,{
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