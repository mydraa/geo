# -*- coding: utf-8 -*-
"""
Full Bilingual GeoGuessr Knowledge Engine Compiler
Builds the complete production data.js with 100% facts preserved, zero humor, and seamless FR/EN localization.
"""

import json
import re
import os

print("Building complete bilingual GeoGuessr engine...")

# Import the existing compiled datasets from generate_bilingual_data.py
import generate_bilingual_data as gen

compiled_countries = gen.compiled_countries
MODES_DATA = gen.MODES_DATA
BOLLARDS_DATA = gen.BOLLARDS_DATA
QUIZ_QUESTIONS_BILINGUAL = gen.QUIZ_QUESTIONS_BILINGUAL

# 1. FUNDAMENTALS_DATA (Bilingual)
FUNDAMENTALS_DATA = {
    "en": {
        "sun_compass": {
            "title": "☀️ Sun Positioning & Hemisphere Logic",
            "points": [
                "Northern Hemisphere: The sun travels along the southern portion of the sky. Looking directly at the midday sun means your in-game compass needle will point SOUTH.",
                "Southern Hemisphere: The sun travels along the northern sky. Looking directly at midday sun means your in-game compass needle will point NORTH.",
                "Equatorial Region: Between the Tropics of Cancer (23.5° N) and Capricorn (23.5° S), the sun can appear directly overhead or slightly to the north/south depending on the month of coverage. Do not rely exclusively on solar angles near the equator.",
                "In-game Compass: The red needle always points NORTH. The white needle always points SOUTH. Rotating your view changes the camera orientation relative to true north."
            ]
        },
        "shadows": {
            "title": "📐 Shadow Projection & Solar Angles",
            "points": [
                "Shadows cast directly opposite to the position of the sun.",
                "If a utility pole or tree casts its shadow towards the NORTH, the sun is situated in the SOUTH → Northern Hemisphere.",
                "If shadows project towards the SOUTH, the sun is located in the NORTH → Southern Hemisphere.",
                "Short noon shadows indicate tropical or summer coverage, whereas long dramatic shadows indicate high-latitude nations (Nordics, Iceland, southern Chile/Argentina, Russia) or winter coverage."
            ]
        },
        "satellite_dishes": {
            "title": "📡 Satellite Dish Orientation (Geostationary Orbit)",
            "points": [
                "Telecommunication satellites orbit in geostationary trajectories directly above the equator.",
                "In the Northern Hemisphere, domestic satellite dishes universally tilt toward the SOUTH.",
                "In the Southern Hemisphere, satellite dishes tilt toward the NORTH.",
                "USA Longitude Trick: The primary US domestic television satellites are situated directly south of Texas. In western states (California, Washington, Oregon), dishes aim SOUTH-EAST. In eastern states (New York, Florida, Carolinas), dishes aim SOUTH-WEST. In central states (Kansas, Texas, Nebraska), dishes aim straight SOUTH."
            ]
        },
        "road_orientation": {
            "title": "🧭 Road Heading & Compass Alignment",
            "points": [
                "In remote areas with sparse road networks (Patagonia, Outback Australia, Mongolia, Botswana, northern Russia), road angle is a definitive locator.",
                "Technique: Pan straight down to view the road beneath the car. Align your view exactly parallel with the road markings. Observe the compass heading.",
                "Open the mini-map and locate roads sharing that exact geographic bearing (e.g. North-East / South-West at 45°). In desolate expanses, often only one single highway matches that heading."
            ]
        }
    },
    "fr": {
        "sun_compass": {
            "title": "☀️ Position du Soleil & Détermination de l'Hémisphère",
            "points": [
                "Hémisphère Nord : Le soleil traverse la partie SUD du ciel. Regarder le soleil de midi signifie que l'aiguille de votre boussole pointera vers le SUD.",
                "Hémisphère Sud : Le soleil culmine dans la partie NORD du ciel. Regarder le soleil de midi signifie que l'aiguille de votre boussole pointera vers le NORD.",
                "Zone Équatoriale : Entre le tropique du Cancer (23,5° N) et du Capricorne (23,5° S), le soleil peut être zénithal ou basculer au nord/sud selon la saison. Ne vous fiez pas exclusivement au soleil à proximité immédiate de l'équateur.",
                "Boussole en jeu : L'aiguille ROUGE pointe constamment vers le NORD géographique. L'aiguille BLANCHE pointe vers le SUD."
            ]
        },
        "shadows": {
            "title": "📐 Orientation des Ombres & Angles Solaires",
            "points": [
                "Les ombres sont projetées à l'opposé exact de la position du soleil.",
                "Si l'ombre d'un poteau ou d'un arbre s'étire vers le NORD, le soleil est au SUD → Hémisphère Nord.",
                "Si l'ombre est projetée vers le SUD, le soleil brille au NORD → Hémisphère Sud.",
                "Des ombres courtes de midi signalent une latitude tropicale ou estivale, tandis que de très longues ombres rasantes caractérisent les hautes latitudes (Scandinavie, Islande, Patagonie chilienne/argentine, Sibérie)."
            ]
        },
        "satellite_dishes": {
            "title": "📡 Orientation des Paraboles Satellitaires (Orbite Géostationnaire)",
            "points": [
                "Les satellites de télécommunication sont positionnés en orbite géostationnaire au-dessus de l'équateur.",
                "Dans l'Hémisphère Nord, toutes les paraboles domestiques pointent vers le SUD.",
                "Dans l'Hémisphère Sud, les paraboles sont orientées vers le NORD.",
                "Astuce de longitude aux États-Unis : Les principaux satellites TV américains se situent au sud du Texas. Dans les États de l'Ouest (Californie, Oregon, Washington), les paraboles visent le SUD-EST. Dans les États de l'Est (New York, Floride), elles visent le SUD-OUEST. Au centre (Kansas, Texas, Nebraska), elles pointent plein SUD."
            ]
        },
        "road_orientation": {
            "title": "🧭 Orientation de la Chaussée & Boussole",
            "points": [
                "Dans les contrées désertiques ou isolées (Patagonie, Outback australien, Mongolie, Botswana, grand nord russe), l'orientation de la route est un indice décisif.",
                "Méthode : Inclinez la caméra verticalement vers le sol pour vous aligner parfaitement sur la route. Observez l'azimut sur la boussole.",
                "Consultez la mini-carte pour rechercher les rares tronçons partageant cet angle précis (ex: axe Nord-Est / Sud-Ouest à 45°). Dans les zones reculées, une seule route correspond souvent à cet alignement."
            ]
        }
    }
}

