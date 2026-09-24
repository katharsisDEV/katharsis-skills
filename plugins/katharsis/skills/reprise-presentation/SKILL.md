---
name: reprise-presentation
description: Reprendre une présentation client (PDF, PPTX, Google Slides export) pour la compléter et la mettre à la charte Katharsis Event — remplir les zones de schéma laissées vides, vectoriser les captures d'écran, ajouter les slides manquantes, vérifier les références matériel sur les sites fabricants et produire les annexes avec liens. Utiliser ce skill dès que Vincent fournit une présentation ou un dossier technique existant et demande de le compléter, l'améliorer, le finaliser, le mettre en forme, y ajouter des schémas ou des références — même s'il ne nomme ni « skill » ni « charte ». Utiliser aussi pour corriger des références produit dans un dossier déjà repris, ou pour scinder un dossier en version client et version interne.
---

# Reprise d'une présentation client

Une présentation qui arrive en reprise est presque toujours une **base** : des zones
de schéma annoncées mais vides, des captures d'écran basse définition, des renvois
qui ne tombent pas juste, et des références matériel approximatives. Le travail
consiste à la rendre complète, exacte et diffusable.

Le piège à éviter : traiter ça comme un exercice de mise en page. La valeur est
d'abord dans le **fond** — les références produit sont fausses plus souvent qu'on
ne croit, et tout ce qui en dépend (adressage, puissance, masses) l'est alors aussi.

## Environnement

Une fois par session, si les outils PDF manquent :

```bash
uv venv "$SCRATCH/venv" -q && uv pip install --python "$SCRATCH/venv/bin/python" -q pymupdf
```

Chrome headless sert au rendu PDF ; aucun serveur, aucune dépendance réseau au build.

## Phase 1 — Lire la source, vraiment

```bash
python scripts/ingest_pdf.py <source.pdf> <dossier-de-travail>
```

Le script sort le texte page par page, rend chaque page en PNG et extrait les
images intégrées au-delà d'un seuil de taille.

**Regarder toutes les pages rendues, pas seulement le texte.** Les zones vides ne
laissent aucune trace textuelle : une carte « Régie » sans contenu ressemble, dans
l'extraction, à un simple titre. Le PNG, lui, montre le trou.

En lisant, dresser trois listes :

- **Zones à remplir** — « à représenter », « schéma à intégrer », « prévoir ici »,
  cartes au titre seul, listes de puces qui décrivent un schéma au lieu de le montrer.
- **Visuels à refaire** — toute capture d'écran ou image pixelisée d'un synoptique.
  Elle sera redessinée en SVG. Les plans et photos, eux, se conservent : les extraire.
