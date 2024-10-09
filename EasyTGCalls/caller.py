from pyrogram import Client, idle
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import JoinGroupCall, LeaveGroupCall, GetGroupCall
from pyrogram.raw.types import UpdateGroupCallConnection, Updates, DataJSON, GroupCall
from ntgcalls import NTgCalls, MediaDescription
from typing import Union
from EasyTGCalls.types import Media
from EasyTGCalls.stream_methods import StreamMethods

class Caller(StreamMethods):
    def __init__(
        self: "Caller",
        pyro_client: Client,
        wrtc: NTgCalls = None
    ):
        self.wrtc = wrtc or NTgCalls()
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

    # thanks for the examples Laky64
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

    async def get_call(
        self,
        chat_id
    ) -> Union[bool, GroupCall]:
        # check app connection
        if not self.client.is_connected:
            await self.client.connect()

        call = (await self.client.invoke(GetFullChannel(
            channel=await self.client.resolve_peer(chat_id)
        ))).full_chat.call

        if not call:
            return False

        call = (await self.client.invoke(GetGroupCall(
            call=call,
            limit=-1
        )))

        return call
            
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
            video_stopped=video_stopped,
        )
        # connection
        await self.wrtc.connect(chat_id, call_data)

    async def leave_call(
        self,
        chat_id: int
    ) -> bool:
        # check app connection
        if not self.client.is_connected:
            await self.client.connect()

        call = (await self.client.invoke(GetFullChannel(
            channel=await self.client.resolve_peer(chat_id)
        ))).full_chat.call

        if not call:
            return False

        r = await self.client.invoke(LeaveGroupCall(
            call=call,
            source=0,
        ))
        return None or r.updates

    async def run(self):
        await idle()