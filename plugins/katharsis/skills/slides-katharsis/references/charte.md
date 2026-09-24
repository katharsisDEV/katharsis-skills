# Charte Katharsis Event

Relevée sur katharsis-event.fr (styles calculés, pas approximés) et confirmée par le
logo, dont le tracé est en `#9a1c20`. Tout est déjà codé dans `assets/theme.css` :
ce fichier explique **pourquoi**, pour savoir trancher quand un cas n'est pas prévu.

## Sommaire

1. Tokens
2. Signatures visuelles — ce qui rend une page « Katharsis »
3. Usage de la couleur
4. Typographie et fontes
5. Rythme et capacité d'une page
6. Ce qu'on ne fait pas

## 1. Tokens

| Rôle | Valeur | Variable |
|---|---|---|
| Titres | Poppins 600 (500 pour les chapeaux) | `--title` |
| Texte courant | Inter 400 / 600 | — |
| Fond de page | `#ffffff` | `--bg` |
| Cartes | `#f8f9fa`, filet `#dee2e6`, rayon 10 pt | `--card`, `--line` |
| Texte | `#212529` · secondaire `#3f464e` · atténué `#5c636a` · discret `#868e96` | `--txt` `--txt2` `--dim` `--muted` |
| Accent | **`#9a1b21`** — bordeaux de la marque | `--accent` (alias `--gold`) |
| Aplat accent | `#fbf2f2`, filet `#e3bfc1` | `--accent-soft`, `--accent-line` |
| Pastilles | rayon 100 pt — reprend les boutons du site | — |
| Séries | `#9a1b21` · `#212529` · `#6c757d` · `#adb5bd` · `#c9ced4` | `--s1` … `--s5` |

Format : **959 × 540 pt paysage** (16:9), fixé par `@page`. Même format pour tous
les documents — dossier bancaire, commercial, technique, interne.

## 2. Signatures visuelles

Ce sont elles qui font qu'une page est reconnaissable. Chacune est présente sur
toutes les pages de contenu :

- **Pastille de section** (`.eyebrow`) en haut à gauche : `03 · Structuration`.
  Numéro de partie + nom court. Pas un simple libellé : une pastille arrondie rosée.
- **Titre avec mot accentué** : la fin du titre en bordeaux via `<em>`.
  `<h1>Schéma de détention <em>et flux financiers</em></h1>`. Un seul `<em>` par titre,
  sur le segment qui porte le sens (souvent le dernier groupe de mots).
- **Filet bordeaux** de 62 × 2 pt sous le titre (`.rule`).
- **Pied de page** en trois temps : logo + nom du document · section · numéro de page.
- **Cartes « acc »** : fond blanc, filet rosé, petit trait bordeaux en haut à gauche.
  C'est la carte par défaut pour un argument ; la carte grise `.card` sert au contexte,
  la carte `.flat` aux tableaux.

Couverture : deux colonnes, texte à gauche (kicker, titre 44 pt avec `<em>`, filet,
chapeau, résumé à filet gauche, métadonnées), à droite un **visuel** (photo, plan)
ou un **panneau de 3 chiffres clés** en dégradé rosé. Logo en haut à gauche.

## 3. Usage de la couleur

Le bordeaux est la **seule** couleur vive. Il est rare par construction : c'est ce qui
lui donne du poids. Il sert à :

- signaler la structure (pastille, filet, puces, numéros, intitulés `.lbl.g`) ;
- désigner **la** donnée qui porte le message (la barre de l'année en cours, la ligne
  de total, le chiffre du bandeau).

Tout le reste est en gris. Dans un graphique, la série de comparaison est grise
(`#adb5bd` / `#c9ced4`), jamais d'une deuxième couleur vive.

**Aucune couleur inventée.** Pas de vert pour « positif », pas de rouge vif pour
« alerte », pas de bleu. Un écart négatif se lit par le signe (−) et, si besoin, par
un `.callout`. Si un schéma a besoin de distinguer plus de 4 flux, c'est le schéma
qui est trop chargé : le découper.

