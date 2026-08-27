# Exact K2P and K3P theta-trinet collisions

A binary semi-directed strict level-two theta trinet with a genuine nontrivial
3-blob shares an exact three-leaf distribution with a three-star tree under the
Kimura two-parameter (K2P) model. Because K2P is a submodel of the Kimura
three-parameter (K3P) model, this one collision already refutes universal
tree--theta disjointness for both models. A second exact construction breaks
K2P symmetry at the network-parameter level, and full K3P rank yields nearby
shared distributions outside every globally character-relabeled K2P submodel.

## Canonical version

**Use only [`k2p_k3p_theta_clarified/`](k2p_k3p_theta_clarified/) for reading,
verification, citation, submission, or archival deposit.** Open the current
[`combined-paper-clarified.pdf`](k2p_k3p_theta_clarified/combined-paper-clarified.pdf)
or its [`combined-paper-clarified.tex`](k2p_k3p_theta_clarified/combined-paper-clarified.tex)
source directly.

The current frozen submission/replay snapshot is version `1.2.4`, identified by
the venue-neutral annotated Git tag `k2p-k3p-theta-v1.2.4` at full commit
`87d86cf348e888b29df94681426611ac601afe62`. Its validated ZIP, tar.gz, and
checksum files are under
[`releases/k2p-k3p-theta-v1.2.4/`](releases/k2p-k3p-theta-v1.2.4/). Versions
`1.2.3`, `1.2.2`, `1.2.1`, `1.2.0`, and `1.1.0` remain historical snapshots
in their own release directories.

A neutral, copied AI-referee handoff is under
[`referee_packages/k2p-k3p-theta-ai-referee-v1.2.4/`](referee_packages/k2p-k3p-theta-ai-referee-v1.2.4/).
It contains the exact tagged manuscript and replay materials, a fail-closed
fresh-folder driver, a neutral review prompt, and a report template. Prior
reviews and author dispositions are deliberately excluded from that packet.
The portable [`referee ZIP`](referee_packages/k2p-k3p-theta-ai-referee-v1.2.4.zip)
has SHA-256
`031a1fbb115995ab7edb382d0e52f7791fd512b0e53887fc4a1c8fe5bfb93f6b`;
its sibling `.sha256` file is the transport checksum.

All superseded parent-level files are isolated under
[`legacy/DO_NOT_SUBMIT-pre-clarification/`](legacy/DO_NOT_SUBMIT-pre-clarification/).
The immutable version `1.0.0` replay archive is retained separately under
[`legacy/releases/`](legacy/releases/). Nothing under `legacy/` is a current
submission input.

The K2P witness is an exact counterexample to Lemma 5.6 and the K2P part of
Corollary 5.8 in arXiv:2607.12919v2. Version 3 removes the formal
arbitrary-level K2P lemma and the K2P part of the corresponding global
corollary, records the leaf-order obstruction, and leaves high-level K2P and
K3P trinet questions open. The exact K2P collision answers both questions
negatively by model inclusion. The quartic construction additionally gives an
exact genuinely K3P network parameter for a globally character-relabeled K2P shared
distribution; the rank-15 local theorem supplies genuinely K3P shared
distributions. Neither result affects the corrected paper's JC or level-one
results.

The fixed theta maps are Zariski dense in the effective three-leaf K2P and K3P
Fourier spaces. Their local collision loci fiber over the tree models with
11- and 14-dimensional fixed-output network fibers. A common-subtree theorem
also inserts one invisible theta blob at any chosen internal vertex of every
labelled unrooted binary tree on `n >= 3` leaves. No multi-blob composability
claim is made.

## Replay the canonical package

Python 3.10 or newer and the standard library are required.

```bash
cd k2p_k3p_theta_clarified
python3 verify_k2p_simple.py
python3 verify_k2p_displayed_trees.py
python3 src/verify_k2p_four_leaf_graft.py
python3 verify.py
PYTHONOPTIMIZE=1 python3 verify.py
```

The focused displayed-tree verifier reconstructs the four displayed trees from
the rooted graph and checks all 64 ordinary-state probabilities by exact Markov
pruning. The focused four-leaf verifier checks the one-blob graft theorem on
all 256 Fourier coordinates and all 256 ordinary-state probabilities. The
complete suite additionally checks the edgewise strictly continuous-time K2P
witness, fixed-order audit, all-six-order sign point, derived K2P dimension and
fiber arithmetic, the K3P collision and symmetry distinction, direct K3P
ordinary-state pruning, the rank and tangent data, and adversarial semantic
mutation rejections. `CERTIFICATE_FIELD_COVERAGE.md` distinguishes recomputed
or semantically bound values from consistency-only and informational fields.
Edgewise embeddability allows a different generator and rate ratio on each edge
and imposes no molecular clock or global timing. Successful complete output
ends with `ALL EXACT CHECKS PASSED`.

## Canonical files

- `k2p_k3p_theta_clarified/combined-paper-clarified.tex` / `.pdf`: manuscript.
- `k2p_k3p_theta_clarified/technical-summary-clarified.tex` / `.pdf`: technical overview.
- `k2p_k3p_theta_clarified/k2p_displayed_tree_clarification.tex` / `.pdf`: focused historical clarification note.
- `k2p_k3p_theta_clarified/verify.py` and its companion modules: exact replay suite.
- `k2p_k3p_theta_clarified/certificate_*.json`: exact certificates.
- `k2p_k3p_theta_clarified/submission/biorxiv/`: bioRxiv metadata and upload checklist.
- `k2p_k3p_theta_clarified/CITATION.cff`: citation metadata.
- `k2p_k3p_theta_clarified/LICENSES.md`: package licensing boundaries.
- `releases/k2p-k3p-theta-v1.2.4/`: commit-pinned current replay archives and checksums.
- `referee_packages/k2p-k3p-theta-ai-referee-v1.2.4/`: neutral copied referee handoff and replay driver.
- `referee_packages/k2p-k3p-theta-ai-referee-v1.2.4.zip`: portable referee handoff with checksum sidecar.
- `legacy/`: superseded drafts and immutable historical release archives, kept outside the current submission path.

## Build and release

```bash
cd k2p_k3p_theta_clarified
bash src/build_pdfs.sh
bash submission/build_release.sh --output-dir /absolute/path/to/release-output --commit k2p-k3p-theta-v1.2.4 --version 1.2.4
```

The release builder archives only the tracked canonical release files at an
exact Git commit. It explicitly excludes the author-facing
`submission/biorxiv/` worksheet/checklists, the legacy parent package,
untracked caches, and local build debris.

The current archives were built from the frozen version `1.2.4` tag and passed
the clean replay gates documented in their release README. Versions `1.2.3`,
`1.2.2`, `1.2.1`, `1.2.0`, `1.1.0`, and `1.0.0` remain historical records.

Submission-specific status, unresolved author choices, and official bioRxiv
guidance are maintained in
[`submission/biorxiv/`](k2p_k3p_theta_clarified/submission/biorxiv/).
