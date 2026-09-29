import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_code = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html_code = f.read()

selectors = set(re.findall(r"querySelectorAll\(['\"]([^'\"]+)['\"]\)", app_code))
print(f"Total querySelectorAll in app.js: {len(selectors)}")
for sel in selectors:
    # check simple class selectors
    classes = re.findall(r"\.([a-zA-Z0-9_-]+)", sel)
    for c in classes:
        if f'class="{c}"' not in html_code and f'"{c}"' not in html_code and f' {c} ' not in html_code and f' {c}"' not in html_code and f'"{c} ' not in html_code:
            # check if dynamically rendered in app.js
            if c not in app_code:
                print(f"Potential missing class for selector '{sel}': {c}")

print("Selector verification complete.")
