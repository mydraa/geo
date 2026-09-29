import json
import re

print("=== STARTING COMPLETE DATA ENRICHMENT (CARS, GIVEAWAYS, PARAGRAPHS, IMAGES) ===")

with open('data.js', 'r', encoding='utf-8') as f:
    code = f.read()

# --------------------------------------------------------------------------
# 1. FIXED IMAGE URLS (Replace Wikimedia Commons rate-limited/400 URLs)
# --------------------------------------------------------------------------
code = code.replace(
    'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Vaduz_Castle_Liechtenstein.jpg/640px-Vaduz_Castle_Liechtenstein.jpg',
    'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/japan-low.png'
)
code = code.replace(
    'https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Liechtenstein_road_sign.jpg/640px-Liechtenstein_road_sign.jpg',
    'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/bol-austria.png'
)
code = code.replace(
    'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/License_plate_Liechtenstein.svg/640px-License_plate_Liechtenstein.svg.png',
    'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/0lp-tunisia-e1557386842522.png'
)
code = code.replace(
    'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Northwest_Territories_license_plate_polar_bear.png/640px-Northwest_Territories_license_plate_polar_bear.png',
    'https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/canada-plates-front-rear-e1557383988674.png'
)

# --------------------------------------------------------------------------
# 2. EXPANDED CAR META (44 Vehicles & Clues)
# --------------------------------------------------------------------------
NEW_CARS_EN = [
  {
    "country": "Kenya (Snorkel)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/00-kenya-car-e1564396284275.png",
    "clue": "Black snorkel air intake attached to the front-right pillar of the Google car. Distinctive across most rural and highway coverage."
  },
  {
    "country": "Kenya (Escort 4WD)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/kenya-escort-car.png",
    "clue": "4-wheel drive escort vehicle following the Google car (often 20 to 100 meters behind). Visible in rural national parks and highways."
  },
  {
    "country": "Ghana (Black Tape)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/00000-ghana-e1565162834182.png",
    "clue": "Visible roof rack with thick black electrical tape wrapped securely around the front-right bar."
  },
  {
    "country": "Uganda (White Car & Mirrors)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/00000-uganda-e1565162687433.png",
    "clue": "White car hood with visible front bumper and large black side mirrors over bright red laterite soil."
  },
  {
    "country": "Mongolia (Camping Tent / Bed)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/geo-mongolia-tent-e1571975220325.png",
    "clue": "Pickup truck bed loaded with camping equipment, wrapped luggage, and spare tires beneath the rear camera."
  },
  {
    "country": "Mongolia (Red Mirrors)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/geo-mongolia-red-sides-e1571975334741.png",
    "clue": "Alternative Mongolian vehicle featuring distinct red-colored side mirrors alongside visible roof bars."
  },
  {
    "country": "Kyrgyzstan (Roof Bars & Mirrors)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/kyr.png",
    "clue": "Metal roof rack bars visible with black and white side mirrors in dramatic mountainous Central Asian terrain."
  },
  {
    "country": "Guatemala (Roof Bars & Big Mirrors)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/guatemala-car.png",
    "clue": "Prominent roof rack bars with two large black side-view mirrors. Unique in Central America."
  },
  {
    "country": "Senegal (White Truck)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/senegal2-1.png",
    "clue": "White open-back utility truck with visible roof rack bars used across newer Senegalese coverage."
  },
  {
    "country": "Senegal (Silver Truck)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/sen2-1.png",
    "clue": "Silver metallic utility truck with bars beneath the camera, complementing the white truck."
  },
  {
    "country": "Senegal (Sky Rifts)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rifts-senegal.png",
    "clue": "Prominent vertical sky rifts (stitching tears in the sky) combined with the metal roof rack bars."
  },
  {
    "country": "Montenegro (Sky Rifts)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rifts-mont.png",
    "clue": "Giant stitching rifts in the sky appearing across almost the entire country outside the central Podgorica oval."
  },
  {
    "country": "Albania (Sky Rifts)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rifts-mont-2-1.png",
    "clue": "Sky rifts appearing in scattered regions across Albania, complementing the double blue license plate bands."
  },
  {
    "country": "Nigeria (Police Escort)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/nigeria-car-1.png",
    "clue": "Police escort 4WD: Silver pickup in greater Lagos; White pickup with emergency police lights outside Lagos; Black 4WD in Benin City."
  },
  {
    "country": "Nigeria (Bars & Blur)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/nigeria-more-1.png",
    "clue": "White vehicle with visible black/yellow patterned bars beneath or large circular blur."
  },
  {
    "country": "Tunisia (Green Escort Vehicle)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/tunisia-car.png",
    "clue": "Dark green Mazda following the Street View car (with dashboard map in Sfax/Gabes); Darker green Toyota following in Tunis."
  },
  {
    "country": "Curaçao (Tubular Roll Bars)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/bars-under-car-e1557829019453.png",
    "clue": "White pickup truck with prominent black tubular steel cab guard / roll bars directly behind the cabin."
  },
  {
    "country": "Dominican Republic (Thick Rubber Bars)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/sd.png",
    "clue": "Extra-long vehicle with roof rack bars mounted on thick black rubber pads with parallel lines."
  },
  {
    "country": "Panama (Wrap-Around Bars)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/cr-car-image-1.png",
    "clue": "White pickup truck with distinctive extra curved bars wrapping around the front and unique antenna."
  },
  {
    "country": "Costa Rica (White Truck No Extra Bars)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/cr-car-image-1.png",
    "clue": "White pickup truck without the extra wrap-around bars found in Panama, navigating lush mountainous terrain."
  },
  {
    "country": "US Virgin Islands (Bulky Ute)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/usvi-car.png",
    "clue": "Bulky open-bed pickup truck (white in northern islands, red/white in southern island); drives on the LEFT."
  },
  {
    "country": "Bermuda (Open Buggy)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/usvi-car.png",
    "clue": "Compact electric open-frame buggy / utility cart; drives on the LEFT on narrow walled lanes."
  },
  {
    "country": "Sri Lanka (French Flag Stripes)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/sri-lanka-car.png",
    "clue": "White car featuring blue, white, and red vertical stripes (resembling the French flag) on the front bumper/bars."
  },
  {
    "country": "Jordan (Black Car)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/jordan-car-black.png",
    "clue": "Black car body visible when panning straight down in arid desert environments."
  },
  {
    "country": "United Arab Emirates (White Car)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/uae-white-car.png",
    "clue": "White car or pickup visible panning straight down on modern paved multi-lane highways."
  },
  {
    "country": "Oman (White Pickup & Antenna)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/oman12-1.png",
    "clue": "White pickup truck with luggage rack bars in the bed; direction of the antenna indicates regional heading."
  },
  {
    "country": "Qatar (Far-Left Antenna)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/qatar-car-1.jpg",
    "clue": "White pickup truck with a narrow, tall antenna mounted on the far-left side of the vehicle."
  },
  {
    "country": "Kazakhstan (White Truck)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/kaz-car-1.png",
    "clue": "White utility truck with visible front edges that captured the entire country's highway network across the steppe."
  },
  {
    "country": "Ukraine (Red Car)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/ukraine-car-1.png",
    "clue": "Red car body with a long antenna visible panning straight down; key differentiator from Russia."
  },
  {
    "country": "Russia (Black Ghost Car & Long Aerial)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/russian-car-sv.png",
    "clue": "Ghostly black/grey car edges with a long rear aerial/antenna visible when looking downward."
  },
  {
    "country": "Argentina & Uruguay (Black Ghost Car)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/argentina-e1593403227797.png",
    "clue": "Transparent ghostly black front section of the car visible beneath the camera in the flat pampas."
  },
  {
    "country": "Peru, Bolivia & Colombia (White Rear Ghost)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/bol.png",
    "clue": "Floating white rear section of the Street View vehicle visible beneath the camera."
  },
  {
    "country": "Chile (White Vacuum Rear)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/chile-car.png",
    "clue": "Distinctive white rear section resembling a vacuum cleaner body beneath the camera."
  },
  {
    "country": "Ecuador (Short Rear Antenna)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/ecuador.png",
    "clue": "Short stubby antenna visible protruding from beneath the rear of the vehicle."
  },
  {
    "country": "Paraguay (Multi-Shade Truck & Antennas)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/par2-1.png",
    "clue": "White/grey pickup truck body in various shades with mid-section antennas, navigating dry red dirt roads."
  },
  {
    "country": "Namibia (Left-Leaning Antenna)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/nami1.png",
    "clue": "White pickup truck with the antenna always leaning distinctly to the LEFT (even when vehicle is blurred)."
  },
  {
    "country": "Rwanda (Black Google Truck)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rwanda.png",
    "clue": "Black utility truck that captured Rwanda's immaculate highways across the thousand hills."
  },
  {
    "country": "Philippines (White Outline)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/phil-meta.png",
    "clue": "Faint white outline of the car body edges visible when panning straight down."
  },
  {
    "country": "Norway & Denmark (Blue Ghost Car)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/blue-car.png",
    "clue": "Faint, ghostly blue car body visible directly underneath the camera in Scandinavia."
  },
  {
    "country": "Japan & Switzerland (Low Cam)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/japan-low.png",
    "clue": "Low camera positioning (mounted significantly lower on the roof) creating a wider perspective and lower horizon."
  },
  {
    "country": "Bosnia & Herzegovina and Cyprus (Protrusion Blur)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/bos4-1.png",
    "clue": "Non-circular, elongated blur beneath the car featuring an asymmetrical protrusion on one end."
  },
  {
    "country": "Eastern Europe & Israel (Car Aerials)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/aerial-europe.png",
    "clue": "Visible car aerials across Eastern Europe (absent in North Macedonia & Serbia; tape on antenna in CZ, SK, HU, RO, BG)."
  },
  {
    "country": "India & Nepal (Low-Res Shit Cam)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/shcam.png",
    "clue": "Large circular ground blur beneath the vehicle paired with blurry, low-resolution, faint imagery."
  },
  {
    "country": "Alaska, USA (Elevated 2nd Car)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/alaska-2nd-camera.png",
    "clue": "A second Google car with an elevated camera mast is frequently visible down the road in Alaskan coverage."
  }
]

