import json
import re

print("Starting generate_bilingual_data.py...")

# Load raw extracted data
cheat_sheet = json.load(open('country_cheat_sheet.json', encoding='utf-8'))
modes_json = json.load(open('01_modes.json', encoding='utf-8'))
fund_json = json.load(open('02_fundamentals.json', encoding='utf-8'))
highways_json = json.load(open('03_highway_numbering.json', encoding='utf-8'))
general_json = json.load(open('04_general_clues.json', encoding='utf-8'))
meta_json = json.load(open('05_meta.json', encoding='utf-8'))
plates_json = json.load(open('06_license_plates.json', encoding='utf-8'))
languages_json = json.load(open('07_languages.json', encoding='utf-8'))

# Clean text helper
def clean_humor(text):
    if not text:
        return ""
    humor_patterns = [
        r"\(not the type of logic used in the recent poorly executed.*?Rotten Tomatoes\)",
        r"if my abacus is calibrated correctly, that means",
        r"\(everyone say this in unison\)\s*“fun and educational”",
        r"In pragmatic terms, GeoGuessr may only be useful if you are kidnapped.*?saying copyright counts as copyright, right\?",
        r"on a screen that looks uncannily like a smirking face, aware of the difficult locations that await you",
        r"predictably named ‘challenge’ button will allow you to invite friends or foe to play the same map against you to see who really is superior in a very esoteric task that has very little real-world purpose",
        r"and like The Lion, the Witch and the Wardrobe, you will be transported to a magical world with talking animals, mythical beasts and more restrictive GeoGuessr settings \(at least one of these three things is true\)\.",
        r"and shall be punishable by death\.",
        r"then good luck in recognising the individual blades of grass if your name isn’t Blinky \(the Roger Federer of GeoGuessr\)\.",
        r"something akin to being dropped in a location with binoculars whilst your legs are tied up\.",
        r"Everyone has a shady cousin whose scent whiffs of recreational drugs.*?memorised every road name in Ghana\.",
        r"which may come as a surprise to some Americans\.",
        r"\(I take back my previous remark\)",
        r"note: this may not be true for astronauts aboard the International Space Station\.",
        r"In theory, you could be provided a location in Eastern Russia.*?It’s a tough decision\.",
        r"my impatience means that I prefer",
        r"This will ensure that rounds don’t surpass the age of the observable universe\.",
        r"Are the point requirements for medals seemingly arbitrary numbers\? Yep\. Is it fun to play Explorer Mode, excluding the featureless Mongolian map\? Absolutely\.",
        r"\(and 2020 appropriate\)",
        r"doesn’t describe a potential future challenge for GeoWizard in which he must streak across each US state\.",
        r"memorise and perhaps get tattooed on your body",
        r"I yearn for the day that GeoGuessr add a ‘Mongolian Province Streak’ mode.*",
        r"widely known as earth\.",
        r"\(I refuse to call them ‘energy points’\)",
        r"\*checks calculator\*",
        r"If you are brave \(or foolish enough\) to click on ‘Multiplayer’",
        r"I’m glad that finally good variants of something have been released upon the world\.",
        r"\(position where you rank in the world and an extra number that you can lie about\)",
        r"although I don’t understand why people play these unranked versions\. Update: I’m reliably informed that apparently some people are not hyper-competitive about every activity in their waking lives\.",
        r"finally have a good reason to be anti-social on the weekends too\.",
        r"ferocious fight to the death between Prince Harry and Prince William in which the last prince standing inherits the throne \(although I would pay money to see this\)\.",
        r"rather than heading off down the road in search of kangaroos\.",
        r"stress-inducing",
        r"This version of the game could easily be used in cardiologists’ offices in which patients’ hearts need to be monitored whilst performing a stressful activity\.",
        r"who have no idea of the distress that awaits you\.",
        r"\(and also crowned the person with the sturdiest heart\)",
        r"\(and you may also be a liar as Andorra’s width is less than 30km\)",
        r"This is akin to dating lots of people at the same time and hoping that one is a reasonable human being \(and interested in GeoGuessr\)\.",
        r"descend into a game in which you try to destroy your opponent- then you are wrong\. Welcome to ‘Duels’\.",
        r"with the aim of vanquishing them with your GeoGuessr prowess\.",
        r"\(or enemies that you wish to crush with your GeoGuessr prowess\)",
        r"words not in my vocabulary\. You must work together \(more words not in my vocabulary\)",
        r"boffins have managed to squeeze another game mode",
        r"Personally I’m boycotting Google and will be reverting to search engine Alta Vista.*",
        r"\*Insert a rant involving something to do with the Geneva Convention\*\.",
        r"surviving any impending nuclear war, outliving the cockroaches and even the Kardashians\.",
        r"By now you have listened to far too much of my ramblings that are perhaps more suited to graffiti on a toilet wall\.",
        r"Firstly, I have never seen a street in Antarctica on the game and in fact I was unaware that Antarctica was a thriving metropolis that has frequent traffic jams\.",
        r"\(all hail Mr\. Wallén\)",
        r"\(I now have a useless knowledge of obscure Russian roads taking up space in my brain\)",
        r"Think of these maps as the communism of GeoGuessr, if that communism is a computer game involving geography largely outside of communist countries\.",
        r"\(providing further evidence that computers are plotting to take over the world\)",
        r"to muggings\.",
        r"causing you to make an appointment with an optometrist\?.*",
        r"A movie idea- A Street View driver captures their own death on Halloween as they are killed by monsters\. Trademark\.",
        r"Which of these traits is more useful is debatable\.",
        r"and rotating your computer around won’t move this compass\.",
        r"akin to some ancient civilisation’s infatuated worshipping of the sun",
        r"I for one stand against streaming services such as Netflix due to their potential destruction of TV satellite dishes.*",
        r"This of course ignores drunk drivers, hoons and those overtaking the chug-chug steady paced Google Street View car\.",
        r"Finding a left-hand side of the road car in GeoGuessr is akin to finding a dragon’s egg, wrapped in unicorn hair in the possession of a justifiably famous Kardashian\.",
        r"\(they aren’t invisible, there are just no cars around\)",
        r"For instance a ‘warning Lannister army approaching’ sign situated by the right hand side of the road \(from your perspective\) will likely mean that drivers in that country or fictional HBO world drive on the right side of the road\.",
        r"If the road is one way, you suspect a drunk driver is not obeying the country appropriate side-of-road driving law",
        r"resemble the 1976 boxing movie that I’m reliably informed they are named after\. Also they look rocky\.",
        r"\(AKA the ocean\)",
        r"Coincidence or conspiracy involving the government’s road naming department, corn growers and aliens\?",
    ]
    res = text
    for pat in humor_patterns:
        res = re.sub(pat, "", res, flags=re.IGNORECASE)
    res = re.sub(r'\s{2,}', ' ', res).strip()
    return res

