import discord
from discord import app_commands
import random
import os

# CART3R Configuration
TOKEN = os.getenv("DISCORD_TOKEN")

class CART3R(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.questions = {}

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"CART3R is online as {self.user}!")
        await self.change_presence(
            activity=discord.Game("Helping with homework")
        )

bot = CART3R()


# PING COMMAND
@bot.tree.command(name="ping", description="Check if CART3R is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"🤖 CART3R is online! Latency: {round(bot.latency * 1000)}ms"
    )


# HELP COMMAND
@bot.tree.command(name="help", description="Show CART3R commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 CART3R Help Centre",
        description="Your personal Discord homework tester!",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="/ping",
        value="Check if CART3R is online.",
        inline=False
    )

    embed.add_field(
        name="/quiz",
        value="Generate a random maths question.",
        inline=False
    )

    embed.add_field(
        name="/answer",
        value="Submit your answer to a question.",
        inline=False
    )

    embed.add_field(
        name="/help",
        value="Show this help menu.",
        inline=False
    )

    await interaction.response.send_message(embed=embed)


# QUIZ COMMAND
@bot.tree.command(name="quiz", description="Generate a maths question")
async def quiz(interaction: discord.Interaction):

    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)

    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        answer = num1 + num2

    elif operation == "-":
        answer = num1 - num2

    else:
        answer = num1 * num2

    bot.questions[interaction.user.id] = answer

    embed = discord.Embed(
        title="📝 CART3R Homework Test",
        description=f"What is **{num1} {operation} {num2}**?",
        color=discord.Color.green()
    )

    embed.set_footer(text="Use /answer to submit your answer!")

    await interaction.response.send_message(embed=embed)


# ANSWER COMMAND
@bot.tree.command(name="answer", description="Submit your quiz answer")
@app_commands.describe(answer="Your numerical answer")
async def answer(interaction: discord.Interaction, answer: int):

    user_id = interaction.user.id

    if user_id not in bot.questions:
        await interaction.response.send_message(
            "❌ You don't have an active question! Use /quiz first.",
            ephemeral=True
        )
        return

    correct_answer = bot.questions[user_id]

    if answer == correct_answer:

        await interaction.response.send_message(
            "✅ **Correct!** Great work! CART3R approves your answer. 🎉"
        )

    else:

        await interaction.response.send_message(
            "❌ **Not quite!** Try another question with /quiz."
        )

    del bot.questions[user_id]


# START CART3R
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing.")

bot.run(TOKEN)
