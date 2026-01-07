module.exports = {
  apps: [
    {
      name: 'cyber-news-bot',
      script: 'src/index.py',
      interpreter: 'python',
      env:
       {
        NODE_ENV: 'production',
       },
    },
  ],
};