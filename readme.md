# Easy Telegram Calls 

`Easy Telegram Calls` is a Python library designed to simplify making calls using the Telegram API. It abstracts the complexity of interacting with Telegram's API, allowing developers to easily integrate voice and video calls into their applications.

## Features

- Simple interface to initiate/join voice and video calls on Telegram.
- Easily configure call parameters.
- Asynchronous.
- Minimal dependencies for easy integration.

## Installation

Not Yet Finished

## Usage

Here’s an example of how to initiate a Telegram call:

```python
from EasyTGCalls import Caller, Media, Video
from pyrogram import Client
import asyncio

async def main():
    chat_id = -1002416874723
    app = Client(":memory:", ...)
    client = Caller(app)

    # media is optional
    await client.join_call(
        chat_id=chat_id,
        media=Media(
            video=Video("video.mp3")
        )
    )

    # calls pyrogram idle
    await client.run()

asyncio.run(main())
```

## Getting Started

### Prerequisites

- Python 3.8+
- [ntgcalls](https://github.com/pytgcalls/ntgcalls/tree/master)

### Calls Example


#### Joining voice chat

```python
from EasyTGCalls import Caller, Media, Video
from pyrogram import Client
import asyncio

async def main():
    chat_id = -1002416874723
    app = Client(":memory:", ...)
    client = Caller(app)

    # media is optional
    await client.join_call(
        chat_id=chat_id,
        media=Media(
            video=Video("video.mp3")
        )
    )

    # calls pyrogram idle
    await client.run()

asyncio.run(main())
```

#### playing a youtube video (yt-dlp required)

```python
from EasyTGCalls import Caller, youtube_video
from pyrogram import Client
import asyncio

async def main():
    chat_id = -1002416874723
    app = Client(":memory:", ...)
    client = Caller(app)
    video = await youtube_video("https://www.youtube.com/watch?v=xvFZjo5PgG0")

    # join & play a youtube video
    await client.join_call(
        chat_id=chat_id,
        media=video
    )

    # calls pyrogram idle
    await client.run()

asyncio.run(main())
```

## Contributing

We welcome contributions! If you'd like to contribute, please fork the repository and create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.