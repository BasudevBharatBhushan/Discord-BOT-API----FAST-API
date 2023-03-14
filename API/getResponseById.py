from dotenv import load_dotenv
import os
import discord
import asyncio
from fastapi import FastAPI, HTTPException
from discord.utils import get
from discord import Permissions

load_dotenv()

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

#######################################################################

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

      # Debug statement to check if the bot is able to find the server
    for guild in client.guilds:
        print(f"Bot is connected to server: {guild.name}")

    # Debug statement to check if the bot is able to find the "Bot" role
    global bot_role
    bot_role = get(client.guilds[0].roles, name="Bot")
    if bot_role is not None:
        print(f"Bot role found: {bot_role.name}")
    else:
        print("Bot role not found")

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

######################################################################

# Fetch Message by ID

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


# Fetch Reaction by user_ID and Channel_ID

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

# Fetch Avatar by user_id

@app.get('/user/pfp/{user_id}')
async def get_user_pfp(user_id:int):
    user = await client.fetch_user(user_id)
    return str(user.avatar.url)

# Fetch Server Invites

@app.get('/server-invites')
async def get_server_invites():
    invites = await client.guilds[0].invites()
    invite_data = []
    for invite in invites:
        invite_data.append({
            "code": invite.code,  #Invite Code
            "uses": invite.uses,  # How many times the code has been used (How many users accepted the invite)
            "max_uses": invite.max_uses, # Max no of times invite can be used (0 if it is unlimited)
            "inviter_id": invite.inviter.id  # Id of the user who invites
        })
    return invite_data

# Fetch Server Invites by user_id
@app.get('/server-invites/{user_id}')
async def get_server_invites_by_user(user_id: int):
    invites = await client.guilds[0].invites()
    invite_data = []
    for invite in invites:
        if invite.inviter.id == user_id:
            invite_data.append({
                "code": invite.code,  #Invite Code
                "uses": invite.uses,  # How many times the code has been used (How many users accepted the invite)
                "inviter_id": invite.inviter.id,  # Id of the user who invites
            })
    return invite_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
