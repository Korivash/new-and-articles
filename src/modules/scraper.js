const axios = require('axios');
const cheerio = require('cheerio');

async function scrapeWebsite(url) {
  try {
    const response = await axios.get(url);
    const html = response.data;
    return extractArticleData(html, url);
  } catch (error) {
    console.error(`Error scraping ${url}: ${error}`);
    return [];
  }
}

function extractArticleData(html, baseUrl) {
  const $ = cheerio.load(html);
  const articles = [];

  // This is a placeholder, you'll need to adjust the selectors
  // based on the specific website you are scraping.
  $('article').each((index, element) => {
    const title = $(element).find('h2 a').text().trim();
    const url = new URL($(element).find('h2 a').attr('href'), baseUrl).href;
    const summary = $(element).find('p').text().trim();
    const published_date = new Date(); // Replace with actual date extraction

    if (title && url) {
      articles.push({
        source: baseUrl,
        title: title,
        published_date: published_date,
        url: url,
        keywords: [], // Extract keywords if available
        summary: summary,
      });
    }
  });

  return articles;
}

module.exports = { scrapeWebsite, extractArticleData };