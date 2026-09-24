---
name: slides-katharsis
description: Créer des présentations et dossiers en slides (PDF paysage 16:9) à la charte Katharsis Event — Poppins/Inter, bordeaux #9a1b21, pastilles de section, cartes, chiffres clés, schémas SVG et graphiques vectoriels — avec les bonnes pratiques maison de rédaction, de contrôle de mise en page et de rigueur sur les chiffres. Utiliser ce skill dès que Vincent demande une présentation, des slides, un deck, un dossier (bancaire, commercial, financement, technique, partenaire, investisseur, client, interne), une plaquette ou un support de réunion pour Katharsis Event ou l'une de ses sociétés liées (KGroup, SCI, VLMD…), même s'il ne mentionne ni « charte » ni « skill », et quel que soit le sujet. Utiliser aussi pour mettre un document existant à la charte Katharsis ou ajouter des pages à un dossier déjà dans ce format. Pour la reprise d'une présentation technique client fournie en PDF/PPTX (schémas manquants, références matériel), combiner avec le skill reprise-presentation.
---

# Slides à la charte Katharsis Event

Un document Katharsis se reconnaît à trois choses : une mise en page sobre sur fond
blanc où **le bordeaux est rare et porte le sens**, des pages qui disent **une chose
chacune, chiffrée**, et un fond **vérifié** — chiffres recalculés, sources tracées,
rien d'inventé. Ce skill fournit le thème, le gabarit, les outils de contrôle, et les
règles pour tenir ces trois exigences sur n'importe quel sujet.

## Ce que contient le skill

| Fichier | Rôle | Quand le lire |
|---|---|---|
| `assets/theme.css` | toute la charte en CSS (tokens, composants) | copié, jamais réécrit |
| `assets/template.html` | gabarit : couverture, sommaire, chiffres clés, tableau, schéma, équipe, intercalaire, synthèse | **avant d'écrire la première page** |
| `references/charte.md` | tokens, signatures, couleur, typo, capacité d'une page | avant de concevoir |
| `references/composants.md` | catalogue HTML + quelle mise en page pour quel message | en construisant |
| `references/schemas-graphiques.md` | schémas SVG, graphiques `charts.py` | dès qu'il y a un schéma ou des chiffres à tracer |
| `references/redaction.md` | écriture, typo française, rigueur des chiffres, version client / interne, README | avant de rédiger, et avant de livrer |
| `scripts/new_deck.sh` | prépare un dossier (thème, fontes, logo, gabarit, scripts) | au démarrage |
| `scripts/build.sh` | HTML → PDF 959 × 540 pt via Chrome headless | à chaque itération |
| `scripts/check_layout.py` | texte coupé par une carte, bloc sous le pied de page, liens du PDF | après chaque build |
| `scripts/preview.sh` | PDF → PNG par page pour la relecture visuelle | après chaque build |
| `scripts/charts.py` | graphiques SVG dans la charte (barres, courbe, anneau…) | pour tout graphique |

`SKILL` ci-dessous désigne le dossier de ce skill.

## Déroulé

### 1. Cadrer avant de mettre en page

Établir, à partir de la demande et des pièces fournies — et demander seulement ce qui
manque vraiment :

- **Lecteur et objectif** : qui lit (banque, client, bailleur, partenaire, associés)
  et ce qu'il doit penser ou faire en refermant le document.
- **Sources** : lire **toutes** les pièces fournies (PDF, comptes, devis, plans,
  captures). Regarder les images, pas seulement le texte extrait.
- **Version** : un seul document, ou dossier client + note interne (voir `redaction.md` §4).

Puis écrire le **plan** : une ligne par page, sous la forme « titre-conclusion → mise
en page » (voir le tableau de `composants.md` §2). Le montrer à Vincent si le document
dépasse une dizaine de pages ou si l'angle n'est pas évident — réorganiser un plan
coûte une minute, réorganiser 20 pages en coûte trente.

