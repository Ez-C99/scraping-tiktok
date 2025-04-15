import asyncio
import os
import random
import time
import aiohttp
import pandas as pd
from TikTokApi import TikTokApi
from dotenv import load_dotenv
import urllib.parse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
# Set the logging level to INFO for the TikTokApi
logging.getLogger("TikTokApi").setLevel(logging.INFO)

# Load environment variables
load_dotenv()
MS_TOKEN = os.getenv("MS_TOKEN")
logging.info(f"MS_TOKEN available: {'Yes' if MS_TOKEN else 'No'}")

# Just use the one working proxy you found
PROXY_LIST = [
    "http://188.68.52.244:80"
]

async def test_proxy(session, proxy):
    """Test if a proxy is working using aiohttp"""
    try:
        start_time = time.time()
        async with session.get('http://httpbin.org/ip', 
                              proxy=proxy, 
                              timeout=5) as response:
            if response.status == 200:
                elapsed = time.time() - start_time
                logging.info(f"✓ {proxy} works! ({elapsed:.2f}s)")
                return proxy, True
            else:
                logging.warning(f"✗ {proxy} failed with status {response.status}")
                return proxy, False
    except Exception as e:
        logging.error(f"✗ {proxy} error: {str(e)[:50]}...")
        return proxy, False

async def find_working_proxies(proxy_list, max_workers=5):
    """Test multiple proxies concurrently and return working ones"""
    working_proxies = []
    
    conn = aiohttp.TCPConnector(limit=max_workers, ttl_dns_cache=300)
    timeout = aiohttp.ClientTimeout(total=10)
    
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        tasks = [test_proxy(session, proxy) for proxy in proxy_list]
        
        for i in range(0, len(tasks), max_workers):
            batch = tasks[i:i+max_workers]
            results = await asyncio.gather(*batch, return_exceptions=True)
            
            for result in results:
                if isinstance(result, tuple) and result[1]:
                    working_proxies.append(result[0])
    
    return working_proxies

def format_proxy_for_tiktokapi(proxy_url):
    """Format proxy URL for TikTokApi's expected format"""
    # Parse the proxy URL
    parsed = urllib.parse.urlparse(proxy_url)
    
    # Extract host and port
    host = parsed.hostname
    port = parsed.port or 80  # Default to port 80 if not specified
    
    # Return in the format expected by TikTokApi
    return {
        "server": host,
        "port": port
    }

async def fetch_tiktok_data(username, ms_token, proxy=None):
    """Fetch TikTok user data and recent videos"""
    try:
        # Initialize the TikTokApi
        api = TikTokApi()
        
        # Format proxy if provided
        formatted_proxy = None
        if proxy:
            formatted_proxy = format_proxy_for_tiktokapi(proxy)
            logging.info(f"Using formatted proxy: {formatted_proxy}")
        
        # Create a session
        logging.info("Creating session...")
        await api.create_sessions(
            num_sessions=1,
            ms_tokens=[ms_token],
            proxies=[formatted_proxy] if formatted_proxy else None
        )
        
        logging.info("Session created successfully")
        
        # Get user data
        logging.info(f"Getting info for user: {username}")
        user = api.user(username)
        user_info = await user.info()
        
        logging.info("User info retrieved")
        
        stats = user_info.get("stats", {})
        user_data = {
            "username": username,
            "follower_count": stats.get("followerCount"),
            "following_count": stats.get("followingCount"),
            "video_count": stats.get("videoCount"),
            "heart_count": stats.get("heartCount", stats.get("likesCount", 0))
        }
        
        # Get videos data
        videos = []
        video_count = 0
        logging.info("Fetching videos...")
        
        # Use a limit to avoid too many requests
        async for video in user.videos(count=5):
            video_dict = video.as_dict
            video_stats = video_dict.get("stats", {})
            videos.append({
                "video_id": video_dict.get("id"),
                "description": video_dict.get("desc"),
                "create_time": video_dict.get("createTime"),
                "play_count": video_stats.get("playCount"),
                "digg_count": video_stats.get("diggCount"),
                "comment_count": video_stats.get("commentCount"),
                "share_count": video_stats.get("shareCount")
            })
            video_count += 1
            logging.info(f"Retrieved video {video_count}")
            
            if video_count >= 5:  # Just get 5 videos for testing
                break
        
        # Close the session
        await api.close_sessions()
        
        return user_data, videos
    
    except Exception as e:
        logging.error(f"Error in fetch_tiktok_data: {e}")
        # Try to properly close the session if it exists
        try:
            if 'api' in locals() and hasattr(api, 'close_sessions'):
                await api.close_sessions()
        except Exception as close_error:
            logging.error(f"Error closing session: {close_error}")
        return None, None

async def main_async():
    username = "therock"
    
    if not MS_TOKEN:
        logging.error("Error: MS_TOKEN not found.")
        return
    
    logging.info("Trying without proxy...")
    user_data, videos_data = await fetch_tiktok_data(username, MS_TOKEN)
    
    # Process results
    if user_data:
        # Save user data
        user_df = pd.DataFrame([user_data])
        logging.info("\nUser Information:")
        logging.info(user_df)
        user_df.to_csv(f"{username}_info.csv", index=False)
        
        # Save videos data
        if videos_data and videos_data:
            videos_df = pd.DataFrame(videos_data)
            logging.info(f"\nFound {len(videos_data)} videos:")
            logging.info(videos_df)
            videos_df.to_csv(f"{username}_videos.csv", index=False)
        else:
            logging.info("No videos data retrieved.")
    else:
        logging.warning("Failed to retrieve user data.")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()