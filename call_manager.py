import uuid
import asyncio
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import InputAudioStream, InputVideoStream
from pytgcalls.types.raw import AudioParameters, VideoParameters

class CallManager:
    def __init__(self):
        self.active_calls = {}

    async def start_call(self, api_id, api_hash, phone, target, media_url):
        call_id = str(uuid.uuid4())

        client = Client(
            f"session_{call_id}",
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone
        )

        await client.start()

        call = PyTgCalls(client)
        await call.start()

        await call.join_group_call(
            target,
            InputAudioStream(media_url),
        )

        self.active_calls[call_id] = {
            "client": client,
            "call": call,
            "status": "in_progress",
            "target": target
        }

        return call_id

    async def stop_call(self, call_id):
        if call_id in self.active_calls:
            data = self.active_calls[call_id]
            await data["call"].leave_group_call(data["target"])
            await data["client"].stop()
            data["status"] = "ended"

    def get_status(self, call_id):
        if call_id in self.active_calls:
            return {"call_id": call_id, "status": self.active_calls[call_id]["status"]}
        return {"call_id": call_id, "status": "not_found"}
