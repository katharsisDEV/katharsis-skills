# -*- coding: utf-8 -*-
"""Graphiques SVG inline, aux couleurs de la charte Katharsis.

Chaque fonction renvoie une chaîne <svg class="dg" …> à insérer telle quelle dans
une carte. Aucune dépendance : pas de matplotlib, pas de PNG — le texte reste
vectoriel et net dans le PDF, dans les fontes de la charte.

    import sys; sys.path.insert(0, "<chemin du skill>/scripts")
    from charts import barres_verticales, eur
    svg = barres_verticales([120, 180, 240], ["2024", "2025", "2026"], 420, 220)

Couleurs : accent bordeaux pour la donnée qui porte le message, gris pour le
contexte (année de comparaison, reste). Une donnée provisoire se hachure
(paramètre `hachure`) plutôt que de changer de couleur.

`w` et `h` sont les dimensions du viewBox : les choisir proches du rapport
largeur/hauteur de la carte, sinon le texte est agrandi ou écrasé.
"""
GOLD, GREY, LINE, TXT, MUT = "#9a1b21", "#adb5bd", "#dee2e6", "#212529", "#868e96"

def eur(n, cur=True, dec=0):
    s = f"{n:,.{dec}f}".replace(",", " ").replace(".", ",")
    return s + (" €" if cur else "")

def _lbl(x, y, t, size=8.5, fill=MUT, anchor="middle", weight=400):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-size="{size}" fill="{fill}" font-weight="{weight}">{t}</text>')

