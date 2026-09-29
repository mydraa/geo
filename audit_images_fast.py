import json
import re
import urllib.request
import concurrent.futures
import time

print("Starting full audit of all 1568 image URLs...")

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

urls = list(set(re.findall(r'https?://[^\s"\'`]+(?:\.png|\.jpg|\.jpeg|\.webp|\.svg)[^\s"\'`]*', content)))
print(f"Total unique URLs to check: {len(urls)}")

def check_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        req = urllib.request.Request(url, headers=headers)
        req.get_method = lambda: 'HEAD'
        with urllib.request.urlopen(req, timeout=7) as resp:
            if resp.status < 400:
                return url, resp.status, None
    except Exception:
        pass
    
    # Try GET if HEAD was not accepted
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=7) as resp:
            return url, resp.status, None
    except Exception as e:
        return url, None, str(e)

start_time = time.time()
results = []
broken = []

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    future_to_url = {executor.submit(check_url, u): u for u in urls}
    done_count = 0
    for f in concurrent.futures.as_completed(future_to_url):
        done_count += 1
        u, status, err = f.result()
        if err or (status and status >= 400):
            broken.append((u, status, err))
        else:
            results.append((u, status))
        if done_count % 300 == 0:
            print(f"Progress: {done_count}/{len(urls)} checked (broken: {len(broken)})...")

print(f"Audit completed in {time.time() - start_time:.1f}s.")
print(f"Total checked: {len(urls)} | Valid: {len(results)} | Broken: {len(broken)}")

with open('broken_images.json', 'w', encoding='utf-8') as f:
    json.dump(broken, f, indent=2)

print("Saved broken_images.json")
