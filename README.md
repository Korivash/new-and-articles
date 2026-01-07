# Cyber News Discord Bot

A Discord bot that scrapes websites to provide cybersecurity and world news to subscribed channels.

## Setup

1.  Install dependencies: `pip install -r requirements.txt`
2.  Create a `.env` file with the following variables:
    ```
    DISCORD_TOKEN=<your_discord_bot_token>
    MONGODB_URI=<your_mongodb_connection_string>
    ```
3.  Run the bot: `python src/index.py` or `npm start` (using PM2)

## PM2 Deployment

1.  Install PM2: `npm install -g pm2`
2.  Start the bot with PM2: `pm2 start pm2.config.js`
