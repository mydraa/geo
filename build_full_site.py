import json
import re

print("Starting build_full_site.py...")

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

def get_driving_side(country_name):
    if country_name in LEFT_DRIVING_COUNTRIES:
        return "Left"
    return "Right"

# Country specific instant key giveaways
KEY_GIVEAWAYS = {
    "Kenya": "Black snorkel mounted on the right front pillar of the Google car.",
    "Ghana": "Visible roof rack with distinctive black electrical tape wrapped around one bar.",
    "Guatemala": "Google car roof rack with protruding side mirrors visible in rear view.",
    "Mongolia": "Pickup truck bed packed with camping gear, spare tires, and luggage under a tarp.",
    "Senegal": "Roof rack visible with distinct sky rifts (tears in the 360-degree panorama).",
    "Nigeria": "Followed or led by a police pickup escort vehicle with flashing red/blue light bar.",
    "Curaçao": "Black pickup truck bed with prominent tubular steel bars.",
    "Bermuda": "Compact open-hood buggy vehicle; driving on the left; white stepped roofs.",
    "Dominican Republic": "White metal roof rack bars with black rubber feet.",
    "Reunion": "Blue/white car with antenna; steep tropical volcanic terrain; French signs.",
    "Uganda": "White car with visible roof rack and white front bumper; rich red soil.",
    "Sri Lanka": "White car with visible side mirrors and camera pole shadow; Sinhala/Tamil script; drives on left.",
    "Jordan": "Black or white pickup truck with roof rack and antenna; desert landscape; Arabic signage.",
    "France": "Cylindrical white bollard with red/gray reflector band; yellow 'D-xxx' departmental road signs; double blue plate bands.",
    "Poland": "Concrete utility poles with ladder holes ('Swiss cheese'); white bollards with slanted red band.",
    "Iceland": "Bright yellow bollards; volcanic treeless landscapes; wooden snow stakes; yellow center lines absent.",
    "Norway": "Yellow center road lines with white outer dashed lines (unique in Europe); green E-road signs; deep fjords.",
    "Sweden": "Blue rectangular road number signs without letter prefixes; yellow dashed outer edge lines; Falun red wooden houses.",
    "Finland": "Red rectangular main highway signs (1-29); yellow secondary (40-99); non-Germanic double vowel road names (-tie, -katu).",
    "Denmark": "White bollard with yellow reflector; flat terrain; thatched or red brick houses; red/white bicycle signs.",
    "Germany": "Black-capped bollard with vertical front reflector and two dots on rear; extensive camera blurring in older coverage; no speed limit signs on Autobahn.",
    "Austria": "Sloping curved-top bollards; alpine architecture; green motorway signs; white pedestrian crossing on blue square.",
    "Switzerland": "Low Gen 4 camera; yellow diamond warning signs with white borders; yellow diamond pedestrian crossing signs; bilingual cantons.",
    "Italy": "Double blue strips on license plates with small front plate; black-capped bollards with red front / white rear reflectors.",
    "Spain": "Ladder utility poles with metal rungs; AP-xxx, A-xxx, N-xxx highways; white bollards with black cap.",
    "Portugal": "Yellow stripe on right side of older license plates; ladder concrete poles; blue motorway signs.",
    "United Kingdom": "White front and yellow rear license plates; driving on the left; red circular speed limit signs with black numbers in mph.",
    "Ireland": "Yellow diamond warning signs (like US); yellow dashed outer road lines; bilingual road signs (Gaeilge in italic + English); driving on the left.",
    "USA": "Yellow diamond warning signs; double yellow center lines; metal signposts with punched holes; 'SPEED LIMIT' signs in mph; interstate shield grid.",
    "Canada": "'MAXIMUM' speed limit signs in km/h; Trans-Canada Highway 1 green maple leaf; white wooden utility poles; bilingual stop signs ('ARRET / STOP') in Quebec.",
    "Mexico": "Octagonal red 'ALTO' stop signs; Gen 2 camera in desert highways; white federal highway shields; triple-bolted wooden/concrete poles.",
    "Brazil": "BR-xxx highway numbering grid; phone area codes 11-99 on commercial signs; red soil; Araucaria (Paraná pine) in southern states.",
    "Argentina": "Black-and-white chevron curve arrows; flat pampas; RN national route shields with white numbers on black background.",
    "Chile": "White dashed outer edge lines; extremely narrow country; Andes mountains visible eastward.",
    "Colombia": "Yellow license plates on all public transport/taxis; white cross marking on back of road signs; mountainous Andean roads.",
    "Peru": "Utility poles with bottom half painted black and white stripes; high Andean altiplano; mototaxis (tuk-tuks) in towns.",
    "Bolivia": "Unpaved dirt highways; Cholita bowler hats and traditional dress; brick buildings without external plastering.",
    "Australia": "Driving on the left; eucalyptus trees; white wooden/metal guideposts with red reflector on left and white on right; blurry Gen 1/2 in outback.",
    "New Zealand": "Driving on the left; lush rolling green hills; wooden posts with white reflector front and red rear; dashed white center lines.",
    "Japan": "Driving on the left; blue national highway shields; yellow license plates on Kei cars; low utility poles with intricate cable bundles.",
    "South Korea": "Driving on the right; Hangul script; yellow license plates on commercial vehicles; urban blue highway shields.",
    "Taiwan": "Yellow and black diagonal striped utility poles; Traditional Chinese characters; scooters everywhere.",
    "Thailand": "Driving on the left; Thai script with small loops; curved concrete utility poles; spirit houses outside homes.",
    "Cambodia": "Driving on the right; Khmer script with squiggly feet; blue beer advertising signboards; Khmer architecture.",
    "Indonesia": "Driving on the left; black and white striped curbs; 'Jl.' for Jalan; red and white national flag; tropical lush volcanic landscape.",
    "Malaysia": "Driving on the left; Federal route shields with yellow/white numbers on black; 'Jalan' written in full; palm oil plantations.",
    "Philippines": "Driving on the right; English/Tagalog signage; Jeepneys and tricycles; yellow diamond warning signs.",
    "South Africa": "Driving on the left; yellow outer road shoulder lines; white on blue chevron arrows; English signage; .za domain.",
    "Botswana": "Driving on the left; very flat arid savannah; low thorny acacia scrub; white-faced donkey carts.",
    "Eswatini": "Driving on the left; hilly green terrain; yellow outer road lines; pine plantations; southern African architecture.",
    "Lesotho": "Driving on the left; mountainous highland scenery without trees; traditional Basotho blankets and conical straw hats.",
    "Russia": "Birch tree forests; Cyrillic signage; M/R/A highway numbering; concrete bus stops; Gen 3/4 camera.",
    "Ukraine": "Cyrillic containing unique letters 'і', 'ї', 'є'; blue and yellow painted infrastructure; concrete poles with white-painted bases.",
    "Israel": "Both front and rear license plates yellow; Hebrew and Arabic signage; red and white curb markings.",
    "Turkey": "Slanted top white bollards with red reflector on right, white on left; Turkish letters (ç, ğ, ı, ö, ş, ü); D-xxx road signs.",
    "Greece": "Greek alphabet (Ω, Δ, Σ, etc.); blue motorway signs; solar water heaters on flat concrete rooftops.",
}