COUNTRY_FR_MAP = {
    "USA": ("États-Unis", "Amérique du Nord"),
    "Canada": ("Canada", "Amérique du Nord"),
    "Puerto Rico": ("Porto Rico", "Amérique du Nord"),
    "The Dominican Republic": ("République Dominicaine", "Amérique du Nord"),
    "Costa Rica": ("Costa Rica", "Amérique du Nord"),
    "Mexico": ("Mexique", "Amérique du Nord"),
    "Guatemala": ("Guatemala", "Amérique du Nord"),
    "US Virgin Islands": ("Îles Vierges des États-Unis", "Amérique du Nord"),
    "Bermuda": ("Bermudes", "Amérique du Nord"),
    "Panama": ("Panama", "Amérique du Nord"),
    "Ireland": ("Irlande", "Europe"),
    "The U.K.": ("Royaume-Uni", "Europe"),
    "The Isle of Man": ("Île de Man", "Europe"),
    "Jersey": ("Jersey", "Europe"),
    "Portugal": ("Portugal", "Europe"),
    "Spain": ("Espagne", "Europe"),
    "The Canary Islands": ("Îles Canaries", "Europe"),
    "Andorra": ("Andorre", "Europe"),
    "Gibraltar": ("Gibraltar", "Europe"),
    "France": ("France", "Europe"),
    "Belgium": ("Belgique", "Europe"),
    "The Netherlands": ("Pays-Bas", "Europe"),
    "Luxembourg": ("Luxembourg", "Europe"),
    "Italy": ("Italie", "Europe"),
    "San Marino": ("Saint-Marin", "Europe"),
    "Norway": ("Norvège", "Europe"),
    "Svalbard": ("Svalbard", "Europe"),
    "Sweden": ("Suède", "Europe"),
    "Finland": ("Finlande", "Europe"),
    "Denmark": ("Danemark", "Europe"),
    "The Faroe Islands": ("Îles Féroé", "Europe"),
    "Iceland": ("Islande", "Europe"),
    "Greenland": ("Groenland", "Europe"),
    "Germany": ("Allemagne", "Europe"),
    "Austria": ("Autriche", "Europe"),
    "Switzerland": ("Suisse", "Europe"),
    "Liechtenstein": ("Liechtenstein", "Europe"),
    "Poland": ("Pologne", "Europe"),
    "Lithuania": ("Lituanie", "Europe"),
    "Latvia": ("Lettonie", "Europe"),
    "Estonia": ("Estonie", "Europe"),
    "Czechia (The Czech Republic)": ("Tchéquie", "Europe"),
    "Slovakia": ("Slovaquie", "Europe"),
    "Slovenia": ("Slovénie", "Europe"),
    "Hungary": ("Hongrie", "Europe"),
    "Croatia": ("Croatie", "Europe"),
    "Bosnia and Herzegovina": ("Bosnie-Herzégovine", "Europe"),
    "Albania": ("Albanie", "Europe"),
    "Greece": ("Grèce", "Europe"),
    "Cyprus": ("Chypre", "Europe"),
    "Romania": ("Roumanie", "Europe"),
    "Montenegro": ("Monténégro", "Europe"),
    "Serbia": ("Serbie", "Europe"),
    "North Macedonia": ("Macédoine du Nord", "Europe"),
    "Bulgaria": ("Bulgarie", "Europe"),
    "Ukraine": ("Ukraine", "Europe"),
    "Russia": ("Russie", "Europe"),
    "The Russian Landscape": ("Paysages Russes (Régions)", "Europe"),
    "Malta": ("Malte", "Europe"),
    "Australia": ("Australie", "Océanie"),
    "New Zealand": ("Nouvelle-Zélande", "Océanie"),
    "American Samoa": ("Samoa américaines", "Océanie"),
    "Northern Mariana Islands": ("Îles Mariannes du Nord", "Océanie"),
    "Guam": ("Guam", "Océanie"),
    "Midway Atoll": ("Atoll de Midway", "Océanie"),
    "Christmas Island": ("Île Christmas", "Océanie"),
    "South Africa": ("Afrique du Sud", "Afrique"),
    "Botswana": ("Botswana", "Afrique"),
    "Eswatini": ("Eswatini", "Afrique"),
    "Lesotho": ("Lesotho", "Afrique"),
    "Namibia": ("Namibie", "Afrique"),
    "Uganda": ("Ouganda", "Afrique"),
    "Kenya": ("Kenya", "Afrique"),
    "Rwanda": ("Rwanda", "Afrique"),
    "Ghana": ("Ghana", "Afrique"),
    "Nigeria": ("Nigeria", "Afrique"),
    "Senegal": ("Sénégal", "Afrique"),
    "Tunisia": ("Tunisie", "Afrique"),
    "Reunion": ("La Réunion", "Afrique"),
    "Madagascar": ("Madagascar", "Afrique"),
    "Sao Tome and Principe": ("Sao Tomé-et-Principe", "Afrique"),
    "Bhutan": ("Bhoutan", "Asie"),
    "Hong Kong": ("Hong Kong", "Asie"),
    "Macau": ("Macao", "Asie"),
    "Japan": ("Japon", "Asie"),
    "Cambodia": ("Cambodge", "Asie"),
    "Thailand": ("Thaïlande", "Asie"),
    "Taiwan": ("Taïwan", "Asie"),
    "South Korea": ("Corée du Sud", "Asie"),
    "The United Arab Emirates": ("Émirats Arabes Unis", "Asie"),
    "Jordan": ("Jordanie", "Asie"),
    "Qatar": ("Qatar", "Asie"),
    "Oman": ("Oman", "Asie"),
    "Israel": ("Israël", "Asie"),
    "Palestine": ("Palestine", "Asie"),
    "Lebanon": ("Liban", "Asie"),
    "Kyrgyzstan": ("Kirghizistan", "Asie"),
    "Mongolia": ("Mongolie", "Asie"),
    "Kazakhstan": ("Kazakhstan", "Asie"),
    "Indonesia": ("Indonésie", "Asie"),
    "Malaysia": ("Malaisie", "Asie"),
    "Vietnam": ("Vietnam", "Asie"),
    "Laos": ("Laos", "Asie"),
    "The Philippines": ("Philippines", "Asie"),
    "Sri Lanka": ("Sri Lanka", "Asie"),
    "Bangladesh": ("Bangladesh", "Asie"),
    "Nepal": ("Népal", "Asie"),
    "India": ("Inde", "Asie"),
    "Pakistan": ("Pakistan", "Asie"),
    "Singapore": ("Singapour", "Asie"),
    "Turkey": ("Turquie", "Asie"),
    "Brazil": ("Brésil", "Amérique du Sud"),
    "How to Identify the Regions of Brazil": ("Régions du Brésil (Guide détaillé)", "Amérique du Sud"),
    "Paraguay": ("Paraguay", "Amérique du Sud"),
    "Argentina": ("Argentine", "Amérique du Sud"),
    "Uruguay": ("Uruguay", "Amérique du Sud"),
    "Ecuador": ("Équateur", "Amérique du Sud"),
    "Colombia": ("Colombie", "Amérique du Sud"),
    "Peru": ("Pérou", "Amérique du Sud"),
    "Bolivia": ("Bolivie", "Amérique du Sud"),
    "Chile": ("Chili", "Amérique du Sud"),
    "Curaçao": ("Curaçao", "Amérique du Sud"),
    "Curaao": ("Curaçao", "Amérique du Sud")
}

FLAG_TLD_MAP = {
    "USA": ("🇺🇸", ".us"),
    "Canada": ("🇨🇦", ".ca"),
    "Puerto Rico": ("🇵🇷", ".pr"),
    "The Dominican Republic": ("🇩🇴", ".do"),
    "Costa Rica": ("🇨🇷", ".cr"),
    "Mexico": ("🇲🇽", ".mx"),
    "Guatemala": ("🇬🇹", ".gt"),
    "US Virgin Islands": ("🇻🇮", ".vi"),
    "Bermuda": ("🇧🇲", ".bm"),
    "Panama": ("🇵🇦", ".pa"),
    "Ireland": ("🇮🇪", ".ie"),
    "The U.K.": ("🇬🇧", ".uk"),
    "The Isle of Man": ("🇮🇲", ".im"),
    "Jersey": ("🇯🇪", ".je"),
    "Portugal": ("🇵🇹", ".pt"),
    "Spain": ("🇪🇸", ".es"),
    "The Canary Islands": ("🇮🇨", ".es"),
    "Andorra": ("🇦🇩", ".ad"),
    "Gibraltar": ("🇬🇮", ".gi"),
    "France": ("🇫🇷", ".fr"),
    "Belgium": ("🇧🇪", ".be"),
    "The Netherlands": ("🇳🇱", ".nl"),
    "Luxembourg": ("🇱🇺", ".lu"),
    "Italy": ("🇮🇹", ".it"),
    "San Marino": ("🇸🇲", ".sm"),
    "Norway": ("🇳🇴", ".no"),
    "Svalbard": ("🇸🇯", ".sj"),
    "Sweden": ("🇸🇪", ".se"),
    "Finland": ("🇫🇮", ".fi"),
    "Denmark": ("🇩🇰", ".dk"),
    "The Faroe Islands": ("🇫🇴", ".fo"),
    "Iceland": ("🇮🇸", ".is"),
    "Greenland": ("🇬🇱", ".gl"),
    "Germany": ("🇩🇪", ".de"),
    "Austria": ("🇦🇹", ".at"),
    "Switzerland": ("🇨🇭", ".ch"),
    "Liechtenstein": ("🇱🇮", ".li"),
    "Poland": ("🇵🇱", ".pl"),
    "Lithuania": ("🇱🇹", ".lt"),
    "Latvia": ("🇱🇻", ".lv"),
    "Estonia": ("🇪🇪", ".ee"),
    "Czechia (The Czech Republic)": ("🇨🇿", ".cz"),
    "Slovakia": ("🇸🇰", ".sk"),
    "Slovenia": ("🇸🇮", ".si"),
    "Hungary": ("🇭🇺", ".hu"),
    "Croatia": ("🇭🇷", ".hr"),
    "Bosnia and Herzegovina": ("🇧🇦", ".ba"),
    "Albania": ("🇦🇱", ".al"),
    "Greece": ("🇬🇷", ".gr"),
    "Cyprus": ("🇨🇾", ".cy"),
    "Romania": ("🇷🇴", ".ro"),
    "Montenegro": ("🇲🇪", ".me"),
    "Serbia": ("🇷🇸", ".rs"),
    "North Macedonia": ("🇲🇰", ".mk"),
    "Bulgaria": ("🇧🇬", ".bg"),
    "Ukraine": ("🇺🇦", ".ua"),
    "Russia": ("🇷🇺", ".ru"),
    "The Russian Landscape": ("🇷🇺", ".ru"),
    "Malta": ("🇲🇹", ".mt"),
    "Australia": ("🇦🇺", ".au"),
    "New Zealand": ("🇳🇿", ".nz"),
    "American Samoa": ("🇦🇸", ".as"),
    "Northern Mariana Islands": ("🇲🇵", ".mp"),
    "Guam": ("🇬🇺", ".gu"),
    "Midway Atoll": ("🇺🇸", ".us"),
    "Christmas Island": ("🇨🇽", ".cx"),
    "South Africa": ("🇿🇦", ".za"),
    "Botswana": ("🇧🇼", ".bw"),
    "Eswatini": ("🇸🇿", ".sz"),
    "Lesotho": ("🇱🇸", ".ls"),
    "Namibia": ("🇳🇦", ".na"),
    "Uganda": ("🇺🇬", ".ug"),
    "Kenya": ("🇰🇪", ".ke"),
    "Rwanda": ("🇷🇼", ".rw"),
    "Ghana": ("🇬🇭", ".gh"),
    "Nigeria": ("🇳🇬", ".ng"),
    "Senegal": ("🇸🇳", ".sn"),
    "Tunisia": ("🇹🇳", ".tn"),
    "Reunion": ("🇷🇪", ".re"),
    "Madagascar": ("🇲🇬", ".mg"),
    "Sao Tome and Principe": ("🇸🇹", ".st"),
    "Bhutan": ("🇧🇹", ".bt"),
    "Hong Kong": ("🇭🇰", ".hk"),
    "Macau": ("🇲🇴", ".mo"),
    "Japan": ("🇯🇵", ".jp"),
    "Cambodia": ("🇰🇭", ".kh"),
    "Thailand": ("🇹🇭", ".th"),
    "Taiwan": ("🇹🇼", ".tw"),
    "South Korea": ("🇰🇷", ".kr"),
    "The United Arab Emirates": ("🇦🇪", ".ae"),
    "Jordan": ("🇯🇴", ".jo"),
    "Qatar": ("🇶🇦", ".qa"),
    "Oman": ("🇴🇲", ".om"),
    "Israel": ("🇮🇱", ".il"),
    "Palestine": ("🇵🇸", ".ps"),
    "Lebanon": ("🇱🇧", ".lb"),
    "Kyrgyzstan": ("🇰🇬", ".kg"),
    "Mongolia": ("🇲🇳", ".mn"),
    "Kazakhstan": ("🇰🇿", ".kz"),
    "Indonesia": ("🇮🇩", ".id"),
    "Malaysia": ("🇲🇾", ".my"),
    "Vietnam": ("🇻🇳", ".vn"),
    "Laos": ("🇱🇦", ".la"),
    "The Philippines": ("🇵🇭", ".ph"),
    "Sri Lanka": ("🇱🇰", ".lk"),
    "Bangladesh": ("🇧🇩", ".bd"),
    "Nepal": ("🇳🇵", ".np"),
    "India": ("🇮🇳", ".in"),
    "Pakistan": ("🇵🇰", ".pk"),
    "Singapore": ("🇸🇬", ".sg"),
    "Turkey": ("🇹🇷", ".tr"),
    "Brazil": ("🇧🇷", ".br"),
    "How to Identify the Regions of Brazil": ("🇧🇷", ".br"),
    "Paraguay": ("🇵🇾", ".py"),
    "Argentina": ("🇦🇷", ".ar"),
    "Uruguay": ("🇺🇾", ".uy"),
    "Ecuador": ("🇪🇨", ".ec"),
    "Colombia": ("🇨🇴", ".co"),
    "Peru": ("🇵🇪", ".pe"),
    "Bolivia": ("🇧🇴", ".bo"),
    "Chile": ("🇨🇱", ".cl"),
    "Curaçao": ("🇨🇼", ".cw"),
    "Curaao": ("🇨🇼", ".cw")
}

