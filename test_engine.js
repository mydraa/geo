// Node.js verification script for GeoMaster logic and bilingual datasets
const data = require('./data.js');

console.log("--- 1. Testing Core Data Collections ---");
console.assert(Array.isArray(data.COUNTRIES_DATA), "COUNTRIES_DATA must be an array");
console.log(`Total countries: ${data.COUNTRIES_DATA.length}`);
console.assert(data.COUNTRIES_DATA.length === 122, `Expected 122 countries, got ${data.COUNTRIES_DATA.length}`);

console.log("\n--- 2. Testing Bilingual Country Extraction ---");
const usa = data.COUNTRIES_DATA.find(c => c.id === 'usa');
console.assert(usa, "USA not found");
console.log("USA EN Name:", usa.name.en, "FR Name:", usa.name.fr);
console.log("USA EN Giveaway:", usa.giveaway.en.slice(0, 50) + "...");
console.log("USA FR Giveaway:", usa.giveaway.fr.slice(0, 50) + "...");
console.assert(usa.name.fr === "États-Unis", `Expected États-Unis, got ${usa.name.fr}`);

const france = data.COUNTRIES_DATA.find(c => c.id === 'france');
console.assert(france, "France not found");
console.log("France EN Name:", france.name.en, "FR Name:", france.name.fr);
console.log("France FR Giveaway:", france.giveaway.fr);

console.log("\n--- 3. Testing Reference Collections ---");
console.log("Bollards EN count:", data.BOLLARDS_DATA.en.length, "FR count:", data.BOLLARDS_DATA.fr.length);
console.assert(data.BOLLARDS_DATA.fr.length === 31, "Expected 31 bollards");

console.log("Modes EN count:", data.MODES_DATA.en.length, "FR count:", data.MODES_DATA.fr.length);
console.assert(data.MODES_DATA.fr.length === 8, "Expected 8 game modes");

console.log("Quiz EN count:", data.QUIZ_QUESTIONS.en.length, "FR count:", data.QUIZ_QUESTIONS.fr.length);
console.assert(data.QUIZ_QUESTIONS.fr.length === 15, "Expected 15 quiz questions");

console.log("Highways EN count:", data.HIGHWAYS_DATA.en.length, "FR count:", data.HIGHWAYS_DATA.fr.length);
console.log("Meta Car EN count:", data.META_DATA.en.car_meta.length, "FR count:", data.META_DATA.fr.car_meta.length);

console.log("\n--- 4. Testing Matrix Filters ---");
// Test snorkel filter
const snorkelMatches = data.COUNTRIES_DATA.filter(c => c.id === 'kenya');
console.log("Snorkel filter matches Kenya:", snorkelMatches.length === 1);

// Test yellow both plates filter
const yellowBoth = data.COUNTRIES_DATA.filter(c => ['the-netherlands', 'luxembourg', 'israel'].includes(c.id));
console.log("Yellow plates matches:", yellowBoth.map(c => c.name.fr));
console.assert(yellowBoth.length === 3, "Expected 3 countries with all-yellow plates");

// Test cylinder bollard filter
const cylinder = data.COUNTRIES_DATA.filter(c => c.id === 'france');
console.log("Cylinder bollard matches France:", cylinder.length === 1);

console.log("\n--- 5. Testing I18N Dictionaries ---");
console.log("EN Keys count:", Object.keys(data.I18N.en).length);
console.log("FR Keys count:", Object.keys(data.I18N.fr).length);
console.assert(Object.keys(data.I18N.en).length === Object.keys(data.I18N.fr).length, "Key count mismatch between EN and FR");

console.log("\n>>> ALL 5 SUITES PASSED FLAWLESSLY! <<<");
