import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import PrivateMessage, GroupMessage, Group


class PrivateConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        me = self.scope["user"]
        them = self.scope["url_route"]["kwargs"]["username"]

        if me.username == them:
            await self.close()          # no talking to yourself
            return

        # deterministic room name
        room = "_".join(sorted([me.username, them]))
        self.room_group_name = f"private_{room}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = await self.save_private(data["message"])
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def save_private(self, text):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        them = User.objects.get(
            username=self.scope["url_route"]["kwargs"]["username"])
        msg = PrivateMessage.objects.create(
            sender=self.scope["user"],
            receiver=them,
            text=text
        )
        return {"sender": msg.sender.username, "text": msg.text, "time": str(msg.sent_at)}


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.room_group_name = f"group_{self.group_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = await self.save_group(data["message"])
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def save_group(self, text):
        group = Group.objects.get(name=self.group_name)
        msg =  GroupMessage.objects.create(
            author=self.scope["user"],
            group=group,
            text=text
        )
        return {"author": msg.author.username,
        "text": msg.text,
        "time": str(msg.sent_at)}