LEFT_DRIVING_COUNTRIES = {
    "The U.K.", "Ireland", "The Isle of Man", "Jersey", "Malta", "Cyprus",
    "South Africa", "Botswana", "Eswatini", "Lesotho", "Namibia", "Kenya", "Uganda",
    "Japan", "Hong Kong", "Macau", "Singapore", "Malaysia", "Thailand", "Indonesia",
    "Sri Lanka", "Bangladesh", "India", "Bhutan", "Pakistan",
    "Australia", "New Zealand", "Christmas Island",
    "US Virgin Islands", "Bermuda"
}

KEY_GIVEAWAYS_BILINGUAL = {
    "Kenya": {
        "en": "Black snorkel mounted on the right front pillar of the Google car.",
        "fr": "Snorkel d'admission noir monté sur le montant avant-droit de la Google car."
    },
    "Ghana": {
        "en": "Visible roof rack with distinctive black electrical tape wrapped around one bar.",
        "fr": "Galerie de toit avec ruban adhésif noir distinctif enroulé autour d'une barre."
    },
    "Guatemala": {
        "en": "Google car roof rack with protruding side mirrors visible in rear view.",
        "fr": "Galerie de toit avec deux rétroviseurs latéraux bien visibles vers l'arrière."
    },
    "Mongolia": {
        "en": "Pickup truck bed packed with camping gear, spare tires, and luggage under a tarp.",
        "fr": "Benne de pickup remplie de matériel de camping, pneus de secours et sacs sous bâche."
    },
    "Senegal": {
        "en": "Roof rack visible with distinct sky rifts (tears in the 360-degree panorama).",
        "fr": "Barres de toit visibles et déchirures prononcées dans le ciel à 360 degrés."
    },
    "Nigeria": {
        "en": "Followed or led by a police pickup escort vehicle with flashing red/blue light bar.",
        "fr": "Véhicule d'escorte policier (pick-up avec gyrophare) visible devant ou derrière."
    },
    "Curaçao": {
        "en": "Black pickup truck bed with prominent tubular steel bars.",
        "fr": "Benne de pick-up noire avec arceaux tubulaires métalliques massifs."
    },
    "Bermuda": {
        "en": "Compact open-hood buggy vehicle; driving on the left; white stepped roofs.",
        "fr": "Petit buggy à capot ouvert, conduite à gauche et toits étagés blancs caractéristiques."
    },
    "Dominican Republic": {
        "en": "White metal roof rack bars with black rubber feet.",
        "fr": "Barres de toit métalliques blanches avec pieds de fixation en caoutchouc noir."
    },
    "Reunion": {
        "en": "Blue/white car with antenna; steep tropical volcanic terrain; French signs.",
        "fr": "Voiture bleue ou blanche avec antenne sur relief volcanique abrupt et panneaux français."
    },
    "Uganda": {
        "en": "White car with visible roof rack and white front bumper; rich red soil.",
        "fr": "Voiture blanche avec galerie et pare-chocs avant blanc sur terre rouge vif."
    },
    "Sri Lanka": {
        "en": "White car with visible side mirrors and camera pole shadow; Sinhala/Tamil script; drives on left.",
        "fr": "Voiture blanche avec rétroviseurs et ombre du mât; écritures cingalaise/tamoule; conduite à gauche."
    },
    "Jordan": {
        "en": "Black or white pickup truck with roof rack and antenna; desert landscape; Arabic signage.",
        "fr": "Pick-up noir ou blanc avec galerie et antenne en milieu désertique arabophone."
    },
    "France": {
        "en": "Cylindrical white bollard with red/gray reflector band; yellow 'D-xxx' departmental road signs; double blue plate bands.",
        "fr": "Bollards cylindriques blancs à bande rouge/grise (uniques en Europe), bornes départementales 'D-xxx' et double bande bleue sur plaque."
    },
    "Poland": {
        "en": "Concrete utility poles with ladder holes ('Swiss cheese'); white bollards with slanted red band.",
        "fr": "Poteaux électriques en béton perforés de trous ronds (type 'gruyère') et délinéateurs à bande rouge inclinée."
    },
    "Iceland": {
        "en": "Bright yellow bollards; volcanic treeless landscapes; wooden snow stakes; yellow center lines absent.",
        "fr": "Bollards entièrement jaune vif; immenses paysages volcaniques dépourvus d'arbres."
    },
    "Norway": {
        "en": "Yellow center road lines with white outer dashed lines (unique in Europe); green E-road signs; deep fjords.",
        "fr": "Ligne centrale jaune continue avec lignes blanches tiretées sur les côtés (unique en Europe) et fjords escarpés."
    },
    "Sweden": {
        "en": "Blue rectangular road number signs without letter prefixes; yellow dashed outer edge lines; Falun red wooden houses.",
        "fr": "Panneaux routiers bleus rectangulaires sans préfixe de lettre, lignes de rive tiretées blanches et maisons en bois rouge de Falun."
    },
    "Finland": {
        "en": "Red rectangular main highway signs (1-29); yellow secondary (40-99); non-Germanic double vowel road names (-tie, -katu).",
        "fr": "Numéros de routes principaux en rouge (1-29), secondaires en jaune (40-99); suffixes de rues finnois en '-tie' ou '-katu'."
    },
    "Denmark": {
        "en": "White bollard with yellow reflector; flat terrain; thatched or red brick houses; red/white bicycle signs.",
        "fr": "Bollards blancs à réflecteur jaune; relief plat; maisons en briques rouges et fléchages cyclables rouges et blancs."
    },
    "Germany": {
        "en": "Black-capped bollard with vertical front reflector and two dots on rear; extensive camera blurring in older coverage; no speed limit signs on Autobahn.",
        "fr": "Bollards à sommet noir (trait vertical avant, deux points arrière); floutage massif d'habitations dans l'ancienne couverture; panneaux d'Autobahn."
    },
    "Austria": {
        "en": "Sloping curved-top bollards; alpine architecture; green motorway signs; white pedestrian crossing on blue square.",
        "fr": "Bollards à sommet biseauté et incurvé; chalets alpins soignés et panneaux autoroutiers verts."
    },
    "Switzerland": {
        "en": "Low Gen 4 camera; yellow diamond warning signs with white borders; yellow diamond pedestrian crossing signs; bilingual cantons.",
        "fr": "Caméra Gen 4 basse; passages piétons avec marquage jaune vif au sol; panneaux losanges jaunes bordés de blanc."
    },
    "Italy": {
        "en": "Double blue strips on license plates with small front plate; black-capped bollards with red front / white rear reflectors.",
        "fr": "Double bande bleue sur plaque avec plaque avant raccourcie; bollards à capuchon noir (réflecteur rouge avant, blanc arrière)."
    },
    "Spain": {
        "en": "Ladder utility poles with metal rungs; AP-xxx, A-xxx, N-xxx highways; white bollards with black cap.",
        "fr": "Poteaux électriques en béton avec échelons métalliques (style échelle); routes AP-xxx, A-xxx et N-xxx; bollards à dessus noir."
    },
    "Portugal": {
        "en": "Yellow stripe on right side of older license plates; ladder concrete poles; blue motorway signs.",
        "fr": "Bande jaune sur le côté droit des anciennes plaques; poteaux en béton à échelons; trottoirs en calçada portugaise."
    },
    "The U.K.": {
        "en": "White front and yellow rear license plates; driving on the left; red circular speed limit signs with black numbers in mph.",
        "fr": "Plaques avant blanches et arrière jaunes; conduite à gauche; limitations de vitesse rondes bordées de rouge en mph."
    },
    "Ireland": {
        "en": "Yellow diamond warning signs (like US); yellow dashed outer road lines; bilingual road signs (Gaeilge in italic + English); driving on the left.",
        "fr": "Panneaux de danger losanges jaunes; lignes de rive tiretées jaunes; signalisation bilingue anglais/irlandais (en italique)."
    },
    "USA": {
        "en": "Yellow diamond warning signs; double yellow center lines; metal signposts with punched holes; 'SPEED LIMIT' signs in mph; interstate shield grid.",
        "fr": "Panneaux losanges jaunes; double ligne centrale jaune; poteaux métalliques à trous perforés; panneaux 'SPEED LIMIT' en miles."
    },
    "Canada": {
        "en": "'MAXIMUM' speed limit signs in km/h; Trans-Canada Highway 1 green maple leaf; white wooden utility poles; bilingual stop signs ('ARRET / STOP') in Quebec.",
        "fr": "Panneaux de vitesse 'MAXIMUM' en km/h; Autoroute 1 transcanadienne (feuille d'érable verte); poteaux en bois peints en blanc."
    },
    "Mexico": {
        "en": "Octagonal red 'ALTO' stop signs; Gen 2 camera in desert highways; white federal highway shields; triple-bolted wooden/concrete poles.",
        "fr": "Panneaux stop octogonaux 'ALTO'; caméra Gen 2 dans les zones désertiques; shields fédéraux blancs à bordure noire."
    },
    "Brazil": {
        "en": "BR-xxx highway numbering grid; phone area codes 11-99 on commercial signs; red soil; Araucaria (Paraná pine) in southern states.",
        "fr": "Réseau autoroutier BR-xxx; indicatifs téléphoniques régionaux (11 à 99) omniprésents; terre rouge; pins du Paraná au sud."
    },
    "Argentina": {
        "en": "Black-and-white chevron curve arrows; flat pampas; RN national route shields with white numbers on black background.",
        "fr": "Chevrons de virage noirs et blancs; immensité plate de la Pampa; routes nationales RN en blanc sur fond noir."
    },
    "Chile": {
        "en": "White dashed outer edge lines; extremely narrow country; Andes mountains visible eastward.",
        "fr": "Lignes de rive tiretées blanches; relief très effilé; imposante cordillère des Andes systématiquement visible à l'Est."
    },
    "Colombia": {
        "en": "Yellow license plates on all public transport/taxis; white cross marking on back of road signs; mountainous Andean roads.",
        "fr": "Plaques d'immatriculation jaunes sur tous les taxis et bus; croix blanche peinte au dos des panneaux routiers."
    },
    "Peru": {
        "en": "Utility poles with bottom half painted black and white stripes; high Andean altiplano; mototaxis (tuk-tuks) in towns.",
        "fr": "Poteaux électriques rayés noir et blanc à la base; mototaxis à 3 roues (tuk-tuks); paysages andins arides."
    },
    "Bolivia": {
        "en": "Unpaved dirt highways; Cholita bowler hats and traditional dress; brick buildings without external plastering.",
        "fr": "Pistes en terre battue; chapeaux melons traditionnels des Cholitas; maisons en briques apparentes non crépies."
    },
    "Australia": {
        "en": "Driving on the left; eucalyptus trees; white wooden/metal guideposts with red reflector on left and white on right; blurry Gen 1/2 in outback.",
        "fr": "Conduite à gauche; eucalyptus omniprésents; délinéateurs à réflecteur rouge à gauche et blanc à droite; flou Gen 1/2 dans l'outback."
    },
    "New Zealand": {
        "en": "Driving on the left; lush rolling green hills; wooden posts with white reflector front and red rear; dashed white center lines.",
        "fr": "Conduite à gauche; collines vallonnées d'un vert intense; piquets en bois à réflecteur blanc avant et rouge arrière."
    },
    "Japan": {
        "en": "Driving on the left; blue national highway shields; yellow license plates on Kei cars; low utility poles with intricate cable bundles.",
        "fr": "Conduite à gauche; shields triangulaires bleus; plaques jaunes sur petites voitures Kei; densité extrême de câbles électriques."
    },
    "South Korea": {
        "en": "Driving on the right; Hangul script; yellow license plates on commercial vehicles; urban blue highway shields.",
        "fr": "Conduite à droite; écriture Hangul avec cercles et barres géométriques; plaques jaunes sur véhicules commerciaux."
    },
    "Taiwan": {
        "en": "Yellow and black diagonal striped utility poles; Traditional Chinese characters; scooters everywhere.",
        "fr": "Poteaux électriques à base peinte de rayures diagonales jaunes et noires; caractères chinois traditionnels; nuées de scooters."
    },
    "Thailand": {
        "en": "Driving on the left; Thai script with small loops; curved concrete utility poles; spirit houses outside homes.",
        "fr": "Conduite à gauche; écriture thaïlandaise à petites boucles; poteaux électriques à section carrée ou incurvée."
    },
    "Cambodia": {
        "en": "Driving on the right; Khmer script with squiggly feet; blue beer advertising signboards; Khmer architecture.",
        "fr": "Conduite à droite; écriture khmère ornée avec empattements ondulés sous les lettres; enseignes de bière bleues en bord de route."
    },
    "Indonesia": {
        "en": "Driving on the left; black and white striped curbs; 'Jl.' for Jalan; red and white national flag; tropical lush volcanic landscape.",
        "fr": "Conduite à gauche; trottoirs peints en noir et blanc; mention 'Jl.' (Jalan); végétation tropicale volcanique dense."
    },
    "Malaysia": {
        "en": "Driving on the left; Federal route shields with yellow/white numbers on black; 'Jalan' written in full; palm oil plantations.",
        "fr": "Conduite à gauche; routes fédérales avec numéro blanc/jaune sur shield noir; mot 'Jalan' écrit en toutes lettres; palmiers à huile."
    },
    "Philippines": {
        "en": "Driving on the right; English/Tagalog signage; Jeepneys and tricycles; yellow diamond warning signs.",
        "fr": "Conduite à droite; panneaux entièrement rédigés en anglais; Jeepneys colorés et tricycles; panneaux losanges jaunes."
    },
    "South Africa": {
        "en": "Driving on the left; yellow outer road shoulder lines; white on blue chevron arrows; English signage; .za domain.",
        "fr": "Conduite à gauche; ligne de rive jaune continue en bord de route; chevrons de virage blancs sur fond bleu; domaine .za."
    },
    "Botswana": {
        "en": "Driving on the left; very flat arid savannah; low thorny acacia scrub; white-faced donkey carts.",
        "fr": "Conduite à gauche; savane plate et semi-aride; acacias épineux bas; charrettes tirées par des ânes."
    },
    "Eswatini": {
        "en": "Driving on the left; hilly green terrain; yellow outer road lines; pine plantations; southern African architecture.",
        "fr": "Conduite à gauche; relief montagneux verdoyant; lignes de rive jaunes; plantations de pins."
    },
    "Lesotho": {
        "en": "Driving on the left; mountainous highland scenery without trees; traditional Basotho blankets and conical straw hats.",
        "fr": "Conduite à gauche; hautes montagnes dénudées sans arbres; couvertures basotho traditionnelles et chapeaux de paille coniques."
    },
    "Russia": {
        "en": "Birch tree forests; Cyrillic signage; M/R/A highway numbering; concrete bus stops; Gen 3/4 camera.",
        "fr": "Forêts de bouleaux denses; alphabet cyrillique; routes M, R et A; abribus massifs en béton; absence de plaques bleues."
    },
    "Ukraine": {
        "en": "Cyrillic containing unique letters 'і', 'ї', 'є'; blue and yellow painted infrastructure; concrete poles with white-painted bases.",
        "fr": "Cyrillique contenant les lettres uniques 'і', 'ї', 'є'; rambardes peintes aux couleurs nationales (bleu et jaune); bases de poteaux blanches."
    },
    "Israel": {
        "en": "Both front and rear license plates yellow; Hebrew and Arabic signage; red and white curb markings.",
        "fr": "Plaques d'immatriculation jaunes à l'avant et à l'arrière; écritures hébraïque et arabe; trottoirs rayés rouge et blanc."
    },
    "Turkey": {
        "en": "Slanted top white bollards with red reflector on right, white on left; Turkish letters (ç, ğ, ı, ö, ş, ü); D-xxx road signs.",
        "fr": "Bollards blancs à sommet biseauté orienté vers la droite; lettres turques spécifiques (ç, ğ, ı, ö, ş, ü); routes 'D-xxx'."
    },
    "Greece": {
        "en": "Greek alphabet (Ω, Δ, Σ, etc.); blue motorway signs; solar water heaters on flat concrete rooftops.",
        "fr": "Alphabet grec unique (Ω, Δ, Σ, etc.); panneaux autoroutiers bleus; chauffe-eaux solaires sur tous les toits plats."
    }
}

