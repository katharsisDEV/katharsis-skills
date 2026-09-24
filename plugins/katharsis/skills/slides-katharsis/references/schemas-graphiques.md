# Schémas et graphiques

Tout visuel de données ou d'organisation est **vectoriel et dessiné dans la charte** :
SVG inline pour les schémas, `scripts/charts.py` pour les graphiques. Jamais de
capture d'écran, jamais de PNG exporté d'Excel ou de matplotlib — ils sont flous à
l'impression, dans une autre typo et d'autres couleurs.

## Schémas SVG

### Marqueurs de flèches — une fois par document
Le bloc `<svg width="0" height="0">…<defs>` avec `ar-1` à `ar-4` est en tête de
`assets/template.html`, juste après `<body>`. Les classes `.f1`…`.f4` y renvoient.
Un marqueur supplémentaire se déclare dans le même bloc, avec la même géométrie.

### Classes

| Classe | Usage |
|---|---|
| `.box` | boîte neutre (acteur, étape) |
| `.box-g` | élément central — contour bordeaux, fond blanc |
| `.box-f` + `.tw` / `.tw2` | élément principal en aplat bordeaux, texte blanc |
| `.box-r` | sortie, destinataire, terminal — aplat rosé |
| `.box-n` | tiers, équipement, élément externe |
| `.zone` | regroupement en pointillés |
| `.t1` `.t2` `.t3` | titre de boîte · sous-titre · annotation |
| `.tk` | intertitre d'étage bordeaux en capitales |
| `.tr` | repère bordeaux (numéro, pourcentage) |
| `.lab` | libellé de flèche (ajouter `fill` de la couleur du flux) |
| `.f1` `.f2` `.f3` `.f4` `.f1d` | liaisons fléchées (voir charte §3) |
| `.f10` `.f20` `.f30` | mêmes liaisons sans flèche (chaînage) |
| `.pin` + `.pt` | pastille numérotée sur un plan (cercle + chiffre blanc) |

### Motifs éprouvés

- **Étages** (commande → distribution → sortie ; associés → holding → société) :
  un `.tk` et un filet `#dee2e6` par étage, boîtes alignées dessous, liaisons verticales.
- **Détention et flux** : boîtes en étages, pourcentages de détention en `.tr` sur les
  liaisons `.f2`, flux financiers dans les couleurs de série, légende en HTML.
- **Chaîne numérotée** : quand la source listait « 01 …, 02 …, 03 … », reprendre ces
  numéros en `.tk` au-dessus de chaque boîte — le lecteur retrouve sa liste, devenue schéma.
- **Guirlande** : appareils identiques en série, segments `.f10`, terminaison en bout.
- **Options A / B** : deux schémas côte à côte dans deux cartes, même échelle, la
  différence en bordeaux.
- **Plan annoté** : image du plan en `<image>` dans le SVG, `.pin` numérotés dessus,
  tableau de correspondance à côté.

### Dimensionnement
Pleine page : `<div class="dgwrap"><svg class="dg" viewBox="0 0 1340 580" preserveAspectRatio="xMidYMid meet">`.
Le viewBox doit avoir **à peu près le rapport de la place disponible** (≈ 867 × 360 pt
sans sous-titre) ; sinon le schéma est rétréci et le texte devient illisible. Pour un
grand viewBox, grossir les textes via une classe locale
(`.dgL .t1{font-size:13px}` …) plutôt que de réduire le viewBox.

### Placement du texte — le défaut n° 1, invisible avant le rendu
- SVG ne revient pas à la ligne : un texte trop long déborde de sa boîte. Deux `<text>`.
- `text-anchor="middle"` étale le texte des deux côtés : vérifier qu'il ne mord pas
  sur la boîte voisine.
- Libellé de flèche : **à côté** de la ligne, jamais dessus ; sous la rangée de boîtes
  s'il s'agit d'une liaison horizontale.
- Largeur d'une boîte ≈ 7 × nombre de caractères du `.t1` (à 12 px) + 24.

### Légende
En HTML sous le schéma, pas en SVG :
```html
<div class="legend">
 <span><i style="background:#212529"></i>Capital</span>
 <span><i class="dash" style="color:#9a1b21"></i>Compte courant</span>
 <span><i class="sq" style="background:#9a1b21"></i>Katharsis</span>
</div>
```

## Graphiques — `scripts/charts.py`

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from charts import (barres_verticales, barres_groupees, barres_horizontales,
                    barres_empilees, barres_cumulees, courbe, anneau, eur, pct)
```

| Fonction | Pour montrer |
|---|---|
| `barres_verticales(vals, labels, w, h, couleurs=, hachure=[i])` | une grandeur par année ; `hachure` pour une valeur provisoire |
| `barres_groupees([s1, s2], labels, w, h, noms)` | deux séries comparées (mois N-1 / N) |
| `barres_horizontales([(lib, v)…], w, h, pct_total=)` | classement, répartition par client / poste |
| `barres_empilees(labels, bas, haut, w, h, noms)` | parts en % (mix d'activité) |
| `barres_cumulees(labels, bas, haut, w, h, noms)` | total décomposé en deux (valeur) |
| `courbe([s1, s2], labels, w, h, noms)` | évolution continue (trésorerie, effectif) |
| `anneau([(lib, v)…], centre="56 %", sous="intégration")` | 2 à 4 parts d'un tout |

Règles :
- **Le chiffre est écrit sur le graphique** (valeur au sommet de la barre). Pas d'axe
  gradué : le lecteur ne doit pas mesurer.
- La donnée qui porte le message en bordeaux, le reste en gris (paramètre `couleurs`).
- `w, h` proches du rapport de la carte ; une carte d'un tiers de page ≈ `280, 200`,
  une demi-page ≈ `420, 220`, pleine largeur ≈ `860, 240`.
- Montants : `eur(123456)` → « 123 456 € » ; pourcentages : `pct(12.5, 1)` → « 12,5 % ».
- Un graphique a toujours une carte de lecture à côté ou un `.sub` qui dit ce qu'il montre.

Quand un document a beaucoup de chiffres : les centraliser dans un `data.py`, générer
le HTML par un `build_html.py` qui importe `charts.py`, et ne **jamais** corriger un
chiffre dans le HTML généré.
