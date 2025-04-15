import asyncio
import os
import random
import time
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from TikTokApi import TikTokApi
from dotenv import load_dotenv
import urllib.parse

# Load environment variables
load_dotenv()
MS_TOKEN = os.getenv("MS_TOKEN")
print(f"MS_TOKEN available: {'Yes' if MS_TOKEN else 'No'}")

# Use your static list (or you could scrape the free-proxy-list.net page)
PROXY_LIST = [
    "http://8.210.232.181:7888",
    "http://165.232.129.150:80",
    "http://188.68.52.244:80",
    "http://188.40.59.208:3128",
    "http://213.183.56.99:80",
    "http://97.70.7.157:80",
    "http://47.243.113.74:5555",
    "http://47.238.67.96:8888",
    "http://81.169.213.169:8888",
    "http://123.30.154.171:7777",
    "http://13.40.63.96:8001",
    "http://27.79.168.232:16000",
    "http://45.61.159.42:3128",
    "http://83.217.23.36:8090",
    "http://34.244.90.35:80",
    "http://71.14.218.2:8080",
    "http://5.106.6.235:80",
    "http://47.236.8.166:18080",
    "http://18.188.127.31:3128",
    "http://47.88.59.79:82",
    "http://51.254.78.223:80",
    "http://86.106.132.194:3128",
    # ... Add more if desired
]

async def is_proxy_working(proxy_url, session):
    """
    Asynchronously tests a proxy by sending a GET request to httpbin.org/ip.
    Returns the proxy URL if it works, else returns None.
    """
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with session.get("http://httpbin.org/ip", proxy=proxy_url, timeout=timeout) as response:
            if response.status == 200:
                data = await response.json()
                print(f"✓ {proxy_url} works! - Response: {data}")
                return proxy_url
    except Exception as e:
        print(f"✗ {proxy_url} failed: {e}")
    return None

async def get_working_proxies_concurrently(proxy_list, max_workers=20):
    """
    Checks the given proxies concurrently and returns a list of working proxies.
    Each proxy is tried only once.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [is_proxy_working(proxy, session) for proxy in proxy_list]
        results = await asyncio.gather(*tasks)
    working = [result for result in results if result is not None]
    return working

def format_proxy_for_tiktokapi(proxy_url):
    """
    Formats a proxy URL into the TikTokApi expected dict format.
    """
    parsed = urllib.parse.urlparse(proxy_url)
    host = parsed.hostname
    port = parsed.port or 80
    return {"server": host, "port": port}

async def fetch_tiktok_data(username, ms_token, proxies):
    """
    Fetches TikTok profile info and video metrics.
    Uses a formatted proxy (if provided) when creating the session.
    """
    try:
        async with TikTokApi() as api:
            # If a proxy is provided, choose one at random from the working list
            formatted_proxy = None
            if proxies:
                chosen = random.choice(proxies)
                formatted_proxy = format_proxy_for_tiktokapi(chosen)
                print(f"Using proxy: {chosen} (formatted: {formatted_proxy})")
            
            # Create the session. If no proxy is used, pass None.
            await api.create_sessions(
                num_sessions=1,
                ms_tokens=[ms_token],
                proxies=[formatted_proxy] if formatted_proxy else None,
                sleep_after=3,
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            )
            
            # Check that the session initialized the browser
            if not hasattr(api, "browser"):
                raise Exception("Browser session was not initialized. Check configuration.")
            
            # Wait a random delay to mimic human behavior.
            await asyncio.sleep(random.uniform(1, 3))
            
            # Retrieve user info
            user = api.user(username=username)
            user_info = await user.info()
            stats = user_info.get("stats", {})
            user_data = {
                "username": username,
                "follower_count": stats.get("followerCount"),
                "following_count": stats.get("followingCount"),
                "video_count": stats.get("videoCount"),
                "heart_count": stats.get("heartCount") or stats.get("likesCount", 0)
            }
            
            await asyncio.sleep(random.uniform(1, 3))
            
            # Retrieve up to 5 videos (for testing)
            videos = []
            video_count = 0
            async for video in user.videos(count=5):
                await asyncio.sleep(random.uniform(0.5, 2))
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
                print(f"Retrieved video {video_count}")
                
                if video_count >= 5:
                    break
            
            # Close the sessions properly
            await api.close_sessions()
            return user_data, videos
    except Exception as e:
        print(f"Error in fetch_tiktok_data: {e}")
        try:
            if 'api' in locals() and hasattr(api, 'close_sessions'):
                await api.close_sessions()
        except Exception as close_e:
            print(f"Error closing session: {close_e}")
        return None, None

async def main_async():
    username = "therock"
    
    if not MS_TOKEN:
        print("Error: MS_TOKEN not found.")
        return
    
    print("Checking proxies concurrently...")
    working_proxies = await get_working_proxies_concurrently(PROXY_LIST, max_workers=20)
    if not working_proxies:
        print("No working proxies found. Continuing without proxy.")
    else:
        print("Working proxies:", working_proxies)
    
    # Use the working proxies list (if any)
    user_data, videos_data = await fetch_tiktok_data(username, MS_TOKEN, working_proxies)
    
    if user_data is None:
        print("Failed to retrieve user data.")
        return
    
    # Process user data
    user_df = pd.DataFrame([user_data])
    print("User Information:")
    print(user_df)
    user_df.to_csv(f"{username}_info.csv", index=False)
    user_df.to_parquet(f"{username}_info.parquet", index=False)
    
    if videos_data:
        videos_df = pd.DataFrame(videos_data)
        print("\nVideos Information:")
        print(videos_df)
        videos_df.to_csv(f"{username}_videos.csv", index=False)
        videos_df.to_parquet(f"{username}_videos.parquet", index=False)
    else:
        print("No videos retrieved.")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
