# Discord BOT API | Fast API [PYTHON]

## Steps to run in local machine

- Step 1: Clone the Repo  
  ` git clone https://github.com/BasudevBharatBhushan/Discord-BOT-API----FAST-API`

- Step 2: Create a Virtual Env  
  ` python -m discordapi-env`

- Step 3: Activate the env  
  ` discordapi-env\Scripts\activate.bat`

- Step 4: Install the dependencies  
  ` pip3 install -r requirements.txt`

- Step 5: Add .enf file  
  `DISCORD_BOT_TOKEN =[Enter your Discord Bot Token] `
  See Here - [How to create a Discord BOT](#create-a-discord-bot)

- Step 5: Start the Server

  - get_API_Call - `  uvicorn API.getResponse:app --reload`
  - event_Trigger - `  uvicorn API.getEvents:app --reload`

- Step 6: Go to Swagger UI to test API  
  ` localhost:8000/docs`

## Alternatively the Discord API can be also tested through Python Launcher

- Step 1: cd into the API  
  `cd .\API`
- Step 2: Run the Application  
  `py -3 events.py`

## Create a Discord BOT

- Step 1: Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Step 2: Click New Application & give a name
- Step 3: Go to the "Bot" tab and click "Add Bot". Give your bot a name and optionally upload an avatar image.
- Step 4: Under the "Token" section, click "Copy" to copy your bot token.
  > **_NOTE:_** Keep this token secret!
- Step 5: Check the intents and scopes as per the need
- Step 6: Go to OAuth2 , Copy the Client ID and Visit  
  ` https://discord.com/api/oauth2/authorize?client_id=[Copied Client ID]&scope=bot`
- Step 7: Choose the Server, where you want to add the bot to and then authorize.

### Switch On the Applicaton Test Mode for Your Bot

- Step 1 - Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Step 2 - Copy Application ID
- Step 3 - Go to Discord Setting > APP SETTINGS > Advanced > Application Test Mode > Paste the Application ID

> **_NOTE:_** You might have to billing method to be enable Application Mode

# Reference

- [Discord Python SDK](https://discordpy.readthedocs.io/en/stable/index.html)

- [Event References](https://discordpy.readthedocs.io/en/stable/api.html#event-reference)

- [Stage Event](https://discordpy.readthedocs.io/en/latest/api.html?highlight=on_stage_instance_create#discord.on_stage_instance_create)

- Fetch Message

  - [TextChannel.history](https://discordpy.readthedocs.io/en/stable/api.html?highlight=textchannel.history#discord.TextChannel.history)
  - [Message](https://discordpy.readthedocs.io/en/stable/api.html?highlight=discord%20message#discord.Message)

- [Fetch Reaction](https://discordpy.readthedocs.io/en/stable/api.html#discord.Reaction)

- [Fetching Avatar (pfp)](https://discordpy.readthedocs.io/en/stable/api.html?highlight=user%20avatar_url#discord.User.avatar_url)

- [Fetching Invites](https://discordpy.readthedocs.io/en/stable/api.html?highlight=guild%20invites#discord.Guild.invites)

- [Thread Event](https://discordpy.readthedocs.io/en/latest/api.html?highlight=on_thread_join#discord.on_thread_join)

- [Voice Event](https://discordpy.readthedocs.io/en/latest/api.html#discord.on_voice_state_update)
