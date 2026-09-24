#!/usr/bin/env python3
"""Détecte le contenu rogné dans un deck HTML, et contrôle les liens d'un PDF.

    python check_layout.py <deck.html> [autre.html ...]
    python check_layout.py --links <sortie.pdf>

Le thème coupe proprement ce qui dépasse d'une carte (`overflow:hidden`), donc une
ligne de tableau ou une puce peut disparaître du PDF sans aucun signe dans le HTML.
C'est le mode de défaillance dominant de ce format, et il est invisible tant qu'on
ne compare pas scrollHeight et clientHeight dans le navigateur.

Le script injecte une sonde dans une copie temporaire du fichier, la charge dans
Chrome headless une fois les fontes prêtes, et rapporte chaque élément rogné avec
sa page et son intitulé.

Quand un élément déborde, retirer du contenu plutôt que réduire la typo : le
rétrécissement en cascade abîme tout le document.
"""
import sys, os, re, json, html, subprocess, argparse

CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

PROBE = """
<script>
(function () {
  // On mesure les lignes de texte, pas les elements : un paragraphe qui contient
  // du <b> n'est pas une feuille, et sa derniere ligne passerait inapercue. Un
  // Range sur chaque noeud texte donne un rectangle par ligne rendue — c'est la
  // seule mesure qui attrape une ligne coupee en deux par le bord d'une carte.
  function inside(node, box, sel) {
    for (var p = node.parentElement; p && p !== box; p = p.parentElement)
      if (p.matches(sel)) return true;
    return false;
  }
  function scan(box, skipSel) {
    var br = box.getBoundingClientRect();
    var clipBottom = br.top + box.clientTop + box.clientHeight;
    var w = document.createTreeWalker(box, NodeFilter.SHOW_TEXT, null);
    var node, worst = null;
    while ((node = w.nextNode())) {
      var t = node.textContent.trim();
      if (!t) continue;
      if (skipSel && inside(node, box, skipSel)) continue;
      var range = document.createRange();
      range.selectNodeContents(node);
      var rects = range.getClientRects();
      for (var i = 0; i < rects.length; i++) {
        var lost = rects[i].bottom - clipBottom;
        if (lost > 1 && (!worst || lost > worst.lost))
          worst = { lost: Math.round(lost), text: t.slice(0, 70) };
      }
    }
    return worst;
  }
  function measure() {
    var cut = [], tight = [];
    document.querySelectorAll('.slide').forEach(function (slide, si) {
      var f = slide.querySelector('.foot span:last-child');
      var page = f ? f.textContent.trim() : String(si + 1);

      var boxes = [].slice.call(slide.querySelectorAll('.card, .toc')).map(function (b) {
        return { el: b, skip: null };
      });
      boxes.push({ el: slide, skip: '.card, .toc, .foot' });

      boxes.forEach(function (b) {
        var l = b.el.querySelector('.lbl');
        var name = (l ? l.textContent
                      : (b.el === slide ? '(hors carte)' : b.el.className))
                     .trim().slice(0, 64);
        var worst = scan(b.el, b.skip);
        if (worst) cut.push({ page: page, label: name, lost: worst.lost, text: worst.text });
        else if (b.el.scrollHeight - b.el.clientHeight > 1)
          tight.push({ page: page, label: name,
                       over: b.el.scrollHeight - b.el.clientHeight });
      });
    });
    var d = document.createElement('div');
    d.id = '__probe__';
    d.textContent = JSON.stringify({ cut: cut, tight: tight });
    document.body.appendChild(d);
  }
  var go = function () { setTimeout(measure, 120); };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(go);
  else window.addEventListener('load', go);
})();
</script>
"""


def check_html(path):
    src = open(path, encoding="utf-8").read()
    if "</body>" in src:
        probed = src.replace("</body>", PROBE + "</body>", 1)
    else:
        probed = src + PROBE
    # la copie doit rester dans le meme dossier : theme.css et assets/ sont relatifs
    tmp = os.path.join(os.path.dirname(os.path.abspath(path)), ".__check.html")
    open(tmp, "w", encoding="utf-8").write(probed)
    try:
        dom = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
             "--virtual-time-budget=8000", "--dump-dom", "file://" + tmp],
            capture_output=True, text=True, timeout=120).stdout
    finally:
        os.path.exists(tmp) and os.remove(tmp)

    m = re.search(r'<div id="__probe__">(.*?)</div>', dom, re.S)
    if not m:
        print(f"{path} : sonde non exécutée — Chrome introuvable ou page en erreur ?")
        return 2
    try:
        res = json.loads(html.unescape(m.group(1)))
    except json.JSONDecodeError:
        print(f"{path} : sonde illisible")
        return 2

    name = os.path.basename(path)
    cut, tight = res.get("cut", []), res.get("tight", [])

    if cut:
        print(f"!!  {name} — {len(cut)} bloc(s) de texte coupe(s) :")
        for it in cut:
            print(f"      page {it['page']:>3}  «{it['label']}»")
            print(f"                  perdu : «{it['text']}» ({it['lost']} px sous la coupe)")
        print("      → retirer du contenu (fusionner une puce, raccourcir une")
        print("        formulation, supprimer une ligne redondante), pas reduire la typo")
    if tight:
        print(f"{'    ' if cut else 'i   '}{'' if cut else name + ' — '}"
              f"{len(tight)} carte(s) sans marge basse (texte entier, respiration mangee) :")
        for it in tight:
            print(f"      page {it['page']:>3}  «{it['label']}»  — {it['over']} px")
    if not cut and not tight:
        print(f"OK  {name} — rien de coupe")
    return 1 if cut else 0


def check_links(path):
    try:
        import pymupdf
    except ImportError:
        sys.exit(f"pymupdf manquant :\n  uv pip install --python {sys.executable} pymupdf")
    d = pymupdf.open(path)
    r = d[0].rect
    print(f"{os.path.basename(path)} : {d.page_count} pages · "
          f"{r.width:.0f} × {r.height:.0f} pt · "
          f"{'paysage' if r.width > r.height else 'PORTRAIT'}")
    seen = {}
    for i, p in enumerate(d, 1):
        for l in p.get_links():
            if l.get("uri"):
                seen.setdefault(l["uri"], []).append(i)
    if not seen:
        print("  aucun lien — si le document cite des fiches fabricants, "
              "elles ne sont pas cliquables")
        return 1
    print(f"  {sum(len(v) for v in seen.values())} liens, {len(seen)} URL distinctes :")
    for u, pages in sorted(seen.items()):
        print(f"    p{','.join(map(str, pages)):<10} {u}")
    print("  → vérifier chaque URL avec curl avant diffusion")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--links", action="store_true",
                    help="contrôler les liens et le format d'un PDF au lieu du HTML")
    a = ap.parse_args()
    rc = 0
    for f in a.files:
        rc = max(rc, check_links(f) if a.links else check_html(f))
    sys.exit(rc)
