# Schémas SVG

Les synoptiques sont dessinés en SVG inline dans le HTML. Les classes utilitaires
(`.box`, `.dmx`, `.t1`…) sont définies dans `theme.css` : les schémas suivent donc
automatiquement la charte, y compris si les couleurs changent plus tard.

## Marqueurs de flèches — une seule fois par document

À placer juste après `<body>`. Les `marker-end` des classes y font référence ;
un seul bloc suffit pour tous les schémas de la page.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <marker id="ar-dmx" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9a1b21"/></marker>
  <marker id="ar-net" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#212529"/></marker>
  <marker id="ar-spi" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#6c757d"/></marker>
  <marker id="ar-pwr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#adb5bd"/></marker>
</defs></svg>
```

## Classes disponibles

| Classe | Usage |
|---|---|
| `.box` | boîte neutre |
| `.box-g` | élément central ou accentué — contour bordeaux |
| `.box-r` | sortie, appareil terminal — aplat rosé |
| `.box-n` | équipement réseau |
| `.zone` | regroupement en pointillés |
| `.t1` `.t2` `.t3` | titre de boîte, sous-titre, annotation |
| `.tk` | intertitre bordeaux en capitales |
| `.tr` | repère bordeaux (numéro d'univers, de ligne) |
| `.dmx` `.net` `.spi` `.pwr` | liaisons fléchées |
| `.dmx0` | liaison DMX sans flèche (chaînage) |

## Motifs

**Synoptique en étages** — commande / distribution / diffusion. Un intertitre `.tk`
et un filet par étage, les boîtes alignées dessous, les liaisons verticales entre.

```html
<text class="tk" x="0" y="9">COMMANDE</text>
<line x1="0" y1="16" x2="620" y2="16" stroke="#dee2e6"/>
<rect class="box-g" x="0" y="26" width="196" height="46" rx="8"/>
<text class="t1" x="12" y="45">Ordinateur régie</text>
<text class="t2" x="12" y="61">MadMapper + ONYX</text>
<path class="net" d="M98,72 L98,127"/>
```

**Chaînage en guirlande** — appareils identiques en série, terminaison en bout.
Dessiner les segments en `.dmx0` (sans flèche) entre les boîtes, et refermer sur un
petit rectangle `fill="#fbf2f2" stroke="#9a1b21"` légendé « 120 Ω ».

**Chaîne numérotée** — quand le document d'origine listait « 01 Interface, 02 Ligne,
03 Drivers… », reprendre ces numéros en `.tk` au-dessus de chaque élément. Le lecteur
retrouve la liste qu'il connaît, devenue schéma.

**Élévation de principe** — pour une implantation (comptoir, étagères), un panneau
`fill="#f8f9fa"` et des rectangles `#e9ecef` pour le mobilier, les sources lumineuses
en bordeaux. Suffisant pour situer, sans prétendre au plan d'exécution.

## Placement du texte

Les collisions sont le défaut le plus fréquent, et elles ne se voient qu'au rendu.

- Un libellé de liaison se place **sous** la ligne des boîtes, pas à leur hauteur :
  centré sur la flèche, à une vingtaine d'unités sous le bas des boîtes.
- `text-anchor="middle"` élargit le texte de part et d'autre du point d'ancrage —
  vérifier que la moitié gauche ne recouvre pas la boîte précédente.
- Un texte long dans une boîte `.box-r` déborde sans prévenir : SVG ne renvoie pas
  à la ligne. Raccourcir, ou passer sur deux `<text>`.

## Légende

Sous le schéma, en HTML plutôt qu'en SVG — c'est plus simple à faire évoluer :

```html
<div class="legend">
  <span><i style="background:#9a1b21"></i>DMX512</span>
  <span><i style="background:#212529"></i>Réseau eDMX</span>
</div>
```
