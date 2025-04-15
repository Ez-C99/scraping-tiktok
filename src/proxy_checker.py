import requests

# Example list of proxies (replace with your own or scraped list)
proxies = [
    "http://123.45.67.89:8080",
    "http://98.76.54.32:3128",
    # Add more proxies here...
]

def is_proxy_working(proxy_url):
    try:
        response = requests.get("http://httpbin.org/ip", proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
        if response.status_code == 200:
            print(f"Working proxy: {proxy_url} - Response: {response.json()}")
            return True
    except Exception as e:
        print(f"Proxy {proxy_url} failed: {e}")
    return False

working_proxies = [proxy for proxy in proxies if is_proxy_working(proxy)]
print("Working proxies:", working_proxies)
