import logging
import os
import random
import time

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

from src import api_utils, classes, configure_logger, utils

logger = logging.getLogger(__name__)

configure_logger.create_custom_logger("./configs/logging_config.json")

logger.info("Starting Helldivers 2 Discord Bot...")
logger.debug("==============================================")
logger.debug("==============================================")

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN environment variable must be set.")

CLIENT = os.getenv("SUPER_CLIENT")
CONTACT = os.getenv("SUPER_CONTACT")
if CLIENT is None or CONTACT is None:
    raise ValueError("SUPER_CLIENT and SUPER_CONTACT environment variables must be set.")

intents = discord.Intents.default()
intents.message_content = True

#brasch = classes.HellDivers()

api = classes.InfoAPI(
    name = "Helldivers 2 API",
    super_client = CLIENT,
    super_contact = CONTACT,
)

if api.test_api() != 200:
    raise ConnectionError(
        "Failed to connect to the Helldivers 2 API. "
        "Please check your API settings and network connection.")

# Initialize data caches for API data
assignments_cache = []
# assignments_cache = classes.APICache(
#     data = requests.Response(),  # Placeholder for the initial data
#     response_code= -1, # -1 indicates the cache has not been populated
#     timestamp = time.time(),
# )

inspirational_quotes = utils.parse_quotes(os.path.join(".", "data"), "inspirational_quotes.txt")
error_quotes = utils.parse_quotes(os.path.join(".", "data"), "error_phrases.txt")

bot = commands.Bot(command_prefix="$", intents=intents)
    
@bot.command(name="inspire", help="Inspires our brave Helldivers with a quote.")
@commands.cooldown(5, 30, commands.BucketType.user) # 30 seconds cooldown per user
async def enlist(ctx):
    response = random.choice(inspirational_quotes)
    await ctx.send(response)
    
@bot.command(name="orders", help="Get the current Major Orders.")
@commands.cooldown(1, 60, commands.BucketType.user) # 1 minute cooldown per user
async def major_orders(ctx):
    logger.info(
        f"Major Orders Command Invoked by {ctx.author.name}#{ctx.author.discriminator} "
        + f"in {ctx.guild.name if ctx.guild else 'DM'}")
    try:
        # TODO: Get data from new cache setup of a list of MajorOrder objects
        raw_data, response_code = assignments_cache.get_cache()
        logger.debug(f"Assignments Cache Attempt: {response_code == 304}, Response Code: {response_code}")
    except (ValueError, TimeoutError):
        # TODO: Log the error; cache not populated yet
        raw_data, response_code = await api_utils.query_api(
            api = api,
            query = "assignments",
        )
        logger.debug(f"API Query: {raw_data}, Response Code: {response_code}")
        
        if response_code != 200:
            await ctx.send(
                "Error: Unable to fetch Major Orders.\n"
                + f"Error Code: {response_code}"
                )
            return None
    
        parsed_data = api_utils.parse_requests_data(raw_data)
        logger.debug("Parsed Data: %s", parsed_data)
    
        orders = api_utils.parse_major_orders(parsed_data)
    
        for order in orders:
            logger.debug(
                "Major Order: %s  "
                + "Rewards Type: %s "
                + "Rewards Amount: %d "
                + "Expiration: %s"
                + order.briefing, order.reward_type, order.reward_amount, order.expiration
                )
            
            #order.ttl = utils.ttl_from_now(order.expiration)
            #logger.debug("Major Order %s TTL: %d seconds", order.briefing, order.ttl)
            
            if order in assignments_cache:
                # Update the TLL if its in the cache
                order.ttl = utils.ttl_from_now(order.expiration)
            else:
                assignments_cache.append(order)
                logger.debug("Added new order to cache: %s", order.order_id)
            
            # Check if the order is expired
            if order.ttl <= 0:
                # If the order is expired, remove it from the cache
                assignments_cache.remove(order)
                logger.debug("Removed expired order from cache: %s", order.order_id)
                
    # Now just use the cache since its updated

    ## probably refactor this function
    for assignment in assignments_cache:
        await ctx.send(
            "Solder, your orders are as follows:\n"
            + "Major Order: %s\n", assignment.briefing
            + "Rewards: %d %s\n", assignment.reward_amount, assignment.reward_type
            + "Expires in: %s\n", utils.days_from_now(assignment.expiration)
            )
    
    ##


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): 
        if ctx.command.name == "orders":
            await ctx.send(
                f"{random.choice(error_quotes)}"
                + f" Wait {int(error.retry_after)} seconds before you ask me that again."
            )
        if ctx.command.name == "inspire":
            # TODO: Change the messages to fit the command context
            await ctx.send(
                f"{random.choice(error_quotes)}"
                + f" Wait {int(error.retry_after)} seconds before you ask me that again."
            )
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please check the command name.")
    else:
        await ctx.send("An error occurred while processing your command.")
        logger.error(f"Error: {error}")

        
bot.run(TOKEN) # type: ignore
