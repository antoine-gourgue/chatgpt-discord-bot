import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Initialisez l'API d'OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configurez les intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialisez le bot Discord avec les Intents
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')


@bot.command()
async def chat(ctx, *, question):
    try:
        response = openai.Completion.create(engine="curie", prompt=question, max_tokens=150)
        await ctx.send(response.choices[0].text.strip())
    except Exception as e:
        await ctx.send(f"Erreur : {e}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"Erreur : {error}")
    raise error


bot.run(os.getenv('DISCORD_BOT_TOKEN'))
