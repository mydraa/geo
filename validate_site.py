import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html_code = f.read()

ids_in_app = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", app_code))
ids_in_html = set(re.findall(r"id=['\"]([^'\"]+)['\"]", html_code))

print(f"Total getElementById calls in app.js: {len(ids_in_app)}")
print(f"Total ids in index.html: {len(ids_in_html)}")

missing_ids = ids_in_app - ids_in_html
print("Missing IDs in index.html:", missing_ids)
