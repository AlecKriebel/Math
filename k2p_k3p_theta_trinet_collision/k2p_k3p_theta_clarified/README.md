# Canonical K2P and K3P theta-trinet collision package

This directory is the sole current manuscript and reproducibility package for
the exact K2P/K3P tree--theta-trinet collision results. Use it for reading,
verification, citation, bioRxiv submission, and any archival deposit.

The current submission snapshot is version `1.2.2`, published under the Git tag
`k2p-k3p-theta-v1.2.2`. The tag, rather than the mutable `main` branch,
is the stable source cited by the manuscript.

Historical pre-clarification files have been moved into the parent
`legacy/DO_NOT_SUBMIT-pre-clarification/` directory. They are not current
submission or release inputs. Immutable versions `1.2.1`, `1.2.0`, and `1.1.0`
are retained under the parent `releases/` directory, and version `1.0.0`
remains under `legacy/releases/`.

## Manuscript

- `combined-paper-clarified.tex` / `.pdf`: canonical manuscript.
- `technical-summary-clarified.tex` / `.pdf`: technical overview.
- `k2p_displayed_tree_clarification.tex` / `.pdf`: focused clarification note
  retained for provenance; it is not a replacement manuscript.

The manuscript makes the displayed-tree edge placement and the derivation of
the four-switching matrix explicit. The exact certificates and verifier suite
cover the compact and edgewise strictly continuous-time K2P collisions,
fixed-order audit, K2P ranks and collision families, exact K3P
parameter-symmetry distinction, K3P rank and analytic extension, local
fixed-output fiber dimensions, and an exact four-leaf grafting regression.
Here `edgewise` means that each edge separately admits a positive-rate
generator; no shared generator, rate ratio, molecular clock, or global
temporal compatibility is asserted.

The K2P construction is an exact counterexample to the arbitrary-level K2P
statements in arXiv:2607.12919v2. Version 3 removes those statements, records
the leaf-order obstruction, and leaves high-level K2P and K3P questions open.
Because K2P is nested in K3P, the compact K2P collision answers both questions
negatively. The separate quartic construction gives an exact theta-network
parameter outside every globally character-relabeled K2P specialization,
although its shared distribution lies in a globally character-relabeled K2P
tree model. Here the same character permutation is imposed on every edge and
leaf; edge-dependent relabelings are excluded. Full K3P rank yields nearby
shared distributions outside all globally character-relabeled K2P models.

The full-rank results also give Zariski-dense fixed-theta images, local
collision loci of dimensions 17 and 23, and fixed-output network fibers of
dimensions 11 and 14. A common-subtree theorem replaces any selected internal
vertex of any labelled unrooted binary tree by one theta blob while preserving
all leaf-pattern probabilities. This is a single-blob theorem, not a claim
that multiple replacements compose. The corrected source paper's JC and
level-one results are not affected.

## Exact replay

Python 3.10 or newer and the standard library are needed.

```bash
python3 verify_k2p_simple.py
python3 verify_k2p_displayed_trees.py
python3 src/verify_k2p_four_leaf_graft.py
python3 verify.py
PYTHONOPTIMIZE=1 python3 verify.py
```

The graph-based verifier begins with the rooted arc list, deletes the two
unselected reticulation arcs in each switching, derives descendant labels and
Fourier monomials, and independently performs ordinary-state Markov pruning.
The four-leaf verifier checks all 256 Fourier coordinates and all 256 pattern
probabilities for one exact pendant-subtree lift; the universal all-tree result
is proved by the manuscript's common-kernel argument rather than by finite
enumeration.
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
bash submission/build_release.sh --output-dir /absolute/path/to/release-output --commit k2p-k3p-theta-v1.2.2 --version 1.2.2
```

The builder refuses tracked or nonignored untracked changes in this canonical subtree,
requires the requested version, `CITATION.cff`, and release tag to identify the
same commit, verifies the canonical manifest and stored transcripts, and
rebuilds and compares the PDFs in a clean extraction. It uses `git archive`,
excludes ignored caches and all `submission/biorxiv/` author-only files,
creates ZIP and `.tar.gz` forms, and emits both combined and per-archive SHA-256
sidecars. Each archive also contains
`RELEASE_PROVENANCE.txt` with its full commit/version and `FILE_SHA256SUMS`
covering exactly the committed files included in the archive. Do not use or
refresh the historical parent-directory ZIP for a new deposit.

The archive opens directly into a single commit-addressed directory containing this
README and the replay files; no monorepo checkout is needed.
