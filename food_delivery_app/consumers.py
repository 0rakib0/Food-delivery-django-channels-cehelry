from channels.consumer import AsyncConsumer
import json


class FoodDelibery(AsyncConsumer):
    
    async def websocket_connect(self, event):
        print("Websocket successfully connected....")
        
        await self.send({
            'type':'websocket.accept'
        })
        
    
    async def websocket_receive(self, event):
        print("Websocket get message...", event)
        
    async def websocket_disconnected(self, event):
        print("Connection lost")