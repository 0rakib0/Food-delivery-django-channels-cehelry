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