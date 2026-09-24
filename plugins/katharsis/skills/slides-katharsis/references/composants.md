# Composants et gabarits de page

Toutes les classes sont dans `assets/theme.css`. `assets/template.html` montre chaque
type de page assemblé et rendu : l'ouvrir en premier, copier la `<section>` la plus
proche, puis adapter.

## Sommaire

1. Squelette d'une page
2. Choisir la mise en page selon le message
3. Catalogue des composants
4. Couverture, sommaire, intercalaire, synthèse

## 1. Squelette d'une page

```html
<section class="slide">
<span class="eyebrow">03 · Nom de la section</span>
<h1>Début du titre <em>fin accentuée</em></h1>
<p class="sub">Une phrase qui dit ce que la page démontre</p>   <!-- facultatif -->
<div class="rule"></div>
<div class="body"> … </div>
<div class="foot"><div class="brand"><img src="assets/logo-katharsis.svg" alt=""><span>Nom court du document</span></div><span>Nom de la section</span><span>03</span></div>
</section>
```

- `.body` est une rangée flex ; `.body.rows` empile verticalement. Imbriquer
  `.body.rows > .stats + .body` pour « chiffres en haut, cartes dessous ».
- `.col` = colonne de cartes. Répartir la largeur par `style="flex:1.6"` / `flex:1`.
- `.grow` fait remplir la hauteur disponible à une carte.
- `.grid2`, `.grid3` pour des cartes de taille égale.
- Le numéro de page du pied de page est celui que lit `check_layout.py` : le tenir juste.

## 2. Choisir la mise en page selon le message

Partir du **message de la page**, pas du contenu disponible :

| Le message est… | Mise en page |
|---|---|
| « Voici l'essentiel en chiffres » | `.stats` (3–5 chiffres) + 3 cartes `.acc` |
| « Trois raisons / trois volets » | 3 cartes `.acc.grow` côte à côte |
| « Voici les chiffres détaillés » | tableau `.t` dans une carte `.flat` (60 %) + carte lecture + `.callout` (40 %) |
| « Ça évolue / ça progresse » | graphique `charts.py` dans une carte + carte de lecture |
| « Voici comment c'est organisé » | schéma SVG pleine largeur dans `.dgwrap` + `.legend` |
| « Voici qui porte le projet » | cartes personnes (`.assoc` + `.mono`) + `.metier` |
| « Voici ce qu'on a fait » | `.grid3` de `.card.real` (tag, titre, lieu, texte, chiffre `.rm`) |
| « Étapes / trajectoire » | `.steps` (points qui s'allument) ou `ul.n` numérotée |
| « Ce qu'il faut retenir » | `table.syn` + `.banner` |
| « Point d'attention » | `.callout` sous le contenu, jamais seul sur une page |

Une page = **un** message. Deux messages → deux pages.

## 3. Catalogue des composants

### Cartes
```html
<div class="card acc grow"><div class="ct">Titre de carte</div><ul class="b"><li>…</li></ul></div>
<div class="card"><div class="lbl">INTITULÉ GRIS</div><p>…</p></div>
<div class="card flat"><div class="lbl">Tableau (€)</div><table class="t dense">…</table></div>
```
Variantes : `.acc` (argument, défaut), `.card` gris (contexte), `.flat` (tableau),
`.tight` (padding réduit quand 2 rangées de cartes), `.lbl.g` (intitulé bordeaux).

### Listes
`ul.b` puces bordeaux · `ul.n` numérotation 01, 02, 03 en bordeaux.
Une puce = une ligne, deux au plus. Le mot qui compte en `<b>`.

### Chiffres clés
```html
<div class="stats">                      <!-- .stats.sm si 5 chiffres ou page chargée -->
 <div class="stat"><div class="k">Libellé</div><div class="v">450 000 €</div><div class="s">précision</div></div>
</div>
```
`.k` dit ce qu'on mesure, `.v` le chiffre seul (unité comprise), `.s` le contexte
(durée, comparaison, source) en bordeaux.

### Bandeau et encart
```html
<div class="banner">Mensualité <b>2 727 €</b> sur 20 ans</div>
<div class="callout">Conclusion ou point d'attention.</div>
<div class="callout n">Variante neutre : renvoi, méthode, source.</div>
```

### Phrase-manifeste
`<p class="hero">Une phrase <em>qui claque</em></p>` en tête de carte de présentation.

### Étiquettes
`<span class="tag">Intégration</span>` · `<span class="tag n">2024</span>` ·
`<div class="chips"><span class="chip">…</span><span class="chip n">…</span></div>`

### Tableaux
```html
<table class="t dense">
 <thead><tr><th>Poste</th><th class="r">2025</th></tr></thead>
 <tbody>
  <tr><td>Ligne</td><td class="r">12 000</td></tr>
  <tr class="sub"><td>Sous-total</td><td class="r">…</td></tr>
  <tr class="tot"><td>Total</td><td class="r">…</td></tr>
 </tbody>
</table>
```
Nombres alignés à droite (`.r`, chiffres tabulaires). Unité dans l'intitulé de la
carte (« en € HT ») plutôt que répétée dans chaque cellule. `td.u` = repère bordeaux
en première colonne (référence, date). Liens `<a href>` dans les cellules : soulignés
bordeaux automatiquement et cliquables dans le PDF.

### Personnes
```html
<div class="assoc"><div class="mono">VS</div><div><div class="an">Vincent Segu</div><div class="at">Associé</div><div class="ad">Informatique</div></div></div>
```

### Métiers / piliers
```html
<div class="metier"><div class="mn">01</div><div><b>Prestation</b><p>Une ligne.</p></div></div>
```

### Étapes
```html
<div class="steps">
 <div class="step"><div class="dots"><i></i></div><div class="sn">2020</div><div class="sy">création</div></div>
 <div class="step last"><div class="dots"><i></i><i></i><i></i></div><div class="sn">2026</div><div class="sy">aujourd'hui</div></div>
</div>
```

### Références / réalisations
```html
<div class="grid3" style="grid-template-rows:1fr 1fr">
 <div class="card acc real"><span class="tag">Intégration</span><div class="rt">Client</div><div class="rl">Lieu · année</div><p>Ce qui a été fait.</p><div class="rm">Chiffre ou résultat</div></div>
</div>
```

## 4. Couverture, sommaire, intercalaire, synthèse

Voir `assets/template.html` pour le code complet de chacun.

- **Couverture** `.slide.cover` : pas d'eyebrow ni de pied de page. Colonne gauche
  (`kicker` = type de document + date, `h1` avec `<em>`, `.rule`, `.lead`,
  `.cover-sum`, `.meta`). Colonne droite : `.cover-visual` avec une `<img>`
  (photo de réalisation, plan) **ou** `.cover-visual.panel` avec 3 `.kpi`.
  Les chiffres du panneau doivent déjà figurer dans le document.
- **Sommaire** : `.toc` en deux colonnes, `.row` = numéro · titre + `<small>` · page.
  `.toc.compact` au-delà de 10 entrées. Obligatoire au-delà de 8 pages.
- **Intercalaire** `.slide.divider` : grand numéro, titre, une phrase. Seulement pour
  les documents longs (> 15 pages) à parties nettement distinctes.
- **Synthèse** : `table.syn` (intitulé bordeaux | phrase), ligne `.hl` sur la
  demande ou la conclusion, `.banner` pour le chiffre final.
- **Annexes** : pastille `Annexe A · …`, tableaux `.dense`, liens cliquables.
