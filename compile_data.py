import json
import re
import os

print("Starting data compilation for GeoGuessr website...")

# Load all JSON sources
cheat_sheet = json.load(open('country_cheat_sheet.json', encoding='utf-8'))
modes_json = json.load(open('01_modes.json', encoding='utf-8'))
fund_json = json.load(open('02_fundamentals.json', encoding='utf-8'))
highways_json = json.load(open('03_highway_numbering.json', encoding='utf-8'))
general_json = json.load(open('04_general_clues.json', encoding='utf-8'))
meta_json = json.load(open('05_meta.json', encoding='utf-8'))
plates_json = json.load(open('06_license_plates.json', encoding='utf-8'))
languages_json = json.load(open('07_languages.json', encoding='utf-8'))

print(f"Loaded source files. Country count: {len(cheat_sheet['countries'])}")

# Helper to remove humor and rambling from text
def clean_text(text):
    if not text:
        return ""
    # Common humorous / rambling phrases to strip or clean up
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
    cleaned = text
    for pat in humor_patterns:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)
    
    # clean extra spaces
    cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
    return cleaned

print("clean_text helper configured.")
