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


@client.event
async def on_message(message):
    # if message.author == client.user:
    #     return
    
    print(f'Author:{message.author} Message received: {message.content} Author_Id: {message.author.id} ')
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

@client.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        # Member roles have been updated
        added_roles = [role for role in after.roles if role not in before.roles]
        removed_roles = [role for role in before.roles if role not in after.roles]
        print(f"Member {after.id} updated their roles. Added roles: {added_roles}. Removed roles: {removed_roles}")

@client.event
async def on_member_join(member):
    invite = await get_invite(member)
    print(invite)
    if invite is not None:
        invite_data = {
            "code": invite.code,
            "inviter_id": invite.inviter.id,
            "uses": invite.uses,
            "max_uses": invite.max_uses
        }
        print(f"Member {member.id} joined using invite: {invite_data}")

    print(f"{member.id} has joined the server!")

@client.event
async def on_member_remove(member):
    # Do something when a member leaves or is kicked from the server
   print(f"{member.id} has left the server!")
  


async def get_invite(member):
    invites = await member.guild.invites()
    for invite in invites:
        if invite.uses < invite.max_uses and invite.inviter == member:
            # This invite link was used by the member to join the server
            return invite
    return None




async def on_stage_instance_create(stage_instance):
    print(f"Stage instance created: {stage_instance.topic} in channel {stage_instance.channel.name}")
        
client.run('MTA4NDg3MTM5ODk5Mzk1Mjg3OQ.Ggis5C.p872h_wGAHV_xw5YH6Cu7BwgJfMpeCKwLAjkUo')