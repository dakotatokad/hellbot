import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src import api, utils

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

brasch = api.HellDivers()

bot = commands.Bot(command_prefix="$", intents=intents)
        
@bot.command(name="inspire", help="Inspires our brave Helldivers with a quote.")
async def enlist(ctx):
    quotes = [
        "Terminids. Unthinking monstrosities that want nothing more than to eat every last human. And every last human includes your family. Don't let your family get eaten. Enlist today!",
        "The automatons. Heartless killing machines. It is an undeniable fact that they do not have hearts. And heart is what Super Earth is all about. Prove your humanity. Show you care. Enlist in the Super Earth Armed Forces and destroy the automaton threat.",
    ]
    
    response = random.choice(quotes)
    await ctx.send(response)
    
@bot.command(name="orders", help="Get the current Major Orders.")
async def major_orders(ctx):
    briefing, rewards, expires, code= brasch.get_major_order()
    if code == 200:
        expires_in = utils.days_from_now(expires)
        
        await ctx.send(
            f"Major Order: {briefing}\n"
            + f"Rewards: {rewards} Medals\n"
            + f"Expires in: {expires_in}")
        
    else:
        await ctx.send("Error: Unable to fetch Major Orders.")
        
bot.run(TOKEN) # type: ignore
