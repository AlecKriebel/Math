# Exact K2P and K3P theta-trinet collisions

A binary semi-directed strict level-two theta trinet with a genuine nontrivial 3-blob shares an exact three-leaf distribution with a three-star tree under both the Kimura two-parameter (K2P) and three-parameter (K3P) substitution models.

Under the conventions stated in Brits, Holtgrefe, van Iersel, and Martin, *On Tree--Network Distinguishability and Full Identifiability of Phylogenetic Networks* (arXiv:2607.12919v2), the K2P witness conflicts with the K2P conclusion of their Lemma 5.6 and with the K2P case of their Corollary 5.8. The K3P witness answers their Discussion's open high-level K3P trinet question negatively. Neither result tests the source paper's JC or level-one results. The source authors have been contacted and are auditing the construction.

## Clarification revision

The current revision is in [`k2p_k3p_theta_clarified/`](k2p_k3p_theta_clarified/). It explicitly fixes the placement of `S` on both arcs out of `p` and `T` on both arcs out of `q`, derives the four-switching formula from retained-edge graphs, and adds an independent exact direct-pruning verifier for the simple witness. No mathematical parameter or conclusion changed. The pre-clarification paper, summary, certificates, and original verifier modules remain in this parent directory; these navigation and provenance files were updated to point to the clarification.

## Compact K2P verification

```bash
python3 verify_k2p_simple.py
```

Only Python 3 and the standard library are required. This checks the rooted and semi-directed topology, all network and tree edge inequalities, the sixteen-entry factorization, all 64 Fourier coordinates, all 64 site-pattern probabilities, positivity, normalization, the exact minimum probability, and `Q=0`.

The clarification revision adds the graph-derived replay:

```bash
cd k2p_k3p_theta_clarified
python3 verify_k2p_displayed_trees.py
```

It literally reconstructs all four displayed trees and independently checks all 64 probabilities by ordinary-state Markov pruning.

## Complete verification

```bash
python3 verify.py
```

Successful output ends with:

```text
ALL EXACT CHECKS PASSED
```

The complete verifier additionally checks the strict continuous-time K2P witness, direct ordinary-state Markov pruning, the fixed-order induction audit, the all-six-order rational sign point, K2P rank and collision-family results, and the K3P collision, rank, and analytic implicit-function data.

## Main files

- `k2p_k3p_theta_clarified/combined-paper-clarified.tex` / `.pdf`: current unified K2P and K3P proof.
- `k2p_k3p_theta_clarified/technical-summary-clarified.tex` / `.pdf`: current two-page technical overview.
- `k2p_k3p_theta_clarified/k2p_displayed_tree_clarification.tex` / `.pdf`: focused two-page clarification.
- `k2p_k3p_theta_clarified/verify_k2p_displayed_trees.py`: exact graph-reconstruction and direct-pruning verifier.
- `certificate_k2p_simple.json`: the compact `Q(sqrt(71))` K2P collision certificate.
- `certificate_k2p_continuous_time.json`: the strict continuous-time K2P collision certificate.
- `certificate_k3p.json`, `jacobian_certificate_k3p.json`, `continuous_time_certificate_k3p.json`: the K3P collision, Jacobian, and continuous-time certificates.
- `verify_k2p_simple.py`: standalone dependency-free verifier for the compact K2P witness.
- `verify.py`: orchestrates the complete verifier suite in `src/`.
- `verification_report.txt` / `verification_report_simple.txt`: successful verifier transcripts.
- `k2p_k3p_theta_clarified/CHANGELOG.md` and `PROVENANCE.md`: current revision history and reproducibility record.

## Source-paper version

The package cites arXiv:2607.12919v2. ArXiv lists v2 as posted 29 July 2026; the PDF manuscript itself is dated 30 July 2026.

## Building the PDFs

A TeX installation with `latexmk`/`pdflatex` or `tectonic` and TikZ is sufficient. For the current revision:

```bash
cd k2p_k3p_theta_clarified
bash src/build_pdfs.sh
```

## Continuous-time status

The K2P package contains an explicit exact strict continuous-time collision. The K3P strict continuous-time result is an analytic existence theorem: exact algebra verifies the implicit-function hypotheses and tangent signs, and the real-analytic implicit-function theorem supplies the nearby fixed-output branch.
