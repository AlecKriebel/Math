# Exact K2P and K3P theta-trinet collisions

A binary semi-directed strict level-two theta trinet with a genuine nontrivial
3-blob shares an exact three-leaf distribution with a three-star tree under
both the Kimura two-parameter (K2P) and three-parameter (K3P) substitution
models.

## Canonical version

**Use only [`k2p_k3p_theta_clarified/`](k2p_k3p_theta_clarified/) for reading,
verification, citation, submission, or archival deposit.** Its
`combined-paper-clarified.tex` and `combined-paper-clarified.pdf` are the
canonical manuscript.

The frozen bioRxiv/replay snapshot is version `1.0.0`, identified by the Git
tag `k2p-k3p-theta-biorxiv-v1.0.0`.

Files in this parent directory with names such as `combined-paper.tex`,
`combined-paper.pdf`, `technical-summary.*`, `verify.py`, and the parent
certificates are retained solely as pre-clarification history. They are not a
second current version and must not be submitted or included in a new release.

Under the conventions stated in Brits, Holtgrefe, van Iersel, and Martin,
*On Tree--Network Distinguishability and Full Identifiability of Phylogenetic
Networks* (arXiv:2607.12919v2), the K2P witness conflicts with the K2P
conclusion of their Lemma 5.6 and with the K2P case of their Corollary 5.8. The
K3P witness answers their Discussion's high-level K3P trinet question
negatively. Neither result tests the source paper's JC or level-one results.

## Replay the canonical package

Python 3.10 or newer and the standard library are required.

```bash
cd k2p_k3p_theta_clarified
python3 verify_k2p_simple.py
python3 verify_k2p_displayed_trees.py
python3 verify.py
```

The focused displayed-tree verifier reconstructs the four displayed trees from
the rooted graph and checks all 64 ordinary-state probabilities by exact Markov
pruning. The complete suite additionally checks the strict continuous-time K2P
witness, fixed-order audit, all-six-order sign point, K2P ranks and collision
families, and the K3P collision, rank, and analytic implicit-function data.
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

## Build and release

```bash
cd k2p_k3p_theta_clarified
bash src/build_pdfs.sh
bash submission/build_release.sh --output-dir /absolute/path/to/release-output --version 1.0.0
```

The release builder archives only the tracked canonical release files at an
exact Git commit. It explicitly excludes the author-facing
`submission/biorxiv/` worksheet/checklists, as well as the legacy parent
package, untracked caches, and local build debris.

The package cites arXiv:2607.12919v2, posted 29 July 2026. Submission-specific
status, unresolved author choices, and official bioRxiv guidance are maintained
in [`submission/biorxiv/`](k2p_k3p_theta_clarified/submission/biorxiv/).
