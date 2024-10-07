from ntgcalls import NTgCalls, MediaDescription
from pyrogram import Client, idle, errors
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import JoinGroupCall
from pyrogram.raw.types import UpdateGroupCallConnection, Updates, DataJSON, InputChannel
from typing import Union
from EasyTGCalls.types import Media

class Caller:
    def __init__(
        self: "Caller",
        pyro_client: Client
    ):
        self.wrtc = NTgCalls()
        self.client = pyro_client

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

    async def call_data(
        self: "Caller",
        chat_id: Union[int, str],
        call_params: str,
        muted: bool,
        video_stopped: bool
    ):
        chat = await self.client.resolve_peer(chat_id)
        app_peer = await self.client.resolve_peer((await self.client.get_me()).id)
        input_call = (await self.client.invoke(
            GetFullChannel(
                channel=chat
            )
        )).full_chat.call
        result: Updates = await self.client.invoke(
            JoinGroupCall(
                call=input_call,
                join_as=app_peer,
                video_stopped=video_stopped,
                muted=muted,
                params=DataJSON(data=call_params)
            ), sleep_threshold=0, retries=0
        )

        for update in result.updates:
            if isinstance(update, UpdateGroupCallConnection):
                return update.params.data
            
    # abstract methods
            
    async def join_call(
        self: "Caller",
        chat_id: int,
        media: Media = Media(),
        muted: bool = True,
        video_stopped: bool = True,
    ):
        # check app connection
        if not self.client.is_connected:
            await self.client.connect()

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
            video_stopped=video_stopped
        )
        # connection
        await self.wrtc.connect(chat_id, call_data)

    async def run(self):
        await idle()