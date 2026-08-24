# Canonical K2P and K3P theta-trinet collision package

This directory is the sole current manuscript and reproducibility package for
the exact K2P/K3P tree--theta-trinet collision results. Use it for reading,
verification, citation, bioRxiv submission, and any archival deposit.

The submission snapshot is version `1.0.0`, published under the Git tag
`k2p-k3p-theta-biorxiv-v1.0.0`. The tag, rather than the mutable `main` branch,
is the stable source cited by the manuscript.

The similarly named files one directory above are preserved pre-clarification
history. They are not current submission or release inputs.

## Manuscript

- `combined-paper-clarified.tex` / `.pdf`: canonical manuscript.
- `technical-summary-clarified.tex` / `.pdf`: technical overview.
- `k2p_displayed_tree_clarification.tex` / `.pdf`: focused clarification note
  retained for provenance; it is not a replacement manuscript.

The manuscript makes the displayed-tree edge placement and the derivation of
the four-switching matrix explicit. The exact certificates and verifier suite
cover the compact K2P collision, strict continuous-time K2P collision,
fixed-order audit, K2P ranks and collision families, K3P collision, K3P rank,
and analytic continuous-time extension.

## Exact replay

Python 3.10 or newer and the standard library are needed.

```bash
python3 verify_k2p_simple.py
python3 verify_k2p_displayed_trees.py
python3 verify.py
```

The graph-based verifier begins with the rooted arc list, deletes the two
unselected reticulation arcs in each switching, derives descendant labels and
Fourier monomials, and independently performs ordinary-state Markov pruning.
Successful complete output ends with:

```text
ALL EXACT CHECKS PASSED
```

The stored `verification_report_*.txt` files are transcripts, not substitutes
for replaying the current code and certificates.

`manifest.sha256` covers the committed files intended for the public replay
archive, apart from itself. It deliberately omits the author-only
`submission/biorxiv/` staging worksheets, which are not supplement content.
From this directory, check it with `sha256sum -c manifest.sha256` (or
`shasum -a 256 -c manifest.sha256` on systems without `sha256sum`).

## PDF build

Use a TeX installation providing either `latexmk` with `pdflatex`, or
`tectonic`, together with TikZ:

```bash
bash src/build_pdfs.sh
```

## Citation and licenses

- `CITATION.cff` describes the research package and its preferred manuscript
  citation.
- `LICENSE-CODE` applies the MIT License only to executable `.py` and `.sh`
  source files in this canonical directory.
- `LICENSES.md` records the boundaries between code, manuscript, certificates,
  and the author-selected bioRxiv distribution option.

No bioRxiv manuscript license is selected in this repository. The author must
make that choice deliberately in the bioRxiv upload form.

## bioRxiv and archival preparation

The dated official-requirements audit, metadata worksheet, and final upload
checklist are in [`submission/biorxiv/`](submission/biorxiv/). These are
author-facing staging files and the release builder excludes them from the
supplement. Before portal approval, replace every applicable placeholder and
make the portal metadata match the final PDF exactly.

To build clean deterministic archives from an exact committed snapshot:

```bash
bash submission/build_release.sh --output-dir /absolute/path/to/release-output --version 1.0.0
```

The builder refuses tracked or untracked changes in this canonical subtree,
uses `git archive`, excludes ignored caches and all `submission/biorxiv/`
author-only files, creates ZIP and `.tar.gz` forms, and emits both combined and
per-archive SHA-256 sidecars. Each archive also contains
`RELEASE_PROVENANCE.txt` with its full commit/version and `FILE_SHA256SUMS`
covering exactly the committed files included in the archive. Do not use or
refresh the historical parent-directory ZIP for a new deposit.

The archive opens directly into a single versioned directory containing this
README and the replay files; no monorepo checkout is needed.
