# Latest main-paper TeX sources

This folder was assembled from the local working tree of the Math repository
at commit `f6f9a1598d760e55efd7b55d137d4d00e8b3545f` on 2026-08-27. The selected
source paths were clean relative to Git when copied.

Exactly four files in this collection contain `\\documentclass`, one for each
requested main paper. Supporting `.tex`, `.tikz`, and `.bib` files are included
only when loaded by one of those four entry points.

## 1. STC/JC sharp boundary

- Entry point: `01_stc_jc_sharp_boundary/main.tex`
- Original: `s_tc_jc_landmark_closure/source/paper/main.tex`
- Rationale: the project README explicitly names `source/paper/main.tex` as the
  manuscript source.
- Included dependencies: `references.bib` and the seven TeX figures loaded by
  the entry point.

## 2. K2P/K3P theta-trinet collision

- Entry point: `02_k2p_k3p_theta_collision/combined-paper-clarified.tex`
- Original:
  `k2p_k3p_theta_trinet_collision/k2p_k3p_theta_clarified/combined-paper-clarified.tex`
- Rationale: the package README calls this the canonical manuscript and calls
  the other document-class TeX files a technical overview and a provenance
  clarification note.
- Included dependency: `figures/theta_network.tikz`.
- The package-level `references.bib` is not included because this manuscript
  uses an inline `thebibliography` and does not load that file.

## 3. K2P level-2 identifiability

- Entry point: `03_k2p_level2_identifiability/main.tex`
- Original:
  `k2p_level2_identifiability_closure/proof_compression_submission/article/main.tex`
- Rationale: the project README identifies `article/main.tex` and
  `article/references.bib` as the article source pair.
- Included dependency: `references.bib`.

## 4. K3P level-2 identifiability

- Entry point: `04_k3p_level2_identifiability/main.tex`
- Original: `k3p_level2_identifiability_final/manuscript/main.tex`
- Rationale: the project README identifies the `manuscript` tree as the
  canonical article, while submission wrappers and the reader supplement are
  separate products.
- Included dependencies: `references.bib`, all 17 section files loaded by the
  entry point, and all four TeX figures loaded by those sections.

## Exclusions

No supplement TeX, journal wrapper, arXiv wrapper, cover letter, technical
summary, clarification note, frozen input, historical manuscript, release-copy
duplicate, draft-gap note, PDF, auxiliary build file, or computational artifact
was copied.

## Validation

- All 36 source files are byte-for-byte copies of the selected local originals.
- The collection contains exactly four `\\documentclass` entry points and no
  supplement-named TeX source files.
- Tectonic 0.16.9 compiled papers 1--3 directly from the collection (33, 20,
  and 26 pages, respectively).
- The byte-exact latest K3P source contains a pre-existing delimiter typo at
  `sections/17_reproducibility.tex:40`: `(5\\)-minor` instead of
  `\\(5\\)-minor`. The exact source was preserved rather than silently edited.
  A temporary one-character validation repair allowed the fourth paper to
  compile completely (38 pages), showing that the copied dependency set is
  otherwise complete.