# Compile Countries
compiled_countries = []
for c in cheat_sheet['countries']:
    name = c['country']
    fr_name, fr_cont = COUNTRY_FR_MAP.get(name, (name, c['continent']))
    en_cont = c['continent']
    cid = c['id']
    flag, tld = FLAG_TLD_MAP.get(name, ("🏳️", ".com"))
    is_left = name in LEFT_DRIVING_COUNTRIES
    
    # Giveaway
    giveaways = KEY_GIVEAWAYS_BILINGUAL.get(name, {
        "en": f"Official Street View coverage with standard {en_cont} infrastructure.",
        "fr": f"Couverture Street View officielle avec infrastructure typique d'{fr_cont}."
    })
    
    # Paragraphs (English raw cleaned)
    clean_p = [clean_humor(p) for p in c['paragraphs'] if p and len(clean_humor(p)) > 10]
    
    # Filter valid images
    clean_imgs = []
    for img in c['images']:
        src = img.get('src')
        if src and ('somerandomstuff1.wordpress.com' in src or 'wikimedia.org' in src or 'imgur' in src):
            clean_imgs.append({
                "src": src,
                "alt": clean_humor(img.get('alt', '')),
                "caption": clean_humor(img.get('caption', ''))
            })
            
    compiled_countries.append({
        "id": cid,
        "name": { "en": name, "fr": fr_name },
        "continent": { "en": en_cont, "fr": fr_cont },
        "flag": flag,
        "tld": tld,
        "drivingSide": {
            "en": "Left" if is_left else "Right",
            "fr": "Gauche" if is_left else "Droite"
        },
        "isLeft": is_left,
        "giveaway": giveaways,
        "paragraphs": clean_p,
        "images": clean_imgs[:15]
    })

