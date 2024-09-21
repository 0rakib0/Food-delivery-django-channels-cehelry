from channels.consumer import AsyncConsumer
import json


class FoodDelibery(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("Websocket successfully connected....")
        
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order_%s' % self.room_name
        print(self.room_group_name)
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name  # Use self.channel_name, which is automatically assigned
        )
        
        await self.send({
            'type':'websocket.accept'
        })
        
    
    async def websocket_receive(self, event):
        print("Websocket get message...", event)
        
        
    async def order_status(self, event):
        
        order_data = event['data']
        
        await self.send({
            'type':'websocket.send',
            'text':json.dumps(order_data)
        })
        
        
    async def websocket_disconnect(self, event):
        print("Connection lost")
        
        
class SendNotification(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("Websocket successfully connected....")
        
        
        self.room_group_name = 'notification_brotcast'
        print(self.room_group_name)
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name  # Use self.channel_name, which is automatically assigned
        )
        
        await self.send({
            'type':'websocket.accept'
        })
        
    
    async def websocket_receive(self, event):
        print("Websocket get message...", event)
        
        
    async def notifiction_send(self, event):
        notification_data = event['data']
        await self.send({
            'type':'websocket.send',
            'text': notification_data
        })
        
        
    async def websocket_disconnect(self, event):
        print("Connection lost")