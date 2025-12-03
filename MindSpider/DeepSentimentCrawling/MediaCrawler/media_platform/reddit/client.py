import httpx
from typing import Dict, Optional, Any
import asyncio
from loguru import logger

class RedditClient:
    def __init__(self, proxies: Optional[Dict] = None):
        self.proxies = proxies
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.timeout = 30

    async def request(self, method: str, url: str, params: Optional[Dict] = None) -> Dict:
        """
        Make an HTTP request to Reddit JSON endpoints
        """
        async with httpx.AsyncClient(proxy=self.proxies, timeout=self.timeout) as client:
            try:
                logger.info(f"[RedditClient] Requesting URL: {url} | Method: {method} | Params: {params}")
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    follow_redirects=True
                )
                logger.info(f"[RedditClient] Response Status: {response.status_code}")
                if response.status_code == 200:
                    logger.info(f"[RedditClient] Response Content (First 200 chars): {response.text[:200]}")
                
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"[RedditClient] HTTP Error: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"[RedditClient] Request Failed: {e}")
                raise

    async def search(self, keyword: str, limit: int = 25) -> Dict:
        """
        Search Reddit for a keyword
        """
        url = "https://www.reddit.com/search.json"
        params = {
            "q": keyword,
            "limit": limit,
            "sort": "new",
            "type": "link" # Only search for posts (links), not subreddits or users
        }
        return await self.request("GET", url, params)

    async def get_comments(self, post_id: str) -> list:
        """
        Get comments for a specific post
        post_id: should be the ID without prefix (e.g., 'xyz123') or with prefix
        """
        # Reddit ID usually comes as t3_xyz, but URL needs just xyz or full t3_xyz works too?
        # Actually /comments/{id}.json works best with the ID.
        # If input is t3_xyz, strip t3_
        clean_id = post_id.split('_')[-1] if '_' in post_id else post_id
        
        url = f"https://www.reddit.com/comments/{clean_id}.json"
        return await self.request("GET", url)