print(f"Bilingual compilation complete: {len(compiled_countries)} countries processed.")

# Fully translated bilingual section datasets

MODES_DATA = {
    "en": [
        {
            "id": "classic",
            "title": "Classic & Custom Maps",
            "badge": "Core Gameplay",
            "summary": "Standard GeoGuessr matches consisting of 5 rounds per game. Play on the World Map, Famous Places, United States, European Union, or community maps.",
            "points": [
                "Scoring: Maximum 5,000 points per round (25,000 perfect score). Points scale by distance from 5,000 pts within ~150 meters down to 0 at the antipode.",
                "Time Limits: Configurable from 10 seconds (blitz) to 10 minutes or infinite exploration.",
                "Movement Modes: Moving (standard navigation), No Move (NM - rotate and zoom only), or No Move Pan Zoom (NMPZ - still frame testing pure visual memory)."
            ]
        },
        {
            "id": "explorer",
            "title": "Explorer Mode",
            "badge": "Country Mastery",
            "summary": "Single-player medal challenge to master individual nation maps and unlock global badges.",
            "points": [
                "Bronze Medal: 5,000+ points.",
                "Silver Medal: 15,000+ points.",
                "Gold Medal: 22,500+ points (demands near-pinpoint accuracy in 5 rounds).",
                "Strategy: Tough countries with repetitive rural coverage (e.g. Mongolia, Kyrgyzstan) can be conquered by taking notes on unique landscape features, road angles, and repeating coverage locations."
            ]
        },
        {
            "id": "streaks",
            "title": "Country Streaks & US State Streaks",
            "badge": "Survival Streak",
            "summary": "Consecutive guessing mode where one single mistake ends your run. Build the longest possible streak.",
            "points": [
                "Country Streaks: Identify the nation correctly. Tip: In-game flag trick—if you spot an unfamiliar flag on a building or pole, click countries on the guessing map to match the flag artwork.",
                "US State Streaks: Demands mastery of US Interstate odd/even numbering, unique state highway shield silhouettes, front vs. rear license plate laws (19 states require rear only), and speed limit signs (65-70 mph East vs. 75-80 mph West)."
            ]
        },
        {
            "id": "daily",
            "title": "The Daily Challenge",
            "badge": "Daily Competitive",
            "summary": "A fresh curated 5-round seed every 24 hours played against the entire global player base.",
            "points": [
                "Time Limit: 3 minutes per round.",
                "Conditions: Moving, panning, and zooming permitted.",
                "Competitive Etiquette: External web searching is frowned upon; top leaderboard ranks require pure unassisted deduction."
            ]
        },
        {
            "id": "maprunner",
            "title": "Maprunner",
            "badge": "Rogue-lite Mode",
            "summary": "Progressive path-based challenge where player energy serves as health.",
            "points": [
                "Energy Health: Start with 10,000 energy points. Points below 5,000 in a round are deducted from your energy (e.g., scoring 4,000 loses 1,000 energy).",
                "Power-ups: Pick paths strategically to gain power-ups and energy restorations to survive through to the finish line."
            ]
        },
        {
            "id": "battle-royale-countries",
            "title": "Battle Royale: Countries",
            "badge": "Multiplayer Knockout",
            "summary": "10-player knockout match where players race to identify the correct country before the timer runs out.",
            "points": [
                "Eliminated Flags: Wrong guesses by other players appear in the top-right corner. Use these to eliminate possibilities—never guess an already discarded flag.",
                "Early Rounds: Take your time; all players who guess correctly before the timer expires advance.",
                "Late Game (Final 2-3 players): Lock in an intuitive guess early before the timer starts, then keep moving while the timer counts down.",
                "The 1v1 Standoff: When you know the location, wait until the yellow warning timer is almost exhausted before locking in your guess to prevent your opponent from copying or panicking into your choice.",
                "50/50 Lifeline: Reserve the 50/50 lifeline for round 3 onwards or when down to your final lifeline after 2 failed guesses."
            ]
        },
        {
            "id": "battle-royale-distance",
            "title": "Battle Royale: Distance",
            "badge": "Multiplayer Precision",
            "summary": "10-player match where the player furthest from the actual Street View location is eliminated each round.",
            "points": [
                "Round Time: 1 minute per round. Maximum 3 guesses per round.",
                "Leaderboard Gap Tracking: Live display shows distance (km) behind the leader and gap to the player behind you. If a subsequent guess reduces your gap, you're heading in the correct direction.",
                "Capital City Bias: In large countries when lacking pinpoint clues (e.g. Ukraine, Colombia, Russia), central urban / capital guesses (Kyiv, Bogotá, Moscow) minimize maximum distance risk.",
                "Conserving Guesses: Extra guesses are awarded for advancing; bank saved guesses for the high-pressure final rounds.",
                "Endgame 1v1 Tactic: If your opponent has 3 guesses and you have only 1, hold your guess until the final 15 seconds so they cannot calibrate their guesses against your distance."
            ]
        },
        {
            "id": "duels",
            "title": "Duels (1v1 Competitive)",
            "badge": "Premier Ranked",
            "summary": "Intense head-to-head battle with 6,000 starting Health Points. Damage dealt equals traditional point score difference.",
            "points": [
                "Damage Multipliers: Starting in Round 5, damage multiplies by 1.5x, escalating by +0.5x each round (Round 6 = 2.0x, Round 7 = 2.5x, Round 8 = 3.0x).",
                "15-Second Clock: The instant the first player submits a guess, a 15-second countdown triggers for the opponent.",
                "Fast Guess Tactic: If you spot an unmistakable country clue (e.g., Polish Swiss-cheese pole, Kenyan snorkel, Ghanaian tape), guess immediately to trap your opponent in the 15-second scramble.",
                "Defensive Strategy: If your opponent guesses first, place your pin immediately on your best estimate, but DO NOT press submit! Use the entire 15 seconds to look for street signs or town names—the system locks your pin automatically when the clock hits zero.",
                "Avoid Pinpoint Traps: Never waste time finding an exact intersection or building in Duels—general regional accuracy and speed win matches."
            ]
        }
    ],
    "fr": [
        {
            "id": "classic",
            "title": "Cartes Classiques & Personnalisées",
            "badge": "Mode Fondamental",
            "summary": "Parties standard GeoGuessr en 5 manches. Jouez sur la carte du Monde, Lieux Célèbres, États-Unis, Union Européenne ou sur des cartes créées par la communauté.",
            "points": [
                "Système de points : Maximum 5 000 points par manche (score parfait à 25 000). Les points s'échelonnent de 5 000 pts à ~150 mètres jusqu'à 0 à l'antipode.",
                "Contrôle du temps : Configurable de 10 secondes (blitz ultra-rapide) à 10 minutes, ou sans limite de temps.",
                "Paramètres de déplacement : Moving (déplacement libre), No Move (NM - rotation et zoom uniquement), No Move Pan Zoom (NMPZ - image fixe, test ultime de mémoire visuelle)."
            ]
        },
        {
            "id": "explorer",
            "title": "Mode Explorateur",
            "badge": "Maîtrise Nationale",
            "summary": "Défi solo pays par pays pour débloquer les médailles et maîtriser les spécificités de chaque nation.",
            "points": [
                "Médaille de Bronze : 5 000+ points.",
                "Médaille d'Argent : 15 000+ points.",
                "Médaille d'Or : 22 500+ points (exige une excellente précision sur les 5 manches).",
                "Stratégie : Pour les pays ruraux complexes (ex. Mongolie, Kirghizistan), notez les angles de routes, paysages caractéristiques et repérez les positions récurrentes."
            ]
        },
        {
            "id": "streaks",
            "title": "Séries de Pays & Séries d'États US",
            "badge": "Mode Survie",
            "summary": "Mode de survie consécutive où une seule erreur met fin à votre partie. Visez la plus longue série possible.",
            "points": [
                "Séries de Pays : Astuce des drapeaux : si vous repérez un drapeau inconnu sur un bâtiment ou un mât, cliquez sur la carte en bas pour comparer son dessin avec les drapeaux nationaux.",
                "Séries d'États US : Exige la maîtrise de la numérotation des Interstates (pairs/impairs), des silhouettes de panneaux d'États, des lois de plaques d'immatriculation (19 États à plaque arrière seule) et des panneaux de vitesse (65-70 mph à l'Est vs 75-80 mph à l'Ouest)."
            ]
        },
        {
            "id": "daily",
            "title": "Le Défi Quotidien (Daily Challenge)",
            "badge": "Compétition Quotidienne",
            "summary": "Une sélection quotidienne de 5 manches renouvelée toutes les 24 heures et disputée par les joueurs du monde entier.",
            "points": [
                "Temps imparti : 3 minutes par manche.",
                "Conditions : Déplacement, rotation et zoom autorisés.",
                "Éthique : La recherche externe est proscrite ; les meilleurs scores reposent sur la pure déduction géographique."
            ]
        },
        {
            "id": "maprunner",
            "title": "Maprunner",
            "badge": "Mode Aventure Rogue-lite",
            "summary": "Parcours stratégique par étapes où les points d'énergie constituent vos points de vie.",
            "points": [
                "Points d'énergie : Départ à 10 000 points. Tout score inférieur à 5 000 pts sur une manche est déduit de votre énergie (ex. un score de 4 000 vous fait perdre 1 000 points d'énergie).",
                "Bonus : Choisissez judicieusement vos embranchements pour obtenir des bonus et recharges d'énergie jusqu'à l'arrivée."
            ]
        },
        {
            "id": "battle-royale-countries",
            "title": "Battle Royale : Pays",
            "badge": "Élimination Multijoueur",
            "summary": "Affrontement à 10 joueurs où chacun doit deviner le pays correct avant la fin du temps imparti pour survivre.",
            "points": [
                "Drapeaux éliminés : Les mauvaises réponses des adversaires s'affichent en haut à droite. Ne devinez JAMAIS un pays déjà éliminé.",
                "Premières manches : Prenez votre temps ; tous les joueurs qui trouvent le bon pays avant la fin du compte à rebours se qualifient.",
                "Fin de partie (2-3 joueurs restants) : Validez immédiatement une intuition dès l'écran de chargement, puis explorez pendant que le chronomètre s'écoule.",
                "Le duel final 1v1 : Si vous connaissez la réponse, attendez que la jauge jaune soit presque écoulée avant de valider pour empêcher votre adversaire de vous copier.",
                "Joker 50/50 : Réservez votre joker 50/50 pour la manche 3 ou en cas d'urgence absolue après 2 essais manqués."
            ]
        },
        {
            "id": "battle-royale-distance",
            "title": "Battle Royale : Distance",
            "badge": "Précision Multijoueur",
            "summary": "Tournoi à 10 joueurs où le joueur dont le marqueur est le plus éloigné est éliminé à chaque manche.",
            "points": [
                "Durée de manche : 1 minute. Maximum 3 essais par manche.",
                "Suivi des écarts : Le classement en direct affiche votre écart kilométrique avec le joueur devant et derrière vous. Si un deuxième essai réduit l'écart, persévérez dans cette direction.",
                "Biais des capitales : Dans les grands pays sans indice d'intersection (ex. Ukraine, Colombie, Russie), placer votre marqueur au centre ou sur la capitale (Kyiv, Bogotá, Moscou) minimise le risque d'élimination.",
                "Gestion des essais : Épargnez vos essais bonus pour les manches finales à haute intensité.",
                "Tactique 1v1 finale : Si l'adversaire dispose de 3 essais et vous d'un seul, attendez les 15 dernières secondes pour valider afin de l'empêcher d'ajuster son tir."
            ]
        },
        {
            "id": "duels",
            "title": "Duels 1v1 Compétitifs",
            "badge": "Mode Classé Élite",
            "summary": "Affrontement direct avec 6 000 points de vie de départ. Les dégâts subis équivalent à la différence de points de la manche.",
            "points": [
                "Multiplicateurs de dégâts : Dès la manche 5, les dégâts sont multipliés par 1.5x, puis augmentent de +0.5x à chaque manche suivante (Manche 6 = 2.0x, Manche 7 = 2.5x, Manche 8 = 3.0x).",
                "Chrono de 15 secondes : Dès que le premier joueur valide son pronostic, un compte à rebours de 15 secondes est imposé à l'adversaire.",
                "Attaque rapide : Dès que vous identifiez un pays de façon certaine (ex. poteau gruyère polonais, snorkel kényan, ruban ghanéen), validez immédiatement pour asphyxier l'adversaire.",
                "Défense tactique : Si l'adversaire valide en premier, posez votre repère sur votre meilleure estimation SANS CLIQUER sur Valider ! Profitez des 15 secondes pleines pour chercher un panneau de ville—le jeu valide automatiquement votre marqueur à 0s.",
                "Pas de perte de temps : En duel, ne cherchez pas le 5 000 points parfait : la vitesse et la précision régionale globale font remporter le match."
            ]
        }
    ]
}

