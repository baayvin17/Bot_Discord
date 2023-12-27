# commands.py

from googletrans import Translator
from discord.ext import commands
from game import GuessingGame
import discord
from game import CapitalQuizGame
from game import HangmanGame


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


translator = Translator()
guessing_game = GuessingGame()
hangman_game = None


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
    global quiz_game  # Assure que la variable quiz_game est globale et accessible

    # Vérifie si le jeu de quiz a été initialisé
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
            quiz_game = None  # Réinitialise le jeu pour permettre de commencer un nouveau quizz

@commands.command(name='jeu')
async def jeu_command(ctx):
    games_available = "Voici les jeux disponibles :\n" \
                      "1. Guessing Game (!start_guessing_game)\n" \
                      "2. Capital Quiz Game (!quizz)\n"\
                      "3. Hangman Game (!pendu)"
    await ctx.send(games_available)


@client.command(name='pendu')
async def start_pendu(ctx):
    global hangman_game

    if not hangman_game:
        hangman_game = HangmanGame()

    instructions = hangman_game.display_instructions()
    word_display = hangman_game.display_word()
    hangman_display = hangman_game.display_hangman()

    await ctx.send(f"{instructions}\nMot à deviner : {word_display}\n{hangman_display}\nPour répondre, utilisez !guess_pendu (lettre)")

@client.command(name='guess_pendu')
async def guess_pendu(ctx, letter):
    global hangman_game

    if not hangman_game:
        await ctx.send("Le jeu du pendu n'a pas encore commencé. Utilisez !pendu pour commencer.")
    else:
        result = hangman_game.guess(letter)
        instructions = hangman_game.display_instructions()
        word_display = hangman_game.display_word()
        hangman_display = hangman_game.display_hangman()

        await ctx.send(f"{instructions}\n{result}\nMot partiel : {word_display}\n{hangman_display}\nPour répondre, utilisez !guess_pendu (lettre)")

        if '_' not in hangman_game.word_display:
            await ctx.send("Félicitations ! Vous avez deviné le mot.")
            hangman_game = None  # Réinitialise le jeu pour permettre de commencer un nouveau jeu du pendu

        elif hangman_game.attempts_left == 0:
            await ctx.send(f"Désolé, vous avez épuisé toutes vos tentatives. Le mot était : {hangman_game.word_to_guess}")
            hangman_game = None  # Réinitialise le jeu pour permettre de commencer un nouveau jeu du pendu
