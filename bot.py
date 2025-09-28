import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_embed_message = None  # store last embed message ID

@bot.event
async def on_message(message: discord.Message):
    global last_embed_message

    # Only act in the target channel
    if message.channel.id != CHANNEL_ID:
        return

    # Only act on webhook messages
    if message.webhook_id:
        # Delete the triggering webhook message
        try:
            await message.delete()
        except discord.NotFound:
            pass

        # Delete the last embed message if exists
        if last_embed_message:
            try:
                old_msg = await message.channel.fetch_message(last_embed_message)
                await old_msg.delete()
            except discord.NotFound:
                pass

        # Build the embed
        embed = discord.Embed(
            title="This is the introduction channel.",
            description=(
                "When joining a server, you can use this channel to write information "
                "about yourself to let other members know general information of you as a person.\n\n"
                "You can write your introduction however you want to, it doesn't need to meet any criteria, "
                "as long as it contains your name and what you like doing.\n\n"
                f"**User’s introduction:**\n{message.content}"
            ),
            color=0xFFDC5D
        )
        embed.set_footer(text=f"Webhook message")

        # Send the embed
        sent = await message.channel.send(embed=embed)

        # Save ID of last embed message
        last_embed_message = sent.id

    # Ensure other commands still work
    await bot.process_commands(message)

bot.run(TOKEN)
