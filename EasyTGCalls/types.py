from ntgcalls import (
    MediaDescription,
    AudioDescription,
    VideoDescription,
    InputMode
)
from typing import Literal, List
from dataclasses import dataclass
import os

INPUT_MODE_MAP = {
    "file": InputMode.FILE,
    "shell": InputMode.SHELL,
    "ffmpeg": InputMode.FFMPEG,
    "no_latenct": InputMode.NO_LATENCY
}
AUDIO_TO_PCM16L = (lambda path, sample_rate, channel_count, log_level="": f"ffmpeg -i {path} {log_level}-f s16le -ac {channel_count} -ar {sample_rate} pipe:1")
REMOVE_VIDEO_AUDIO = (lambda path, fps, width, height, log_level="": f"ffmpeg -i {path} {log_level}-f rawvideo -r {fps} -pix_fmt yuv420p -vf scale={width}:{height} pipe:1")

class Audio:
    def __init__(
        self,
        media_path: str,
        input_mode: Literal["file", "shell", "ffmpeg", "no_latency"] = "shell",
        sample_rate: int = 96000,
        bits_per_sample: int = 16,
        channel_count: int = 2,
        auto_shell_command: bool = True
    ):
        self.raw = media_path
        self.input_mode = input_mode
        self.sample_rate = sample_rate
        self.bits_per_sample = bits_per_sample
        self.channel_count = channel_count

        assert 0 <= sample_rate <= 96000, f"sample_rate should be in range 0-96000 not {sample_rate}"
        assert bits_per_sample in [8, 16], f"bits_per_sample should be either 8 or 16 not {bits_per_sample}"
        assert 0 < channel_count < 3, f"channel_count should be 1 or 2 not {channel_count}"

        if input_mode == "file":

            if not os.path.isfile(self.path):
                raise Exception(f"media file not found {media_path}")
            
            self.path = self.raw
        
        elif input_mode == "shell":

            if auto_shell_command:
                # change voice format to PCM16L
                self.path = AUDIO_TO_PCM16L(self.raw, f"{(str(self.sample_rate//1000)+'k') if self.sample_rate >= 1000 else (str(self.sample_rate))}",self.channel_count)
            else:
                self.path = self.raw

        else:
            self.path = self.raw
        
    def __call__(self) -> AudioDescription:
        return AudioDescription(
            input_mode=INPUT_MODE_MAP[self.input_mode],
            input=self.path,
            sample_rate=self.sample_rate,
            bits_per_sample=self.bits_per_sample,
            channel_count=self.channel_count
        )

class Video:
    def __init__(
        self,
        media_path: str,
        input_mode: Literal["file", "shell", "ffmpeg", "no_latency"] = "shell",
        width: int = 1280,
        height: int = 720,
        fps: int = 30,
        auto_shell_command: bool = True
    ):
        self.raw = media_path
        self.input_mode = input_mode
        self.width = width
        self.height = height
        self.fps = fps

        if input_mode == "file":

            if not os.path.isfile(self.path):
                raise Exception(f"media file not found {media_path}")
            
            self.path = self.raw
        
        elif input_mode == "shell":
            if auto_shell_command:
                self.path = REMOVE_VIDEO_AUDIO(self.raw, self.fps, self.width, self.height)
            else:
                self.path = self.raw
        
        else:
            self.path = self.raw
        
    def __call__(self) -> VideoDescription:
        return VideoDescription(
            input_mode=INPUT_MODE_MAP[self.input_mode],
            input=self.path,
            width=self.width,
            height=self.height,
            fps=self.fps
        )
    
class Media:
    def __init__(
        self,
        audio: Audio = None,
        video: Video = None,
        overwrite_audio: bool = True
    ) -> None:
        self.audio: Audio = audio
        self.video: Video = video
        self.overwrite = overwrite_audio

    def __call__(self) -> MediaDescription:
        # overwrite video audio
        if self.video:
            if self.audio and self.overwrite:
                self.audio.path = self.audio.path.replace(self.audio.raw, self.video.raw)
            elif not self.audio and self.overwrite:
                self.audio = Audio(media_path=self.video.raw)
            else:
                pass

        return MediaDescription(
            audio=None if not self.audio else self.audio(),
            video=None if not self.video else self.video()
        )

@dataclass
class VoiceMediaState:
    muted: bool
    video_paused: bool
    video_stopped: bool