require('dotenv').config();
const { Client, GatewayIntentBits, SlashCommandBuilder } = require('discord.js');
const db = require('./modules/db');
const scraper = require('./modules/scraper');

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const NEWS_TYPES = ['cybersecurity', 'world'];
const NEWS_SOURCES = {
  'cybersecurity': ['https://example.com/cybersecurity'], // Replace with actual URLs
  'world': ['https://example.com/world'], // Replace with actual URLs
};

client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);

  // Register slash commands
  const addChannelCommand = new SlashCommandBuilder()
    .setName('add_channel')
    .setDescription('Add this channel to receive news updates for a specific type.')
    .addStringOption(option =>
      option.setName('news_type')
        .setDescription('The type of news to receive.')
        .setRequired(true)
        .addChoices(
          ...NEWS_TYPES.map(type => ({
            name: type, value: type
          }))
        ));

  const removeChannelCommand = new SlashCommandBuilder()
    .setName('remove_channel')
    .setDescription('Remove this channel from receiving news updates.');

  client.application.commands.create(addChannelCommand);
  client.application.commands.create(removeChannelCommand);
});

client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'add_channel') {
    const news_type = interaction.options.getString('news_type');
    try {
      await db.addChannel(interaction.channelId, [news_type]);
      await interaction.reply(`This channel will now receive ${news_type} news updates.`);
    } catch (error) {
      console.error(error);
      await interaction.reply({ content: 'There was an error adding this channel.', ephemeral: true });
    }
  }

  if (interaction.commandName === 'remove_channel') {
    try {
      await db.removeChannel(interaction.channelId);
      await interaction.reply('This channel will no longer receive news updates.');
    } catch (error) {
      console.error(error);
      await interaction.reply({ content: 'There was an error removing this channel.', ephemeral: true });
    }
  }
});

async function sendNewsUpdates() {
  for (const newsType of NEWS_TYPES) {
    const channels = await db.getChannelsByNewsType(newsType);
    const sources = NEWS_SOURCES[newsType];

    if (!channels || channels.length === 0) continue;

    for (const source of sources) {
      const articles = await scraper.scrapeWebsite(source);

      for (const article of articles) {
        for (const channel of channels) {
          try {
            const discordChannel = await client.channels.fetch(channel.channel_id);
            if (discordChannel) {
              discordChannel.send(`${article.title}\n${article.url}`);
            }
          } catch (error) {
            console.error(`Error sending news to channel ${channel.channel_id}: ${error}`);
          }
        }
      }
    }
  }
}

// Schedule news updates (e.g., every hour)
setInterval(sendNewsUpdates, 3600000);

db.connectDB(process.env.MONGODB_URI)
  .then(() => {
    client.login(process.env.DISCORD_TOKEN);
  });