# 2. HIGHWAYS_DATA (Bilingual)
HIGHWAYS_DATA = {
    "en": [
        {
            "region": "United States",
            "system": "Interstate Highway System",
            "rules": [
                "Even-numbered Interstates (I-10, I-40, I-80, I-90) run East-West. Route numbers increase sequentially from South to North (I-10 borders the Gulf of Mexico, I-90 borders Canada).",
                "Odd-numbered Interstates (I-5, I-15, I-35, I-75, I-95) run North-South. Route numbers increase sequentially from West to East (I-5 along the Pacific Coast, I-95 along the Atlantic Coast).",
                "3-Digit Interstates: Auxiliary bypasses or spurs. An EVEN first digit (e.g. I-405 in LA, I-285 in Atlanta) forms a loop or beltway connecting at two points. An ODD first digit (e.g. I-195) represents a radial spur entering an urban center.",
                "US Highways vs Interstates: US Highways predate Interstates and follow the OPPOSITE numbering grid (US-1 is on the Atlantic East Coast, US-101 is on the Pacific West Coast; US-10 is north, US-90 is south)."
            ]
        },
        {
            "region": "Brazil",
            "system": "Rodovias Federais (BR Network)",
            "rules": [
                "BR-0xx (Radial Highways): Radiate outwards in all directions directly from the federal capital Brasília (e.g. BR-040 connects Brasília to Rio de Janeiro, BR-070 towards Bolivia).",
                "BR-1xx (Longitudinal Highways): Run strictly North-South. Numbering increases from East to West (BR-101 hugs the Atlantic coast, BR-163 cuts through central Amazonia).",
                "BR-2xx (Transversal Highways): Run strictly East-West. Numbering increases from North to South (BR-230 Trans-Amazonian in the north, BR-290 in Rio Grande do Sul in the south).",
                "BR-3xx (Diagonal Highways): Cross the nation diagonally (North-West to South-East, or North-East to South-West).",
                "BR-4xx (Connecting Links): Shorter bypasses linking two major federal routes or border crossings."
            ]
        },
        {
            "region": "United Kingdom",
            "system": "Radial Numbering Zones",
            "rules": [
                "Zone 1: Between A1 (London north to Edinburgh) and A2 (London south-east to Dover) — covers East Anglia and Essex.",
                "Zone 2: South of the Thames, between A2 and A3 (London south-west to Portsmouth) — covers Kent, Sussex, and Surrey.",
                "Zone 3: Between A3 and A4 (London west to Bristol) — covers Hampshire and Berkshire.",
                "Zone 4: Between A4 and A5 (London north-west to Holyhead) — covers Oxford, Cotswolds, and Midlands.",
                "Zone 5: Between A5 and A6 (London north to Carlisle) — covers North Wales and North-West England.",
                "Zone 6: Between A6 and A1 — covers Yorkshire, Durham, and Northumberland.",
                "Zones 7, 8, 9: Cover Scotland, radiating clockwise around Edinburgh."
            ]
        },
        {
            "region": "Europe",
            "system": "International E-road Network",
            "rules": [
                "Standard Signage: Green rectangular signs with white bold text and white outer border.",
                "North-South Reference Routes: Double-digit numbers ending strictly in '5' (E05, E15, E25, E35, E45, E55, E65, E75, E85, E95, E105, E115). Numbers escalate systematically from West to East (E05 in Spain/France, E75 through Poland/Greece, E115 in Russia).",
                "East-West Reference Routes: Double-digit numbers ending strictly in '0' (E10, E20, E30, E40, E50, E60, E70, E80, E90). Numbers escalate systematically from North to South (E10 in northern Norway, E90 through southern Italy/Greece/Turkey).",
                "Intermediate Routes: Numbered according to their grid quadrant between reference corridors."
            ]
        },
        {
            "region": "Russia",
            "system": "Federal Highway Network (M, R, A)",
            "rules": [
                "M-Highways: Major federal arterial corridors radiating directly from Moscow (M1 to Belarus border, M2 towards Ukraine, M3 to Kyiv direction, M4 'Don' to the Black Sea, M5 'Ural' to Chelyabinsk, M7 'Volga' to Kazan/Ufa, M8 'Kholmogory' to Arkhangelsk, M9 'Baltic' to Latvia, M10/M11 'Neva' to St. Petersburg).",
                "R-Highways (P in Cyrillic): Regional federal connector highways (e.g. R21 'Kola' to Murmansk, R256 'Chuya' scenic route in Altai).",
                "A-Highways: Access roads, orbital rings (e.g. A107/A108 Moscow rings), and cross-border connector links."
            ]
        },
        {
            "region": "Nordic Countries",
            "system": "Norway, Sweden & Finland Signage",
            "rules": [
                "Norway: Green signs reserved for European E-roads; Riksvei (Rv) national highways and Fylkesvei (Fv) county roads displayed on white rectangular signs with black lettering and black border.",
                "Sweden: Blue rectangular signs with white numbers without letter prefixes (e.g. 50, 70, 26). E-roads use standard green signs.",
                "Finland: Red rectangular signs for primary national highways (numbered 1 to 29); yellow rectangular signs with black lettering for secondary routes (40 to 99); blue rectangular signs for regional routes (100 to 999)."
            ]
        },
        {
            "region": "Japan",
            "system": "National Highways & Expressways",
            "rules": [
                "National Highways (Kokudō): Blue triangular-shield shaped signs with white bold digits (numbered 1 to 507). Route 1 connects Tokyo to Osaka.",
                "Expressways (Kōsokudōro): Green rectangular signs featuring routes prefixed by the letter 'E' (e.g. E1 Tōmei Expressway, E4 Tōhoku Expressway)."
            ]
        }
    ],
    "fr": [
        {
            "region": "États-Unis",
            "system": "Réseau Autoroutier Interstate",
            "rules": [
                "Numéros PAIRS (I-10, I-40, I-80, I-90) : Voies Est-Ouest. La numérotation augmente du Sud vers le Nord (I-10 longe le Golfe du Mexique, I-90 longe la frontière canadienne).",
                "Numéros IMPAIRS (I-5, I-15, I-35, I-75, I-95) : Voies Nord-Sud. La numérotation augmente de l'Ouest vers l'Est (I-5 sur la côte Pacifique, I-95 sur la côte Atlantique).",
                "Interstates à 3 chiffres : Rocades et bretelles urbaines. Si le 1er chiffre est PAIR (ex. I-405 à Los Angeles, I-285 à Atlanta), c'est une boucle/rocade contournant la ville. Si le 1er chiffre est IMPAIR (ex. I-195), c'est une antenne pénétrante menant au centre-ville.",
                "US Highways vs Interstates : Les anciennes US Routes suivent la logique INVERSE (US-1 est sur la côte Est Atlantique, US-101 sur la côte Ouest Pacifique)."
            ]
        },
        {
            "region": "Brésil",
            "system": "Rodovias Federais (Réseau BR)",
            "rules": [
                "BR-0xx (Autoroutes Radiales) : Rayonnent dans toutes les directions depuis la capitale fédérale Brasília (ex. BR-040 relie Brasília à Rio de Janeiro, BR-070 vers la Bolivie).",
                "BR-1xx (Autoroutes Longitudinales) : Strictement orientées Nord-Sud. La numérotation croît d'Est en Ouest (BR-101 longe la côte Atlantique, BR-163 traverse l'Amazonie centrale).",
                "BR-2xx (Autoroutes Transversales) : Strictement orientées Est-Ouest. La numérotation croît du Nord vers le Sud (BR-230 Transamazonienne au nord, BR-290 dans le Rio Grande do Sul au sud).",
                "BR-3xx (Autoroutes Diagonales) : Traversent le pays en diagonale (Nord-Ouest / Sud-Est ou Nord-Est / Sud-Ouest).",
                "BR-4xx (Voies de Raccordement) : Bretelles courtes reliant deux grands axes fédéraux ou des postes frontières."
            ]
        },
        {
            "region": "Royaume-Uni",
            "system": "Zones Radiales du Réseau Routier",
            "rules": [
                "Zone 1 : Entre l'A1 (Londres vers Édimbourg) et l'A2 (Londres vers Douvres) — couvre l'Est-Anglie et l'Essex.",
                "Zone 2 : Au sud de la Tamise, entre l'A2 et l'A3 (Londres vers Portsmouth) — couvre le Kent, le Sussex et le Surrey.",
                "Zone 3 : Entre l'A3 et l'A4 (Londres vers Bristol) — couvre le Hampshire et le Berkshire.",
                "Zone 4 : Entre l'A4 et l'A5 (Londres vers Holyhead) — couvre Oxford, les Cotswolds et les Midlands.",
                "Zone 5 : Entre l'A5 et l'A6 (Londres vers Carlisle) — couvre le Nord du Pays de Galles et le Nord-Ouest anglais.",
                "Zone 6 : Entre l'A6 et l'A1 — couvre le Yorkshire, Durham et le Northumberland.",
                "Zones 7, 8, 9 : Couvrent l'Écosse en rayonnant dans le sens horaire autour d'Édimbourg."
            ]
        },
        {
            "region": "Europe",
            "system": "Réseau International des Routes E (E-Roads)",
            "rules": [
                "Signalétique : Panneaux rectangulaires verts bordés de blanc avec texte blanc gras préfixé d'un 'E'.",
                "Axes de référence Nord-Sud : Numéros à deux chiffres se terminant impérativement par '5' (E05, E15, E25... E75, E85, E115). Les numéros augmentent d'Ouest en Est (E05 en Espagne/France, E75 en Pologne/Grèce, E115 en Russie).",
                "Axes de référence Est-Ouest : Numéros à deux chiffres se terminant impérativement par '0' (E10, E20, E30... E90). Les numéros augmentent du Nord au Sud (E10 en Norvège du Nord, E90 en Italie/Grèce/Turquie).",
                "Routes secondaires : Numérotées en fonction de leur quadrant de rattachement aux axes majeurs."
            ]
        },
        {
            "region": "Russie",
            "system": "Réseau Autoroutier Fédéral (M, P, A)",
            "rules": [
                "Routes M : Grands corridors fédéraux rayonnant directement depuis Moscou (M1 vers la Biélorussie, M2 vers l'Ukraine, M3 vers Kyiv, M4 'Don' vers la Mer Noire, M5 'Oural' vers Tcheliabinsk, M7 'Volga' vers Kazan, M8 vers Arkhangelsk, M9 'Baltique' vers la Lettonie, M10/M11 vers Saint-Pétersbourg).",
                "Routes P (R en alphabet cyrillique) : Liaisons fédérales régionales (ex. P21 'Kola' vers Mourmansk, P256 'Tchouïa' dans l'Altaï).",
                "Routes A : Voies d'accès, rocades orbitales (A107/A108 autour de Moscou) et liaisons transfrontalières."
            ]
        },
        {
            "region": "Pays Nordiques",
            "system": "Signalétique Routière en Norvège, Suède et Finlande",
            "rules": [
                "Norvège : Panneaux verts réservés aux routes E ; routes nationales Riksvei (Rv) et départementales Fylkesvei (Fv) indiquées sur panneaux blancs à bordure et texte noirs.",
                "Suède : Panneaux rectangulaires bleus avec numéros blancs sans préfixe de lettre (ex. 50, 70, 26). Panneaux verts pour les routes E.",
                "Finlande : Panneaux rectangulaires rouges pour les routes nationales principales (1 à 29) ; jaunes pour les secondaires (40 à 99) ; bleus pour les régionales (100 à 999)."
            ]
        },
        {
            "region": "Japon",
            "system": "Routes Nationales & Voies Express",
            "rules": [
                "Routes Nationales (Kokudō) : Panneau distinctif en forme d'écusson triangulaire bleu avec chiffres blancs (numérotées de 1 à 507). La Route 1 relie Tokyo à Osaka.",
                "Voies Express (Kōsokudōro) : Panneaux rectangulaires verts avec numéros précédés de la lettre 'E' (ex. E1 Tomei Expressway, E4 Tohoku)."
            ]
        }
    ]
}