### 2. Préparer le dossier

```bash
SKILL/scripts/new_deck.sh <dossier-du-projet> presentation.html
```

Le script copie `theme.css`, `assets/` (logo, fontes statiques), le gabarit et les
scripts. Ne pas recopier le CSS à la main ni charger les fontes depuis Google Fonts
(fonte variable → Type3 dans le PDF, voir `charte.md` §4). Les ajustements propres à un
document vont dans le `<style>` de son HTML, jamais dans `theme.css`.

### 3. Construire

Une `<section class="slide">` par page, en partant de la section du gabarit la plus
proche. Les réflexes qui font la charte :

- pastille `NN · Section`, titre avec un `<em>` sur le segment qui porte le sens,
  filet, pied de page à trois temps avec le bon numéro ;
- cartes `.acc` pour les arguments, `.stats` pour les chiffres clés, tableaux `.t` ;
- **schémas en SVG inline, graphiques avec `charts.py`** — jamais de capture ni de PNG ;
- bordeaux uniquement pour la structure et la donnée qui porte le message ;
- une page tient ≈ 380 pt de contenu : si ça ne rentre pas, **découper ou couper du
  texte**, ne pas réduire la typo (plancher 9 pt pour le contenu).

Beaucoup de chiffres → `data.py` (source unique) + `build_html.py` qui génère le HTML ;
on corrige les chiffres dans `data.py`, jamais dans le HTML généré.

### 4. Contrôler — à chaque build

```bash
./build.sh presentation.html && python3 check_layout.py presentation.html && ./preview.sh presentation.pdf
```

`check_layout.py` est indispensable : le thème masque proprement ce qui dépasse d'une
carte, donc une ligne de tableau ou une puce peut **disparaître du PDF sans aucun
signe**, et une carte tronquée a l'air finie à l'œil. Il signale aussi les blocs qui
descendent sous le pied de page. Tout « texte coupé » est bloquant ; « sans marge
basse » est cosmétique mais à corriger si facile.

Puis **regarder chaque PNG** de `_preview/`. Le contrôle automatique ne voit pas :
un libellé SVG qui déborde de sa boîte ou chevauche une flèche, deux entrées de légende
de même couleur, une page déséquilibrée (une carte pleine, une vide), un `<em>` mal
placé, un numéro de page faux dans le sommaire.

Enfin, le fond (`redaction.md` §3) : totaux et ratios recalculés, un même chiffre
identique partout, HT/TTC explicites, provisoire signalé.

### 5. Livrer

- PDF nommé clairement : `<Entité>_<Objet>[_<Destinataire>].pdf`
  (ex. `Katharsis-Event_Dossier_Entreprise.pdf`).
- `README.md` du dossier à jour : sources, retraitements, points relevés, commandes
  de build (`redaction.md` §5).
- Si version client : `grep` des réserves à zéro (`redaction.md` §4).
- Envoyer le PDF avec `SendUserFile`, et dire en clair ce qui reste ouvert : erreurs
  trouvées dans les sources, hypothèses retenues, informations manquantes.

## Mettre un document existant à la charte

Reprendre le texte **mot pour mot** sauf demande contraire ; changer la forme, pas le
fond. Redessiner en SVG tout schéma ou tableau capturé en image ; conserver photos et
plans. Relever les erreurs trouvées (calcul faux, renvoi erroné) dans le README et les
signaler à Vincent plutôt que de les corriger en silence. Pour un dossier technique
client à compléter (zones vides, références matériel à vérifier), suivre en plus le
skill `reprise-presentation`.

## Environnement

Chrome (`/Applications/Google Chrome.app`, surchargeable par `CHROME=`), Python 3,
`pdftoppm` (poppler) pour les aperçus. `check_layout.py --links` demande `pymupdf` :

```bash
uv venv "$SCRATCH/venv" -q && uv pip install --python "$SCRATCH/venv/bin/python" -q pymupdf
```
