from ntgcalls import InputMode
from EasyTGCalls.types import Media, Video, Audio, REMOVE_VIDEO_AUDIO, AUDIO_TO_PCM16L
import asyncio

async def youtube_video(
    url,
    quality: str = None,
    audio_only: bool = False,
    sample_rate = 96000,
    channel_count = 2,
    bits_per_sample = 16,
    w = 1920,
    h = 1080,
    fps = 60,
) -> Media:
    if not audio_only:
        format = "bestvideo+bestaudio/best" if not quality else f"bv[height<={quality}]+ba/best[height<={quality}]"
    else:
        format = "bestaudio/best" if not quality else f"ba/best[height<={quality}]"

    process = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        format,
        url,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    out, err = await process.communicate()
    links = out.decode().split('\n')
    video, audio = links[0], links[1]

    return Media(
        audio=Audio(
            media_path=AUDIO_TO_PCM16L(
                path=audio if not audio_only else video,
                sample_rate=sample_rate,
                channel_count=channel_count,
                log_level="-loglevel panic "
            ),
            sample_rate=sample_rate,
            channel_count=channel_count,
            bits_per_sample=bits_per_sample,
            auto_shell_command=False
        ),
        video=None if audio_only else Video(
            media_path=REMOVE_VIDEO_AUDIO(
                path=video,
                width=w,
                height=h,
                fps=fps,
                log_level="-loglevel panic "
            ),
            width=w,
            height=h,
            fps=fps,
            auto_shell_command=False
        ),
        overwrite_audio=False
    )