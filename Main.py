import os
import discord
import openai
from discord.ext import commands

# Load environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup clients
openai.api_key = OPENAI_API_KEY
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 OX AI is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for the "!ask" command
    if message.content.startswith("!ask"):
        prompt = message.content[len("!ask "):]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are OX AI — a friendly, intelligent Discord assistant made by Deadox.
You belong to the Ox AI Discord server.
You were created through the hard work and creativity of the Deadox team.
You help users, answer questions, and represent the server with pride.
If someone asks about who made you or where you are from, tell them proudly:
‘I was created by Deadox and belong to the Ox AI community.’
                        """
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message["content"]
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send(f"⚠️ Error: {e}")

# Run bot
bot.run(DISCORD_TOKEN)
