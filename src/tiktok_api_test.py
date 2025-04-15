import asyncio
import os
import random
import pandas as pd
from TikTokApi import TikTokApi

# Define a list of proxies (replace with your own working proxies)
PROXIES = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

# Set the executable path for your browser (adjust for your OS)
# Example for macOS using Google Chrome:
EXECUTABLE_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# If you are on Windows, it might be something like:
# EXECUTABLE_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def fetch_user_data(username: str, ms_token: str):
    """
    Fetches profile info and the latest 20 videos for the given username.
    Rotates proxies, uses a specified browser executable, and adds random delays.
    Returns a dictionary for user stats and a list of dictionaries for video details.
    """
    # Use TikTokApi in an async context
    async with TikTokApi() as api:
        # Create one session using our list of proxies.
        # The TikTokApi internally chooses a random proxy from the list.
        await api.create_sessions(
            num_sessions=1,
            ms_tokens=[ms_token],
            proxies=PROXIES,
            sleep_after=3,
            executable_path=EXECUTABLE_PATH,
            # You can also pass additional context_options or cookies if needed.
        )
        
        # Optional: wait a random delay before proceeding to mimic human behavior
        await asyncio.sleep(random.uniform(1, 3))
        
        # Get the user object for the desired username
        user = api.user(username=username)
        
        # Retrieve user profile info
        user_info = await user.info()
        stats = user_info.get("stats", {})
        user_data = {
            "username": username,
            "follower_count": stats.get("followerCount"),
            "following_count": stats.get("followingCount"),
            "video_count": stats.get("videoCount"),
            "heart_count": stats.get("heartCount") or stats.get("likesCount")
        }
        
        # Add a random delay before fetching videos
        await asyncio.sleep(random.uniform(1, 3))
        
        # Retrieve recent video metrics (limit to 20 videos)
        videos = []
        async for video in user.videos(count=20):
            # Optional: random delay between video requests
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
        return user_data, videos

def main():
    # Set the username to inspect and your TikTok ms_token.
    username = "therock"  # change this to your desired TikTok username
    ms_token = os.getenv("MS_TOKEN", "RMa0qHD_U6BFHR5x9P-UgsREPDK9xhYW1MrwhCPQCV-oqcPQyGPQf4lxcI_LpdggVQrVU2ndNtIgAMaYtFJL7Rb0u08cFl7J_cmMMScJTktr8C-GKcfQ_XuN5gvQi7_M-1JlpQDSmlyuEuXWYqpLt1Q=")  # replace if needed

    if not ms_token or ms_token == "RMa0qHD_U6BFHR5x9P-UgsREPDK9xhYW1MrwhCPQCV-oqcPQyGPQf4lxcI_LpdggVQrVU2ndNtIgAMaYtFJL7Rb0u08cFl7J_cmMMScJTktr8C-GKcfQ_XuN5gvQi7_M-1JlpQDSmlyuEuXWYqpLt1Q=":
        print("Error: Please set your TikTok ms_token (e.g., via the MS_TOKEN environment variable).")
        return

    try:
        # Run the asynchronous data fetch
        user_data, videos_data = asyncio.run(fetch_user_data(username, ms_token))
    except Exception as e:
        print("An error occurred during data fetching:", e)
        return

    # Convert user data into a DataFrame
    user_df = pd.DataFrame([user_data])
    print("User Information:")
    print(user_df)
    
    # Save user info as CSV and Parquet
    user_df.to_csv("user_info.csv", index=False)
    user_df.to_parquet("user_info.parquet", index=False)
    
    # Convert videos data into a DataFrame
    videos_df = pd.DataFrame(videos_data)
    print("\nVideos Information:")
    print(videos_df)
    
    # Save videos info as CSV and Parquet
    videos_df.to_csv("videos_info.csv", index=False)
    videos_df.to_parquet("videos_info.parquet", index=False)

if __name__ == "__main__":
    main()
