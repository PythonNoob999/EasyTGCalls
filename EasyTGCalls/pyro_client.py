from pyrogram import Client 
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import (
    JoinGroupCall,
    LeaveGroupCall,
    GetGroupCall
)
from pyrogram.raw.types import (
    InputPeerChannel,
    InputPeerChat,
    InputGroupCall,
    DataJson,
    Updates,
    GroupCall
)
from pyrogram.raw.base import InputPeer
from pyrogram.raw.types.messages import (
    ChatFull
)
from typing import Union

class Pyro(Client):
    def __init__(
        self,
        client: Client
    ):
        self.client= client
    
    def connected(func):
        async def check_connection(self, *args, **kwargs):
            if not self.client.is_connected:
                await self.client.connect()
            
            return await func(self, *args, **kwargs)

        return check_connection

    ## define abstraction for low-level methods

    @connected
    async def get_full_channel(
        self,
        chat_peer: Union[int, InputPeerChannel, InputPeerChat]
    ) -> ChatFull:
        if isinstance(chat_peer, int):
            chat_peer = await self.client.resolve_peer(chat_peer)

        return await self.client.invoke(
            GetFullChannel(
                channel=chat_peer
            )
        )
    
    @connected
    async def join_group_call(
        self,
        call: InputGroupCall,
        video_stopped: bool,
        muted: bool,
        params: DataJson,
        join_as: InputPeer= None,
        sleep_threshhold: int = 9,
        retries: int = 0,
    ) -> Updates:
        if join_as is None:
            join_as = await self.client.resolve_peer((await self.client.get_me()).id)
        
        return await self.client.invoke(
            JoinGroupCall(
                call=call,
                join_as=join_as,
                params=params,
                muted=muted,
                video_stopped=video_stopped,
            ),
            sleep_threshold=sleep_threshhold,
            retries=retries
        )
    
    @connected
    async def get_group_call(
        self,
        call: InputGroupCall,
        limit: int = -1
    ) -> GroupCall:
        return await self.client.invoke(
            GetGroupCall(
                call=call,
                limit=limit
            )
        )
    
    @connected
    async def leave_group_call(
        self,
        call: InputGroupCall,
        source=0
    ) -> Updates:
        return await self.client.invoke(
            LeaveGroupCall(
                call=call,
                source=source
            )
        )