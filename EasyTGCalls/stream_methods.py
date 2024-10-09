from EasyTGCalls.types import VoiceMediaState, Media

class StreamMethods:
    # stream methods
    async def change_media(
        self,
        chat_id: int,
        new_media: Media
    ):
        return await self.wrtc.change_stream(
            chat_id,
            new_media()
        )
    
    async def mute(self, chat_id: int) -> bool:
        return await self.wrtc.mute(chat_id)
    
    async def pause(self, chat_id: int) -> bool:
        return await self.wrtc.pause(chat_id)
    
    async def resume(self, chat_id: int) -> bool:
        return await self.wrtc.resume(chat_id)

    async def unmute(self, chat_id: int) -> bool:
        return await self.wrtc.unmute(chat_id)

    async def get_voice_status(self, chat_id: int) -> VoiceMediaState:
        state = await self.wrtc.get_state(chat_id)
        return VoiceMediaState(
            muted=state.muted,
            video_paused=state.video_paused,
            video_stopped=state.video_stopped
        )