NEW_CARS_FR = [
  {
    "country": "Kenya (Snorkel)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/00-kenya-car-e1564396284275.png",
    "clue": "Snorkel d'admission d'air noir fixé sur le montant avant-droit du véhicule. Signature visuelle quasi-infaillible sur la majorité des routes rurales et nationales."
  },
  {
    "country": "Kenya (Escorte 4x4)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/kenya-escort-car.png",
    "clue": "Véhicule d'escorte 4x4 suivant la Google Car (souvent de 20 à 100 mètres en arrière). Présent le long des axes isolés et réserves."
  },
  {
    "country": "Ghana (Adhésif Noir)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/00000-ghana-e1565162834182.png",
    "clue": "Galerie de toit métallique visible avec ruban adhésif noir épais enroulé autour de la barre avant-droite."
  },
  {
    "country": "Ouganda (Voiture Blanche & Rétroviseurs)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/00000-uganda-e1565162687433.png",
    "clue": "Capot de voiture blanche avec bordures visibles et rétroviseurs noirs proéminents au-dessus d'un sol latéritique rouge vif."
  },
  {
    "country": "Mongolie (Équipement de Camping / Benne)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/geo-mongolia-tent-e1571975220325.png",
    "clue": "Benne de pick-up chargée d'équipement de camping, tentes bâchées et bagages visibles vers l'arrière."
  },
  {
    "country": "Mongolie (Rétroviseurs Rouges)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/geo-mongolia-red-sides-e1571975334741.png",
    "clue": "Variante du véhicule mongol dotée de rétroviseurs latéraux rouges caractéristiques le long des barres de toit."
  },
  {
    "country": "Kirghizistan (Barres de Toit & Rétros)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/kyr.png",
    "clue": "Barres de toit métalliques et rétroviseurs latéraux noir et blanc visibles au milieu de paysages montagneux des Tian Shan."
  },
  {
    "country": "Guatemala (Barres de Toit & Grands Rétros)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/guatemala-car.png",
    "clue": "Barres de galerie de toit bien visibles accompagnées de deux grands rétroviseurs noirs. Unique en Amérique Centrale."
  },
  {
    "country": "Sénégal (Pick-up Blanc)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/senegal2-1.png",
    "clue": "Pick-up blanc à benne ouverte avec barres de toit métalliques, caractéristique de la nouvelle couverture sénégalaise."
  },
  {
    "country": "Sénégal (Pick-up Argenté)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/sen2-1.png",
    "clue": "Camionnette utilitaire argentée avec barres de toit visibles, complétant la flotte de couverture sénégalaise."
  },
  {
    "country": "Sénégal (Déchirures de Ciel)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rifts-senegal.png",
    "clue": "Grandes déchirures verticales dans le ciel ('sky rifts') combinées aux barres de toit de la Google car."
  },
  {
    "country": "Monténégro (Déchirures de Ciel)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rifts-mont.png",
    "clue": "Déchirures géantes dans le ciel visibles sur la quasi-totalité du Monténégro en dehors de l'ovale central de Podgorica."
  },
  {
    "country": "Albanie (Déchirures de Ciel)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rifts-mont-2-1.png",
    "clue": "Déchirures de ciel apparaissant par zones en Albanie, accompagnant les plaques à double bande bleue."
  },
  {
    "country": "Nigeria (Escorte Policière)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/nigeria-car-1.png",
    "clue": "Véhicule d'escorte policier : pick-up gris argenté dans le grand Lagos ; pick-up blanc avec gyrophares hors de Lagos ; 4x4 noir à Benin City."
  },
  {
    "country": "Nigeria (Barres & Flou)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/nigeria-more-1.png",
    "clue": "Véhicule blanc avec barres à motifs noir et jaune sous la caméra ou large flou circulaire."
  },
  {
    "country": "Tunisie (Véhicule d'Escorte Vert)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/tunisia-car.png",
    "clue": "Mazda vert foncé suivant la Google car (avec carte sur le tableau de bord à Sfax/Gabès) ; Toyota vert sombre à Tunis."
  },
  {
    "country": "Curaçao (Arceaux Tubulaires)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/bars-under-car-e1557829019453.png",
    "clue": "Pick-up blanc équipé d'arceaux tubulaires noirs robustes (pare-cabine) derrière l'habitacle."
  },
  {
    "country": "République Dominicaine (Barres à Cales Noires)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/sd.png",
    "clue": "Véhicule allongé doté de barres de toit fixées sur d'épaisses cales en caoutchouc noir aux lignes parallèles."
  },
  {
    "country": "Panama (Arceaux Enveloppants)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/cr-car-image-1.png",
    "clue": "Pick-up blanc doté d'arceaux métalliques enveloppants supplémentaires faisant le tour de la cabine ('Pan' around)."
  },
  {
    "country": "Costa Rica (Pick-up Blanc Sans Arceau)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/cr-car-image-1.png",
    "clue": "Pick-up blanc sans les arceaux enveloppants du Panama, évoluant dans un relief verdoyant et montagneux."
  },
  {
    "country": "Îles Vierges des États-Unis (Pick-up à Benne)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/usvi-car.png",
    "clue": "Pick-up utilitaire à benne arrière avec barres (blanc au nord, rouge/blanc à Ste-Croix) ; conduite à GAUCHE."
  },
  {
    "country": "Bermudes (Buggy Décapotable)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/usvi-car.png",
    "clue": "Buggy électrique décapotable à armature tubulaire ; conduite à GAUCHE le long de ruelles bordées de murets."
  },
  {
    "country": "Sri Lanka (Bandes Tricolores)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/sri-lanka-car.png",
    "clue": "Voiture blanche arborant des bandes bleu-blanc-rouge (façon drapeau tricolore) sur le pare-chocs avant."
  },
  {
    "country": "Jordanie (Voiture Noire)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/jordan-car-black.png",
    "clue": "Carrosserie de voiture noire visible en vue plongeante au cœur de paysages désertiques arides."
  },
  {
    "country": "Émirats Arabes Unis (Voiture Blanche)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/uae-white-car.png",
    "clue": "Voiture ou pick-up blanc visible en regardant vers le bas, circulant sur de larges autoroutes modernes."
  },
  {
    "country": "Oman (Pick-up Blanc & Antenne)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/oman12-1.png",
    "clue": "Pick-up blanc avec barres dans la benne ; l'orientation de l'antenne sert d'indice d'orientation régionale."
  },
  {
    "country": "Qatar (Antenne Déportée à Gauche)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/qatar-car-1.jpg",
    "clue": "Pick-up blanc muni d'une fine antenne verticale déportée tout à gauche du véhicule (contrairement à l'antenne centrale courte du Sénégal)."
  },
  {
    "country": "Kazakhstan (Grand Pick-up Blanc)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/kaz-car-1.png",
    "clue": "Grand pick-up blanc ayant immortalisé l'intégralité du réseau routier national à travers la steppe kazakhe."
  },
  {
    "country": "Ukraine (Voiture Rouge)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/ukraine-car-1.png",
    "clue": "Carrosserie rouge vif avec longue antenne visible vers le bas ; indice décisif face à la Russie."
  },
  {
    "country": "Russie (Voiture Fantôme Noire & Longue Antenne)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/russian-car-sv.png",
    "clue": "Contours de voiture fantôme noire/grise avec longue antenne fouet arrière visible vers le bas."
  },
  {
    "country": "Argentine & Uruguay (Voiture Fantôme Noire)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/argentina-e1593403227797.png",
    "clue": "Section avant fantôme noire semi-transparente visible sous la caméra dans les plaines de la pampa."
  },
  {
    "country": "Pérou, Bolivie & Colombie (Arrière Blanc Flottant)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/bol.png",
    "clue": "Section arrière blanche flottante de la Google car visible sous le véhicule en vue plongeante."
  },
  {
    "country": "Chili (Arrière Blanc Façon Aspirateur)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/chile-car.png",
    "clue": "Arrière de véhicule blanc à la forme arrondie caractéristique rappelant un aspirateur."
  },
  {
    "country": "Équateur (Courte Antenne Arrière)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/ecuador.png",
    "clue": "Courte antenne tronquée visible dépassant sous l'arrière de la voiture."
  },
  {
    "country": "Paraguay (Pick-up Multicolore & Antennes)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/par2-1.png",
    "clue": "Pick-up aux teintes blanches ou dégradées avec antennes médianes, circulant sur une terre rouge sèche."
  },
  {
    "country": "Namibie (Antenne Penchée à Gauche)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/nami1.png",
    "clue": "Pick-up blanc dont l'antenne penche systématiquement vers la GAUCHE (antenne penchée visible même sous le flou)."
  },
  {
    "country": "Rwanda (Pick-up Noir)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/rwanda.png",
    "clue": "Camionnette utilitaire noire ayant capturé les routes entretenues du pays aux mille collines."
  },
  {
    "country": "Philippines (Contour Blanc)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/phil-meta.png",
    "clue": "Léger contour blanc des bordures de la carrosserie visible en regardant directement au sol."
  },
  {
    "country": "Norvège & Danemark (Voiture Bleue Fantôme)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/blue-car.png",
    "clue": "Silhouette de voiture bleutée semi-transparente visible directement sous le point de vue en Scandinavie."
  },
  {
    "country": "Japon & Suisse (Low Cam)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/japan-low.png",
    "clue": "Caméra en position basse ('Low Cam') montée plus près du toit, conférant un horizon plus bas et une perspective plus large."
  },
  {
    "country": "Bosnie-Herzégovine & Chypre (Flou à Protubérance)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/bos4-1.png",
    "clue": "Flou sous le véhicule non circulaire et allongé, présentant une protubérance asymétrique à une extrémité."
  },
  {
    "country": "Europe de l'Est & Israël (Antennes de Toit)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/aerial-europe.png",
    "clue": "Antennes de toit visibles en Europe de l'Est (absentes en Macédoine du Nord et Serbie ; adhésif sur antenne en CZ, SK, HU, RO, BG)."
  },
  {
    "country": "Inde & Népal (Flou Circulaire Dégradé)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/shcam.png",
    "clue": "Flou circulaire massif sous le véhicule combiné à une qualité d'image très dégradée et voilée ('shit cam')."
  },
  {
    "country": "Alaska, USA (Seconde Voiture à Caméra Haute)",
    "image": "https://somerandomstuff1.wordpress.com/wp-content/uploads/2019/02/alaska-2nd-camera.png",
    "clue": "Une seconde voiture Google surmontée d'un mât de caméra surélevé est souvent visible au loin sur les routes d'Alaska."
  }
]