def barres_verticales(valeurs, labels, w, h, couleurs=None, fmt=None,
                      hachure=None, top=20, bot=26):
    """Barres verticales avec valeur au sommet."""
    fmt = fmt or (lambda v: eur(v, cur=False))
    couleurs = couleurs or [GOLD] * len(valeurs)
    n = len(valeurs)
    vmax = max(max(valeurs), 0) or 1
    vmin = min(min(valeurs), 0)
    span = vmax - vmin
    ph = h - top - bot
    zero = top + ph * (vmax / span)
    slot = w / n
    bw = min(slot * 0.54, 62)
    o = [f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<line x1="0" y1="{zero:.1f}" x2="{w}" y2="{zero:.1f}" stroke="{LINE}" stroke-width="1"/>')
    for i, v in enumerate(valeurs):
        cx = slot * (i + .5)
        bh = abs(v) / span * ph
        y = zero - bh if v >= 0 else zero
        fill = couleurs[i]
        extra = ''
        if hachure and i in hachure:
            extra = f' fill-opacity=".55" stroke="{fill}" stroke-width="1" stroke-dasharray="3 2"'
        o.append(f'<rect x="{cx-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(bh,1):.1f}" '
                 f'rx="2" fill="{fill}"{extra}/>')
        vy = y - 6 if v >= 0 else y + bh + 11
        o.append(_lbl(cx, vy, fmt(v), 9.5, TXT, weight=600))
        o.append(_lbl(cx, h - 8, labels[i], 9, MUT))
    o.append('</svg>')
    return "".join(o)

def barres_groupees(series, labels, w, h, noms, top=18, bot=24, legende=True):
    """Deux séries côte à côte (mois)."""
    vals = [v for s in series for v in s if v is not None]
    vmax, vmin = max(vals + [0]), min(vals + [0])
    span = vmax - vmin
    ph = h - top - bot - (14 if legende else 0)
    zero = top + ph * (vmax / span)
    n = len(labels)
    slot = w / n
    bw = slot * 0.34
    couleurs = [GREY, GOLD]
    o = [f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    for g in (0.25, 0.5, 0.75):
        y = zero - ph * (vmax / span) * 0 - (zero - top) * g
        o.append(f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}" stroke="{LINE}" stroke-width=".5"/>')
    o.append(f'<line x1="0" y1="{zero:.1f}" x2="{w}" y2="{zero:.1f}" stroke="{LINE}" stroke-width="1"/>')
    for i in range(n):
        for j, s in enumerate(series):
            v = s[i]
            if v is None:
                continue
            x = slot * (i + .5) + (j - .5) * bw * 1.06
            bh = abs(v) / span * ph
            y = zero - bh if v >= 0 else zero
            o.append(f'<rect x="{x-bw/2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(bh,.8):.1f}" '
                     f'rx="1.5" fill="{couleurs[j]}"/>')
        o.append(_lbl(slot * (i + .5), h - (16 if legende else 6), labels[i], 8.5, MUT))
    if legende:
        x = 0
        for j, nom in enumerate(noms):
            o.append(f'<rect x="{x}" y="{h-9}" width="16" height="5" rx="1.5" fill="{couleurs[j]}"/>')
            o.append(_lbl(x + 21, h - 4.2, nom, 8.5, MUT, anchor="start"))
            x += 21 + len(nom) * 4.6 + 20
    o.append('</svg>')
    return "".join(o)

def barres_horizontales(paires, w, h, fmt=None, couleur=None, lw=168, pct_total=None):
    """Libellé à gauche, barre, valeur à droite."""
    fmt = fmt or (lambda v: eur(v))
    n = len(paires)
    row = h / n
    vmax = max(v for _, v in paires) or 1
    bar_x, bar_w = lw, w - lw - 74
    o = [f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    for i, (k, v) in enumerate(paires):
        cy = row * (i + .5)
        col = (couleur[i] if isinstance(couleur, (list, tuple)) else couleur) \
              or (GOLD if i < 2 else (GREY if i >= n - 1 else "#c98a8d"))
        o.append(_lbl(bar_x - 9, cy + 3.2, k, 9, TXT, anchor="end"))
        o.append(f'<rect x="{bar_x}" y="{cy-6.5:.1f}" width="{max(v/vmax*bar_w,1.5):.1f}" height="13" rx="2.5" fill="{col}"/>')
        t = fmt(v) + (f"  ·  {v/pct_total*100:.0f} %" if pct_total else "")
        o.append(_lbl(w, cy + 3.2, t, 9, MUT, anchor="end", weight=600))
    o.append('</svg>')
    return "".join(o)

def barres_empilees(labels, bas, haut, w, h, noms, top=8, bot=44):
    """Barres 100 % : segment bas (accent) + segment haut (gris), part en %."""
    n = len(labels); slot = w / n; bw = min(slot * .5, 70)
    ph = h - top - bot
    o = [f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(n):
        t = bas[i] + haut[i]; pb = bas[i] / t; cx = slot * (i + .5)
        yb = top + ph * (1 - pb)
        o.append(f'<rect x="{cx-bw/2:.1f}" y="{top}" width="{bw:.1f}" height="{ph*(1-pb):.1f}" fill="#dee2e6"/>')
        o.append(f'<rect x="{cx-bw/2:.1f}" y="{yb:.1f}" width="{bw:.1f}" height="{ph*pb:.1f}" fill="{GOLD}"/>')
        lab_y = yb - 6 if pb < .12 else yb + 15
        col = GOLD if pb < .12 else "#ffffff"
        o.append(_lbl(cx, lab_y, f"{pb*100:.0f} %".replace(".", ","), 11, col, weight=600))
        o.append(_lbl(cx, h - bot + 16, labels[i], 9.5, TXT, weight=600))
    x = 0
    for j, (nom, c) in enumerate(zip(noms, [GOLD, "#dee2e6"])):
        o.append(f'<rect x="{x}" y="{h-11}" width="16" height="7" rx="1.5" fill="{c}"/>')
        o.append(_lbl(x + 21, h - 4.5, nom, 9, MUT, anchor="start"))
        x += 21 + len(nom) * 4.9 + 22
    o.append('</svg>')
    return "".join(o)

def barres_cumulees(labels, bas, haut, w, h, noms, top=22, bot=44):
    """Barres empilées en valeur : bas (gris) + haut (accent), total au sommet."""
    n = len(labels); slot = w / n; bw = min(slot * .52, 66)
    tot = [a + b for a, b in zip(bas, haut)]; vmax = max(tot)
    ph = h - top - bot; base = top + ph
    o = [f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
         f'<line x1="0" y1="{base}" x2="{w}" y2="{base}" stroke="{LINE}" stroke-width="1"/>']
    for i in range(n):
        cx = slot * (i + .5); ha = bas[i] / vmax * ph; hb = haut[i] / vmax * ph
        o.append(f'<rect x="{cx-bw/2:.1f}" y="{base-ha:.1f}" width="{bw:.1f}" height="{ha:.1f}" fill="#c9ced4"/>')
        o.append(f'<rect x="{cx-bw/2:.1f}" y="{base-ha-hb:.1f}" width="{bw:.1f}" height="{hb:.1f}" fill="{GOLD}"/>')
        o.append(_lbl(cx, base - ha - hb - 6, eur(tot[i], cur=False), 9.5, TXT, weight=600))
        o.append(_lbl(cx, h - bot + 16, labels[i], 9, MUT))
    x = 0
    for nom, c in zip(noms, ["#c9ced4", GOLD]):
        o.append(f'<rect x="{x}" y="{h-11}" width="16" height="7" rx="1.5" fill="{c}"/>')
        o.append(_lbl(x + 21, h - 4.5, nom, 9, MUT, anchor="start"))
        x += 21 + len(nom) * 4.9 + 22
    o.append('</svg>')
    return "".join(o)


def courbe(series, labels, w, h, noms=None, fmt=None, top=22, bot=26):
    """Une ou deux courbes (évolution) ; la première en accent, valeur au dernier point."""
    fmt = fmt or (lambda v: eur(v, cur=False))
    vals = [v for s in series for v in s if v is not None]
    vmax, vmin = max(vals + [0]), min(vals + [0])
    span = (vmax - vmin) or 1
    leg = 14 if noms else 0
    ph = h - top - bot - leg
    n = len(labels); slot = w / n
    y = lambda v: top + ph * (vmax - v) / span
    couleurs = [GOLD, GREY]
    o = [f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
         f'<line x1="0" y1="{y(0):.1f}" x2="{w}" y2="{y(0):.1f}" stroke="{LINE}" stroke-width="1"/>']
    for j, s in enumerate(series):
        pts = [(slot * (i + .5), y(v)) for i, v in enumerate(s) if v is not None]
        d = " ".join(f"{'M' if k == 0 else 'L'}{px:.1f},{py:.1f}" for k, (px, py) in enumerate(pts))
        o.append(f'<path d="{d}" fill="none" stroke="{couleurs[j]}" stroke-width="{2.2 if j == 0 else 1.6}"/>')
        for px, py in pts:
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{3 if j == 0 else 2.4}" fill="#fff" stroke="{couleurs[j]}" stroke-width="1.6"/>')
        if j == 0 and pts:
            px, py = pts[-1]
            o.append(_lbl(px, py - 9, fmt([v for v in s if v is not None][-1]), 9.5, TXT, weight=600))
    for i, l in enumerate(labels):
        o.append(_lbl(slot * (i + .5), h - 8 - leg, l, 9, MUT))
    if noms:
        x = 0
        for j, nom in enumerate(noms):
            o.append(f'<rect x="{x}" y="{h-9}" width="16" height="3" rx="1" fill="{couleurs[j]}"/>')
            o.append(_lbl(x + 21, h - 4.2, nom, 8.5, MUT, anchor="start"))
            x += 21 + len(nom) * 4.6 + 20
    o.append('</svg>')
    return "".join(o)


def anneau(parts, w=220, h=220, centre=None, sous=None):
    """Répartition en anneau (2 à 4 parts). parts = [(libellé, valeur), …] ;
    la première part est en accent. Légende en HTML à côté (voir references)."""
    import math
    cols = [GOLD, "#6c757d", GREY, LINE]
    tot = sum(v for _, v in parts) or 1
    cx, cy, r, ep = w / 2, h / 2, min(w, h) / 2 - 6, min(w, h) * .16
    o = [f'<svg class="dg" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    a0 = -math.pi / 2
    for i, (_, v) in enumerate(parts):
        a1 = a0 + 2 * math.pi * v / tot
        large = 1 if a1 - a0 > math.pi else 0
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1 - 1e-4), cy + r * math.sin(a1 - 1e-4)
        o.append(f'<path d="M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} 1 {x1:.2f},{y1:.2f}" '
                 f'fill="none" stroke="{cols[i % 4]}" stroke-width="{ep:.1f}"/>')
        a0 = a1
    if centre:
        o.append(_lbl(cx, cy + 6, centre, 20, TXT, weight=600))
    if sous:
        o.append(_lbl(cx, cy + 22, sous, 9, MUT))
    o.append('</svg>')
    return "".join(o)


def pct(n, dec=0):
    """12.5 → '12,5 %' avec espace insécable."""
    return f"{n:.{dec}f}".replace(".", ",") + "\u00a0%"


if __name__ == "__main__":
    # démonstration : python charts.py > demo.svg.html
    print(barres_verticales([98000, 178472, 222942], ["2024", "2025", "2026"], 420, 220, hachure=[2]))
