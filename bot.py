import logging
import os
import random
from datetime import UTC, datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src import api_utils, classes, configure_logger, databases, utils

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

api = classes.InfoAPI(
    name = "Helldivers 2 API",
    super_client = CLIENT,
    super_contact = CONTACT,
)

if api.test_api() != 200:
    raise ConnectionError(
        "Failed to connect to the Helldivers 2 API. "
        "Please check your API settings and network connection.")

inspirational_quotes = utils.parse_quotes(os.path.join(".", "data"), "inspirational_quotes.txt")
error_quotes = utils.parse_quotes(os.path.join(".", "data"), "error_phrases.txt")

databases.create_database_tables()

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
@commands.cooldown(5, 60, commands.BucketType.user) # 1 minute cooldown per user
async def major_orders(ctx):
    logger.debug(
        f"Major Orders Command Invoked by {ctx.author.name}#{ctx.author.discriminator} "
        + f"in {ctx.guild.name if ctx.guild else 'DM'}")
    
    await databases.set_expired_orders_to_inactive()  # Ensure expired orders are set to inactive

    assignments_cache = await databases.get_active_orders()
    logger.debug(f"Assignments cache size: {len(assignments_cache)}")
    logger.debug(f"Assignments cache content: {assignments_cache}")
        
    if len(assignments_cache) == 0 or await databases.last_fetched_a_day_ago():
        logger.debug("Assignments cache is empty, or hasn't been refreshed in a day. Fetching from API...")
        try:
            assignments = await api_utils.fetch_and_parse_from_api(api, "assignments")
            assignments = api_utils.parse_major_orders(assignments)
            if not assignments:
                await ctx.send("No current Major Orders available.")
                return
            logger.debug(f"Fetched {len(assignments)} assignments from API.")
            # Update the cache with the new assignments
            
            existing_orders = await databases.get_major_order_ids()
            logger.debug(f"Existing orders found in database: {len(existing_orders)}")
            logger.debug(f"Existing orders in database: {existing_orders}")
            
            for assignment in assignments:
                if assignment.order_id not in existing_orders:
                    await databases.insert_row(
                        "major_orders",
                        order_id = assignment.order_id,
                        briefing = assignment.briefing,
                        reward_type_index = assignment.reward_type_index,
                        reward_amount = assignment.reward_amount,
                        expiration = assignment.expiration,
                        last_fetched = str(datetime.now(UTC)),
                        reward_type = assignment.reward_type,
                        ttl = utils.ttl_from_now(assignment.expiration),
                        response_code = 200,
                        active = 1,
                    )
        except ConnectionError as e:
            logger.error(f"Failed to fetch assignments from API: {e}")
            await ctx.send("Failed to fetch Major Orders from the API. Please try again later.")
            return
    else:
        logger.debug("Assignments cache is current, using cached data.")
        # If the cache is current, we can use it directly
        # This avoids unnecessary API calls and database queries
    
    # Refresh the cache to ensure we have the latest data
    assignments_cache = await databases.get_active_orders()

    # Now that the cache is current, we can send the assignments to the user
    await ctx.send("Helldiver, your orders are as follows:")
    for _, briefing, reward, reward_type, expires in assignments_cache:
        await ctx.send(f"Major Order: {briefing}\n"
            + f"Rewards: {reward} {reward_type}\n"
            + f"Expires in: {utils.days_from_now(expires)}\n")


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
