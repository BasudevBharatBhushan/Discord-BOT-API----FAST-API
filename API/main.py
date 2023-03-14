import discord

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
    
    print(f'Message received: {message.content} Message Author:{message.author}')
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
client.run('MTA4NDg3MTM5ODk5Mzk1Mjg3OQ.GDhhcQ.jyqIylWR2jmdCEK2FF0dJdQL9yv5-ZnVCZBU18')