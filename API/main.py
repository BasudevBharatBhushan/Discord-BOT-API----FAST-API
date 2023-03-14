from dotenv import load_dotenv
import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # if message.author == client.user:
    #     return
    
    print(f'Author:{message.author} Message received: {message.content} Author_Id: {message.author.id} ')
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')



@client.event
async def on_stage_instance_create(stage_instance):
    stage_data = {
        "channel_id": stage_instance.channel.id,
        "topic": stage_instance.topic,
        "start_time": stage_instance.start_time.timestamp()
    }
    print(stage_data)
        
client.run(os.getenv("DISCORD_BOT_TOKEN"))