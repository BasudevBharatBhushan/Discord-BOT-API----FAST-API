import os
import discord
import asyncio
from fastapi import FastAPI

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    message_data = {
        "id": message.id,
        "channel_id": message.channel.id,
        "channel_name":message.channel.name,
        "author_id": message.author.id,
        "author_name":message.author.name,
        "content": message.content,
        "timestamp": message.created_at.timestamp()
    }
    print(message_data)
    # You can also store this message data in a database or send it to another API endpoint

async def start_bot():
    await client.start('MTA4NDg3MTM5ODk5Mzk1Mjg3OQ.GDhhcQ.jyqIylWR2jmdCEK2FF0dJdQL9yv5-ZnVCZBU18')

async def stop_bot():
    await client.close()

@app.on_event("startup")
async def startup():
    asyncio.create_task(start_bot())

@app.on_event("shutdown")
async def shutdown():
    asyncio.create_task(stop_bot())

@app.get('/messages')
async def get_messages():
    messages = []
    for channel in client.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=100):
                message_data = {
                    "id": message.id,
                    "channel_id": message.channel.id,
                    "channel_name":message.channel.name,
                    "author_id": message.author.id,
                    "author_name":message.author.name,
                    "content": message.content,
                    "timestamp": message.created_at.timestamp()
                }
                messages.append(message_data)
    return messages

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
