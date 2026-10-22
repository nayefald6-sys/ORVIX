# ORVIX

ORVIX is a Python Discord bot built with discord.py 2.x. It is intended to run as a persistent background process so it stays online 24/7 on a hosted worker instead of a temporary app or web server.

## Quick start

1. Create a new Python 3.11 project in Replit or your hosting provider.
2. Upload or clone this project files.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set the environment variables:
   - `DISCORD_BOT_TOKEN` = your real Discord bot token
   - `DISCORD_GUILD_ID` = optional, only for testing in one server
5. Start the bot:
   ```bash
   python bot.py
   ```
6. Confirm that the bot appears online in Discord.
7. Test the slash commands in Discord:
   - `/ping`
   - `/help`
   - `/botinfo`
   - `/serverinfo`
   - `/userinfo`

## Secure token setup

Never hardcode the token in code. Never print it to logs, terminal output, or GitHub.

### Replit Secrets

1. Open your Replit project.
2. Click the "Tools" or "Secrets" section.
3. Add a secret named exactly:
   - `DISCORD_BOT_TOKEN`
4. Paste your Discord bot token into the value field.
5. Save it.

Do not paste the token into `bot.py`, `.env`, or a public readme file.

### Hosting provider environment variables

If you deploy to a hosted Python worker, open the provider's environment variables section and add:
- `DISCORD_BOT_TOKEN` = your actual token
- `DISCORD_GUILD_ID` = optional server ID for testing

The bot reads these values from the environment. If the token is missing, startup exits with a clear error instead of risking a leak.

## Discord bot setup

1. Go to the Discord Developer Portal.
2. Create or open your application.
3. Go to "Bot".
4. Copy the bot token.
5. Enable the required intents:
   - Server Members Intent
   - Message Content Intent
6. Invite the bot to your server with the required permissions.

## Command behavior

This project includes:

- `/ping` — returns Pong and the bot latency
- `/help` — displays the available commands
- `/botinfo` — shows bot information
- `/serverinfo` — shows server details
- `/userinfo` — shows member details

## Reliability and startup checks

The bot:

- reads the token from environment variables only
- logs startup status without exposing secrets
- exits clearly if configuration is missing
- syncs slash commands once at startup
- avoids duplicate command definitions
- uses proper Discord intents

## Deployment for 24/7 uptime

This bot is designed for a persistent background worker, not a static web page.

### What to use

Use a Python worker host that supports long-running background processes. Good choices for a Discord bot include:

- Replit paid plan (persistent worker, but there are plan costs)
- Railway
- Render background workers
- Fly.io
- DigitalOcean App Platform or a small VPS

### Free vs paid

Before choosing a host, always check:

- Is it free?
- Does it sleep after inactivity?
- Is there a background worker option?
- Are there CPU or memory limits?
- Is the service billed monthly or hourly?

Examples:

- Replit free plan: usually sleeps after inactivity and is not reliable for a bot that must stay online 24/7.
- Render free tier: some free plans may sleep, and background workers often have limits.
- Railway/Fly.io: usually paid for stable persistent workers, but they offer predictable bot uptime.
- VPS: fixed monthly cost, but gives full control and usually stays online continuously.

Important: This project does not automatically deploy to any paid service. You must approve the service and cost before paying.

## iPhone-friendly step-by-step

1. Open Replit or your hosting provider.
2. Create a Python 3.11 project.
3. Upload these files from this repo.
4. Open the Secrets or Environment Variables panel.
5. Add `DISCORD_BOT_TOKEN` with the token from the Discord Developer Portal.
6. Add `DISCORD_GUILD_ID` only if you want to test in one server.
7. Run:
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```
8. Wait for the bot to say it has connected.
9. Check Discord for the online status.
10. Run `/ping` in a server where the bot is present.

## Project status

This project is ready for local testing and production hosting, but it is not automatically online in Discord until you run it with a valid Discord token on a persistent worker.

## License

This project is provided as a starter bot for educational and development use.
