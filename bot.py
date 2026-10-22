import asyncio
import logging
import os

import discord
from discord import app_commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("ORVIX")


TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")

if not TOKEN:
    raise RuntimeError(
        "Missing required environment variable: DISCORD_BOT_TOKEN. "
        "Set it in Replit Secrets or your hosting provider environment variables."
    )

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Client(intents=intents)
# The bot uses a tree for slash commands because discord.py 2.x uses app_commands.
# This is the recommended approach for persistent background bots.
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    logger.info("ORVIX is online.")
    logger.info("User: %s#%s (%s)", bot.user.name, bot.user.discriminator, bot.user.id)
    logger.info("Guild count: %s", len(bot.guilds))

    try:
        if GUILD_ID:
            guild_id = int(GUILD_ID)
            logger.info("Syncing commands to guild %s", guild_id)
            await tree.sync(guild=discord.Object(id=guild_id))
        else:
            logger.info("Syncing commands globally")
            await tree.sync()
        logger.info("Slash command registration complete.")
    except ValueError:
        logger.error("DISCORD_GUILD_ID must be a valid integer. Check your environment variables.")
        raise


@tree.command(name="ping", description="Check if the bot is online and measure latency.")
async def ping(interaction: discord.Interaction):
    latency_ms = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! Bot latency: {latency_ms}ms")


@tree.command(name="help", description="Show all available ORVIX commands.")
async def help_command(interaction: discord.Interaction):
    commands = [
        "/ping - Check whether the bot is online",
        "/help - Show available commands",
        "/botinfo - Display bot information",
        "/serverinfo - Show server details",
        "/userinfo - Show basic member information",
    ]
    message = "\n".join(commands)
    await interaction.response.send_message(f"ORVIX commands:\n{message}")


@tree.command(name="botinfo", description="Display ORVIX bot information.")
async def botinfo(interaction: discord.Interaction):
    app = interaction.client.application
    bot_name = app.name if app else "ORVIX"
    bot_id = app.id if app else "Unknown"
    guild_count = len(interaction.client.guilds)
    member_count = sum(g.member_count for g in interaction.client.guilds)

    embed = discord.Embed(
        title=f"{bot_name} Bot Information",
        description="A persistent Discord bot for ORVIX.",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="Bot ID", value=str(bot_id), inline=True)
    embed.add_field(name="Guilds", value=str(guild_count), inline=True)
    embed.add_field(name="Members", value=str(member_count), inline=True)
    embed.add_field(name="Latency", value=f"{round(interaction.client.latency * 1000)}ms", inline=True)
    embed.set_footer(text="ORVIX | discord.py 2.x")
    await interaction.response.send_message(embed=embed)


@tree.command(name="serverinfo", description="Display information about the current server.")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("This command can only be used in a server.")
        return

    owner = guild.owner.mention if guild.owner else "Unknown"
    created = discord.utils.format_dt(guild.created_at, style="F")

    embed = discord.Embed(
        title=f"Server: {guild.name}",
        color=discord.Color.green(),
    )
    embed.add_field(name="Server ID", value=str(guild.id), inline=True)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Members", value=str(guild.member_count), inline=True)
    embed.add_field(name="Text Channels", value=str(len(guild.text_channels)), inline=True)
    embed.add_field(name="Voice Channels", value=str(len(guild.voice_channels)), inline=True)
    embed.add_field(name="Created", value=created, inline=False)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
    await interaction.response.send_message(embed=embed)


@tree.command(name="userinfo", description="Display information about a member.")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    joined = discord.utils.format_dt(target.joined_at, style="F") if target.joined_at else "Unknown"
    roles = " ".join(role.mention for role in target.roles[1:]) or "No extra roles"

    embed = discord.Embed(
        title=f"User Info: {target.display_name}",
        color=discord.Color.orange(),
    )
    embed.add_field(name="Username", value=f"{target.name}#{target.discriminator}", inline=True)
    embed.add_field(name="ID", value=str(target.id), inline=True)
    embed.add_field(name="Joined", value=joined, inline=False)
    embed.add_field(name="Roles", value=roles, inline=False)
    embed.set_thumbnail(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed)


async def main():
    logger.info("Starting ORVIX...")
    logger.info("Token loaded: %s", "yes" if TOKEN else "no")
    logger.info("Guild override: %s", GUILD_ID or "not set")

    try:
        await bot.start(TOKEN)
    except discord.LoginFailure:
        logger.error("Discord login failed. Check that DISCORD_BOT_TOKEN is valid.")
        raise SystemExit(1)
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
    finally:
        logger.info("ORVIX shutting down.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as exc:
        logger.error("Startup failed: %s", exc)
        raise SystemExit(1)
