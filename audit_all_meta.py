import json
import re

print("--- AUDITING ALL SOURCE JSONS FOR CARS, VEHICLES & META ---")

# 1. Inspect 05_meta.json
with open('05_meta.json', 'r', encoding='utf-8') as f:
    meta_json = json.load(f)

print(f"\nTotal items in 05_meta.json: {len(meta_json.get('content', []))}")
for i, item in enumerate(meta_json.get('content', [])):
    text = item.get('text', '')
    src = item.get('src', '')
    caption = item.get('caption', '')
    alt = item.get('alt', '')
    itype = item.get('type', '')
    
    if itype == 'image':
        print(f"IMG [{i}]: src={src} | caption={caption} | alt={alt}")
    elif any(k in text.lower() for k in ['car', 'camera', 'vehicle', 'rack', 'snorkel', 'tape', 'mirror', 'truck', 'bars', 'blur', 'antenna', 'escort', 'gen 1', 'gen 2', 'gen 3', 'gen 4', 'rift']):
        print(f"TXT [{i}]: {text[:150]}")

# 2. Check full guide for car references across all countries
with open('geoguessr_complete_guide.json', 'r', encoding='utf-8') as f:
    full_guide = json.load(f)

print(f"\nSections in full guide: {len(full_guide)}")
car_mentions = []
for sec_idx, sec in enumerate(full_guide):
    title = sec.get('title', f"Section {sec_idx}")
    for item in sec.get('content', []):
        t = item.get('text', '')
        if any(w in t.lower() for w in ['google car', 'street view car', 'snorkel', 'roof rack', 'follow car', 'police car', 'escort', 'black tape', 'red car', 'white car', 'pickup', 'truck with', 'sky rift', 'low cam', 'antenna', 'bars on']):
            car_mentions.append((title, item.get('type'), t[:160]))

print(f"\nFound {len(car_mentions)} car/vehicle mentions in full guide:")
for sec_title, itype, txt in car_mentions[:40]:
    print(f"[{sec_title}] {txt}")