# 3. META_DATA (Bilingual)
META_DATA = {
    "en": {
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
        ]
    },
    "fr": {
        "camera_generations": [
            {
                "gen": "Génération 1 (2007-2008)",
                "traits": "Résolution extrêmement basse, pixellisation très lourde, artefacts de compression prononcés, couleurs délavées. Strictement cantonnée aux États-Unis et à l'Australie."
            },
            {
                "gen": "Génération 2 (2008-2010)",
                "traits": "Flou circulaire violet ou noir sous la Google car ; halo lumineux très marqué autour du soleil ; contraste affaibli. Fréquente dans les déserts mexicains, le grand nord canadien, l'Afrique du Sud et les premières couvertures européennes."
            },
            {
                "gen": "Génération 3 (2011-2017)",
                "traits": "Haute définition nette ; flou de voiture circulaire standard ; raccords panoramiques soignés ; équilibre naturel des couleurs. Le standard mondial couvrant plus de 80 nations."
            },
            {
                "gen": "Génération 4 (2017 à aujourd'hui)",
                "traits": "Résolution Ultra-HD 4K ; saturation vibrante des couleurs ; discret reflet bleuté sur l'objectif ; netteté chirurgicale permettant de lire les petits panneaux et crêtes d'horizons lointains."
            }
        ],
        "car_meta": [
            {"country": "Kenya", "clue": "Snorkel d'admission d'air noir monté sur le montant avant-droit de la Google car."},
            {"country": "Ghana", "clue": "Galerie de toit métallique visible avec de l'adhésif d'électricien noir entourant l'une des barres."},
            {"country": "Guatemala", "clue": "Galerie de toit visible avec deux rétroviseurs latéraux dressés devant la caméra."},
            {"country": "Mongolie", "clue": "Benne de pick-up chargée d'équipement d'expédition, pneus de secours et sacs de voyage sous bâche."},
            {"country": "Sénégal", "clue": "Barres de toit métalliques associées à de nettes déchirures panoramiques dans le ciel (rifts)."},
            {"country": "Nigeria", "clue": "Présence constante d'un pick-up de police d'escorte avec rampe lumineuse allumée (visible à l'avant ou à l'arrière)."},
            {"country": "Curaçao", "clue": "Pick-up noir avec arceaux tubulaires imposants dans la benne."},
            {"country": "République Dominicaine", "clue": "Barres de toit blanches aux pieds de fixation en caoutchouc noir."},
            {"country": "Bermudes", "clue": "Petit buggy décapotable roulant sur la gauche de la chaussée."},
            {"country": "La Réunion", "clue": "Voiture bleue ou blanche avec antennes de toit caractéristiques sur reliefs tropicaux abrupts."},
            {"country": "Sri Lanka", "clue": "Voiture blanche avec rétroviseurs et ombre distincte du mât de caméra sur la route."},
            {"country": "Jordanie", "clue": "Pick-up noir ou blanc avec antenne dans les paysages désertiques jordaniens."},
            {"country": "Ouganda", "clue": "Voiture blanche avec barres de toit et pare-chocs blanc au-dessus d'une terre rouge vif."}
        ]
    }
}

