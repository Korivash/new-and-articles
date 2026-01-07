const mongoose = require('mongoose');

const channelSchema = new mongoose.Schema({
  channel_id: {
    type: String,
    required: true,
    unique: true,
  },
  news_types: {
    type: [String],
    required: true,
  },
  sources: {
    type: [String],
    default: [],
  },
  keywords: {
    type: [String],
    default: [],
  },
});

module.exports = mongoose.model('Channel', channelSchema);