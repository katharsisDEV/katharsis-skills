# Rédaction et rigueur du fond

La mise en forme ne rattrape pas un fond faux. Les dossiers Katharsis sont lus par des
banquiers, des clients, des bailleurs, des partenaires techniques : un chiffre qui ne
tombe pas juste coûte plus cher qu'une page moins jolie.

## Sommaire

1. Écrire une page
2. Typographie française
3. Chiffres : sources, calculs, cohérence
4. Réserves : version client et version interne
5. Traçabilité — le README du dossier

## 1. Écrire une page

- **Le titre dit la conclusion**, pas le sujet. « Des loyers qui couvrent 1,5 fois
  l'emprunt » plutôt que « Loyers ». Court : une ligne, deux au plus en 25 pt.
- **Le sous-titre** (`p.sub`) précise le périmètre ou la méthode, en une phrase.
- **Phrases affirmatives, factuelles, chiffrées.** Pas de superlatifs (« leader »,
  « unique », « exceptionnel »), pas de formules creuses (« une solution innovante »).
  Un fait daté ou chiffré vaut mieux qu'un adjectif.
- **Puces courtes** : une idée, une ligne (deux au plus). Commencer par le mot fort.
  Pas de point final dans les puces, sauf si elles contiennent plusieurs phrases.
- **Mettre en gras 1 à 2 éléments par carte**, jamais une phrase entière.
- **Ne pas répéter** un chiffre sur trois pages : le poser une fois là où il est
  démontré, y renvoyer ailleurs (« voir p. 08 »).
- **Parler au lecteur du document** : un banquier cherche capacité de remboursement,
  garanties, antériorité ; un client cherche résultat, délai, références ; un partenaire
  technique cherche références exactes, schémas, contraintes.
- **Ne rien inventer.** Une information absente reste absente : la demander, ou la
  signaler comme point ouvert. Jamais de référence, de nom, de date ou de chiffre
  « plausible ».

### Structure type d'un dossier

1. Couverture — ce qu'est le document, pour qui, les 3 chiffres qui comptent
2. Sommaire (au-delà de 8 pages)
3. Vue d'ensemble — l'essentiel en une page (chiffres clés + 3 arguments)
4. Corps — une section par question que se pose le lecteur
5. Synthèse — ce qu'il faut retenir, ce qui est attendu du lecteur
6. Annexes — détails, références, sources, liens

## 2. Typographie française

- **Espace insécable** (`&nbsp;` ou ` `) : entre un nombre et son unité
  (`450 000 €`, `20 ans`, `12 %`, `359,6 m²`), avant `: ; ! ?`, à l'intérieur des
  guillemets `« … »`, dans les milliers.
- **Milliers séparés par une espace**, décimales par une **virgule** : `1 234,5`.
- `€` après le nombre ; `k€` accepté dans les tableaux et schémas, pas dans le texte.
  Préciser **HT / TTC** dès qu'un montant peut être compris des deux façons.
- Signe moins typographique `−` (U+2212) dans les tableaux, pas le tiret `-`.
- Pourcentages : `12,5 %`. Multiplicateurs : `× 2,7`.
- Dates : `12 septembre 2026` dans le texte, `12/09/2026` dans les tableaux.
- Guillemets français `« »`, apostrophe typographique `’` acceptée mais pas obligatoire.
- Majuscule seulement en début de titre et aux noms propres : « Vue d'ensemble »,
  pas « Vue d'Ensemble ».
- Nom de la société : **Katharsis Event** dans le texte ; conserver l'écriture
  officielle (« Katharsis-event ») quand il s'agit de la dénomination sociale dans
  un acte, un bail, des statuts.

## 3. Chiffres : sources, calculs, cohérence

- Chaque chiffre a une **source** (document fourni, calcul, site, déclaration de
  Vincent). La noter dans le README ; en note de bas de carte (`.note`) si le lecteur
  en a besoin.
- **Refaire les calculs** avant de mettre en page : totaux, sous-totaux, taux,
  mensualités, ratios. Une erreur trouvée dans une source se **signale** à Vincent,
  on ne la corrige pas en silence et on ne la propage pas en silence non plus.
- **Un chiffre, une valeur** dans tout le document : le même montant écrit de deux
  façons (arrondi, HT/TTC) est une incohérence pour le lecteur.
- Provisoire ≠ définitif : un exercice non clos, une estimation, une projection se
  signalent (hachure dans le graphique, « provisoire » ou « prévisionnel » dans la légende).
- Beaucoup de chiffres → `data.py` comme source unique, HTML généré.

## 4. Réserves : version client et version interne

Avant de finaliser, demander la forme de sortie :

- **un seul document** portant ses réserves en clair (« à confirmer », annexe des
  points ouverts) ;
- **deux documents** : un dossier client sans aucune réserve, et une note interne qui
  trace tout ce qui en a été retiré.

En double export :
1. Retirer du dossier client toute mention de réserve. Contrôle :
   `grep -icE "à confirmer|à préciser|à arbitrer|à figer|hypoth|non arrêté|non identifié|TODO|XXX" deck.html`
2. **Remplacer, ne pas effacer** : une reformulation affirmative et vraie garde la
   page dense ; une cellule vidée laisse un trou.
3. La note interne trace chaque retrait (page, texte d'origine, remplacement) et ouvre
   sur les arbitrages attendus.
4. Une **règle de conception** (« marge de 20 % ») ou un renvoi documentaire n'est pas
   une réserve : il reste dans la version client.

## 5. Traçabilité — le README du dossier

Chaque dossier de présentation a un `README.md` court :

- **Sortie** : nom du PDF, nombre de pages, format.
- **Sources** : chaque fichier fourni et ce qu'il contient réellement.
- **Retraitements et hypothèses** : chaque calcul non trivial, chaque choix.
- **Points relevés** : erreurs trouvées dans les sources, informations manquantes.
- **Chaîne de production** : les commandes pour reconstruire le PDF.

C'est ce qui permet de reprendre le dossier dans six mois, ou de répondre à une
question du lecteur sans tout refaire.
