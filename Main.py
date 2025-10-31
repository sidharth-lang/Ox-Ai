import discord
import openai
import nest_asyncio
import asyncio

# --- IMPORTANT: Replace with your own tokens ---
DISCORD_TOKEN = "YOUR_DIACORD_TOKEN_HERE"
OPENAI_API_KEY = "YOUR_OPENAI_KEY_HERE"

# Setup
openai.api_key = OPENAI_API_KEY
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Only respond if message starts with "!"
    if message.content.startswith("!"):
        prompt = message.content[1:]
        await message.channel.send("🤖 Thinking...")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are OX AI, a helpful Discord assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response["choices"][0]["message"]["content"]
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send(f"❌ Error: {e}")

# Fix asyncio for Colab
nest_asyncio.apply()

async def start_bot():
    await client.start(DISCORD_TOKEN)

asyncio.run(start_bot())
