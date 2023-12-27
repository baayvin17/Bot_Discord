import asyncio
import discord
from discord.ext import commands
import json
from commands import  translate_command, start_guessing_game, guess_number, answer_quizz, start_quizz
from commands import jeu_command, start_pendu, guess_pendu
    

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)

class TreeNode:
    def __init__(self, question, yes_node=None, no_node=None, answer=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node
        self.answer = answer

    async def ask_question(self, ctx):
        await ctx.send(self.question)
        response = await wait_for_yes_or_no(ctx)

        if response:
            if self.yes_node:
                await self.yes_node.ask_question(ctx)
            elif self.answer:
                await ctx.send(self.answer)
            else:
                await ctx.send("Conversation terminée.")
        else:
            if self.no_node:
                await self.no_node.ask_question(ctx)
            elif self.answer:
                await ctx.send(self.answer)
            else:
                await ctx.send("Conversation terminée.")

    async def reset_conversation(self, ctx):
        await ctx.send("La conversation a été réinitialisée.")
        await start_questionnaire(ctx)

    async def speak_about(self, ctx, topic):
        valid_topics = {"repas", "pates", "pizza", "nourritures", "burger"}

        if topic.lower() in valid_topics:
            await ctx.send(f"Oui, je peux parler de {topic}.")
        else:
            await ctx.send(f"Non, je ne parle pas de {topic} dans cette conversation.")

    def get_supported_topics(self):
        topics = set()
        if self.yes_node:
            topics.update(self.yes_node.get_supported_topics())
        if self.no_node:
            topics.update(self.no_node.get_supported_topics())
        return topics

async def wait_for_yes_or_no(ctx):
    def check(message):
        return message.author == ctx.author and message.content.lower() in ["oui", "non"]

    try:
        response = await ctx.bot.wait_for("message", check=check, timeout=30)
        return response.content.lower() == "oui"
    except asyncio.TimeoutError:
        await ctx.send("Temps écoulé. Conversation terminée.")
        return False

# Arbre de décision mis à jour
root_node = TreeNode(
    "Aimez-vous les pizzas?",
    yes_node=TreeNode(
        "Voulez-vous de la sauce tomate sur votre pizza?",
        yes_node=TreeNode(
            "Préférez-vous une garniture végétarienne?",
            yes_node=TreeNode(
                "Aimez-vous les champignons?",
                yes_node=TreeNode(question="Fin, vous pourriez aimer une pizza aux champignons et légumes!"),
                no_node=TreeNode(question="Fin, une pizza aux légumes pourrait vous plaire!")
            ),
            no_node=TreeNode(
                "Voulez-vous des ingrédients épicés?",
                yes_node=TreeNode(question="Fin, une pizza pepperoni épicée pourrait être votre choix!"),
                no_node=TreeNode(question="Fin, une pizza margherita pourrait vous plaire.")
            )
        ),
        no_node=TreeNode(  
            "Voulez-vous de la crème fraîche sur votre pizza?",
            yes_node=TreeNode(
                "Voulez-vous une pizza avec du poisson?",
                yes_node=TreeNode(
                    "Voulez-vous du saumon sur votre pizza?",
                    yes_node=TreeNode(question="Fin, optez pour une pizza crème fraîche saumon."),
                    no_node=TreeNode(question="Fin, pas de pizza au poisson, à part le saumon.")
                ),
                no_node=TreeNode(
                    "Voulez-vous du poulet curry sur votre pizza?",
                    yes_node=TreeNode(question="Fin, optez pour une pizza crème fraiche au poulet curry."),
                    no_node=TreeNode(question="Fin, optez pour une pizza sans crème fraîche mais avec des légumes.")
                )
            )
        )
    ),
    no_node=TreeNode(
        "Aimez-vous les pâtes?",
        yes_node=TreeNode(
            "Aimeriez-vous les pâtes à la sauce tomate?",
            yes_node=TreeNode(
                "Aimeriez-vous la viande hachée?",
                yes_node=TreeNode(
                    "Préférez-vous des pâtes épicées?",
                    yes_node=TreeNode(
                        "Aimeriez-vous des pâtes à la bolognaise épicées?",
                        yes_node=TreeNode(question="Fin, des pâtes à la bolognaise épicées pourraient être délicieuses !"),
                        no_node=TreeNode(question="Fin, des pâtes à la bolognaise classiques pourraient vous plaire.")
                    ),
                    no_node=TreeNode(
                        "Aimeriez-vous des pâtes aux olives et tomates séchées?",
                        yes_node=TreeNode(question="Fin, essayez des pâtes aux olives et tomates séchées peut-être."),
                        no_node=TreeNode(question="Fin, explorez d'autres options de sauce pour vos pâtes.")
                    )
                )
            ),
            no_node=TreeNode(
                "Aimeriez-vous les pâtes à la crème fraîche?",
                yes_node=TreeNode(
                    "Aimeriez-vous du poulet dans vos pâtes à la crème fraîche?",
                    yes_node=TreeNode(question="Fin, des pâtes Alfredo au poulet pourraient vous plaire !"),
                    no_node=TreeNode(
                        "Aimeriez-vous du saumon dans vos pâtes à la crème fraîche?",
                        yes_node=TreeNode(question="Fin, des pâtes au saumon avec de la crème fraîche pourraient vous plaire."),
                        no_node=TreeNode(question="Fin, explorez d'autres options de sauce pour vos pâtes.")
                    )
                ),
                no_node=TreeNode(
                    "Aimeriez-vous les pâtes avec une autre sauce que la tomate et la crème fraîche?",
                    yes_node=TreeNode(question="Fin, explorez d'autres options de sauce pour vos pâtes."),
                    no_node=TreeNode(question="Fin, optez pour un autre repas.")
                )
            )
        ),
        no_node=TreeNode(
            "Préférez-vous les burgers?",
            yes_node=TreeNode(
                "Aimez-vous les burgers végétariens?",
                yes_node=TreeNode(
                    "Aimez-vous les alternatives de viande?",
                    yes_node=TreeNode(
                        "Aimez-vous les burgers végétariens classiques(oui) ou épicés?(non)",
                        yes_node=TreeNode(question="Fin, essayez un burger végétarien classique."),
                        no_node=TreeNode(question="Fin, explorez des options de burgers végétariens épicés.")
                    )
                ),
                no_node=TreeNode(
                    "Aimez-vous les burgers classiques?",
                    yes_node=TreeNode(
                        "Un burger classique au poulet?",
                        yes_node=TreeNode(question="Fin, optez pour un burger classique au poulet."),
                        no_node=TreeNode(question="Fin, optez pour un burger classique au steak.")
                    ),
                    no_node=TreeNode(
                        "Aimez-vous les burgers avec des ingrédients spécifiques?",
                        yes_node=TreeNode(
                            "Aimez-vous les burgers avec du fromage?",
                            yes_node=TreeNode(
                                "Préférez-vous un burger avec du fromage fondu(oui) ou du fromage bleu(non) ?",
                                yes_node=TreeNode(question="Fin, essayez un burger avec du fromage fondu."),
                                no_node=TreeNode(question="Fin, optez pour un burger avec du fromage bleu.")
                            )
                        ),
                        no_node=TreeNode(question="Fin, explorez d'autres options de burgers avec des ingrédients spécifiques.")
                    )
                )
            ),
            no_node=TreeNode(question="Fin, optez pour un autre repas.")
        )
    )
)


async def start_questionnaire(ctx):
    await root_node.ask_question(ctx)

class CommandNode:
    def __init__(self, content):
        self.content = content
        self.prev = None
        self.next = None

# Charger l'historique des commandes depuis le fichier JSON
try:
    with open("command_history.json", "r") as file:
        command_history_data = json.load(file)
        command_history = {}

        # Convertir les données en listes chaînées
        for user_id, commands in command_history_data.items():
            if commands:
                head = CommandNode(commands[0])
                current_node = head
                for command in commands[1:]:
                    new_node = CommandNode(command)
                    current_node.next = new_node
                    new_node.prev = current_node
                    current_node = new_node

                command_history[user_id] = head
except FileNotFoundError:
    command_history = {}

# File d'attente pour gérer l'accès concurrentiel à l'historique
command_history_locks = {}

@client.event
async def on_ready():
    print("Le bot est prêt !")

@client.event
async def on_typing(channel, user, when):
    await channel.send(f"{user.name} is typing")

@client.command(name='start')
async def start_questionnaire(ctx):
    await root_node.ask_question(ctx)

@client.event
async def on_member_join(member):
    general_channel = client.get_channel(1044900412551073832)
    await general_channel.send(f"Bienvenue sur le serveur ! {member.name}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    command = message.content.lower()

    # Ajouter la commande à la liste chaînée, sauf si c'est la commande !last_command
    if command != "!last_command":
        async with asyncio.Lock():
            if user_id not in command_history:
                command_history[user_id] = CommandNode(command)
            else:
                new_node = CommandNode(command)
                new_node.next = command_history[user_id]
                command_history[user_id].prev = new_node
                command_history[user_id] = new_node

            # Sauvegarder l'historique dans le fichier JSON à chaque nouvelle commande
            save_command_history()

    if command.startswith("hello"):
        await message.channel.send("Hello")

    if "baayvin" in command:
        await message.channel.send("Baayvin = Neymar")

    if "cochon" in command:
        await message.channel.send("R")

    if command == "azerty":
        await message.channel.send("qwerty")

    await client.process_commands(message)

@client.command(name='reset')
async def reset_conversation(ctx):
    await root_node.reset_conversation(ctx)

@client.command(name='speak_about')
async def speak_about(ctx, topic):
    await root_node.speak_about(ctx, topic)

@client.command(name='last_command')
async def last_command(ctx):
    user_id = str(ctx.author.id)

    async with get_lock(user_id):
        if user_id in command_history and command_history[user_id]:
            last_command = command_history[user_id].content
            await ctx.send(f"Last command: {last_command}")
        else:
            await ctx.send("No command history for this user.")

@client.command(name='all_commands')
async def all_commands(ctx):
    user_id = str(ctx.author.id)

    async with get_lock(user_id):
        if user_id in command_history and command_history[user_id]:
            all_commands = []
            current_node = command_history[user_id]
            while current_node:
                all_commands.append(current_node.content)
                current_node = current_node.next

            all_commands_str = '\n'.join(all_commands)
            await ctx.send(f"All commands for this user:\n{all_commands_str}")
        else:
            await ctx.send("No command history for this user.")

@client.command(name='clear_history')
async def clear_history(ctx):
    user_id = str(ctx.author.id)

    async with get_lock(user_id):
        if user_id in command_history and command_history[user_id]:
            del command_history[user_id]
            save_command_history()

            await ctx.send("Command history cleared.")
        else:
            await ctx.send("No command history for this user.")

def save_command_history():
    # Sauvegarder l'historique dans le fichier JSON
    command_history_data = {}
    for user_id, head_node in command_history.items():
        commands = []
        current_node = head_node
        while current_node:
            commands.append(current_node.content)
            current_node = current_node.next    

        command_history_data[user_id] = commands

    with open("command_history.json", "w") as file:
        json.dump(command_history_data, file)

# Fonction pour obtenir le verrou associé à un utilisateur
def get_lock(user_id):
    if user_id not in command_history_locks:
        command_history_locks[user_id] = asyncio.Lock()

    return command_history_locks[user_id]


client.add_command(translate_command)
client.add_command(start_guessing_game)
client.add_command(guess_number)
client.add_command(answer_quizz)
client.add_command(start_quizz)
client.add_command(jeu_command)
client.add_command(start_pendu)
client.add_command(guess_pendu)

@client.command(name='commands')
async def show_commands(ctx):
    all_commands = [
        '!last_command', '!all_commands', '!start', '!guess', '!start_guessing_game', '!reset', '!speak_about',
        '!clear_history', '!commands', '!quizz' , '!jeu', '!start_pendu', '!guess_pendu'
    ]
    commands_str = '\n'.join(all_commands)
    await ctx.send(f"Les commandes disponibles:\n{commands_str}")



client.run("Bot-token")