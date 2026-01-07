import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime

class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    async def extract_article_data(self, url: str, source: str) -> Dict:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            soup = BeautifulSoup(response.content, 'html.parser')

            if source == 'SecurityAffairs':
                title = soup.find('h1', class_='entry-title').text.strip()
                published_date = soup.find('time', class_='entry-date published').get('datetime')
                content = soup.find('div', class_='entry-content clearfix').text.strip()

            elif source == 'TheHackerNews':
                title = soup.find('h1', class_='post-title').text.strip()
                published_date = soup.find('span', class_='post-date').text.strip()
                published_date = datetime.strptime(published_date, '%A, %B %d, %Y').isoformat()
                content = soup.find('div', class_='articlebody').text.strip()

            else:
                return None

            # Basic keyword extraction (can be improved)
            keywords = title.lower().split()
            summary = content[:200]  # First 200 characters as summary

            article_data = {
                'source': source,
                'title': title,
                'published_date': published_date,
                'url': url,
                'keywords': keywords,
                'summary': summary
            }

            return article_data

        except requests.exceptions.RequestException as e:
            print(f"Error during request to {url}: {e}")
            return None
        except Exception as e:
            print(f"Error parsing article from {url}: {e}")
            return None


    async def scrape_website(self, url: str, source: str) -> List[Dict]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            article_links = []

            if source == 'SecurityAffairs':
                for article in soup.find_all('h2', class_='entry-title'):
                    link = article.find('a')['href']
                    article_links.append(link)

            elif source == 'TheHackerNews':
                for article in soup.find_all('a', class_='story-link'):
                    link = article['href']
                    article_links.append(link)

            else:
                return []

            articles = []
            for link in article_links:
                article = await self.extract_article_data(link, source)
                if article:
                    articles.append(article)

            return articles

        except requests.exceptions.RequestException as e:
            print(f"Error during request to {url}: {e}")
            return []
        except Exception as e:
            print(f"Error parsing website {url}: {e}")
            return []

# Example Usage (not for execution):
# scraper = Scraper()
# asyncio.run(scraper.scrape_website("https://securityaffairs.co/", "SecurityAffairs"))