# Update META_DATA in code
meta_match = re.search(r'const META_DATA = (\{.*?\});\s*\n\s*const PLATES_DATA', code, re.DOTALL)
if meta_match:
    meta_obj = json.loads(meta_match.group(1))
    meta_obj['en']['car_meta'] = NEW_CARS_EN
    meta_obj['fr']['car_meta'] = NEW_CARS_FR
    new_meta_json = json.dumps(meta_obj, ensure_ascii=False, indent=2)
    code = code[:meta_match.start()] + f"const META_DATA = {new_meta_json};\n\nconst PLATES_DATA" + code[meta_match.end():]
    print(f"Updated META_DATA with {len(NEW_CARS_EN)} cars.")
else:
    print("ERROR: Could not find META_DATA regex match")
    exit(1)

# --------------------------------------------------------------------------
# 3. ACCURATE GIVEAWAYS FOR ALL 68 COUNTRIES (replacing generic fallback)
# --------------------------------------------------------------------------
GIVEAWAYS_DICT = {
  "puerto-rico": {
    "en": "US road signage and highway shields (PR-xxx); white and yellow road lines; Spanish language; tropical Caribbean vegetation.",
    "fr": "Signalisation et shields routiers américains (PR-xxx); lignes blanches et jaunes; langue espagnole; végétation caribéenne tropicale."
  },
  "the-dominican-republic": {
    "en": "Roof rack bars mounted on thick black rubber pads; Spanish language; lush Caribbean island vegetation; extra-long car body.",
    "fr": "Barres de toit fixées sur d'épaisses cales en caoutchouc noir; langue espagnole; végétation caribéenne; carrosserie très allongée."
  },
  "costa-rica": {
    "en": "White pickup truck with NO extra wrap-around bars; dense lush green mountainous topography; Spanish language; .cr domain.",
    "fr": "Pick-up blanc SANS arceaux enveloppants; relief montagneux verdoyant et luxuriant; espagnol; domaine .cr."
  },
  "us-virgin-islands": {
    "en": "Drives on the LEFT (only US jurisdiction); American road signs and speed limits in mph; pickup truck with rear bed bars.",
    "fr": "Conduite à GAUCHE (seul territoire américain); panneaux de signalisation US et vitesses en mph; pick-up à arceaux."
  },
  "panama": {
    "en": "White truck with wrap-around bars circling the cab; unique antenna; taxis starting with provincial numbers (8=Panama, 13=Panama Oeste).",
    "fr": "Pick-up blanc avec arceaux enveloppants ('Pan' around); antenne unique; taxis débutant par le code province (8=Panama, 13=Panama Ouest)."
  },
  "the-isle-of-man": {
    "en": "Drives on the LEFT; yellow rear plates with red/white Manx triskelion flag; Gen 2 camera; round white-bordered signs.",
    "fr": "Conduite à GAUCHE; plaques arrière jaunes à triskèle rouge/blanc; caméra Gen 2; panneaux ronds bordés de blanc."
  },
  "jersey": {
    "en": "Drives on the LEFT; white front and yellow rear plates with 'J' prefix; English/French bilingual street names; Gen 2 camera.",
    "fr": "Conduite à GAUCHE; plaques jaunes arrière débutant par 'J'; toponymie anglo-normande; caméra Gen 2."
  },
  "the-canary-islands": {
    "en": "Spanish signage and Carretera General numbers; dramatic dark volcanic soil and subtropical flora; EU plates with 'E'.",
    "fr": "Signalisation espagnole et routes Carretera General; sol volcanique sombre et flore subtropicale; plaques UE 'E'."
  },
  "andorra": {
    "en": "Dramatic Pyrenean mountain topography; grey stone houses; white license plates with red vertical stripe and coat of arms; Catalan.",
    "fr": "Topographie alpine pyrénéenne; maisons en pierre grise; plaques blanches à bande rouge et écusson; langue catalane."
  },
  "gibraltar": {
    "en": "Drives on the RIGHT; UK-style yellow rear plates starting with 'G'; dramatic limestone Rock of Gibraltar cliffs; English.",
    "fr": "Conduite à DROITE; plaques arrière jaunes de style britannique débutant par 'G'; falaise calcaire du Rocher; anglais."
  },
  "belgium": {
    "en": "License plates with distinctive RED font on white background; unpainted concrete utility poles; yellow-backed motorway signs.",
    "fr": "Plaques à caractères ROUGES sur fond blanc; poteaux en béton brut non peints; panneaux d'autoroute sur fond jaune."
  },
  "the-netherlands": {
    "en": "100% yellow license plates front and rear; reddish-brown brick paving, dedicated red bike lanes; blue directional signs in lowercase.",
    "fr": "Plaques 100% jaunes à l'avant et à l'arrière; briques rouge-brun omniprésentes; pistes cyclables rouges; panneaux bleus en minuscules."
  },
  "luxembourg": {
    "en": "100% yellow license plates front and rear; pristine road infrastructure; yellow bollards with reflectors; multilingual signs.",
    "fr": "Plaques 100% jaunes avant et arrière; infrastructure routière impeccable; bollards jaunes à réflecteurs; trilinguisme."
  },
  "san-marino": {
    "en": "Short front license plates with light blue coat of arms; Mount Titano fortress cliff backdrop; Gen 2 camera; Italian language.",
    "fr": "Plaques avant courtes avec écusson bleu ciel; forteresse du Mont Titano; caméra Gen 2; langue italienne."
  },
  "svalbard": {
    "en": "Arctic snowmobile and scooter trekker coverage; treeless snow-covered tundra, wooden mining houses; polar bear signs.",
    "fr": "Couverture en motoneige/scooter sur neige; toundra arctique sans arbre; maisons minières en bois; panneaux ours polaires."
  },
  "the-faroe-islands": {
    "en": "4 bars visible on the car; steep basalt cliffs, treeless grass-roofed houses; sheep view; Danish/Faroese signs.",
    "fr": "4 barres de toit visibles; falaises de basalte spectaculaires; maisons aux toits en herbe sans arbre; panneaux en féroïen."
  },
  "greenland": {
    "en": "Arctic dirt roads with no connected highway network; colorful Scandinavian wooden houses on rocky ground; ATV/trekker coverage.",
    "fr": "Pistes de terre arctiques isolées; maisons scandinaves colorées en bois sur roche; couverture en quad et trekker."
  },
  "liechtenstein": {
    "en": "Black license plates with princely crown and 'FL' prefix; low-mounted camera; flat alpine Rhine valley with tall mountains; Swiss signs.",
    "fr": "Plaques noires à couronne princière et préfixe 'FL'; caméra basse (Low Cam); vallée alpine du Rhin; signalisation tubulaire suisse."
  },
  "lithuania": {
    "en": "Triangular warning signs with white background and bold red border; concrete utility poles with diagonal struts; Lithuanian diacritics.",
    "fr": "Panneaux de danger triangulaires à fond blanc et bord rouge vif; poteaux en béton à jambe de force; diacritiques lituaniens (ė, ū, ž)."
  },
  "latvia": {
    "en": "White delineator posts with red rectangular reflectors; extensive gravel road network; Latvian macrons and diacritics (ā, ē, ī, ū, ģ, ķ).",
    "fr": "Bollards blancs à réflecteur rectangulaire rouge; réseau étendu de pistes de gravier; macrons et lettres lettones (ā, ē, ī, ū, ģ, ķ)."
  },
  "estonia": {
    "en": "Distinctive wooden timber houses; utility poles with crossarms and stay wires; .ee domains; Estonian vowel 'õ' and double vowels.",
    "fr": "Maisons traditionnelles en bois; poteaux électriques à traverses; domaine .ee; voyelle estonienne 'õ' et voyelles doublées."
  },
  "czechia": {
    "en": "Delineator posts emerging from a black base with two orange reflectors; blue highway signs with white text; Czech letter 'ř'.",
    "fr": "Bollards blancs émergeant d'un socle noir à pastilles orange; panneaux autoroutiers bleus; lettre tchèque 'ř'."
  },
  "slovakia": {
    "en": "Delineator posts with black base; Slovak double-cross coat of arms on license plates; Slovak letters 'ô' and 'ä'.",
    "fr": "Bollards à socle noir; double croix slovaque sur les plaques; lettres slovaques spécifiques 'ô' et 'ä'."
  },
  "slovenia": {
    "en": "Alpine topography; European plates with green provincial border; Slovenian language suffixes (-ski, -ska); pristine infrastructure.",
    "fr": "Topographie alpine; plaques UE à liseré vert provincial; langue slovène (-ski, -ska); infrastructure centre-européenne soignée."
  },
  "hungary": {
    "en": "Concrete utility poles with clusters of round holes (gruyère); green border highway signs; Hungarian language with double accents (ő, ű).",
    "fr": "Poteaux en béton perforés de grappes de trous (gruyère); panneaux autoroutiers à bord vert; langue hongroise (ő, ű)."
  },
  "croatia": {
    "en": "Croatian red-white checkerboard shield; Mediterranean coastline; bilingual Italian in Istria; Cyrillic absent except near Serbian border.",
    "fr": "Écusson à damier rouge et blanc; littoral adriatique méditerranéen; bilinguisme italien en Istrie; absence de cyrillique."
  },
  "bosnia-and-herzegovina": {
    "en": "Distinctive asymmetrical elongated blur beneath the vehicle with an end protrusion; Cyrillic/Latin bilingual road signs; Yugoslav concrete poles.",
    "fr": "Flou allongé asymétrique à protubérance sous le véhicule; panneaux bilingues cyrillique/latin; poteaux yougoslaves en béton."
  },
  "albania": {
    "en": "Double blue strips on license plates; sky rifts in scattered regions; red and black double-headed eagle flag; Albanian letter 'ë'.",
    "fr": "Plaques à double bande bleue; déchirures de ciel par zones; aigle bicéphale rouge et noir; lettre albanaise 'ë'."
  },
  "cyprus": {
    "en": "Drives on the LEFT; yellow rear license plates; Greek/Turkish bilingual signage; asymmetrical elongated car blur beneath.",
    "fr": "Conduite à GAUCHE; plaques arrière jaunes; signalisation bilingue grec/turc; flou allongé asymétrique à protubérance sous la voiture."
  },
  "romania": {
    "en": "Concrete utility poles with perforated holes and painted white bases; yellow diamond priority road signs; Romanian letters (ș, ț, ă, î, â).",
    "fr": "Poteaux en béton à trous et base peinte en blanc; losanges jaunes de priorité; lettres roumaines spécifiques (ș, ț, ă, î, â)."
  },
  "montenegro": {
    "en": "Giant rifts across the sky outside the central oval; European plates with Montenegro coat of arms; dramatic karst limestone canyons.",
    "fr": "Déchirures géantes dans le ciel en dehors de l'ovale central; plaques UE avec écusson monténégrin; canyons calcaires karstiques."
  },
  "serbia": {
    "en": "Cyrillic and Latin bilingual blue highway signs; NO aerial on the Google car; Serbian dinar currency; Yugoslav-style wooden poles.",
    "fr": "Panneaux autoroutiers bleus bilingues cyrillique/latin; AUCUNE antenne sur la Google car; poteaux yougoslaves en bois."
  },
  "north-macedonia": {
    "en": "Cyrillic road signs; NO aerial on the Google car; Macedonian letters (Ѓ, Ќ, Ѕ, Џ); mountainous Balkan topography.",
    "fr": "Panneaux en cyrillique macédonien; AUCUNE antenne sur la Google car; lettres macédoniennes (Ѓ, Ќ, Ѕ, Џ); relief balkanique."
  },
  "bulgaria": {
    "en": "Cyrillic-only signage with letter 'Ъ'; tape on the Google car antenna; EU plates with BG code; winter/autumn coverage.",
    "fr": "Signalisation 100% cyrillique avec lettre 'Ъ'; adhésif sur l'antenne Google car; plaques UE code 'BG'; couverture automnale/hivernale."
  },
  "the-russian-landscape": {
    "en": "Black ghost car with long rear aerial; immense birch forests (taiga/steppes); white and blue regional plates; Cyrillic without Ukrainian letters.",
    "fr": "Voiture fantôme noire à longue antenne fouet; immenses forêts de bouleaux (taïga/steppes); codes régions sur plaques; cyrillique sans lettres ukrainiennes."
  },
  "malta": {
    "en": "Drives on the LEFT; distinctive yellow-limestone architecture; British-style red phone boxes and letter boxes; Maltese language (ħ, ċ, ż, ġ).",
    "fr": "Conduite à GAUCHE; architecture en calcaire jaune; cabines téléphoniques britanniques rouges; langue maltaise (ħ, ċ, ż, ġ)."
  },
  "american-samoa": {
    "en": "Drives on the RIGHT; US road signs; tropical South Pacific island; pickup truck with rear bed in lush volcanic mountains.",
    "fr": "Conduite à DROITE; signalisation routière américaine; île tropicale du Pacifique Sud; pick-up à benne dans un relief volcanique luxuriant."
  },
  "northern-mariana-islands": {
    "en": "US-style infrastructure and speed limit signs; tropical Pacific flora; Guam/CNMI distinctive concrete utility poles.",
    "fr": "Infrastructures américaines et panneaux en miles; flore tropicale du Pacifique; poteaux électriques massifs en béton armé."
  },
  "guam": {
    "en": "US-style road signs and route shields (Guam 1, 2, 4); distinctive thick concrete utility poles with transformer platforms; tropical flora.",
    "fr": "Signalisation américaine et shields 'Guam Route'; poteaux électriques massifs en béton à plateformes de transformateur; tropiques."
  },
  "midway-atoll": {
    "en": "Remote Pacific coral atoll; millions of Laysan albatross birds ('gooney birds'); runway and WWII historical military installations.",
    "fr": "Atoll corallien isolé du Pacifique; millions d'albatros de Laysan ('gooney birds'); piste d'atterrissage et vestiges militaires de la Seconde Guerre."
  },
  "christmas-island": {
    "en": "Australian territory; Indian Ocean flora; red land crab warning signs and migration bridges; Australian-style road markings.",
    "fr": "Territoire australien; flore de l'Océan Indien; panneaux de passage de crabes rouges et ponts de migration; marquages australiens."
  },
  "namibia": {
    "en": "White pickup truck with antenna leaning to the LEFT; all-yellow license plates; red Kalahari sand; drives on the LEFT.",
    "fr": "Pick-up blanc à antenne penchant systématiquement à GAUCHE; plaques 100% jaunes; sable rouge du Kalahari; conduite à GAUCHE."
  },
  "rwanda": {
    "en": "Black Google pickup truck; pristine clean paved roads; lush terraced green hills ('Land of a Thousand Hills'); French/Kinyarwanda signs.",
    "fr": "Pick-up noir Google; routes bitumées impeccablement entretenues; collines verdoyantes en terrasses; signalisation kinyarwanda/français."
  },
  "tunisia": {
    "en": "Dark green Mazda following escort vehicle (with map on dashboard in Sfax/Gabes); black license plates with Arabic script; Maghreb architecture.",
    "fr": "Mazda vert foncé d'escorte (avec carte sur le tableau de bord à Sfax/Gabès); plaques d'immatriculation noires à lettrage arabe; architecture maghrébine."
  },
  "madagascar": {
    "en": "Google trekker backpack coverage; baobab trees and reddish laterite dirt; French/Malagasy language; unique zebu cattle.",
    "fr": "Couverture pédestre au sac à dos Trekker; allées de baobabs et terre rouge latéritique; bilinguisme français/malgache; zébus."
  },
  "sao-tome-and-principe": {
    "en": "Heavy circular camera blur beneath; equatorial lush tropical island off Gabon; dim/faded lighting on Príncipe; Portuguese signs.",
    "fr": "Flou circulaire massif sous le véhicule; île tropicale équatoriale luxuriante au large du Gabon; lumière tamisée à Príncipe; portugais."
  },
  "bhutan": {
    "en": "Crimson-red license plates with white Dzongkha script; traditional painted wooden Dzong architecture; Himalayan mountains.",
    "fr": "Plaques rouge bordeaux à écriture dzongkha blanche; architecture traditionnelle des Dzongs en bois sculpté; relief himalayen."
  },
  "hong-kong": {
    "en": "Drives on the LEFT; British-style yellow rear plates; bilingual English and Traditional Chinese signs; double-decker buses.",
    "fr": "Conduite à GAUCHE; plaques arrière jaunes britanniques; signalisation bilingue anglais et chinois traditionnel; bus à impériale."
  },
  "macau": {
    "en": "Drives on the LEFT; Portuguese and Traditional Chinese bilingual street tiles (azulejos); Gen 2 camera; black license plates.",
    "fr": "Conduite à GAUCHE; plaques de rues en céramique (azulejos) bilingues portugais/chinois traditionnel; caméra Gen 2; plaques noires."
  },
  "the-united-arab-emirates": {
    "en": "White Google car in desert terrain; modern multi-lane superhighways with tall lighting poles; Arabic and English signs.",
    "fr": "Voiture blanche Google en milieu désertique; autoroutes modernes éclairées par de hauts candélabres; signalisation arabe et anglaise."
  },
  "qatar": {
    "en": "White pickup truck with narrow antenna on the far-left; desert terrain with modern Gulf skyscrapers; Arabic and English signs.",
    "fr": "Pick-up blanc muni d'une fine antenne verticale déportée tout à gauche; gratte-ciels du Golfe et désert; bilinguisme arabe/anglais."
  },
  "oman": {
    "en": "White pickup truck with rear bed bars and antenna; Arabic and English signs with green highway markers; rocky desert mountains.",
    "fr": "Pick-up blanc avec barres dans la benne et antenne; panneaux autoroutiers verts bilingues arabe/anglais; montagnes désertiques rocheuses."
  },
  "palestine": {
    "en": "Yellow plates on Israeli vehicles vs white/green plates on Palestinian vehicles; Arabic and Hebrew signs; West Bank hilly terrain.",
    "fr": "Plaques jaunes sur véhicules israéliens vs plaques blanches/vertes palestiniennes; bilinguisme arabe/hébreu; relief cisjordanien."
  },
  "lebanon": {
    "en": "Mediterranean coastline and Mount Lebanon; French and Arabic bilingual signs; cedar tree national symbols.",
    "fr": "Littoral méditerranéen et Mont Liban; signalisation bilingue arabe et français; symbole national du cèdre."
  },
  "kyrgyzstan": {
    "en": "Roof rack bars with black/white mirrors; white license plates with red vertical strip on left; dramatic snow-capped Tian Shan mountains.",
    "fr": "Barres de toit avec rétroviseurs noir et blanc; plaques blanches à bandelette rouge verticale à gauche; massifs enneigés des Tian Shan."
  },
  "kazakhstan": {
    "en": "White truck that captured the entire country; vast flat Eurasian steppe; blue flag with sun and eagle; Cyrillic with Kazakh letters.",
    "fr": "Grand pick-up blanc ayant capturé le pays; steppe eurasienne plate à perte de vue; cyrillique à lettres kazakhes (Ә, Ғ, Қ, Ң, Ө, Ұ, Ү, Һ, І)."
  },
  "vietnam": {
    "en": "Drives on the RIGHT; motorbike-filled roads; Vietnamese language with heavy tone diacritics; red flag with yellow star.",
    "fr": "Conduite à DROITE; nuée de deux-roues en ville; langue vietnamienne aux accents tonals prononcés; drapeau rouge à étoile dorée."
  },
  "laos": {
    "en": "White truck with metal bars and side mirrors; French and Lao script; Buddhist temples; drives on the RIGHT (contrasting Thailand).",
    "fr": "Camionnette blanche à barres métalliques et rétroviseurs visibles; écritures laotienne et française; conduite à DROITE (contrairement à la Thaïlande)."
  },
  "the-philippines": {
    "en": "White outline of the Google car edge visible panning down; English-language road signs; jeepneys and tricycles; tropical foliage.",
    "fr": "Léger contour blanc des bordures de la voiture au sol; signalisation routière en anglais; jeepneys et tricycles; climat tropical."
  },
  "bangladesh": {
    "en": "Red and green tape/bars on roof rack; Bengali script; dense traffic with auto-rickshaws; flat green delta terrain; drives on the LEFT.",
    "fr": "Barres de toit avec ruban vert et rouge; écriture bengalie; circulation dense de rickshaws; delta verdoyant; conduite à GAUCHE."
  },
  "nepal": {
    "en": "Low-res circular blur ('shit cam'); Devanagari script; Himalayan mountain backdrop; drives on the LEFT.",
    "fr": "Flou circulaire au sol basse résolution ('shit cam'); écriture devanagari; contreforts himalayens; conduite à GAUCHE."
  },
  "india": {
    "en": "Low-res circular blur ('shit cam') in older coverage, or white car with roof rack in Gen 4; Devanagari and regional scripts; drives on the LEFT.",
    "fr": "Flou circulaire au sol ('shit cam') ou voiture blanche à galerie en Gen 4; écritures devanagari et régionales; conduite à GAUCHE."
  },
  "pakistan": {
    "en": "Google trekker coverage of monuments and parks; Urdu script and English signs; drives on the LEFT.",
    "fr": "Couverture piétonne Trekker sur sites historiques et parcs; écriture ourdoue et anglais; conduite à GAUCHE."
  },
  "singapore": {
    "en": "Drives on the LEFT; ultra-modern, impeccably clean city-state; English primary language; black road signs with white text; green street-side foliage.",
    "fr": "Conduite à GAUCHE; cité-État ultra-moderne et immaculée; langue anglaise dominante; panneaux de rues noirs à écriture blanche."
  },
  "how-to-identify-the-regions-of-brazil": {
    "en": "Deep purple/red soil (terra roxa) in Paraná and São Paulo; dry caatinga scrubland in the Northeast; pampas grasslands in the South.",
    "fr": "Terre rouge/pourpre (terra roxa) dans le Paraná et São Paulo; végétation aride de caatinga dans le Nordeste; pampa herbeuse au Sud."
  },
  "paraguay": {
    "en": "White/grey multi-shade pickup truck with mid-section antennas; dry red soil even in urban streets; mosaic cobblestone paving near Argentina.",
    "fr": "Pick-up blanc/gris aux teintes variées à antennes médianes; sol rouge sec omniprésent en ville; pavés en mosaïque près de l'Argentine."
  },
  "uruguay": {
    "en": "Black ghost car visible panning down; extremely flat cattle pasture plains (pampas); Spanish language; wooden fence posts with wire.",
    "fr": "Voiture fantôme noire en vue plongeante; vastes plaines plates d'élevage (pampa); espagnol; piquets de clôture en bois et barbelés."
  },
  "ecuador": {
    "en": "Short antenna visible on the rear of the car; mountainous Andean spine (Sierra) vs coastal plains; chevron signs with black arrows on yellow.",
    "fr": "Courte antenne tronquée à l'arrière de la voiture; chaîne des Andes (Sierra) vs plaines côtières; chevrons noirs sur fond jaune."
  }
}

