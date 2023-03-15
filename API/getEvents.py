from dotenv import load_dotenv
import os
import discord
import asyncio
from fastapi import FastAPI
load_dotenv()

app = FastAPI()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for guild in client.guilds:
        print(f"- {guild.name} (id: {guild.id})")


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

#####################################################################

# Get all Messages from the server

@client.event
async def on_message(message):
    message_data = {
        "message_id": message.id,
        "channel_id": message.channel.id,
        "channel_name":message.channel.name,
        "author_id": message.author.id,
        "author_name":message.author.name,
        "content": message.content,
        "timestamp": message.created_at.timestamp()
    }
    print(message_data)
    # You can also store this message data in a database or send it to another API endpoint

# Trigger Thread Events

@client.event
async def on_thread_member_join(member: discord.ThreadMember):
    thread = member.thread
    print(f"{member.id} joined thread {thread.name} ({thread.id})")

@client.event
async def on_thread_member_remove(member: discord.ThreadMember):
    thread = member.thread
    print(f"{member.id} left thread {thread.name} ({thread.id})")

# Trigger Voice Events

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        # User joined a voice channel
        print(f"{member} joined {after.channel}")
    elif before.channel is not None and after.channel is None:
        # User left a voice channel
        print(f"{member} left {before.channel}")
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        # User switched voice channels
        print(f"{member} switched from {before.channel} to {after.channel}")
    elif before.channel is None and after.channel is None:
        # User did not change voice channels
        print(f"{member} is not in a voice channel")


# Trigger Reaction Events

@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user_id = payload.user_id
    reaction = payload.emoji.name

    reaction_data = {
        "message_id": message.id,
        "channel_id": channel.id,
        "reaction": reaction,
        "user_id": user_id
    }
    print(f"Reaction added {reaction_data}")


@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user_id = await client.fetch_user(payload.user_id)
    reaction = payload.emoji.name
    reaction_data = {
        "message_id": message.id,
        "channel_id": channel.id,
        "reaction": reaction,
        "user_id": user_id
    }
    print(f"Reaction removed {reaction_data}")

# Trigger Member Events

@client.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        # Member roles have been updated
        added_roles = [role for role in after.roles if role not in before.roles]
        removed_roles = [role for role in before.roles if role not in after.roles]
        print(f"Member {after.id} updated their roles. Added roles: {added_roles}. Removed roles: {removed_roles}")

@client.event
async def on_member_join(member):
    print(f"{member.id} has joined the server!")

@client.event
async def on_member_remove(member):
   print(f"{member.id} has left the server!")
  

# Trigger Stage Events

# async def on_stage_instance_create(stage_instance:discord.StageInstance):
#     print("It is triggered")
#     print(f"Stage instance created: {stage_instance.topic} in channel {stage_instance.channel.name}")

# async def on_stage_instance_delete(stage_instance):
#     print("It is triggered2")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))