# Compile cleaned countries
compiled_countries = []
for c in cheat_sheet['countries']:
    name = c['country']
    cont = c['continent']
    cid = c['id']
    flag, tld = FLAG_TLD_MAP.get(name, ("🏳️", ".com"))
    driving = get_driving_side(name)
    giveaway = KEY_GIVEAWAYS.get(name, "")
    
    # Clean paragraphs
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
        "name": name,
        "continent": cont,
        "id": cid,
        "flag": flag,
        "tld": tld,
        "drivingSide": driving,
        "giveaway": giveaway,
        "paragraphs": clean_p,
        "images": clean_imgs[:15] # Top 15 high-yield images
    })

print(f"Compiled {len(compiled_countries)} country profiles.")

# Compile Modes
modes_list = [
    {
        "id": "classic",
        "title": "Classic & Custom Maps",
        "badge": "Core Mode",
        "summary": "Standard GeoGuessr gameplay with 5 rounds per game. Play on World Map, Famous Places, United States, European Union, Stadiums, or thousands of user-created maps.",
        "points": [
            "Scoring: Maximum 5,000 points per round (25,000 perfect score). Points scale by distance from 5,000 pts within ~150 meters down to 0 points at the antipode.",
            "Time limits: Configurable from 10 seconds (ultra-fast blitz) to 10 minutes or infinite exploration.",
            "Movement Settings: Moving (standard navigation), No Move (NM - rotate and zoom only), or No Move Pan Zoom (NMPZ - still frame test of pure recognition)."
        ]
    },
    {
        "id": "explorer",
        "title": "Explorer Mode",
        "badge": "Single Player Mastery",
        "summary": "Country-by-country medal challenge to master individual nation maps and unlock global badges.",
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
        "badge": "Streak Survival",
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
]

# Compile Fundamentals
fundamentals_data = {
    "coverage": {
        "title": "Global Street View Coverage Prevalence",
        "summary": "Street View coverage is heavily concentrated in specific regions. Understanding country probability is critical for high-scoring guesses.",
        "points": [
            "Dominant Countries: Russia, the USA, Brazil, Argentina, Australia, and Western/Northern Europe account for over 70% of random worldwide rounds.",
            "Sparse / Absent Coverage: China (only isolated trekker landmarks), India (limited trekker/official coverage), Central Africa, North Africa (except Tunisia), Middle East (except Jordan, UAE, Qatar, Israel), and Central Asia (except Kyrgyzstan, Mongolia, Kazakhstan).",
            "Probability Rule: When evenly torn between an obscure country and a high-coverage nation (e.g. Eswatini vs. South Africa), statistically favor the high-coverage nation."
        ]
    },
    "sun_compass": {
        "title": "The Sun, Shadows & Compass",
        "summary": "The single most dependable fundamental method to immediately establish hemisphere and latitude.",
        "points": [
            "Compass Mechanics: The red needle always points North. Align the camera view with the road to establish exact compass orientation.",
            "Northern Hemisphere: The sun is positioned in the Southern sky at midday. Shadows point NORTH.",
            "Southern Hemisphere: The sun is positioned in the Northern sky at midday. Shadows point SOUTH.",
            "Tropical / Equatorial Sun: The sun appears directly overhead (90°) between the Tropic of Cancer (23.5°N) and Tropic of Capricorn (23.5°S). Shadows are extremely short directly under objects.",
            "Satellite Dishes: Geosynchronous satellites orbit directly above the Equator. Dishes in the Northern Hemisphere face South (steep vertical angle in Canada/Scandinavia; shallow angle in Southern Europe). Dishes in the Southern Hemisphere face North. Dishes pointing straight up indicate near-equatorial latitude."
        ]
    },
    "driving_side": {
        "title": "Driving Side: Left vs. Right",
        "summary": "Instantly eliminates approximately 75% of the world. Left-side driving is confined to specific historical British heritage regions and islands.",
        "left_countries": [
            "Europe: United Kingdom, Ireland, Isle of Man, Jersey, Malta, Cyprus.",
            "Africa: South Africa, Botswana, Eswatini, Lesotho, Namibia, Kenya, Uganda.",
            "Asia: Japan, Hong Kong, Macau, Singapore, Malaysia, Thailand, Indonesia, Sri Lanka, Bangladesh, India, Bhutan, Pakistan.",
            "Oceania: Australia, New Zealand, Christmas Island.",
            "Americas & Caribbean: US Virgin Islands, Bermuda."
        ],
        "deduction_clues": [
            "No Cars Visible: Check road sign orientations (signs face oncoming traffic on their side of the road).",
            "Car Shadows & Mirrors: Look down at the Google car shadow—protruding side mirrors reveal front and driving position.",
            "Parked Vehicles: Observe driver's seat position (steering wheel on the left = right-side driving; steering wheel on the right = left-side driving)."
        ]
    },
    "image_quality": {
        "title": "Image Quality & Generation 1/2 Blurring",
        "summary": "Heavily blurred, pixelated, or low-resolution imagery is a major geographic clue.",
        "points": [
            "Blurry Gen 1 / Low Quality: Found almost exclusively in the United States and Australia.",
            "US Blurry Regions: Central Plains and rural corridors—North Dakota, South Dakota, Nebraska, Iowa, Kansas.",
            "Australian Blurry Regions: Remote Outback areas across Western Australia, Northern Territory, and Queensland.",
            "Resolution Rule: If the landscape is flat, agricultural, Northern Hemisphere, and blurry = North or South Dakota. If red dirt, sparse scrub, Southern Hemisphere, and blurry = Australian Outback."
        ]
    }
}

# Compile Highways
highways_data = [
    {
        "region": "United States",
        "system": "Interstate & US Highway Grid",
        "rules": [
            "Interstate Grid (2-Digit): Odd numbers run North-South (I-5 in California to I-95 on the East Coast). Even numbers run East-West (I-10 along the Mexican border to I-90 along the Canadian border).",
            "3-Digit Interstates: Even first digit (e.g. I-285, I-405) = full loop or bypass connecting at two ends. Odd first digit (e.g. I-195, I-395) = spur route connecting at only one end.",
            "US Highway System (Inverted Grid!): Odd numbers run North-South (US-101 on the West Coast to US-1 on the East Coast). Even numbers run East-West (US-2 in the North to US-98 in the South).",
            "State Highway Shields: Each US state possesses a unique shield outline (e.g., California spade, Georgia outline, Pennsylvania keystone, Kansas sunflower, New Mexico Zia sun, Washington George Washington silhouette)."
        ]
    },
    {
        "region": "Canada",
        "system": "Trans-Canada & Provincial Systems",
        "rules": [
            "Trans-Canada Highway: Marked by Highway 1 with a green maple leaf shield spanning from Victoria, BC to St. John's, NL.",
            "Provincial Shields: Ontario uses a crown shield; Quebec uses a fleur-de-lis; Alberta uses a distinctive provincial shield; Saskatchewan uses green shields.",
            "Speed Limit Signs: Distinctly read 'MAXIMUM' with the speed in km/h (unlike US signs which explicitly state 'SPEED LIMIT' in mph)."
        ]
    },
    {
        "region": "Mexico",
        "system": "Carreteras Federales",
        "rules": [
            "Federal Shield: White shield with black border and route number.",
            "Numbering Grid: Odd numbers run North-South; Even numbers run East-West.",
            "Stop Signs: Distinctive octagonal red signs with 'ALTO' instead of 'STOP'."
        ]
    },
    {
        "region": "Brazil",
        "system": "Rodovias Federais (BR-xxx)",
        "rules": [
            "BR-0xx (Radiais): Radiate outwards from Brasília in all directions (BR-010 to Belém, BR-020 to Fortaleza, BR-040 to Rio de Janeiro, BR-050, BR-060, BR-070).",
            "BR-1xx (Longitudinais): Run strictly North-South (e.g. BR-101 along the Atlantic coast, BR-116 from Fortaleza to the southern border).",
            "BR-2xx (Transversais): Run strictly East-West (e.g. BR-230 Transamazônica, BR-262).",
            "BR-3xx (Diagonais): Run diagonally (NW-SE or NE-SW).",
            "BR-4xx (Ligação): Connecting routes linking major federal highways.",
            "State Highways: Prefixed by 2-letter state abbreviation (SP-xxx São Paulo, MG-xxx Minas Gerais, RJ-xxx Rio, PR-xxx Paraná, RS-xxx Rio Grande do Sul).",
            "Phone Area Codes (DDD): 11-19 (São Paulo), 21-24 (Rio de Janeiro), 31-38 (Minas Gerais), 41-46 (Paraná), 51-55 (Rio Grande do Sul), 61 (Brasília), 71-77 (Bahia), 81-89 (Northeast), 91-99 (Amazon/North)."
        ]
    },
    {
        "region": "Europe",
        "system": "International E-Road Network",
        "rules": [
            "Sign Appearance: Green rectangular sign with white border and white text (e.g. E 4, E 75).",
            "Grid Orientation: Odd numbers run North-South; Even numbers run East-West.",
            "Numbering Progression: Numbers increase from West to East (E05 in Spain/France to E95 in Russia) and from North to South (E10 in Norway to E90 in Greece/Italy).",
            "Motorway Sign Colors: Blue background in UK, France, Germany, Spain, Austria, Belgium, Netherlands. Green background in Italy, Switzerland, Greece, Sweden, Denmark, Slovenia, Croatia, Serbia, Romania."
        ]
    },
    {
        "region": "United Kingdom",
        "system": "Radial Numbering Zones 1 to 9",
        "rules": [
            "Radial Zones: Radiate clockwise from London (Zones 1-6) and Edinburgh (Zones 7-9).",
            "Zone 1: East Anglia & North (A1 boundary). Zone 2: South-East (A2). Zone 3: South-West (A3). Zone 4: West Midlands & Wales (A4). Zone 5: North-West England (A5). Zone 6: Northern England (A6).",
            "Road Prefixes: 'M' for Motorways (blue sign), 'A' for primary routes (green sign) or non-primary (white sign), 'B' for secondary routes."
        ]
    },
    {
        "region": "Spain",
        "system": "Autopistas, Autovías & Carreteras Nacionales",
        "rules": [
            "AP-xxx: Toll Autopistas (blue sign with AP prefix).",
            "A-xxx: Free public Autovías (blue sign with A prefix).",
            "N-xxx: Carreteras Nacionales (red rectangular sign with white text).",
            "Autonomous Regional Routes: 1st tier (orange shield), 2nd tier (green shield), 3rd tier (yellow shield)."
        ]
    },
    {
        "region": "Russia",
        "system": "Federal Highway Network (M, R, A)",
        "rules": [
            "M-Highways: Federal routes radiating from Moscow (M1 to Belarus border, M2 to Ukraine, M3 to Kyiv, M4 'Don' to Black Sea, M5 'Ural' to Chelyabinsk, M7 'Volga', M8 'Kholmogory', M9 'Baltic', M10/M11 to St. Petersburg).",
            "R-Highways (P in Cyrillic): Regional connecting highways (e.g. R21 'Kola', R256 'Chuya').",
            "A-Highways: Access, orbital, and international connecting links."
        ]
    },
    {
        "region": "Nordic Countries",
        "system": "Norway, Sweden & Finland Route Signs",
        "rules": [
            "Norway: Green E-road signs; Riksvei (Rv) and Fylkesvei (Fv) national/county routes marked on white signs with black border.",
            "Sweden: Blue rectangular signs with white numbers without letter prefixes (e.g. 50, 70, 26).",
            "Finland: Red rectangular signs for primary national routes (1-29); yellow rectangular signs for secondary routes (40-99); blue rectangular signs for regional routes (100-999)."
        ]
    },
    {
        "region": "Japan",
        "system": "National Highways & Expressways",
        "rules": [
            "National Highways: Blue shield-shaped sign with white number (routes 1 to 507).",
            "Expressways: Green rectangular signs with route numbers prefixed by 'E' (e.g. E1 Tomei Expressway, E4 Tohoku)."
        ]
    }
]

# Compile Meta
meta_data = {
    "camera_generations": [
        {
            "gen": "Generation 1 (2007-2008)",
            "traits": "Extremely low resolution, severe pixelation, heavy compression artifacts, washed out colors. Confined exclusively to the United States and Australia."
        },
        {
            "gen": "Generation 2 (2008-2010)",
            "traits": "Circular purple or black blur under the Google car; distinct glowing halo ring around the sun; lower contrast and color bleed. Common in rural Mexico, northern Canada, South Africa, and early European coverage."
        },
        {
            "gen": "Generation 3 (2011-2017)",
            "traits": "Crisp high-definition imagery; standard circular car blur; clean stitching; natural color balance. The global workhorse covering over 80 countries."
        },
        {
            "gen": "Generation 4 (2017-Present)",
            "traits": "Ultra-HD resolution; vibrant true-to-life color saturation; subtle blue camera lens ring/flare; extreme sharpness allowing street signs and distant mountain ridges to be easily read."
        }
    ],
    "car_meta": [
        {"country": "Kenya", "clue": "Black snorkel air intake attached to the front-right pillar of the Google car."},
        {"country": "Ghana", "clue": "Visible roof rack with black electrical tape wrapped securely around one crossbar."},
        {"country": "Guatemala", "clue": "Roof rack visible with two side mirrors protruding in front of the camera."},
        {"country": "Mongolia", "clue": "Pickup truck bed loaded with camping gear, spare tires, and luggage beneath a tarp."},
        {"country": "Senegal", "clue": "Visible metal roof rack with bars and prominent sky rifts (tears in the sky panorama)."},
        {"country": "Nigeria", "clue": "Followed or led by a police pickup escort vehicle with flashing red/blue emergency light bar."},
        {"country": "Curaçao", "clue": "Black pickup truck bed with prominent tubular steel bars."},
        {"country": "Dominican Republic", "clue": "White metal roof bars with black rubber mounting feet."},
        {"country": "Bermuda", "clue": "Compact open-hood buggy vehicle driving on the left."},
        {"country": "Reunion", "clue": "Blue or white car with distinctive roof rack antennas on steep tropical terrain."},
        {"country": "Sri Lanka", "clue": "White car with side mirrors and visible camera pole shadow on the road."},
        {"country": "Jordan", "clue": "Black or white pickup truck with antenna and roof rack in desert terrain."},
        {"country": "Uganda", "clue": "White car with roof rack and white front bumper over bright red soil."}
    ],
    "rifts": [
        {"region": "Senegal", "note": "Frequent vertical and horizontal sky rifts with visible roof rack bars."},
        {"region": "Albania", "note": "Prominent sky stitching tears/rifts in mountainous Mediterranean roads."},
        {"region": "Montenegro", "note": "Sky rifts across Balkan mountain passes."}
    ]
}

# Compile License Plates
plates_data = {
    "europe": [
        {"type": "Standard EU Plate", "description": "Long white rectangular plate with single blue EU strip on the left containing 12 gold stars and country code."},
        {"type": "Double Blue Strips (Left & Right)", "description": "Italy, France, and Albania feature blue strips on BOTH the left (country code) and right (department or province code)."},
        {"type": "Short Front Plate", "description": "Italy and San Marino use noticeably shorter, compact front license plates compared to standard European sizes."},
        {"type": "All-Yellow Plates (Front & Rear)", "description": "Netherlands, Luxembourg, and Israel use yellow license plates on both front and rear."},
        {"type": "White Front, Yellow Rear", "description": "United Kingdom, Gibraltar, Isle of Man, and Cyprus use white front plates and yellow rear plates."},
        {"type": "Red Lettering", "description": "Belgium uses distinctive red letters and numbers on a white plate."},
        {"type": "Black Plates", "description": "Liechtenstein uses black license plates with white lettering."}
    ],
    "usa_laws": {
        "rear_only_states": [
            "Alabama", "Arizona", "Arkansas", "Delaware", "Florida", "Georgia",
            "Indiana", "Kansas", "Kentucky", "Louisiana", "Michigan", "Mississippi",
            "New Mexico", "North Carolina", "Oklahoma", "Pennsylvania", "South Carolina",
            "Tennessee", "West Virginia"
        ],
        "both_front_rear_states": [
            "Alaska", "California", "Colorado", "Connecticut", "Hawaii", "Idaho",
            "Illinois", "Iowa", "Maine", "Maryland", "Massachusetts", "Minnesota",
            "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
            "New York", "North Dakota", "Ohio", "Oregon", "Rhode Island", "South Dakota",
            "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming",
            "Washington D.C."
        ]
    },
    "latin_america": [
        {"country": "Mercosur Standard", "description": "Brazil, Argentina, Uruguay, and Paraguay share the Mercosur format: white plate with blue banner along the top."},
        {"country": "Colombia", "description": "All commercial vehicles, buses, and taxis have bright yellow license plates."}
    ]
}

# Compile Languages
languages_data = {
    "cyrillic": [
        {"language": "Russian", "alphabet": "Standard Cyrillic. Uses: ы, э, ъ. NEVER uses: і, ї, є, ў."},
        {"language": "Ukrainian", "alphabet": "Key letters: і (dotted i), ї (double dotted i), є (reversed e), ’ (apostrophe)."},
        {"language": "Belarusian", "alphabet": "Key letters: ў (short u), і."},
        {"language": "Bulgarian", "alphabet": "Frequent use of ъ at ends/middles of words; lacks ы, э, і."},
        {"language": "Serbian", "alphabet": "Uses Latin-looking ј, plus љ, њ, џ, ћ, ђ."},
        {"language": "Macedonian", "alphabet": "Uses ј, љ, њ, џ, plus ѓ, ќ."},
        {"language": "Mongolian", "alphabet": "Cyrillic with unique vowels ө and ү."},
        {"language": "Kazakh", "alphabet": "Cyrillic with ә, ғ, қ, ң, ө, ұ, ү, һ, і."}
    ],
    "nordic": [
        {"language": "Danish & Norwegian", "characters": "Uses æ and ø. Norwegian street endings: -vei, -gate. Danish: -vej, -gade."},
        {"language": "Swedish & Finnish", "characters": "Uses ä and ö. Swedish street endings: -väg, -gatan. Finnish is non-Germanic with double vowels and endings: -tie, -katu."},
        {"language": "Icelandic & Faroese", "characters": "Uses distinctive letters ð (eth) and þ (thorn)."}
    ],
    "eastern_europe": [
        {"language": "Polish", "features": "Dense consonant clusters (sz, cz, rz) and letters: ł, ą, ę, ś, ć, ż, ź, ń. Street: Ulica (Ul.)."},
        {"language": "Czech", "features": "Distinctive hook letters: ř, ů, ě, č, š, ž."},
        {"language": "Slovak", "features": "Distinctive letters: ä, ô, ŕ, ĺ, ľ."},
        {"language": "Hungarian", "features": "Finno-Ugric vocabulary; letters: ő, ű, á, é, í, ó, ö, ú, ü; digraphs: sz, gy, cs. Street: utca."},
        {"language": "Romanian", "features": "Romance language with letters: ș, ț, ă, â, î. Street: Strada."}
    ],
    "asian_scripts": [
        {"script": "Thai", "appearance": "Flowing cursive script with small loops/circles on character terminals."},
        {"script": "Khmer (Cambodia)", "appearance": "Curvier and more ornate than Thai, with squiggly foot strokes beneath characters."},
        {"script": "Hangul (Korean)", "appearance": "Built from distinct geometric blocks combining circles (ㅇ), horizontal, and vertical lines."},
        {"script": "Japanese", "appearance": "Mixture of complex Kanji (Chinese characters), curved Hiragana (ひらがな), and angular Katakana (カタカナ)."},
        {"script": "Traditional Chinese", "appearance": "Used in Taiwan and Hong Kong; complex, dense pictographic characters."}
    ]
}

# Compile Quiz Questions
quiz_questions = [
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
]

# Write out data.js
output_content = f"""// GeoGuessr Master Playbook Data Engine
// Generated from comprehensive extraction of The Digital Labyrinth guide

const COUNTRIES_DATA = {json.dumps(compiled_countries, indent=2, ensure_ascii=False)};
const MODES_DATA = {json.dumps(modes_list, indent=2, ensure_ascii=False)};
const FUNDAMENTALS_DATA = {json.dumps(fundamentals_data, indent=2, ensure_ascii=False)};
const HIGHWAYS_DATA = {json.dumps(highways_data, indent=2, ensure_ascii=False)};
const META_DATA = {json.dumps(meta_data, indent=2, ensure_ascii=False)};
const PLATES_DATA = {json.dumps(plates_data, indent=2, ensure_ascii=False)};
const LANGUAGES_DATA = {json.dumps(languages_data, indent=2, ensure_ascii=False)};
const QUIZ_QUESTIONS = {json.dumps(quiz_questions, indent=2, ensure_ascii=False)};

if (typeof module !== 'undefined' && module.exports) {{
  module.exports = {{
    COUNTRIES_DATA,
    MODES_DATA,
    FUNDAMENTALS_DATA,
    HIGHWAYS_DATA,
    META_DATA,
    PLATES_DATA,
    LANGUAGES_DATA,
    QUIZ_QUESTIONS
  }};
}}
"""

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(output_content)

print(f"data.js written successfully! Size: {len(output_content)} bytes.")