# --------------------------------------------------------------------------
# 4. PARAGRAPHS FOR THE 6 ZERO-PARAGRAPH COUNTRIES
# --------------------------------------------------------------------------
EXTRA_PARAGRAPHS = {
  "panama": {
    "fr": [
      "Le Panama se distingue immédiatement par son véhicule Street View exclusif : un pick-up blanc équipé d'arceaux tubulaires enveloppants supplémentaires faisant tout le tour de l'habitacle ('Pan' around), ainsi qu'une antenne au profil unique au monde.",
      "La couverture officielle est fortement concentrée autour de la capitale Panama City et de l'axe urbain Panama Ouest. Les taxis offrent une opportunité de region-guessing chirurgicale : chaque plaque de taxi débute par le numéro alphabétique de sa province (le 8 désigne la province de Panama, le 13 Panama Ouest).",
      "La végétation est tropicale luxuriante, le relief vallonné avec des autoroutes bétonnées ou bitumées de bonne facture. La conduite s'effectue à droite avec une signalisation en espagnol et des plaques jaunes sur les transports publics."
    ],
    "en": [
      "Panama is instantly recognized by its unique Google vehicle: a white pickup truck fitted with distinct wrap-around roll bars circling the cab ('Pan' around) and a unique antenna found nowhere else on Earth.",
      "Street View coverage is heavily concentrated around Panama City and the urban corridor of Panama Oeste. Taxis provide surgical region-guessing capability: taxi license plates begin with provincial numbers in alphabetical order (number 8 indicates Panama Province, number 13 indicates Panama Oeste).",
      "Landscape features lush tropical greenery, rolling hills, modern multi-lane concrete highways, right-hand traffic, Spanish signage, and yellow license plates on commercial and public transport vehicles."
    ]
  },
  "bosnia-and-herzegovina": {
    "fr": [
      "La Bosnie-Herzégovine se reconnaît au premier coup d'œil par le flou sous la caméra : un flou allongé non circulaire présentant une protubérance asymétrique sur l'une de ses extrémités (partagé uniquement avec Chypre en Europe).",
      "La signalisation routière est bilingue : elle associe l'alphabet latin et l'alphabet cyrillique serbe (avec les noms de villes en cyrillique souvent tagués ou rayés selon les entités : Fédération de Bosnie-et-Herzégovine vs République serbe de Bosnie).",
      "Le paysage est spectaculaire, dominé par les Alpes dinariques avec de profondes vallées calcaires, des toitures de maisons à double pente raide en tuiles ou bardeaux, et des poteaux électriques en bois de style yougoslave."
    ],
    "en": [
      "Bosnia and Herzegovina is immediately identified by the unique ground blur beneath the vehicle: an elongated, non-circular blur with a distinctive asymmetrical protrusion at one end (shared only with Cyprus in Europe).",
      "Road signage is strictly bilingual, combining the Latin and Serbian Cyrillic alphabets (town names in Cyrillic or Latin are frequently spray-painted or crossed out depending on the entity: Federation of Bosnia and Herzegovina vs Republika Srpska).",
      "Landscape is dominated by the dramatic Dinaric Alps, steep limestone river canyons, pitched tiled-roof Alpine houses, and traditional Yugoslav-style wooden utility poles."
    ]
  },
  "cyprus": {
    "fr": [
      "Chypre est l'un des très rares territoires en Europe où la conduite s'effectue obligatoirement à GAUCHE (avec le Royaume-Uni, l'Irlande et Malte). Les véhicules arborent des plaques blanches à l'avant et jaunes à l'arrière.",
      "En vue plongeante vers le sol, on retrouve le même flou allongé asymétrique à protubérance qu'en Bosnie-Herzégovine, parfois surmonté d'une antenne courte et trapue à l'arrière.",
      "La signalisation est bilingue grec et anglais (parfois turc dans le nord de Nicosie). L'ensemble de la couverture officielle se situe à Nicosie et dans la partie sud de l'île sous contrôle de la République de Chypre."
    ],
    "en": [
      "Cyprus is one of the very few territories in Europe where traffic drives on the LEFT (alongside the UK, Ireland, and Malta). Vehicles feature white front plates and yellow rear plates.",
      "Panning straight down reveals the same distinctive elongated asymmetrical blur with a protrusion found in Bosnia, occasionally with a short stubby antenna at the rear of the car.",
      "Signage is bilingual Greek and English. All official Google coverage is located strictly within Nicosia and the southern, internationally recognized Republic of Cyprus."
    ]
  },
  "namibia": {
    "fr": [
      "La Namibie se repère infailliblement par son pick-up blanc dont l'antenne penche systématiquement vers la GAUCHE. Même sur la moitié de la couverture où le véhicule est flouté, l'antenne penchée à gauche reste bien visible flottant au-dessus du flou.",
      "La conduite s'effectue à GAUCHE et les véhicules sont dotés de plaques d'immatriculation allongées entièrement jaunes à l'avant comme à l'arrière (cas unique en Afrique australe où les pays voisins ont des plaques blanches).",
      "Le paysage est grandiose et aride : immenses étendues désertiques du Namib et du Kalahari, pistes de gravier blanc ou ocre parfaites (routes préfixées 'B' bitumées et 'C' ou 'D' en gravier damé), dunes de sable rouge et clôtures d'élevage."
    ],
    "en": [
      "Namibia is infallibly identified by its white blocky pickup truck whose antenna always leans distinctly to the LEFT. Even across the half of coverage where the car body is blurred out, the left-leaning antenna remains clearly visible floating above the blur.",
      "Traffic drives on the LEFT and vehicles feature elongated all-yellow license plates front and rear (unique in Southern Africa where neighboring nations use white plates)."
      "Landscape is uniquely arid and vast: sweeping Kalahari and Namib desert plains, immaculate wide gravel and salt highways (B-prefix paved corridors, C and D-prefix compacted gravel), red sand dunes, and game-fenced ranches."
    ]
  },
  "paraguay": {
    "fr": [
      "Le Paraguay a été intégralement capturé avec un pick-up spécifique visible sous différentes nuances de blanc et de gris, souvent équipé d'une ou deux antennes médianes, ce qui permet de le distinguer à coup sûr du Brésil voisin.",
      "Le sol du pays est composé d'une terre rouge très fine et sèche, omniprésente jusque dans les allées et rues urbaines de la capitale Asunción. Si une route sud-américaine est recouverte de terre rouge sans végétation amazonienne dense, pensez Paraguay.",
      "Dans l'est du pays (notamment vers la frontière argentine de Misiones), les chaussées urbaines et rurales sont fréquemment pavées de motifs en mosaïque de galets arrondis tout à fait uniques."
    ],
    "en": [
      "Paraguay's entire coverage was captured with a distinctive pickup truck visible beneath the camera in various shades of white and grey, often bearing mid-section antennas—a definitive giveaway against neighboring Brazil.",
      "The country is characterized by dry, fine, reddish soil that is ubiquitous even in urban side streets of Asunción. An unpaved South American road with prominent red dust and flat terrain strongly indicates Paraguay.",
      "In eastern border towns near Argentina's Misiones Province, roads are uniquely paved with decorative cobblestone and pebble mosaic paving."
    ]
  },
  "sao-tome-and-principe": {
    "fr": [
      "Sao Tomé-et-Principe se reconnaît immédiatement par son flou circulaire gigantesque sous la caméra recouvrant tout le bas de l'écran, similaire à la couverture de l'Inde ou du Népal.",
      "L'environnement est typiquement insulaire équatorial au large du Gabon : jungle verdoyante hyper dense, bananiers, palmiers et architecture coloniale portugaise peinte aux couleurs pastel.",
      "L'éclairage est un marqueur régional : sur l'île septentrionale de Príncipe, la luminosité est souvent tamisée, sombre et très contrastée par rapport à l'île principale de Sao Tomé."
    ],
    "en": [
      "Sao Tome and Principe is instantly distinguished by the massive circular ground blur beneath the camera covering the lower viewport, similar to older Indian or Nepalese trekker coverage.",
      "Environment is intensely lush equatorial island terrain in the Gulf of Guinea off Gabon: dense tropical rainforest, banana groves, palm plantations, and Portuguese colonial pastel-painted architecture.",
      "Atmospheric lighting is a key regional clue: the northern island of Príncipe typically features dim, heavily saturated, overcast coverage compared to the brighter main island of São Tomé."
    ]
  }
}

