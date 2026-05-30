from groq import Groq
import discord
from discord.ext import commands



# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
# MEMORY
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
conversation_history = []
max_history = 5

Creator = "YOUR_DISCORD_ID"


def add_to_history(role, content, author_name=None):
    if author_name:
        content = f"[{author_name}]: {content}"
    conversation_history.append({"role": role, "content": content})

    if len(conversation_history) > max_history:
        conversation_history.pop(0)


# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
# DISCORD BOT
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
# API Client
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
client = Groq(
    api_key="API_KEY",
    default_headers={"Groq-Model-Version": "latest"}
)

# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
# PERSONALITY PROMPT
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH


Creator_prompt = f"""

"""

default_prompt = """

"""


# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
# COMMAND: !Bot
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
@bot.command()
async def Bot(ctx, *, user_text):
    # store user's message
    add_to_history("user", user_text, ctx.author.display_name)
    user_id = ctx.author.id

## you can add multiple  prompts for specific people if you'd like the bot to respond differently
    if user_id == Creator:
        active_prompt = Creator_prompt

    else:
        active_prompt = default_prompt

    if active_prompt == default_prompt:
        final_prompt = default_prompt
    else:
        final_prompt = active_prompt + default_prompt

    # ----- BUILD MESSAGES -----
    messages = [
        {"role": "system", "content": final_prompt},
        *conversation_history,
        {"role": "user", "content": user_text}
    ]
    # Groq completion
    completion = client.chat.completions.create(
        model="Groq-Model-Version",
        messages=messages,
        temperature=1,
        max_completion_tokens=300,
        top_p=1,
        stream=False
    )

    reply = completion.choices[0].message.content


    # send reply to Discord
    await ctx.send(reply)
    print(active_prompt)
    print(user_id)


# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
# RUN DISCORD BOT
# HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
bot.run("API_KEY")