# Bilingual Bollards Dataset
BOLLARDS_DATA = {
    "en": [
        {"country": "France", "flag": "🇫🇷", "shape": "Cylindrical Round Post", "reflector": "Red or grey reflective band", "giveaway": "Only country in Europe with round cylindrical bollards. Unique giveaway." },
        {"country": "Poland", "flag": "🇵🇱", "shape": "Flat-topped Rectangular", "reflector": "Red rectangular reflector on a slanted red band", "giveaway": "Instant giveaway: red slanted band on white post." },
        {"country": "Germany", "flag": "🇩🇪", "shape": "Black Cap Post", "reflector": "Vertical rectangular white reflector (front), two round dots (back)", "giveaway": "Black cap with distinctive vertical reflector line." },
        {"country": "Austria", "flag": "🇦🇹", "shape": "Sloping Curved Top", "reflector": "Curved white reflector on front", "giveaway": "Slanted/curved profile distinguishing it from Germany." },
        {"country": "Italy", "flag": "🇮🇹", "shape": "Black Cap Post", "reflector": "Red rectangular reflector (front), white reflector (back)", "giveaway": "Italian delineator with black cap and red front reflector." },
        {"country": "Spain", "flag": "🇪🇸", "shape": "Black Cap Post", "reflector": "Amber/yellow or white reflector", "giveaway": "Frequently found along Carreteras Nacionales and Autovías." },
        {"country": "Norway", "flag": "🇳🇴", "shape": "Slim White Post", "reflector": "Thin red horizontal reflective stripe", "giveaway": "Coupled with yellow continuous center lines." },
        {"country": "Sweden", "flag": "🇸🇪", "shape": "White Rectangular Post", "reflector": "White rectangular reflector", "giveaway": "Blue/white snow poles installed during winter seasons." },
        {"country": "Finland", "flag": "🇫🇮", "shape": "Slanted Top Post", "reflector": "Vertical amber/white reflector", "giveaway": "Slanted top facing toward the road." },
        {"country": "Iceland", "flag": "🇮🇸", "shape": "Bright Yellow Post", "reflector": "White reflector (front), red reflector (back)", "giveaway": "Bright all-yellow body. Unmistakable worldwide." },
        {"country": "Australia", "flag": "🇦🇺", "shape": "White Guidepost", "reflector": "Red reflector on LEFT, white on RIGHT", "giveaway": "Follows left-hand driving traffic conventions." },
        {"country": "New Zealand", "flag": "🇳🇿", "shape": "White Wooden Post", "reflector": "Red horizontal band (front), white (back)", "giveaway": "Often solid timber/wood posts with dashed white road lines." },
        {"country": "Turkey", "flag": "🇹🇷", "shape": "Slanted White Post", "reflector": "Red reflector on right, white on left", "giveaway": "Slanted top profile facing right." },
        {"country": "Czechia & Slovakia", "flag": "🇨🇿 🇸🇰", "shape": "Black Base Post", "reflector": "Two small orange reflectors", "giveaway": "White post emerging from a distinctive black base." }
    ],
    "fr": [
        {"country": "France", "flag": "🇫🇷", "shape": "Poteau cylindrique rond", "reflector": "Bande rétroréfléchissante rouge ou grise", "giveaway": "Seul pays d'Europe utilisant des bollards ronds cylindriques. Indice immédiat." },
        {"country": "Pologne", "flag": "🇵🇱", "shape": "Poteau plat rectangulaire", "reflector": "Réflecteur rectangulaire rouge sur bande rouge inclinée", "giveaway": "Signature visuelle polonaise absolue : bande rouge oblique sur poteau blanc." },
        {"country": "Allemagne", "flag": "🇩🇪", "shape": "Poteau à sommet noir", "reflector": "Bande blanche verticale (avant), deux pastilles blanches (arrière)", "giveaway": "Chapeau noir plat avec trait vertical réflecteur blanc." },
        {"country": "Autriche", "flag": "🇦🇹", "shape": "Sommet biseauté incurvé", "reflector": "Réflecteur blanc incurvé sur l'avant", "giveaway": "Forme biseautée qui la distingue immédiatement du poteau allemand." },
        {"country": "Italie", "flag": "🇮🇹", "shape": "Poteau à sommet noir", "reflector": "Réflecteur rectangulaire rouge à l'avant, blanc à l'arrière", "giveaway": "Bollard italien typique à réflecteur frontal rouge." },
        {"country": "Espagne", "flag": "🇪🇸", "shape": "Poteau à sommet noir", "reflector": "Réflecteur ambre/jaune ou blanc", "giveaway": "Fréquent le long des Carreteras Nacionales et Autovías." },
        {"country": "Norvège", "flag": "🇳🇴", "shape": "Poteau blanc fin", "reflector": "Fine bandelette rouge horizontale", "giveaway": "Systématiquement couplé à des lignes de centre jaunes continues." },
        {"country": "Suède", "flag": "🇸🇪", "shape": "Poteau rectangulaire blanc", "reflector": "Réflecteur blanc rectangulaire", "giveaway": "Piquets à neige rayés bleu et blanc en période hivernale." },
        {"country": "Finlande", "flag": "🇫🇮", "shape": "Poteau à sommet biseauté", "reflector": "Réflecteur vertical blanc ou ambré", "giveaway": "Sommet coupé en biais orienté vers la chaussée." },
        {"country": "Islande", "flag": "🇮🇸", "shape": "Poteau jaune vif intégral", "reflector": "Réflecteur blanc (avant), rouge (arrière)", "giveaway": "Entièrement jaune fluo/vif. Indice décisif mondialement unique." },
        {"country": "Australie", "flag": "🇦🇺", "shape": "Poteau guide blanc", "reflector": "Réflecteur rouge à GAUCHE, blanc à DROITE", "giveaway": "Conforme aux règles de circulation à gauche." },
        {"country": "Nouvelle-Zélande", "flag": "🇳🇿", "shape": "Piquet en bois blanc", "reflector": "Bandelette rouge à l'avant, blanche au dos", "giveaway": "Très souvent des piquets en bois massif le long de lignes tiretées blanches." },
        {"country": "Turquie", "flag": "🇹🇷", "shape": "Poteau blanc biseauté", "reflector": "Réflecteur rouge à droite, blanc à gauche", "giveaway": "Sommet incliné vers la droite le long des routes D-xxx." },
        {"country": "Tchéquie & Slovaquie", "flag": "🇨🇿 🇸🇰", "shape": "Poteau à base noire", "reflector": "Deux petits réflecteurs orange", "giveaway": "Corps blanc émergeant d'une base noire caractéristique." }
    ]
}

