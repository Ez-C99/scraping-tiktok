import asyncio
import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from TikTokApi import TikTokApi
from dotenv import load_dotenv
load_dotenv()  # This loads variables from a .env file into os.environ
print("MS_TOKEN:", os.getenv("MS_TOKEN"))

def get_proxies_from_free_proxy_list():
    """
    Scrapes free-proxy-list.net for HTTPS proxies.
    Returns a list of proxy strings in the form "http://IP:PORT".
    """
    url = "https://free-proxy-list.net/"
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        print(f"Error fetching proxy list: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the table with proxy data
    #   Leave proxies empty to search the page or provide a list of proxies to use
    proxies = [
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
    "http://191.243.46.22:43241",
    "http://156.38.112.11:80",
    "http://27.79.152.108:16000",
    "http://18.144.12.177:80",
    "http://158.255.77.166:80",
    "http://118.173.88.24:8080",
    "http://103.162.37.194:8080",
    "http://222.252.194.204:8080",
    "http://162.223.90.130:80",
    "http://144.126.216.57:80",
    "http://139.162.78.109:8080",
    "http://97.74.87.226:80",
    "http://50.223.246.237:80",
    "http://50.174.7.159:80",
    "http://50.207.199.87:80",
    "http://41.207.187.178:80",
    "http://13.38.153.36:80",
    "http://50.174.7.153:80",
    "http://50.202.75.26:80",
    "http://50.169.37.50:80",
    "http://50.232.104.86:80",
    "http://50.239.72.18:80",
    "http://50.217.226.47:80",
    "http://50.239.72.16:80",
    "http://50.217.226.40:80",
    "http://50.221.74.130:80",
    "http://190.58.248.86:80",
    "http://50.175.212.74:80",
    "http://50.174.7.152:80",
    "http://50.122.86.118:80",
    "http://65.108.195.47:8080",
    "http://35.72.118.126:80",
    "http://43.202.154.212:80",
    "http://3.37.125.76:3128",
    "http://35.76.62.196:80",
    "http://3.127.62.252:80",
    "http://18.228.149.161:80",
    "http://43.200.77.128:3128",
    "http://43.201.121.81:80",
    "http://77.232.128.191:80",
    "http://3.129.184.210:80",
    "http://3.130.65.162:3128",
    "http://51.16.199.206:3128",
    "http://13.48.109.48:3128",
    "http://52.63.129.110:3128",
    "http://54.179.39.14:3128",
    "http://52.65.193.254:3128",
    "http://13.213.114.238:3128",
    "http://3.97.176.251:3128",
    "http://52.16.232.164:3128",
    "http://51.16.179.113:1080",
    "http://63.32.1.88:3128",
    "http://54.179.44.51:3128",
    "http://54.228.164.102:3128",
    "http://51.20.19.159:3128",
    "http://45.140.143.77:18080",
    "http://158.255.77.169:80",
    "http://3.90.100.12:80",
    "http://158.255.77.168:80",
    "http://50.169.222.243:80",
    "http://83.217.23.34:8090",
    "http://50.169.222.241:80",
    "http://50.217.226.43:80",
    "http://50.239.72.17:80",
    "http://50.174.7.157:80",
    "http://50.217.226.44:80",
    "http://50.221.230.186:80",
    "http://50.220.168.134:80",
    "http://50.174.7.162:80",
    "http://213.143.113.82:80",
    "http://64.181.240.152:3128",
    "http://204.236.137.68:80",
    "http://44.219.175.186:80",
    "http://27.79.151.139:16000",
    "http://219.93.101.60:80",
    "http://50.217.226.41:80",
    "http://0.0.0.0:80",
    "http://211.128.96.206:80",
    "http://50.174.7.156:80",
    "http://127.0.0.7:80",
    "http://103.159.96.141:8080",
    "http://196.204.83.233:1981",
    "http://177.93.16.66:8080",
    "http://3.122.84.99:3128",
    "http://3.78.92.159:3128",
    "http://8.215.105.136:7777",
    "http://118.71.141.164:10002",
    "http://27.79.138.191:16000",
    "http://18.223.25.15:80",
    "http://15.236.106.236:3128",
    "http://44.218.183.55:80",
    "http://50.207.199.83:80",
    "http://50.175.212.66:80",
    "http://50.239.72.19:80",
    "http://66.191.31.158:80",
    "http://13.56.192.187:80",
    "http://23.247.136.248:80",
    "http://13.208.56.180:80",
    "http://35.79.120.242:3128",
    "http://3.124.133.93:3128",
    "http://46.51.249.135:3128",
    "http://3.21.101.158:3128",
    "http://54.233.119.172:3128",
    "http://52.196.1.182:80",
    "http://3.12.144.146:3128",
    "http://52.67.10.183:80",
    "http://99.80.11.54:3128",
    "http://51.20.50.149:3128",
    "http://15.156.24.206:3128",
    "http://51.17.58.162:3128",
    "http://3.97.167.115:3128",
    "http://13.55.210.141:3128",
    "http://50.174.7.158:80",
    "http://50.217.226.42:80",
    "http://50.174.7.155:80",
    "http://192.73.244.36:80",
    "http://198.49.68.80:80",
    "http://87.248.129.26:80",
    "http://103.231.236.26:8182",
    "http://103.151.17.201:8080",
    "http://103.133.61.165:1111",
    "http://103.189.122.174:3125",
    "http://177.93.58.33:999",
    "http://203.150.128.60:8080",
    "http://89.46.249.254:60729",
    "http://181.198.63.142:999",
    "http://203.153.121.131:8080",
    "http://114.9.27.142:8080",
    "http://114.9.26.238:8080",
    "http://103.24.215.29:8085",
    "http://13.37.59.99:3128",
    "http://13.38.176.104:3128",
    "http://13.36.87.105:3128",
    "http://62.210.15.199:80",
    "http://185.212.60.62:80",
    "http://3.136.29.104:80",
    "http://54.37.214.253:8080",
    "http://3.212.148.199:3128",
    "http://3.141.217.225:80",
    "http://27.79.193.19:16000",
    "http://200.250.131.218:80",
    "http://41.59.90.171:80",
    "http://66.29.154.105:3128",
    "http://27.79.244.179:16000",
    "http://47.56.110.204:8989",
    "http://68.185.57.66:80",
    "http://101.109.48.10:8080",
    "http://12.133.53.17:83",
    "http://161.82.141.219:8080",
    "http://120.28.194.248:8282",
    "http://45.124.170.5:8080",
    "http://202.154.19.7:8080",
    "http://188.132.150.68:8080",
    "http://116.203.139.209:5678",
    "http://47.251.122.81:8888",
    "http://13.37.89.201:80",
    "http://13.36.104.85:80",
    "http://13.37.73.214:80",
    "http://44.195.247.145:80",
    "http://3.126.147.182:80",
    "http://18.185.169.150:3128",
    "http://51.68.175.56:1080",
    "http://27.79.231.26:16000",
    "http://63.35.64.177:3128",
    "http://52.73.224.54:3128",
    "http://47.251.43.115:33333",
    "http://219.65.73.81:80",
    "http://104.238.160.36:80",
    "http://143.42.66.91:80",
    "http://8.217.124.178:49440",
    "http://66.29.154.103:3128",
    "http://3.123.150.192:80",
    "http://3.139.242.184:80",
    "http://13.246.209.48:1080",
    "http://27.79.224.121:16000",
    "http://23.88.116.40:80",
    "http://203.150.113.140:8080",
    "http://103.231.236.123:8182",
    "http://190.2.210.115:999",
    "http://45.177.17.31:999",
    "http://38.172.167.0:999",
    "http://112.204.238.111:8080",
    "http://47.91.120.190:1234",
    "http://8.211.200.183:1234",
    "http://8.211.194.78:5060",
    "http://47.237.92.86:9080",
    "http://8.215.12.103:82",
    "http://85.215.64.49:80",
    "http://47.91.121.127:8443",
    "http://103.153.76.6:5000",
    "http://8.220.136.174:9080",
    "http://203.115.101.51:82",
    "http://185.212.60.63:80",
    "http://45.144.64.153:8080",
    "http://43.129.201.43:443",
    "http://31.47.58.37:80",
    "http://43.156.59.228:80",
    "http://4.175.200.138:8080",
    "http://8.219.97.248:80",
    "http://209.97.150.167:8080",
    "http://50.207.199.80:80",
    "http://54.67.125.45:3128",
    "http://13.59.156.167:3128",
    "http://134.209.192.30:3128",
    "http://141.11.103.136:8080",
    "http://103.74.107.215:54328",
    "http://103.191.218.37:3125",
    "http://103.180.196.141:8080",
    "http://32.223.6.94:80",
    "http://50.207.199.82:80",
    "http://43.135.78.162:30004",
    "http://50.207.199.86:80",
    "http://50.231.104.58:80",
    "http://50.207.199.81:80",
    "http://5.78.124.240:40000",
    "http://184.169.154.119:80",
    "http://18.228.198.164:80",
    "http://204.236.176.61:3128",
    "http://13.246.184.110:3128",
    "http://16.16.239.39:3128",
    "http://54.152.3.36:80",
    "http://91.65.103.3:80",
    "http://116.125.141.115:80",
    "http://77.91.66.238:8080",
    "http://85.112.71.208:8080",
    "http://13.36.113.81:3128",
    "http://103.114.105.214:5000",
    "http://3.127.121.101:80",
    "http://74.62.179.122:8080",
    "http://65.108.159.129:8081",
    "http://72.10.160.92:8143",
    "http://72.240.9.63:80",
    "http://27.79.224.167:16000",
    "http://142.44.210.174:80",
    "http://84.39.112.144:3128",
    "http://115.77.138.229:10022",
    "http://45.184.152.129:999",
    "http://203.76.151.50:49200",
    "http://202.57.25.127:8080",
    "http://103.169.53.152:8080",
    "http://103.166.254.220:3124",
    "http://103.171.150.56:8080",
    "http://27.79.213.194:16000",
    "http://31.40.248.2:8080",
    "http://216.229.112.25:8080",
    "http://38.242.199.124:8089",
    "http://143.107.205.72:80",
    "http://103.164.229.149:8080",
    "http://103.38.54.64:83",
    "http://103.231.239.6:58080",
    "http://177.242.147.110:3030",
    "http://177.184.199.36:80",
    "http://103.172.71.222:8081",
    "http://8.209.96.245:8080",
    "http://8.213.156.191:199",
    "http://91.107.130.145:11000",
    "http://47.90.205.231:33333",
    "http://27.79.243.67:16000",
    "http://116.254.96.189:8080",
    "http://202.169.51.46:8080",
    "http://72.10.160.174:8005",
    "http://113.160.115.254:8080",
    "http://176.9.239.181:80",
    "http://4.149.210.210:3128",
    "http://162.220.247.66:6661",
    "http://156.228.110.211:3128",
    "http://89.116.78.152:5763",
    "http://104.207.33.178:3128",
    "http://170.106.187.7:8372",
    "http://84.46.204.248:6551",
    "http://156.228.89.216:3128",
    "http://104.207.36.59:3128",
    "http://104.207.51.130:3128",
    "http://104.207.39.97:3128",
    "http://31.57.41.82:5658",
    "http://107.181.154.229:5907",
    "http://84.46.204.59:6362",
    "http://156.228.80.54:3128"
    ]
    if not proxies:
        table = soup.find("table", {"id": "proxylisttable"})
        if table:
            for row in table.tbody.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) >= 7:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    https = cols[6].text.strip()
                    if https.lower() == "yes":
                        proxy = f"http://{ip}:{port}"
                        proxies.append(proxy)
        print("Scraped proxies:", proxies)  # Debug output
    return proxies


