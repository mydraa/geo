import json

with open('geoguessr_complete_guide.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for s in data['sections']:
    items = s.get('content', [])
    subs = s.get('subsections', [])
    p_count = sum(1 for x in items if x.get('type') == 'paragraph')
    img_count = sum(1 for x in items if x.get('type') == 'image')
    list_count = sum(1 for x in items if x.get('type') == 'list')
    print(f"=== {s['title']} ===")
    print(f"  Content items: {len(items)} (P: {p_count}, Img: {img_count}, List: {list_count})")
    print(f"  Subsections: {len(subs)}")
    for sub in subs[:3]:
        sub_items = sub.get('content', [])
        sub_p = sum(1 for x in sub_items if x.get('type') == 'paragraph')
        sub_img = sum(1 for x in sub_items if x.get('type') == 'image')
        print(f"    -> Sub: {sub.get('title')} ({len(sub_items)} items: {sub_p} P, {sub_img} Img)")