# Bilingual Quiz Questions
QUIZ_QUESTIONS_BILINGUAL = {
    "en": [
        {
            "question": "Which country features a prominent black snorkel on the right front pillar of the Google car?",
            "options": ["Kenya", "Uganda", "Botswana", "Senegal"],
            "answer": 0,
            "explanation": "Kenya is famous in GeoGuessr for the black snorkel mounted along the right-hand pillar of the Street View vehicle."
        },
        {
            "question": "If you see a white cylindrical bollard with a red reflector band wrapping completely around it, which European country are you in?",
            "options": ["Germany", "France", "Poland", "Italy"],
            "answer": 1,
            "explanation": "France is unique in Europe for its cylindrical, round-topped white delineator bollards with a red or grey reflective band."
        },
        {
            "question": "Which European nation requires yellow license plates on BOTH the front and rear of private vehicles?",
            "options": ["United Kingdom", "Netherlands", "France", "Belgium"],
            "answer": 1,
            "explanation": "The Netherlands (and Luxembourg and Israel) uses full yellow license plates on both front and rear. The UK uses white on the front and yellow on the rear."
        },
        {
            "question": "Which country features concrete utility poles with round ladder holes dubbed 'Swiss cheese poles'?",
            "options": ["Poland", "Spain", "Norway", "Ireland"],
            "answer": 0,
            "explanation": "Poland is famous for concrete utility poles with rows of circular holes all the way up the pole (also found in France and Hungary)."
        },
        {
            "question": "A road sign with a green background and white text reading 'E 75' indicates what numbering system?",
            "options": ["US Interstate", "European E-Road", "Brazilian Federal Highway", "Russian Federal Highway"],
            "answer": 1,
            "explanation": "European E-roads are marked with green rectangles, white borders, and white text with an 'E' prefix."
        },
        {
            "question": "Which of the following Cyrillic letters is a definitive giveaway for Ukrainian?",
            "options": ["ъ", "ы", "ї", "э"],
            "answer": 2,
            "explanation": "The letter 'ї' (i with two dots) and 'є' (reversed e) are unique to Ukrainian and never appear in Russian."
        },
        {
            "question": "In which country is the Google Street View car consistently followed by a police pickup escort vehicle with flashing lights?",
            "options": ["Ghana", "Nigeria", "South Africa", "Tunisia"],
            "answer": 1,
            "explanation": "In Nigeria, Street View coverage was captured with a police escort truck with flashing light bars visible in rear-view frames."
        },
        {
            "question": "You see yellow center road lines, white outer dashed lines, and green E-road signs in Europe. Where are you?",
            "options": ["Sweden", "Norway", "Finland", "Iceland"],
            "answer": 1,
            "explanation": "Norway is the only country in Europe that consistently uses continuous yellow center lines combined with white outer shoulder markings."
        },
        {
            "question": "How many US states require ONLY a rear license plate on passenger cars?",
            "options": ["10 states", "19 states", "31 states", "50 states"],
            "answer": 1,
            "explanation": "Exactly 19 US states (mainly in the South and Midwest like Florida, Georgia, Michigan, and Pennsylvania) require only a rear license plate."
        },
        {
            "question": "A Brazilian federal highway numbered BR-040 indicates which type of route?",
            "options": ["Longitudinal (North-South)", "Transversal (East-West)", "Radial (originating from Brasília)", "Diagonal"],
            "answer": 2,
            "explanation": "BR-0xx routes in Brazil are radial highways originating from the federal capital Brasília (BR-040 connects Brasília to Rio de Janeiro)."
        },
        {
            "question": "Which country features visible roof rack bars with prominent 'sky rifts' (tears in the sky panorama)?",
            "options": ["Senegal", "Mongolia", "Kenya", "Jordan"],
            "answer": 0,
            "explanation": "Senegal is famous for visible roof bars on the Google car accompanied by distinctive jagged stitching rifts across the sky."
        },
        {
            "question": "In Australia, what are the standard colors on roadside guidepost reflectors?",
            "options": ["Red on left, white on right", "White on left, red on right", "Yellow on both sides", "Blue on both sides"],
            "answer": 0,
            "explanation": "Australia drives on the left and uses white guideposts with a red reflector on the left side of the road and a white reflector on the right."
        },
        {
            "question": "Speed limit signs reading 'MAXIMUM' in kilometers per hour indicate you are in which country?",
            "options": ["United States", "Canada", "Australia", "New Zealand"],
            "answer": 1,
            "explanation": "Canadian speed limit signs distinctly read 'MAXIMUM' in km/h, whereas US signs say 'SPEED LIMIT' in mph."
        },
        {
            "question": "Which script features square and rectangular syllable blocks combining circles ('ㅇ') and straight lines?",
            "options": ["Thai", "Khmer", "Hangul (Korean)", "Japanese Katakana"],
            "answer": 2,
            "explanation": "Korean Hangul is organized in geometric syllable blocks characterized by open circles and perpendicular straight strokes."
        },
        {
            "question": "What is the starting Health Points (HP) for each player in a competitive GeoGuessr Duel?",
            "options": ["1,000 HP", "5,000 HP", "6,000 HP", "10,000 HP"],
            "answer": 2,
            "explanation": "Players start GeoGuessr Duels with 6,000 life points, and damage multipliers escalate starting in Round 5."
        }
    ],
    "fr": [
        {
            "question": "Quel pays se reconnaît instantanément au snorkel noir monté sur le montant avant-droit de la Google car ?",
            "options": ["Kenya", "Ouganda", "Botswana", "Sénégal"],
            "answer": 0,
            "explanation": "Le Kenya est célèbre dans GeoGuessr pour son snorkel noir d'admission d'air fixé sur le montant avant droit du véhicule."
        },
        {
            "question": "Si vous observez un délinéateur routier cylindrique blanc cerclé d'une bande rouge, dans quel pays d'Europe êtes-vous ?",
            "options": ["Allemagne", "France", "Pologne", "Italie"],
            "answer": 1,
            "explanation": "La France est l'unique pays d'Europe à employer des bollards ronds cylindriques avec bande rétroréfléchissante rouge ou grise."
        },
        {
            "question": "Quel pays européen impose des plaques d'immatriculation entièrement JAUNES à l'avant ET à l'arrière ?",
            "options": ["Royaume-Uni", "Pays-Bas", "France", "Belgique"],
            "answer": 1,
            "explanation": "Les Pays-Bas (ainsi que le Luxembourg et Israël) utilisent des plaques jaunes à l'avant et à l'arrière. Le Royaume-Uni a du blanc à l'avant et du jaune à l'arrière."
        },
        {
            "question": "Quel pays est réputé pour ses poteaux électriques en béton perforés de trous ronds (dits 'poteaux gruyère') ?",
            "options": ["Pologne", "Espagne", "Norvège", "Irlande"],
            "answer": 0,
            "explanation": "La Pologne possède typiquement des poteaux électriques en béton troués sur toute leur hauteur (aussi présents en France et Hongrie)."
        },
        {
            "question": "Un panneau routier vert rectangulaire avec l'inscription blanche 'E 75' correspond à quel réseau ?",
            "options": ["Interstate américaine", "Réseau E-Roads européen", "Autoroute fédérale brésilienne", "Route fédérale russe"],
            "answer": 1,
            "explanation": "Les routes européennes E-Roads sont signalées par des rectangles verts bordés de blanc avec le préfixe 'E'."
        },
        {
            "question": "Parmi ces lettres cyrilliques, laquelle prouve sans équivoque que vous êtes en Ukraine ?",
            "options": ["ъ", "ы", "ї", "э"],
            "answer": 2,
            "explanation": "Les lettres 'ї' (i tréma) et 'є' (e inversé) sont exclusives à l'alphabet ukrainien et n'existent pas en russe standard."
        },
        {
            "question": "Dans quel pays la Google car est-elle systématiquement escortée par un pick-up de police aux gyrophares allumés ?",
            "options": ["Ghana", "Nigeria", "Afrique du Sud", "Tunisie"],
            "answer": 1,
            "explanation": "Au Nigeria, la couverture Street View a été filmée sous la surveillance continue d'une camionnette de police visible avec gyrophare."
        },
        {
            "question": "Vous observez des lignes centrales jaunes, des lignes de rive blanches tiretées et des panneaux E-Roads. Où êtes-vous ?",
            "options": ["Suède", "Norvège", "Finlande", "Islande"],
            "answer": 1,
            "explanation": "La Norvège est le seul pays d'Europe à combiner une ligne centrale jaune continue avec des lignes de rive blanches tiretées."
        },
        {
            "question": "Combien d'États américains imposent UNIQUEMENT la plaque d'immatriculation arrière ?",
            "options": ["10 États", "19 États", "31 États", "50 États"],
            "answer": 1,
            "explanation": "Exactement 19 États américains (comme la Floride, la Géorgie, le Michigan et la Pennsylvanie) ne requièrent aucune plaque à l'avant."
        },
        {
            "question": "Au Brésil, que désigne une autoroute fédérale débutant par BR-0xx (ex. BR-040) ?",
            "options": ["Une route Nord-Sud", "Une route Est-Ouest", "Une autoroute radiale partant de Brasília", "Une diagonale"],
            "answer": 2,
            "explanation": "Les routes BR-0xx sont des autoroutes radiales dont le point de départ est la capitale fédérale Brasília (la BR-040 relie Brasília à Rio)."
        },
        {
            "question": "Quel pays présente des barres de toit visibles couplées à d'importantes déchirures panoramiques dans le ciel (sky rifts) ?",
            "options": ["Sénégal", "Mongolie", "Kenya", "Jordanie"],
            "answer": 0,
            "explanation": "Le Sénégal est mondialement réputé dans le jeu pour ses déchirures de ciel (rifts) associées aux barres métalliques de la galerie."
        },
        {
            "question": "En Australie, quelles sont les couleurs des réflecteurs sur les piquets de bord de route ?",
            "options": ["Rouge à gauche, blanc à droite", "Blanc à gauche, rouge à droite", "Jaune des deux côtés", "Bleu des deux côtés"],
            "answer": 0,
            "explanation": "L'Australie roule à gauche et installe des délinéateurs à réflecteur rouge à gauche de la voie et blanc sur la droite."
        },
        {
            "question": "Des panneaux de limitation de vitesse indiquant 'MAXIMUM' en km/h signalent quel pays ?",
            "options": ["États-Unis", "Canada", "Australie", "Nouvelle-Zélande"],
            "answer": 1,
            "explanation": "Le Canada indique 'MAXIMUM' en km/h, tandis que les États-Unis emploient la formule 'SPEED LIMIT' en mph."
        },
        {
            "question": "Quelle écriture se structure en blocs syllabiques carrés mêlant petits cercles ('ㅇ') et traits droits ?",
            "options": ["Thaï", "Khmer", "Hangul (Coréen)", "Katakana japonais"],
            "answer": 2,
            "explanation": "L'écriture coréenne Hangul s'articule en blocs géométriques associant des ronds caractéristiques et des traits perpendiculaires."
        },
        {
            "question": "Combien de points de vie (PV) possède chaque joueur au début d'un Duel compétitif sur GeoGuessr ?",
            "options": ["1 000 PV", "5 000 PV", "6 000 PV", "10 000 PV"],
            "answer": 2,
            "explanation": "Les joueurs démarrent avec 6 000 PV dans les Duels, et les multiplicateurs de dégâts augmentent à partir du round 5."
        }
    ]
}