Code des séries (graphiques et flux de schémas), dans cet ordre de priorité :

| Série | Couleur | Trait | Classe SVG |
|---|---|---|---|
| 1 — principal | `#9a1b21` | plein | `.f1` (pointillé `.f1d`) |
| 2 — secondaire | `#212529` | plein | `.f2` |
| 3 — tertiaire | `#6c757d` | plein | `.f3` |
| 4 — annexe / énergie / loyers | `#adb5bd` | pointillé | `.f4` |

Exemples de correspondances déjà employées :
- technique : DMX `f1`, réseau `f2`, SPI/LED `f3`, 230 V `f4` (alias `.dmx .net .spi .pwr`) ;
- financier : compte courant `f1d`, capital `f2`, dette `f3`, loyers `f4`.

Deux pastilles de légende de la même couleur sur une même page = erreur de lecture.

Un plan ou une photo fournis **gardent leurs couleurs** : ne pas recolorier un plan
d'architecte ou un repère d'origine.

## 4. Typographie et fontes

| Élément | Taille |
|---|---|
| Titre couverture | 44 pt Poppins 600 |
| Titre de page `h1` | 25 pt Poppins 600 |
| Sous-titre `p.sub` | 10,5 pt Inter, gris |
| Titre de carte `.ct` | 13 pt Poppins 600 (12 pt en `.tight`) |
| Texte de carte | 10–10,5 pt Inter, interligne 1,42–1,45 |
| Tableau | 9,5 pt (9 pt en `.dense`) |
| Chiffre clé `.stat .v` | 21 pt Poppins 600 (17 pt en `.sm`) |
| Intitulés en capitales `.lbl`, `.eyebrow`, `th` | 7–7,5 pt, interlettrage .1em |
| Notes, sources | 8 pt, `#868e96` |

**Plancher : 8 pt** pour une note, **9 pt** pour du contenu. En dessous, le contenu est
trop dense : le couper, pas le rétrécir.

**Fontes statiques uniquement** (`assets/fonts/`). Jamais Inter variable de Google
Fonts : Chrome l'embarque en Type3 (un objet par mot, fichier ×2, texte inextractible).
Les statiques s'embarquent proprement en TrueType.

`→`, `Ω`, `≈` ne sont pas dans le sous-ensemble latin d'Inter et retombent sur Arial :
invisible à l'œil, inutile de corriger.

## 5. Rythme et capacité d'une page

- Marges : 30 pt en haut, 46 pt sur les côtés, 52 pt en bas (pied de page à 20 pt).
- En-tête ≈ 75 pt (pastille, titre, filet) ; +18 pt avec un sous-titre.
- Espacement entre blocs : **13 pt** partout (`.body`, `.col`, `.stats`).
- **Capacité utile ≈ 380 pt de hauteur**, 867 pt de largeur.

Repères de remplissage d'une page de contenu :

| Contenu | Tient sur une page |
|---|---|
| Rangée de chiffres clés + 3 cartes | 3–4 puces courtes par carte |
| Tableau `.dense` pleine largeur | 13–15 lignes (moins si retours à la ligne) |
| Deux colonnes de texte | ~120 mots par colonne |
| Schéma pleine page | 1 schéma + 1 légende, rien d'autre |
| Grille 3 × 2 de références | 6 cartes, ~25 mots chacune |

Au-delà : **découper sur deux pages**, pas réduire la typo.

## 6. Ce qu'on ne fait pas

- Fond sombre ou bleu nuit (même en couverture) — la charte est sur fond blanc.
- Dégradés autres que le rosé → gris clair déjà défini (`.panel`, `.banner`).
- Ombres portées, icônes clipart, emojis, images d'illustration génériques.
- Soulignement pour accentuer (réservé aux liens dans les tableaux).
- Capitales dans les titres `h1` : les capitales sont réservées aux petits intitulés.
- Captures d'écran de schémas ou de tableaux : les redessiner en SVG / HTML.
- Graphiques en PNG (matplotlib, Excel) : utiliser `scripts/charts.py`.
- Camembert à plus de 4 parts, graphique 3D, double axe.
