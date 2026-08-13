# Publication package

This directory contains the publication form of the T3-2 result.

- `main.tex` is the main article.
- `technical-supplement.tex` is the cover and index for the full local-proof
  dossier.
- `supplement/` contains mechanically generated LaTeX fragments of the exact
  audited theorem notes.  The source Markdown files and their SHA-256 hashes
  are listed in `supplement-manifest.txt`.
- `build_publication.sh` performs a read-only hash check, regenerates the
  supplement fragments, and compiles both PDFs.
- `postprocess_supplement.py` applies publication-only mechanical layout
  normalization to generated fragments; it never changes authenticated proof
  notes.
- Final PDFs are written to `../output/pdf/`; rendered page images used for
  visual QA are written under `../tmp/pdfs/` and are not publication inputs.

The finite Python certificate verifies finite support, tier, affine, and set
identities only.  It is not used to search reaction orientations, stochastic
paths, or population boxes, and it supplies no drift estimate.

Author metadata is intentionally not hard-coded in the research package.
It can be added to `main.tex` immediately before submission without changing
the mathematics or the audited proof dossier.

The current build produces a 7-page main article and a 189-page supplement
with warning-free TeX logs. Historical status language inside early frozen
fragments is explicitly superseded by the editorial note and final Sections
39--40.
