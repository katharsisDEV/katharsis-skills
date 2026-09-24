#!/usr/bin/env python3
"""Extrait tout ce qu'il faut pour lire une présentation source.

    python ingest_pdf.py <source.pdf> <dossier-de-travail> [--dpi 110]

Produit :
  <dossier>/pages/pNN.png   une image par page, à regarder
  <dossier>/images/         les images intégrées assez grandes pour être réutilisées
                            (plans, photos) — nommées <page>_<largeur>x<hauteur>
et affiche le texte page par page sur la sortie standard.

Les zones vides d'une présentation ne laissent aucune trace dans le texte : il faut
regarder les PNG. C'est pour ça que le script les produit systématiquement.
"""
import sys, os, argparse

try:
    import pymupdf
except ImportError:
    sys.exit("pymupdf manquant :\n"
             f"  uv pip install --python {sys.executable} pymupdf")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("outdir")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--min-pixels", type=int, default=20000,
                    help="seuil au-dessous duquel une image intégrée est ignorée")
    a = ap.parse_args()

    doc = pymupdf.open(a.source)
    pages_dir = os.path.join(a.outdir, "pages")
    imgs_dir = os.path.join(a.outdir, "images")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(imgs_dir, exist_ok=True)

    r = doc[0].rect
    orient = "paysage" if r.width > r.height else "portrait"
    print(f"# {os.path.basename(a.source)}")
    print(f"{doc.page_count} pages · {r.width:.0f} × {r.height:.0f} pt · {orient}")
    meta = {k: v for k, v in (doc.metadata or {}).items() if v}
    if meta:
        print("métadonnées : " + ", ".join(f"{k}={v}" for k, v in meta.items()))
    print()

    kept = []
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=a.dpi).save(os.path.join(pages_dir, f"p{i:02d}.png"))

        print("=" * 72)
        print(f"--- PAGE {i} ---")
        text = page.get_text().strip()
        print(text if text else "(aucun texte)")

        for info in page.get_images(full=True):
            xref = info[0]
            try:
                d = doc.extract_image(xref)
            except Exception:
                continue
            w, h = d["width"], d["height"]
            if w * h < a.min_pixels:
                continue
            fn = f"p{i:02d}_{w}x{h}_{xref}.{d['ext']}"
            with open(os.path.join(imgs_dir, fn), "wb") as f:
                f.write(d["image"])
            kept.append((i, fn, w, h))
        print()

    print("=" * 72)
    print(f"Pages rendues  : {pages_dir}/p01.png … p{doc.page_count:02d}.png")
    print("               → les lire avec l'outil Read, une zone vide ne se voit que là")
    if kept:
        print(f"\nImages extraites ({len(kept)}) dans {imgs_dir} :")
        for pno, fn, w, h in kept:
            print(f"  page {pno:>2}  {w:>5} × {h:<5}  {fn}")
        print("\n  Plans et photos : à conserver et recadrer.")
        print("  Captures de synoptiques : à redessiner en SVG, ne pas réutiliser.")
    else:
        print("\nAucune image intégrée notable.")


if __name__ == "__main__":
    main()
