
// handle websocket connection....


const orderId = JSON.parse(document.getElementById('order-id').textContent)
let ws = new WebSocket(`ws://127.0.0.1:8000/ws/food-delivery/${orderId}/`)


ws.onopen = e =>{
    
    console.log("Websocket Succefully connected....")
}

ws.onmessage = e =>{

    const data = JSON.parse(e.data)
    console.log(data)
    document.getElementById('order-status').innerText = data.status
    let progres = document.getElementById('progress-id')
    progres.value = data.progress
    // if (progres === 100){
    //     progres.classList.add('progress-success')
    //     progres.classList.remove('progress-info')
    // }

}



ws.onerror = e =>{
    console.log(e)
}

ws.onclose = e =>{
    console.log("Websocket conecction lost....")
}





document.addEventListener('click', (event) => {
    const notificationItem = document.getElementById('noti-item');
    const logoPopup = document.getElementById('logo-popup');

    // Check if the click was on the notification item or the logo popup
    if (!notificationItem.contains(event.target) && !logoPopup.contains(event.target)) {
        notificationItem.classList.add('hidden');
    }
});



document.getElementById('logo-popup').addEventListener('click', ()=>{
    const notificationItem = document.getElementById('noti-item')

    console.log()
    if (notificationItem.classList.contains('hidden')){
        notificationItem.classList.remove('hidden')
    } else{
        notificationItem.classList.add('hidden')
    }

    
})




function OrderFunc(id){
    axios.post('/order-api/', {'id':id})
        .then(res =>{
           if(res.data.status=true){
            alert("Your Order succefully receive!")
           }
           else{
            alert("Order not submit, something went wrong!")
           }
        })
}