# 4. PLATES_DATA (Bilingual)
PLATES_DATA = {
    "en": {
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
            "title": "🇺🇸 USA Front vs. Rear Plate Laws (State Streak Master Guide)",
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
        "canada": [
            {"province": "Alberta", "rule": "Rear plate only; red lettering on white."},
            {"province": "Saskatchewan", "rule": "Rear plate only; green lettering on white."},
            {"province": "New Brunswick", "rule": "Both front and rear plates required; red lettering."},
            {"province": "Newfoundland & Labrador", "rule": "Rear plate only; red lettering on white."},
            {"province": "Northwest Territories", "rule": "Unique custom die-cut plate shaped like a polar bear!"}
        ],
        "latin_america": [
            {"region": "Mercosur Standard", "description": "Brazil, Argentina, Uruguay, and Paraguay share the Mercosur format: white plate with blue banner along the top."},
            {"region": "Colombia", "description": "All commercial vehicles, buses, and taxis have bright yellow license plates."}
        ]
    },
    "fr": {
        "europe": [
            {"type": "Plaque UE Standard", "description": "Plaque blanche rectangulaire allongée avec un bandeau bleu unique à gauche arborant les 12 étoiles dorées et l'identifiant pays."},
            {"type": "Double Bandeau Bleu (Gauche & Droite)", "description": "L'Italie, la France et l'Albanie arborent des bandes bleues à la fois à GAUCHE (pays) et à DROITE (département ou province)."},
            {"type": "Plaque Avant Courte", "description": "L'Italie et Saint-Marin utilisent des plaques avant remarquablement courtes et compactes par rapport au standard européen."},
            {"type": "Plaques 100% Jaunes (Avant & Arrière)", "description": "Les Pays-Bas, le Luxembourg et Israël utilisent des plaques entièrement jaunes à l'avant et à l'arrière."},
            {"type": "Blanc à l'Avant / Jaune à l'Arrière", "description": "Le Royaume-Uni, Gibraltar, l'Île de Man et Chypre imposent une plaque blanche à l'avant et jaune à l'arrière."},
            {"type": "Caractères Rouges", "description": "La Belgique se distingue par des caractères rouge bordeaux sur fond blanc."},
            {"type": "Plaques Noires", "description": "Le Liechtenstein utilise des plaques à fond noir avec lettrage blanc."}
        ],
        "usa_laws": {
            "title": "🇺🇸 Lois des Plaques aux USA : Avant vs Arrière (State Streaks)",
            "rear_only_states": [
                "Alabama", "Arizona", "Arkansas", "Caroline du Nord", "Caroline du Sud", "Delaware",
                "Floride", "Géorgie", "Indiana", "Kansas", "Kentucky", "Louisiane",
                "Michigan", "Mississippi", "Nouveau-Mexique", "Oklahoma", "Pennsylvanie",
                "Tennessee", "Virginie-Occidentale"
            ],
            "both_front_rear_states": [
                "Alaska", "Californie", "Colorado", "Connecticut", "Dakota du Nord", "Dakota du Sud",
                "Hawaï", "Idaho", "Illinois", "Iowa", "Maine", "Maryland", "Massachusetts",
                "Minnesota", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
                "New Jersey", "New York", "Ohio", "Oregon", "Rhode Island", "Texas",
                "Utah", "Vermont", "Virginie", "Washington", "Wisconsin", "Wyoming",
                "Washington D.C."
            ]
        },
        "canada": [
            {"province": "Alberta", "rule": "Plaque arrière uniquement ; caractères rouges sur fond blanc."},
            {"province": "Saskatchewan", "rule": "Plaque arrière uniquement ; caractères verts sur fond blanc."},
            {"province": "Nouveau-Brunswick", "rule": "Plaque avant et arrière obligatoires ; caractères rouges."},
            {"province": "Terre-Neuve-et-Labrador", "rule": "Plaque arrière uniquement ; caractères rouges sur fond blanc."},
            {"province": "Territoires du Nord-Ouest", "rule": "Plaque unique au monde découpée en silhouette d'ours polaire !"}
        ],
        "latin_america": [
            {"region": "Standard Mercosur", "description": "Le Brésil, l'Argentine, l'Uruguay et le Paraguay partagent le format Mercosur : plaque blanche surmontée d'un bandeau bleu supérieur."},
            {"region": "Colombie", "description": "Tous les taxis, bus et utilitaires commerciaux possèdent des plaques jaune vif."}
        ]
    }
}

