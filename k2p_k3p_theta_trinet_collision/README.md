# Exact K2P and K3P theta-trinet collisions

A binary semi-directed strict level-two theta trinet with a genuine nontrivial
3-blob shares an exact three-leaf distribution with a three-star tree under
both the Kimura two-parameter (K2P) and three-parameter (K3P) substitution
models.

## Canonical version

**Use only [`k2p_k3p_theta_clarified/`](k2p_k3p_theta_clarified/) for reading,
verification, citation, submission, or archival deposit.** Open the current
[`combined-paper-clarified.pdf`](k2p_k3p_theta_clarified/combined-paper-clarified.pdf)
or its [`combined-paper-clarified.tex`](k2p_k3p_theta_clarified/combined-paper-clarified.tex)
source directly.

The current frozen submission/replay snapshot is version `1.1.0`, identified by
the venue-neutral Git tag `k2p-k3p-theta-v1.1.0`.

All superseded parent-level files have been moved together under
[`legacy/DO_NOT_SUBMIT-pre-clarification/`](legacy/DO_NOT_SUBMIT-pre-clarification/).
The immutable version `1.0.0` replay archive is retained separately under
[`legacy/releases/`](legacy/releases/). Nothing under `legacy/` is a current
submission input.

The K2P witness is an exact counterexample to Lemma 5.6 and the K2P part of
Corollary 5.8 in arXiv:2607.12919v2. Version 3 removes those K2P statements,
records the leaf-order obstruction, and leaves high-level K2P and K3P trinet
questions open. The exact K2P and K3P collisions here answer both questions
negatively. Neither result affects the corrected paper's JC or level-one
results.

## Replay the canonical package

Python 3.10 or newer and the standard library are required.

```bash
cd k2p_k3p_theta_clarified
python3 verify_k2p_simple.py
python3 verify_k2p_displayed_trees.py
python3 verify.py
PYTHONOPTIMIZE=1 python3 verify.py
```

The focused displayed-tree verifier reconstructs the four displayed trees from
the rooted graph and checks all 64 ordinary-state probabilities by exact Markov
pruning. The complete suite additionally checks the edgewise strictly continuous-time K2P
witness, fixed-order audit, all-six-order sign point, K2P ranks and collision
families, and the K3P collision, rank, and edgewise continuous-time analytic
implicit-function data. Edgewise embeddability allows a different generator
and rate ratio on each edge and imposes no molecular clock or global timing.
Successful complete output ends with `ALL EXACT CHECKS PASSED`.

## Canonical files

- `k2p_k3p_theta_clarified/combined-paper-clarified.tex` / `.pdf`: manuscript.
- `k2p_k3p_theta_clarified/technical-summary-clarified.tex` / `.pdf`: technical overview.
- `k2p_k3p_theta_clarified/k2p_displayed_tree_clarification.tex` / `.pdf`: focused historical clarification note.
- `k2p_k3p_theta_clarified/verify.py` and its companion modules: exact replay suite.
- `k2p_k3p_theta_clarified/certificate_*.json`: exact certificates.
- `k2p_k3p_theta_clarified/submission/biorxiv/`: bioRxiv metadata and upload checklist.
- `k2p_k3p_theta_clarified/CITATION.cff`: citation metadata.
- `k2p_k3p_theta_clarified/LICENSES.md`: package licensing boundaries.
- `legacy/`: superseded drafts and immutable historical release archives, kept
  outside the current submission path.

## Build and release

```bash
cd k2p_k3p_theta_clarified
bash src/build_pdfs.sh
bash submission/build_release.sh --output-dir /absolute/path/to/release-output --commit k2p-k3p-theta-v1.1.0 --version 1.1.0
```

The release builder archives only the tracked canonical release files at an
exact Git commit. It explicitly excludes the author-facing
`submission/biorxiv/` worksheet/checklists, as well as the legacy parent
package, untracked caches, and local build debris.

The new archive must be built from the frozen version `1.1.0` tag. The earlier
version `1.0.0` archive and tag remain immutable historical records.

Submission-specific status, unresolved author choices, and official bioRxiv guidance are maintained
in [`submission/biorxiv/`](k2p_k3p_theta_clarified/submission/biorxiv/).
