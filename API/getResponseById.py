from dotenv import load_dotenv
import os
import discord
import asyncio
from fastapi import FastAPI, HTTPException
load_dotenv()

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


async def start_bot():
    await client.start(os.getenv("DISCORD_BOT_TOKEN"))

async def stop_bot():
    await client.close()

@app.on_event("startup")
async def startup():
    asyncio.create_task(start_bot())

@app.on_event("shutdown")
async def shutdown():
    asyncio.create_task(stop_bot())

@app.get('/messages/{user_id}')
async def get_messagesById(user_id:int = None):
    messages = []
    for channel in client.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            async for message in channel.history(limit=100):
                if user_id is not None and message.author.id != user_id:
                    continue
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


@app.get('/reactions/{channel_id}/{user_id}')
async def get_reaction_by_id(channel_id: int, user_id: int):
    channel = client.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")

    reactions = []
    async for message in channel.history(limit=None):
        for reaction in message.reactions:
            if user_id in [user.id async for user in reaction.users()]:
                reaction_data = {
                    "message_id": message.id,
                    "channel_id": message.channel.id,
                    "reaction": reaction.emoji,
                    "count": reaction.count,
                    "users": [user.id async for user in reaction.users()]
                }
                reactions.append(reaction_data)
    return reactions

@app.get('/user/pfp/{user_id}')
async def get_user_pfp(user_id:int):
    user = await client.fetch_user(user_id)
    return str(user.avatar.url)

@client.event
async def on_stage_instance_create(stage_instance):
    stage_data = {
        "channel_id": stage_instance.channel.id,
        "topic": stage_instance.topic,
        "start_time": stage_instance.start_time.timestamp()
    }
    print(stage_data)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
