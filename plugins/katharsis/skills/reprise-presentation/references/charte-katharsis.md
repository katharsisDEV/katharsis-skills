# Charte Katharsis Event

Relevée sur katharsis-event.fr (styles calculés, pas approximés) et confirmée par
le logo, dont le tracé est en `#9a1c20`.

## Tokens

| Rôle | Valeur |
|---|---|
| Titres | Poppins 600 |
| Texte courant | Inter 400 / 600 |
| Fond de page | `#ffffff` |
| Cartes | `#f8f9fa`, filet `#dee2e6`, rayon 10 pt |
| Texte | `#212529` · secondaire `#3f464e` · atténué `#868e96` |
| Accent | **`#9a1b21`** — bordeaux de la marque |
| Aplat accent | `#fbf2f2`, filet `#e3bfc1` |
| Pastilles | rayon 100 pt — reprend les boutons du site |

Tout est déjà dans `assets/theme.css` sous forme de variables CSS ; le copier tel
quel plutôt que de le réécrire.

## Signatures visuelles

- **Mot accentué** dans le titre de couverture : `<h1>Medeline <em>Lumière</em></h1>`
  met le dernier mot en bordeaux, comme le hero du site.
- **Pastille de section** en haut de chaque page (`.eyebrow`), pas un simple libellé.
- **Couverture en deux colonnes** : texte à gauche, visuel à droite dans un cadre
  arrondi — reprend la structure du hero. Le plan du projet fait un bon visuel.
- **Logo** en couverture (haut droite) et dans chaque pied de page.

## Code couleur des schémas

Dérivé de la palette du site, sans couleur inventée. Trois teintes suffisent à
distinguer les flux et restent lisibles à l'impression :

| Flux | Couleur | Classe |
|---|---|---|
| DMX512 / signal principal | `#9a1b21` | `.dmx` |
| Réseau (Art-Net, sACN, eDMX) | `#212529` | `.net` |
| Sortie secondaire (SPI, LED, 24 V) | `#6c757d` | `.spi` |
| Puissance 230 V | `#adb5bd` pointillé | `.pwr` |

Deux pastilles de légende de la même couleur sur une même page = erreur de lecture.
Si deux éléments partagent une teinte, en retirer un de la légende ou le nommer
autrement dans le texte.

Les repères d'un plan existant (souvent en rouge, `#9e0025` sur les plans de Medeline)
se **conservent tels quels** : ils viennent du plan d'origine et s'accordent au
bordeaux. Recolorier un plan fourni est une mauvaise idée.

## Fontes — le piège des fontes variables

Utiliser les **instances statiques** livrées dans `assets/fonts/`, jamais la version
variable d'Inter servie par Google Fonts.

Chrome embarque une fonte variable sous forme de **Type3** dans le PDF : un objet de
fonte par mot, fichier qui double de volume, texte inexploitable à l'extraction. Les
statiques s'embarquent proprement en TrueType.

`→` et `Ω` ne sont pas dans le sous-ensemble latin d'Inter et retombent sur Arial.
C'est invisible à l'œil, inutile de chercher à le corriger.

## Rythme des pages

En-tête ≈ 75 pt : pastille, titre 25 pt, filet 62 × 2 pt.
Corps en flex, pied de page en absolu à 20 pt du bas.
Marges 30 pt en haut, 46 pt sur les côtés.

Une page tient environ **384 pt de contenu**. Un tableau dense y loge 13 à 15 lignes
selon le nombre de retours à la ligne. Au-delà, découper sur deux pages plutôt que
réduire la typo.
