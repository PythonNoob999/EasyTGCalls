from setuptools import setup

setup(
    name="EasyTGCalls",
    version="1.0.0",
    description="Easy Telegram Calls is a Python library designed to simplify making calls using the Telegram API. It abstracts the complexity of interacting with Telegram's API, allowing developers to easily integrate voice and video calls into their applications.",
    author="SpicyPenguin",
    packages=["EasyTGCalls"],
    install_requires=["ntgcalls", "pyrogram"]
)