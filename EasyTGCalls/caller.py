from pyrogram import Client, idle
from pyrogram.raw.types import UpdateGroupCallConnection, Updates, DataJSON, GroupCall
from ntgcalls import NTgCalls, MediaDescription
from typing import Union

from EasyTGCalls.pyro_client import Pyro
from EasyTGCalls.types import Media
from EasyTGCalls.stream_methods import StreamMethods

class Caller(StreamMethods):
    def __init__(
        self: "Caller",
        pyro_client: Client,
        wrtc: NTgCalls = None
    ):
        self.wrtc = wrtc or NTgCalls()
        self.client = Pyro(pyro_client)

    # raw methods
    
    async def get_call_parametrs(
        self,
        chat_id: int,
        media: MediaDescription
    ) -> str:
        params = await self.wrtc.create_call(
            chat_id,
            media
        )
        return params

    # thanks for the examples Laky64
    async def call_data(
        self: "Caller",
        chat_id: Union[int, str],
        call_params: str,
        muted: bool,
        video_stopped: bool
    ):
        input_call = (await self.client.get_full_channel(chat_id)).full_chat.call
        result: Updates = await self.client.join_group_call(
            call=input_call,
            video_stopped=video_stopped,
            muted=muted,
            params=DataJSON(call_params)
        )

        for update in result.updates:
            if isinstance(update, UpdateGroupCallConnection):
                return update.params.data
            
    # abstract methods

    async def get_call(
        self,
        chat_id
    ) -> Union[None, GroupCall]:
        call = (await self.client.get_full_channel(chat_id)).full_chat.call

        if call:
            return await self.client.get_group_call(call)
            
    async def join_call(
        self: "Caller",
        chat_id: int,
        media: Media = Media(),
        muted: bool = True,
        video_stopped: bool = True,
    ):
        # check media
        if media.video:
            video_stopped = False
            muted = False
        
        if media.audio:
            muted = False

        params = await self.get_call_parametrs(chat_id, media())
        call_data = await self.call_data(
            chat_id=chat_id,
            call_params=params,
            muted=muted,
            video_stopped=video_stopped,
        )
        # connection
        await self.wrtc.connect(chat_id, call_data)

    async def leave_call(
        self,
        chat_id: int
    ) -> bool:
        call = (await self.client.get_full_channel(chat_id)).full_chat.call

        if call:
            return await self.client.leave_group_call(
                call=call,
            )

    async def run(self):
        await idle()