# 5. LANGUAGES_DATA (Bilingual)
LANGUAGES_DATA = {
    "en": {
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
    },
    "fr": {
        "cyrillic": [
            {"language": "Russe", "alphabet": "Cyrillique standard. Utilise : ы, э, ъ. N'utilise JAMAIS : і, ї, є, ў."},
            {"language": "Ukrainien", "alphabet": "Lettres signatures : і (i pointé), ї (i tréma), є (e inversé), ’ (apostrophe)."},
            {"language": "Biélorusse", "alphabet": "Lettres signatures : ў (u court) et і."},
            {"language": "Bulgare", "alphabet": "Usage très fréquent de ъ en milieu/fin de mot ; n'emploie pas ы, э, і."},
            {"language": "Serbe", "alphabet": "Emprunte le ј latin, complété par љ, њ, џ, ћ, ђ."},
            {"language": "Macédonien", "alphabet": "Emploie ј, љ, њ, џ, ainsi que ѓ, ќ."},
            {"language": "Mongol", "alphabet": "Alphabet cyrillique avec les voyelles spécifiques ө et ү."},
            {"language": "Kazakh", "alphabet": "Cyrillique avec ә, ғ, қ, ң, ө, ұ, ү, һ, і."}
        ],
        "nordic": [
            {"language": "Danois & Norvégien", "characters": "Emploient æ et ø. Terminaisons de rues en Norvège : -vei, -gate. Au Danemark : -vej, -gade."},
            {"language": "Suédois & Finnois", "characters": "Emploient ä et ö. Terminaisons en Suède : -väg, -gatan. Le finnois est non-germanique avec voyelles doublées et terminaisons -tie, -katu."},
            {"language": "Islandais & Féroïen", "characters": "Lettres uniques islandaises et féroïennes : ð (eth) et þ (thorn)."}
        ],
        "eastern_europe": [
            {"language": "Polonais", "features": "Groupes de consonnes denses (sz, cz, rz) et lettres spécifiques : ł, ą, ę, ś, ć, ż, ź, ń. Rue = Ulica (Ul.)."},
            {"language": "Tchèque", "features": "Lettres à accent circonflexe inversé (hacek) caractéristiques : ř, ů, ě, č, š, ž."},
            {"language": "Slovaque", "features": "Lettres distinctives : ä, ô, ŕ, ĺ, ľ."},
            {"language": "Hongrois", "features": "Langue finno-ougrienne ; lettres : ő, ű, á, é, í, ó, ö, ú, ü ; digraphes : sz, gy, cs. Rue = utca."},
            {"language": "Roumain", "features": "Langue romane avec cédilles sous s et t : ș, ț, ă, â, î. Rue = Strada."}
        ],
        "asian_scripts": [
            {"script": "Thaï", "appearance": "Lignes courbes fluides terminées par de petites boucles circulaires sur chaque lettre."},
            {"script": "Khmer (Cambodge)", "appearance": "Plus ornementé et courbé que le thaï, avec des jambages ondulés sous les caractères."},
            {"script": "Hangul (Coréen)", "appearance": "Composé de blocs géométriques associant des ronds (ㅇ) et des traits droits orthogonaux."},
            {"script": "Japonais", "appearance": "Mélange de Kanji (idéogrammes chinois complexes), Hiragana (courbes fluides) et Katakana (traits droits anguleux)."},
            {"script": "Chinois Traditionnel", "appearance": "Utilisé à Taïwan et Hong Kong ; idéogrammes complexes et denses sans simplification."}
        ]
    }
}

