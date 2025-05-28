import logging
import os
import random

import discord
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
assignments_cache = []  # List to hold MajorOrder objects
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
    logger.info(
        f"Inspire Command Invoked by {ctx.author.name}#{ctx.author.discriminator} "
        + f"in {ctx.guild.name if ctx.guild else 'DM'}")
    response = random.choice(inspirational_quotes)
    await ctx.send(response)
    
@bot.command(name="orders", help="Get the current Major Orders.")
@commands.cooldown(1, 60, commands.BucketType.user) # 1 minute cooldown per user
async def major_orders(ctx):
    global assignments_cache  # List to hold MajorOrder objects
    logger.info(
        f"Major Orders Command Invoked by {ctx.author.name}#{ctx.author.discriminator} "
        + f"in {ctx.guild.name if ctx.guild else 'DM'}")
    
    # If there is nothing in the cache, we'll need to fetch new data regardless
    if len(assignments_cache) == 0:
        logger.debug("Assignments cache is empty, fetching data from API.")
        
        try:
            data = await api_utils.fetch_and_parse_from_api(
                api=api,
                query="assignments",
            )
            orders = api_utils.parse_major_orders(data)
            logger.debug("Parsed %d Major Orders", len(orders))
            assignments_cache = utils.update_assignment_cache_with_orders(orders, assignments_cache)
        except ConnectionError:
            await ctx.send("Error: Unable to fetch Major Orders")
            return None
    
    # If the cache is not empty, we can use it to remove any expired assignments    
    assignments_cache = api_utils.remove_expired_assignments(assignments_cache)
    
    # If any cache item is older than a day, refresh the cache
    if utils.orders_older_than_one_day(assignments_cache):
        # TODO: This code is 1:1 duplicated and should be refactored
        try:
            data = await api_utils.fetch_and_parse_from_api(
                api=api,
                query="assignments",
            )
            orders = api_utils.parse_major_orders(data)
            logger.debug("Parsed %d Major Orders", len(orders))
            assignments_cache = utils.update_assignment_cache_with_orders(orders, assignments_cache)
        except ConnectionError:
            await ctx.send("Error: Unable to fetch Major Orders")
            return None

    # Now that the cache is current, we can send the assignments to the user
    # TODO: Handle when there are no assignments available
    for assignment in assignments_cache:
        await ctx.send(
            "Solder, your orders are as follows:\n"
            + "Major Order: %s\n", assignment.briefing
            + "Rewards: %d %s\n", assignment.reward_amount, assignment.reward_type
            + "Expires in: %s\n", utils.days_from_now(assignment.expiration)
            )


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
