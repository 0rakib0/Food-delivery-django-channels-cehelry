// WebSocket for order status (connect only on order-view route)
console.log("---------------+++++++++++++-----------")

const idElement = document.getElementById('id');
const orderIdElement = document.getElementById('order-id');
if (idElement && orderIdElement) {
    console.log('helloooooooooooooooo')
    const orderId = JSON.parse(orderIdElement.textContent);

    let ws_order_status = new WebSocket(`ws://127.0.0.1:8000/ws/food-delivery/${orderId}/`);

    ws_order_status.onopen = e => {
        console.log("WebSocket Successfully connected to order status....");
    };

    ws_order_status.onmessage = e => {
        const data = JSON.parse(e.data);
        console.log(data);
        document.getElementById('order-status').innerText = data.status;
        let progress = document.getElementById('progress-id');
        progress.value = data.progress;

        // Optionally handle progress
        // if (progress.value === 100) {
        //     progress.classList.add('progress-success');
        //     progress.classList.remove('progress-info');
        // }
    };

    ws_order_status.onerror = e => {
        console.log(e);
    };

    ws_order_status.onclose = e => {
        console.log("WebSocket connection lost for order status....");
    };
}

// WebSocket for notifications (connect for all routes)

let ws_notification_send = new WebSocket('ws://127.0.0.1:8000/ws/send-notification/');

ws_notification_send.onopen = e => {
    console.log("WebSocket successfully connected for notifications.....");
};

ws_notification_send.onmessage = e => {
    console.log("WebSocket successfully received message.....");
    console.log(e)
};

ws_notification_send.onerror = e => {
    console.log(e);
};

ws_notification_send.onclose = e => {
    console.log("WebSocket connection lost for notifications..");
};



// Notification Popup Script
document.addEventListener('click', (event) => {
    const notificationItem = document.getElementById('noti-item');
    const logoPopup = document.getElementById('logo-popup');

    if (!notificationItem.contains(event.target) && !logoPopup.contains(event.target)) {
        notificationItem.classList.add('hidden');
    }
});

document.getElementById('logo-popup').addEventListener('click', () => {
    const notificationItem = document.getElementById('noti-item');

    if (notificationItem.classList.contains('hidden')) {
        notificationItem.classList.remove('hidden');
    } else {
        notificationItem.classList.add('hidden');
    }
});

// Order Function
function OrderFunc(id) {
    axios.post('/order-api/', {'id': id})
        .then(res => {
            if (res.data.status === true) {
                alert("Your order was successfully received!");
            } else {
                alert("Order not submitted, something went wrong!");
            }
        });
}
