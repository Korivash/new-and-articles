const mongoose = require('mongoose');
const Channel = require('../models/channel');

async function connectDB(uri) {
  try {
    await mongoose.connect(uri, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('Connected to MongoDB');
  } catch (error) {
    console.error('Error connecting to MongoDB:', error);
    throw error;
  }
}

async function addChannel(channel_id, news_types) {
  try {
    const channel = new Channel({
      channel_id: channel_id,
      news_types: news_types,
    });
    await channel.save();
    console.log(`Channel ${channel_id} added with news types: ${news_types}`);
  } catch (error) {
    console.error(`Error adding channel ${channel_id}: ${error}`);
    throw error;
  }
}

async function removeChannel(channel_id) {
  try {
    await Channel.deleteOne({ channel_id: channel_id });
    console.log(`Channel ${channel_id} removed`);
  } catch (error) {
    console.error(`Error removing channel ${channel_id}: ${error}`);
    throw error;
  }
}

async function getChannelsByNewsType(news_type) {
  try {
    const channels = await Channel.find({ news_types: news_type });
    return channels;
  } catch (error) {
    console.error(`Error getting channels by news type ${news_type}: ${error}`);
    return [];
  }
}

module.exports = { connectDB, addChannel, removeChannel, getChannelsByNewsType };