# 6. Comprehensive I18N dictionary
I18N = {
    "en": {
        "brandTitle": "GEOMASTER",
        "brandSubtitle": "GeoGuessr Pro Intelligence Engine",
        "brandBadge": "PRO KNOWLEDGE ENGINE",
        "heroTitle": "🌍 Global Country & Territory Playbook",
        "heroSubtitle": "Every single Street View nation parsed with surgical precision. Instant identification via bollards, utility poles, license plates, car meta, and regional giveaways—with zero fluff.",
        "statCountries": "Countries",
        "statAccuracy": "Facts Preserved",
        "statClues": "Visual Clues",
        "searchPlaceholder": "Search countries, bollards, poles, car meta, languages, keywords (e.g. 'snorkel', 'birch', 'Swiss cheese')...",
        "allContinents": "All",
        "filterDrivingAll": "Driving: All",
        "filterDrivingLeft": "🚗 Left Hand Drive (RHD)",
        "filterDrivingRight": "🚙 Right Hand Drive (LHD)",
        "tabCountries": "🌍 Countries (122)",
        "tabMatrix": "⚡ Clue Matrix Guesser",
        "tabBollards": "🛑 Bollards & Signs",
        "tabMeta": "🚗 Car Meta & Cam Gens",
        "tabPlates": "🚙 License Plates",
        "tabHighways": "🛣️ Highway Grids",
        "tabLanguages": "🔤 Languages & Scripts",
        "tabModes": "🎮 Game Modes & Tactics",
        "tabFundamentals": "☀️ Fundamentals & Sun",
        "tabQuiz": "🎯 Practice Quiz",
        "inspectBtn": "Inspect Dossier ➔",
        "giveawayTitle": "⚡ SIGNATURE GIVEAWAY",
        "modalKeyIndicators": "Key Identification Clues",
        "modalGallery": "Visual Clues & Photographic Evidence",
        "modalClose": "Close Dossier",
        "matrixTitle": "⚡ Interactive Clue Matrix & Meta Guesser",
        "matrixSubtitle": "Locked in a game? Select what you see on your screen right now to immediately narrow down the candidate countries.",
        "matrixDrivingTitle": "1. Driving Side",
        "matrixPlateTitle": "2. License Plate Style",
        "matrixCarTitle": "3. Street View Car Meta",
        "matrixPoleTitle": "4. Utility Pole Features",
        "matrixBollardTitle": "5. Delineator Bollard",
        "matrixResetBtn": "↺ Reset All Clues",
        "matrixCandidates": "Candidates",
        "quizTitle": "🎯 Competitive GeoGuessr Practice Quiz",
        "quizSubtitle": "Test your instantaneous recall on car meta, bollards, camera generations, highway networks, and license plates.",
        "quizQuestionOf": "Question",
        "quizOf": "of",
        "quizScore": "Score",
        "quizStreak": "Streak",
        "quizNextBtn": "Next Question ➔",
        "quizCorrectTitle": "✓ Correct! Outstanding deduction.",
        "quizIncorrectTitle": "✗ Incorrect deduction.",
        "quizExplanation": "Strategic Analysis:",
        "anyVal": "Any",
        "photosCount": "Photos",
        "cluesCount": "Clues",
        "drivesOnRight": "🚙 Drives on Right",
        "drivesOnLeft": "🚗 Drives on Left",
        "tldLabel": "TLD",
        "noMatches": "No matching countries found",
        "noMatchesSub": "Try adjusting your search query or clearing the continent filter."
    },
    "fr": {
        "brandTitle": "GEOMASTER",
        "brandSubtitle": "Moteur d'Intelligence GeoGuessr Pro",
        "brandBadge": "MOTEUR PRO DE CONNAISSANCES",
        "heroTitle": "🌍 Guide Magistral des Pays & Territoires",
        "heroSubtitle": "Chaque nation Street View décortiquée avec une précision chirurgicale. Identification immédiate par bollards, poteaux électriques, plaques, méta de la voiture et repères régionaux — zéro blabla.",
        "statCountries": "Pays Couverts",
        "statAccuracy": "Informations Préservées",
        "statClues": "Preuves Visuelles",
        "searchPlaceholder": "Rechercher un pays, bollard, poteau, méta, écriture, mot-clé (ex: 'snorkel', 'bouleau', 'gruyère')...",
        "allContinents": "Tous",
        "filterDrivingAll": "Conduite : Tous",
        "filterDrivingLeft": "🚗 Conduite à gauche (RHD)",
        "filterDrivingRight": "🚙 Conduite à droite (LHD)",
        "tabCountries": "🌍 Pays (122)",
        "tabMatrix": "⚡ Matrice d'Indices",
        "tabBollards": "🛑 Bollards & Panneaux",
        "tabMeta": "🚗 Caméras & Méta Car",
        "tabPlates": "🚙 Plaques d'Immat",
        "tabHighways": "🛣️ Réseaux Routiers",
        "tabLanguages": "🔤 Langues & Écritures",
        "tabModes": "🎮 Modes & Stratégies",
        "tabFundamentals": "☀️ Soleil & Boussole",
        "tabQuiz": "🎯 Quiz d'Entraînement",
        "inspectBtn": "Consulter le dossier ➔",
        "giveawayTitle": "⚡ INDICE SIGNATURE",
        "modalKeyIndicators": "Indices Clés d'Identification",
        "modalGallery": "Galerie de Preuves Visuelles & Délinéateurs",
        "modalClose": "Fermer le Dossier",
        "matrixTitle": "⚡ Matrice d'Indices & Guesser Intelligent",
        "matrixSubtitle": "En pleine partie ? Cochez les éléments visibles sur votre écran pour filtrer instantanément les pays candidats.",
        "matrixDrivingTitle": "1. Sens de Conduite",
        "matrixPlateTitle": "2. Style de Plaque d'Immatriculation",
        "matrixCarTitle": "3. Méta de la Google Car",
        "matrixPoleTitle": "4. Caractéristiques des Poteaux",
        "matrixBollardTitle": "5. Type de Délinéateur (Bollard)",
        "matrixResetBtn": "↺ Réinitialiser les Indices",
        "matrixCandidates": "Candidats Possibles",
        "quizTitle": "🎯 Quiz d'Entraînement Compétitif",
        "quizSubtitle": "Entraînez vos réflexes d'identification immédiate sur la méta car, les bollards, les générations de caméras, les autoroutes et les plaques.",
        "quizQuestionOf": "Question",
        "quizOf": "sur",
        "quizScore": "Score",
        "quizStreak": "Série",
        "quizNextBtn": "Question Suivante ➔",
        "quizCorrectTitle": "✓ Exact ! Excellente déduction.",
        "quizIncorrectTitle": "✗ Mauvaise déduction.",
        "quizExplanation": "Analyse Tactique :",
        "anyVal": "Tous",
        "photosCount": "Photos",
        "cluesCount": "Indices",
        "drivesOnRight": "🚙 Conduite à droite",
        "drivesOnLeft": "🚗 Conduite à gauche",
        "tldLabel": "Domaine",
        "noMatches": "Aucun pays correspondant",
        "noMatchesSub": "Modifiez votre recherche ou réinitialisez le filtre de continent."
    }
}

