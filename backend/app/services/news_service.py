import aiohttp
import feedparser
from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any
from ..config import logger, NEWS_API_KEY
from ..schemas import NewsItem

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
    "https://www.livemint.com/rss/companies",
    "https://www.moneycontrol.com/rss/marketreports.xml"
]

async def fetch_news_via_api(ticker: str) -> List[NewsItem]:
    """Fetch news from NewsData.io API."""
    if not NEWS_API_KEY:
         logger.warning("NewsData.io API key not found. Skipping API fetch.")
         return []

    url = f"https://newsdata.io/api/1/market?apikey={NEWS_API_KEY}&q={ticker}&country=in"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                results = data.get("results", [])
                news_items = []
                for item in results:
                    news_items.append(NewsItem(
                        headline=item.get("title", ""),
                        source=item.get("source_id", "Unknown"),
                        url=item.get("link"),
                        published_at=item.get("pubDate", ""),
                        summary=item.get("description"),
                        sentiment="neutral", # To be refined by Agent 3
                        credibility_tag="tier-2" 
                    ))
                return news_items
            else:
                logger.error(f"Error fetching news from API: {response.status}")
                return []

async def fetch_news_via_rss(ticker: str) -> List[NewsItem]:
    """Fetch news from common Indian financial RSS feeds."""
    news_items = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                # Basic search in headline/summary
                if ticker.lower() in entry.title.lower() or (hasattr(entry, 'summary') and ticker.lower() in entry.summary.lower()):
                     news_items.append(NewsItem(
                        headline=entry.title,
                        source=feed.feed.get("title", "RSS"),
                        url=entry.link,
                        published_at=entry.get("published", ""),
                        summary=getattr(entry, 'summary', ''),
                        sentiment="neutral"
                     ))
        except Exception as e:
            logger.error(f"Error parsing RSS feed {feed_url}: {e}")

    return news_items

async def get_latest_news(ticker: str) -> List[NewsItem]:
    """Combine API and RSS news fetch."""
    api_news = await fetch_news_via_api(ticker)
    rss_news = await fetch_news_via_rss(ticker)
    
    # Deduplicate by headline (crude but works for hackathon)
    seen = set()
    combined = []
    for item in api_news + rss_news:
        if item.headline not in seen:
            seen.add(item.headline)
            combined.append(item)
            
    return combined[:15] # Top 15 items
