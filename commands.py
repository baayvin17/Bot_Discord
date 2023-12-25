# commands.py

from googletrans import Translator
from discord.ext import commands
from game import GuessingGame
import discord
from game import CapitalQuizGame


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


translator = Translator()
guessing_game = GuessingGame()


# Commande de traduction
@commands.command(name='translate')
async def translate_command(ctx, target_language, *text):
    text = ' '.join(text)
    translated_text = translator.translate(text, dest=target_language)
    await ctx.send(f"Texte traduit ({translated_text.dest}): {translated_text.text}")



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

quiz_game = None

@client.command(name='quizz')
async def start_quizz(ctx):
    global quiz_game  

    
    if not quiz_game:
        quiz_game = CapitalQuizGame()

    await ctx.send("Bienvenue au quizz sur les capitales ! Répondez simplement avec !answer+reponse ")
    question = quiz_game.get_next_question()
    await ctx.send(question)

@client.command(name='answer')
async def answer_quizz(ctx, user_answer):
    global quiz_game  

    
    if not quiz_game:
        await ctx.send("Le quizz n'a pas encore commencé. Utilisez !quizz pour commencer.")
    else:
        # Vérifie la réponse et affiche le résultat
        result = quiz_game.check_answer(user_answer)
        await ctx.send(result)

        # Vérifie s'il y a une prochaine question
        next_question = quiz_game.get_next_question()
        if next_question:
            await ctx.send(next_question)
        else:
            # Le quizz est terminé, affiche le score final
            score = quiz_game.get_score()
            await ctx.send(f"Quizz terminé ! {score}")
            quiz_game = None  

@commands.command(name='jeu')
async def jeu_command(ctx):
    games_available = "Voici les jeux disponibles :\n" \
                      "1. Guessing Game (!start_guessing_game)\n" \
                      "2. Capital Quiz Game (!quizz)"
    await ctx.send(games_available)