def is_proxy_working(proxy_url):
    """
    Tests a proxy by sending a GET request to httpbin.org/ip.
    Returns True if the proxy works, else False.
    """
    try:
        # Increase timeout to 10 seconds
        response = requests.get("http://httpbin.org/ip", 
                                proxies={"http": proxy_url, "https": proxy_url}, 
                                timeout=10)
        if response.status_code == 200:
            print(f"Working proxy: {proxy_url} - Response: {response.json()}")
            return True
    except Exception as e:
        print(f"Proxy {proxy_url} failed: {e}")
    return False

def get_working_proxies():
    """
    Retrieves proxies from free-proxy-list.net and returns only the working ones.
    """
    proxies = get_proxies_from_free_proxy_list()
    working_proxies = [proxy for proxy in proxies if is_proxy_working(proxy)]
    return working_proxies

async def fetch_user_data(username: str, ms_token: str, proxies):
    """
    Fetches profile info and the latest 20 videos for the given username.
    Uses a list of proxies, a specified browser executable, and adds random delays.
    Returns a dictionary for user stats and a list of dictionaries for video details.
    """
    async with TikTokApi() as api:
        # Create one session using our list of proxies.
        await api.create_sessions(
            num_sessions=1,
            ms_tokens=[ms_token],
            proxies=proxies,
            sleep_after=3,
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # adjust if needed
        )
        
        # Random delay to mimic human behavior
        await asyncio.sleep(random.uniform(1, 3))
        
        # Get user object for the given username
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
        
        # Random delay before fetching video data
        await asyncio.sleep(random.uniform(1, 3))
        
        # Retrieve metrics for the latest 20 videos
        videos = []
        async for video in user.videos(count=20):
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
    # Set the TikTok username and your ms_token.
    username = "therock"  # Change this as desired.
    ms_token = os.getenv("MS_TOKEN")  # Replace with your actual token
    
    if not ms_token:
        print("Error: Please set your TikTok ms_token (via the MS_TOKEN environment variable or directly in the script).")
        return

    print("Retrieving working proxies...")
    working_proxies = get_working_proxies()
    if not working_proxies:
        print("No working proxies found, please try again or supply a custom list.")
        return
    print("Working proxies:", working_proxies)
    
    try:
        # Run the asynchronous TikTok data fetch
        user_data, videos_data = asyncio.run(fetch_user_data(username, ms_token, working_proxies))
    except Exception as e:
        print("An error occurred during data fetching:", e)
        return

    # Convert and print user data
    user_df = pd.DataFrame([user_data])
    print("User Information:")
    print(user_df)
    user_df.to_csv("user_info.csv", index=False)
    user_df.to_parquet("user_info.parquet", index=False)
    
    # Convert and print videos data
    videos_df = pd.DataFrame(videos_data)
    print("\nVideos Information:")
    print(videos_df)
    videos_df.to_csv("videos_info.csv", index=False)
    videos_df.to_parquet("videos_info.parquet", index=False)

if __name__ == "__main__":
    main()
