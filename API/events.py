# from dotenv import load_dotenv
import discord
# import os

# load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#set stage instance intent be true (Unable to found it in doc)
# intents.stage_instances = True



client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    for guild in client.guilds:
        print(f"- {guild.name} (id: {guild.id})")


# @client.event
# async def on_message(message):
#     # if message.author == client.user:
#     #     return
    
#     print(f'Author:{message.author} Message received: {message.content} Author_Id: {message.author.id} ')
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')



@client.event
async def on_thread_member_join(member: discord.ThreadMember):
    thread = member.thread
    print(f"{thread.id} --- {member}")
    # print(f"{member.name} joined thread {thread.name} ({thread.id})")

@client.event
async def on_thread_member_remove(member: discord.ThreadMember):
    thread = member.thread
    print(f"{thread.id} --- {member}")
    # print(f"{member.name} left thread {thread.name} ({thread.id})")


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



async def on_stage_instance_create(stage_instance):
    print(f"Stage instance created: {stage_instance.topic} in channel {stage_instance.channel.name}")
        
client.run('')