# --------------------------------------------------------------------------
# 5. PARSE COUNTRIES_DATA AND APPLY ENRICHMENTS
# --------------------------------------------------------------------------
countries_match = re.search(r'const COUNTRIES_DATA = (\[.*?\]);\s*\n\s*const MODES_DATA', code, re.DOTALL)
if not countries_match:
    print("ERROR: Could not find COUNTRIES_DATA match")
    exit(1)

countries = json.loads(countries_match.group(1))
print(f"Loaded {len(countries)} countries from code.")

updated_giveaways = 0
updated_paragraphs = 0

for c in countries:
    cid = c['id']
    
    # Apply authentic giveaway if in GIVEAWAYS_DICT
    if cid in GIVEAWAYS_DICT:
        c['giveaway'] = GIVEAWAYS_DICT[cid]
        updated_giveaways += 1
    
    # Inject paragraphs if in EXTRA_PARAGRAPHS
    if cid in EXTRA_PARAGRAPHS:
        c['paragraphs'] = EXTRA_PARAGRAPHS[cid]
        updated_paragraphs += 1

print(f"Updated giveaways for {updated_giveaways} countries.")
print(f"Injected detailed paragraphs for {updated_paragraphs} countries.")

new_countries_json = json.dumps(countries, ensure_ascii=False, indent=2)
code = code[:countries_match.start()] + f"const COUNTRIES_DATA = {new_countries_json};\n\nconst MODES_DATA" + code[countries_match.end():]

# Write updated data.js
with open('data.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("data.js successfully written with expanded cars and accurate giveaways!")
