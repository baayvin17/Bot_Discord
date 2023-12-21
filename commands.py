# commands.py
from googlesearch import search
from googletrans import Translator
from discord.ext import commands
from game import GuessingGame
import discord


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


translator = Translator()
guessing_game = GuessingGame()

# Commande de recherche sur internet
@commands.command(name='search')
async def search_command(ctx, *query):
    query = ' '.join(query)
    await ctx.send(f"Recherche sur internet pour : {query}")

    for j, result in enumerate(search(query, num=5, stop=5, pause=2)):
        await ctx.send(f"Résultat {j + 1}: {result}")

# Commande de traduction
@commands.command(name='translate')
async def translate_command(ctx, target_language, *text):
    text = ' '.join(text)
    translated_text = translator.translate(text, dest=target_language)
    await ctx.send(f"Texte traduit ({translated_text.dest}): {translated_text.text}")


# Nouvelle instance du jeu
guessing_game = GuessingGame()

# Commande pour démarrer le jeu de devinettes
@client.command(name='start_guessing_game')
async def start_guessing_game(ctx):
    global guessing_game
    guessing_game = GuessingGame()
    await ctx.send("Nouveau jeu de devinettes démarré ! Devinez le nombre entre 1 et 100. Pour repondre entrer !guess (nombre) ")

# Commande pour soumettre une devinette
@client.command(name='guess')
async def guess_number(ctx, number: int):
    global guessing_game
    if number < 1 or number > 100:
        await ctx.send("Veuillez deviner un nombre entre 1 et 100.")
        return

    result = guessing_game.guess(number)
    await ctx.send(result)



    