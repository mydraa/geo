# 🧭 GeoMaster — Plateforme d'Intelligence GeoGuessr & Atlas Visuel Compétitif

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmydraa%2Fgeo)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Coverage](https://img.shields.io/badge/countries-122%2F122-emerald.svg)
![Languages](https://img.shields.io/badge/languages-FR%20%7C%20EN-purple.svg)

**GeoMaster** est une plateforme de renseignement tactique pour joueurs GeoGuessr de haut niveau. Conçue pour remplacer les guides verbeux par un playbook compétitif, ultra-rapide et richement illustré, elle préserve **100% des faits et astuces techniques** tout en éliminant toute digression inutile.

---

## ⚡ Fonctionnalités Clés

- 🌍 **122 Fiches Pays Détaillées** : Tous les pays officiellement couverts par Google Street View analysés sous l'angle tactique (végétation, sols, toitures, panneaux, marquages, métas).
- 📸 **2 300+ Photographies Authentiques** : Chaque pays dispose d'une photo d'en-tête et d'une galerie complète. Zoom plein écran via visionneuse Lightbox haute définition.
- 🌐 **Bilinguisme Intégral Instantané (FR 🇫🇷 / EN 🇬🇧)** :
  - Traduction à la volée sans aucun rechargement de page.
  - 388 paragraphes de dossiers traduits chirurgicalement en français et en anglais.
  - Moteur de recherche universel bilingue et persistance dans `localStorage`.
- ⚡ **Matrice d'Indices Interactive (Meta Guesser)** : Cochez les éléments visibles sur votre écran (sens de conduite, style de plaque, méta car, poteaux, délinéateurs) pour isoler le pays candidat en temps réel.
- 🛑 **Guide des 31 Balises & Bollards** : Réflecteurs, formes et délinéateurs mondiaux avec photographies réelles.
- 🚗 **Générations de Caméras & 17 Méta Cars** : Comparatif Gen 1 à Gen 4, cartes de déploiement et signatures véhicules (snorkel du Kenya, scotch du Ghana, déchirures du Sénégal, escorte policière du Nigeria, barres de Curaçao, etc.).
- 🚙 **Législation Mondiale des Plaques** : Cartes des 19 États US et des provinces canadiennes sans plaque avant (pour les *State Streaks*), plaques européennes, formats Mercosur et particularités mondiales.
- 🛣️ **Réseaux Routiers & Grids** : Logique mathématique des Interstates (paires/impaires/boucles à 3 chiffres), réseau BR brésilien, corridors E-Roads.
- 🔤 **Comparateur d'Alphabets** : Cyrillique exclusif (Ukraine vs Russie vs Biélorussie vs Serbie), voyelles nordiques (æ/ø vs ä/ö) et calligraphies d'Asie.
- 🎮 **Modes de Jeu & Duels** : Stratégies de gestion des 6 000 PV, Battle Royale et Maprunner.
- ☀️ **Fondamentaux Solaires** : Azimut, projection des ombres, inclinaison des paraboles satellites et boussole.
- 🎯 **Arène de Quiz Compétitif** : 15 questions interactives avec indices photographiques réels, scoring en direct, jauge et analyse stratégique.

---

## 🚀 Déploiement sur Vercel

Le projet est configuré pour un déploiement statique instantané sur Vercel (zéro-config, chargement < 50ms mondialement grâce au CDN Edge).

### Méthode 1 : Via l'interface Vercel (Recommandé)
1. Rendez-vous sur [vercel.com/new](https://vercel.com/new).
2. Connectez votre compte GitHub et sélectionnez le dépôt **`mydraa/geo`**.
3. Conservez les paramètres par défaut (Framework Preset: **Other**, Root Directory: **`./`**).
4. Cliquez sur **Deploy**.
5. Votre site sera disponible en quelques secondes avec HTTPS automatique sur une URL du type `https://geo-xxx.vercel.app`.

### Méthode 2 : Via Vercel CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## 💻 Développement Local

Pour lancer l'application en local sans aucune dépendance :

```bash
# Avec npx (Node.js)
npx serve .

# Ou avec Python
python -m http.server 8080
```

Ouvrez ensuite [http://localhost:8080](http://localhost:8080) dans votre navigateur.

Pour exécuter la suite de tests de validation :
```bash
node test_engine.js
```

---

## 📁 Structure du Projet

```
├── index.html              # Interface principale SPA (10 onglets tactiques)
├── styles.css              # Design Obsidian Midnight & animations
├── app.js                  # Moteur applicatif, filtres matrice, quiz & i18n
├── data.js                 # Dataset bilingue intégral (122 pays, 2 300+ photos, i18n)
├── vercel.json             # Configuration Vercel & en-têtes de sécurité
├── package.json            # Métadonnées et scripts de build/test
├── test_engine.js          # Suite de tests d'intégrité (5/5 suites)
└── .gitignore              # Fichiers exclus du versionnement
```

---

## 📄 Licence

Ce projet est sous licence MIT. Libre d'utilisation pour la communauté GeoGuessr.
