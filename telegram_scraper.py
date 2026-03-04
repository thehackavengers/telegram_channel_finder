import asyncio
import random
from telethon import TelegramClient
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import FloodWaitError

from metadata import extract_metadata
from rate_limiter import random_delay


class TelegramScraper:

    def __init__(self, api_id, api_hash):

        self.client = TelegramClient("fiu_session", api_id, api_hash)
        self.seen = set()
        self.results = []

    async def start(self):
        await self.client.start()

    async def search_keyword(self, keyword):

        try:

            result = await self.client(
                SearchRequest(
                    q=keyword,
                    limit=100
                )
            )

            for chat in result.chats:

                if chat.id in self.seen:
                    continue

                if chat.username is None:
                    continue

                self.seen.add(chat.id)

                meta = await self.get_channel_info(chat, keyword)

                if meta:
                    self.results.append(meta)

                await random_delay()

        except FloodWaitError as e:

            print("Flood wait:", e.seconds)
            await asyncio.sleep(e.seconds)

    async def get_channel_info(self, channel, keyword):

        try:

            full = await self.client(
                GetFullChannelRequest(channel)
            )

            meta = extract_metadata(channel, full, keyword)

            return meta

        except Exception as e:

            print("Error:", e)

            return None

    async def discover_related(self, channel):

        async for msg in self.client.iter_messages(channel, limit=200):

            if msg.forward and msg.forward.chat:

                chat = msg.forward.chat

                if chat.username and chat.id not in self.seen:

                    self.seen.add(chat.id)

                    meta = await self.get_channel_info(chat, "related")

                    if meta:
                        self.results.append(meta)

    async def run(self, keywords):

        await self.start()

        for k in keywords:

            await self.search_keyword(k)

        return self.results