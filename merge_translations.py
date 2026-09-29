import json
import re

print("Starting merge_translations.py...")

files = {
    'na_sa': 'translated_na_sa.json',
    'eu1': 'translated_eu1.json',
    'eu2': 'translated_eu2.json',
    'asia': 'translated_asia.json',
    'afr_oce': 'translated_afr_oce.json'
}

all_fr = {}
for k, fname in files.items():
    with open(fname, 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Loaded {fname}: {len(data)} countries")
        all_fr.update(data)

print(f"Total translated countries loaded: {len(all_fr)}")

with open('data.js', 'r', encoding='utf-8') as f:
    code = f.read()

m = re.search(r'const COUNTRIES_DATA = (\[.*?\]);\s*\n\s*const MODES_DATA', code, re.DOTALL)
if not m:
    print("Error: Could not locate COUNTRIES_DATA in data.js")
    exit(1)

countries = json.loads(m.group(1))
print(f"Existing countries in data.js: {len(countries)}")

updated_count = 0
for c in countries:
    cid = c['id']
    existing_p = c.get('paragraphs', [])
    if isinstance(existing_p, dict):
        en_p = existing_p.get('en', [])
    else:
        en_p = existing_p

    fr_p = all_fr.get(cid, [])
    if not fr_p and cid in ['the-netherlands', 'netherlands']:
        fr_p = all_fr.get('the-netherlands', all_fr.get('netherlands', []))
    if not fr_p and cid in ['the-uk', 'uk', 'united-kingdom']:
        fr_p = all_fr.get('the-uk', all_fr.get('uk', []))
    if not fr_p and cid in ['the-isle-of-man', 'isle-of-man']:
        fr_p = all_fr.get('the-isle-of-man', all_fr.get('isle-of-man', []))

    c['paragraphs'] = {
        'en': en_p,
        'fr': fr_p
    }
    updated_count += 1

print(f"Updated {updated_count} countries with bilingual paragraphs.")

new_countries_json = json.dumps(countries, ensure_ascii=False, indent=2)

new_code = code[:m.start()] + f"const COUNTRIES_DATA = {new_countries_json};\n\nconst MODES_DATA" + code[m.end():]

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("data.js successfully written!")