- **Incohérences** — numérotation dupliquée, renvois faux (« voir slide 6 » quand
  c'est la 7), orthographes divergentes d'un même nom, fautes, et surtout les
  **erreurs techniques** : un matériel décrit par une fonction qui n'est pas la sienne.

Comparer aussi ce que la couverture promet avec ce que le dossier traite. Un sous-titre
qui annonce trois volets alors que le corps n'en couvre que deux désigne exactement la
slide qui manque.

## Phase 2 — Vérifier le fond avant de mettre en forme

Pour **chaque** matériel nommé, aller chercher la fiche constructeur et en lire les
caractéristiques réelles. Ne jamais se fier au libellé du document d'origine.

Ce que la fiche apporte et qu'il faut ensuite recalculer :

- **modes de canaux** → l'adressage DMX et la charge de chaque univers ;
- **puissance absorbée** → le bilan électrique et le nombre de circuits ;
- **masse et encombrement** → la charge suspendue et les fixations ;
- **connectique et protocoles** → les notes de câblage.

Vérifier que chaque lien répond avant de le citer :

```bash
curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" -L --max-time 15 -A "Mozilla/5.0" "<url>"
```

Deux règles qui évitent de raconter n'importe quoi :

- **Ne jamais inventer une référence.** Un matériel non identifié reste non identifié ;
  c'est une réserve, pas un trou à combler par une supposition plausible.
- **Signaler les erreurs techniques plutôt que les propager.** Si le document appelle
  un contrôleur de pixels un « splitter DMX », le corriger et le tracer. C'est souvent
  la contribution la plus utile de toute la reprise.

Quand une valeur doit être choisie pour que le dossier tienne debout (un mode de canaux,
par exemple), choisir la plus défendable, poser le calcul, et tracer l'hypothèse.

## Phase 3 — Reconstruire

Un fichier HTML par document, une `<section class="slide">` par page, et
`assets/theme.css` copié depuis ce skill. La charte, les tokens et le code couleur
des schémas sont dans `references/charte-katharsis.md` — le lire avant d'écrire la
première page.

Format : **959 × 540 pt, paysage**, fixé par `@page` dans le thème.

Les schémas sont des **SVG inline**, jamais des captures. Les motifs récurrents
(boîtes, flèches, marqueurs, chaînages, légendes) sont dans
`references/schemas-svg.md` avec les classes du thème.

Ce qu'une bonne reprise ajoute :

- les schémas qui manquaient, dessinés d'après ce que le texte décrivait ;
- un sommaire, si le document en est dépourvu ;
- les slides que la couverture promettait ;
- une **annexe des références matériel** : fonction, référence projet, fabricant, lien ;
- une **annexe documentation** : manuels, logiciels, fiches produits ;
- des tableaux de synthèse là où le document listait des puces (patch, bilan de
  puissance, caractéristiques comparées).

Ne pas ajouter de section normative sauf demande explicite.

## Phase 4 — Contrôler, à chaque build

```bash
./build.sh && python scripts/check_layout.py presentation.html
```

`check_layout.py` mesure les lignes de texte dans le navigateur et signale celles
qui passent sous le bord d'une carte. **C'est le mode de défaillance dominant** : le
thème coupe proprement ce qui dépasse, donc une ligne de tableau, une puce ou la
dernière ligne d'un paragraphe disparaît du PDF sans le moindre signe dans le HTML.
Une relecture visuelle ne l'attrape pas de façon fiable — une carte tronquée a l'air
pleine et finie.

Deux niveaux dans le rapport :

- **texte coupé** — bloquant, le script cite la ligne perdue ;
- **sans marge basse** — le contenu tient mais touche le bord ; cosmétique.

Quand une carte déborde, **retirer du contenu** plutôt que rétrécir la typo :
raccourcir une formulation, fusionner deux puces, supprimer une ligne redondante avec
une autre page. Le rétrécissement en cascade abîme tout le document.

Puis regarder les pages rendues. Un contrôle automatique ne voit pas un libellé qui
chevauche une ligne de séparation, ni deux pastilles de légende de la même couleur,
ni un texte SVG qui déborde de sa boîte.

Vérifier enfin que les liens sont bien passés dans le PDF :

```bash
python scripts/check_layout.py --links <sortie.pdf>
```

## Phase 5 — Livrer

Demander la forme de sortie avant de finaliser :

- **un seul document**, portant ses réserves en clair (mentions « à confirmer » et
  annexe des points ouverts) ;
- **deux documents** — un dossier client sans aucune réserve, et un document interne
  qui trace tout ce qui en a été retiré.

Si c'est le double export :

1. Retirer du dossier client toute mention de réserve — *à confirmer, à préciser,
   à arbitrer, à figer, hypothèse, non arrêté, à définir*. Contrôle :
   `grep -icE "à confirmer|à préciser|à arbitrer|à figer|hyp\.|non arrêté|non identifié"`.
2. **Remplacer, ne pas effacer.** Une cellule vidée laisse un trou ; une reformulation
   affirmative garde la page dense. « Node / splitter — réf. à confirmer » devient
   « Node / splitter — 3 univers en sortie ».
3. Le document interne trace chaque retrait : page, emplacement, texte d'origine,
   texte de remplacement. Il ouvre sur les arbitrages attendus, avec pour chacun les
   pages du dossier client concernées.
4. Distinguer une **réserve** d'une **règle de conception**. « Réserve de 20 % de canaux »
   ou « voir l'étude LED » restent dans le dossier client : ce sont des prescriptions et
   des renvois documentaires, pas des points ouverts.

Livrer les PDF avec `SendUserFile`, et signaler en clair ce qui reste ouvert — surtout
les points où le dossier affirme désormais une valeur qui n'est encore qu'une hypothèse.

## Structure du dossier de travail

```
<projet>/
├── presentation.html      dossier client
├── reserves.html          document interne (si double export)
├── theme.css              copié depuis assets/ de ce skill
├── assets/                logo, fontes, plans et photos extraits
├── build.sh               Chrome headless → PDF
└── README.md              sources, charte, décisions, points ouverts
```

`scripts/build.sh` est prêt à copier : il rend chaque source HTML en PDF paysage.