# Output to data.js with rich bilingual dictionaries
output_js = f"""// GeoGuessr Master Playbook & Knowledge Engine
// Fully localized bilingual dataset (French & English)

const COUNTRIES_DATA = {json.dumps(compiled_countries, indent=2, ensure_ascii=False)};
const MODES_DATA = {json.dumps(MODES_DATA, indent=2, ensure_ascii=False)};
const BOLLARDS_DATA = {json.dumps(BOLLARDS_DATA, indent=2, ensure_ascii=False)};
const QUIZ_QUESTIONS = {json.dumps(QUIZ_QUESTIONS_BILINGUAL, indent=2, ensure_ascii=False)};

const I18N = {{
  en: {{
    brandBadge: "PRO KNOWLEDGE ENGINE",
    heroTitle: "🌍 Global Country & Territory Playbook",
    heroSubtitle: "Every single Street View nation parsed with surgical precision. Instant identification via bollards, utility poles, license plates, car meta, and regional giveaways—with zero fluff.",
    statCountries: "Countries",
    statAccuracy: "Facts Preserved",
    statClues: "Visual Clues",
    searchPlaceholder: "Search countries, bollards, poles, car meta, languages, keywords (e.g. 'snorkel', 'birch', 'Swiss cheese')...",
    allContinents: "All",
    filterDrivingAll: "Driving: All",
    filterDrivingLeft: "🚗 Left Hand Drive (RHD)",
    filterDrivingRight: "🚙 Right Hand Drive (LHD)",
    tabCountries: "🌍 Countries (122)",
    tabMatrix: "⚡ Clue Matrix Guesser",
    tabBollards: "🛑 Bollards & Signs",
    tabMeta: "🚗 Car Meta & Cam Gens",
    tabPlates: "🚙 License Plates",
    tabHighways: "🛣️ Highway Grids",
    tabLanguages: "🔤 Languages & Scripts",
    tabModes: "🎮 Game Modes & Tactics",
    tabFundamentals: "☀️ Fundamentals & Sun",
    tabQuiz: "🎯 Practice Quiz",
    inspectBtn: "Inspect Dossier ➔",
    modalKeyIndicators: "Key Identification Clues",
    modalGallery: "Visual Clues & Photographic Evidence",
    matrixTitle: "⚡ Interactive Clue Matrix & Meta Guesser",
    matrixSubtitle: "Locked in a game? Select what you see on your screen right now to immediately narrow down the candidate countries.",
    matrixDrivingTitle: "1. Driving Side",
    matrixPlateTitle: "2. License Plate Style",
    matrixCarTitle: "3. Street View Car Meta",
    matrixPoleTitle: "4. Utility Pole Features",
    matrixBollardTitle: "5. Delineator Bollard",
    matrixResetBtn: "↺ Reset All Clues",
    matrixCandidates: "Candidates",
    quizQuestionOf: "Question",
    quizOf: "of",
    quizScore: "Score",
    quizNextBtn: "Next Question ➔",
    quizCorrectTitle: "✓ Correct! Outstanding deduction.",
    quizIncorrectTitle: "✗ Incorrect.",
    anyVal: "Any"
  }},
  fr: {{
    brandBadge: "MOTEUR PRO DE CONNAISSANCES",
    heroTitle: "🌍 Guide Magistral des Pays & Territoires",
    heroSubtitle: "Chaque nation Street View décortiquée avec une précision chirurgicale. Identification immédiate par bollards, poteaux électriques, plaques, méta de la voiture et repères régionaux — zéro blabla.",
    statCountries: "Pays Couverts",
    statAccuracy: "Informations Préservées",
    statClues: "Preuves Visuelles",
    searchPlaceholder: "Rechercher un pays, bollard, poteau, méta, écriture, mot-clé (ex: 'snorkel', 'bouleau', 'gruyère')...",
    allContinents: "Tous",
    filterDrivingAll: "Conduite : Tous",
    filterDrivingLeft: "🚗 Conduite à gauche (RHD)",
    filterDrivingRight: "🚙 Conduite à droite (LHD)",
    tabCountries: "🌍 Pays (122)",
    tabMatrix: "⚡ Matrice d'Indices",
    tabBollards: "🛑 Bollards & Panneaux",
    tabMeta: "🚗 Caméras & Méta Car",
    tabPlates: "🚙 Plaques d'Immat",
    tabHighways: "🛣️ Réseaux Routiers",
    tabLanguages: "🔤 Langues & Écritures",
    tabModes: "🎮 Modes & Stratégies",
    tabFundamentals: "☀️ Soleil & Boussole",
    tabQuiz: "🎯 Quiz d'Entraînement",
    inspectBtn: "Voir le dossier ➔",
    modalKeyIndicators: "Indices Clés d'Identification",
    modalGallery: "Galerie de Preuves Visuelles & Délinéateurs",
    matrixTitle: "⚡ Matrice d'Indices & Guesser Intelligent",
    matrixSubtitle: "En pleine partie ? Cochez les éléments visibles sur votre écran pour filtrer instantanément les pays candidats.",
    matrixDrivingTitle: "1. Sens de Conduite",
    matrixPlateTitle: "2. Style de Plaque d'Immatriculation",
    matrixCarTitle: "3. Méta de la Google Car",
    matrixPoleTitle: "4. Caractéristiques des Poteaux",
    matrixBollardTitle: "5. Type de Délinéateur (Bollard)",
    matrixResetBtn: "↺ Réinitialiser les Indices",
    matrixCandidates: "Candidats Possibles",
    quizQuestionOf: "Question",
    quizOf: "sur",
    quizScore: "Score",
    quizNextBtn: "Question Suivante ➔",
    quizCorrectTitle: "✓ Exact ! Excellente déduction.",
    quizIncorrectTitle: "✗ Raté.",
    anyVal: "Tous"
  }}
}};

if (typeof module !== 'undefined' && module.exports) {{
  module.exports = {{
    COUNTRIES_DATA,
    MODES_DATA,
    BOLLARDS_DATA,
    QUIZ_QUESTIONS,
    I18N
  }};
}}
"""

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(output_js)

print("data.js successfully regenerated with complete bilingual datasets!")