# 7. Generate final data.js
output_js = f"""// GeoGuessr Master Playbook & Knowledge Engine
// Fully localized bilingual dataset (French & English)
// 100% of facts preserved, zero humor, high-yield competitive reference.

const COUNTRIES_DATA = {json.dumps(compiled_countries, indent=2, ensure_ascii=False)};
const MODES_DATA = {json.dumps(MODES_DATA, indent=2, ensure_ascii=False)};
const BOLLARDS_DATA = {json.dumps(BOLLARDS_DATA, indent=2, ensure_ascii=False)};
const FUNDAMENTALS_DATA = {json.dumps(FUNDAMENTALS_DATA, indent=2, ensure_ascii=False)};
const HIGHWAYS_DATA = {json.dumps(HIGHWAYS_DATA, indent=2, ensure_ascii=False)};
const META_DATA = {json.dumps(META_DATA, indent=2, ensure_ascii=False)};
const PLATES_DATA = {json.dumps(PLATES_DATA, indent=2, ensure_ascii=False)};
const LANGUAGES_DATA = {json.dumps(LANGUAGES_DATA, indent=2, ensure_ascii=False)};
const QUIZ_QUESTIONS = {json.dumps(QUIZ_QUESTIONS_BILINGUAL, indent=2, ensure_ascii=False)};
const I18N = {json.dumps(I18N, indent=2, ensure_ascii=False)};

if (typeof module !== 'undefined' && module.exports) {{
  module.exports = {{
    COUNTRIES_DATA,
    MODES_DATA,
    BOLLARDS_DATA,
    FUNDAMENTALS_DATA,
    HIGHWAYS_DATA,
    META_DATA,
    PLATES_DATA,
    LANGUAGES_DATA,
    QUIZ_QUESTIONS,
    I18N
  }};
}}
"""

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(output_js)

print("SUCCESS: data.js generated with complete bilingual datasets!")
