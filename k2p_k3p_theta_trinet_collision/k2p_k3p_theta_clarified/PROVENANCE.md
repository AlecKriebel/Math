# Provenance and reproducibility

## Public status

This repository is public. The pre-clarification combined K2P/K3P directory first appears in the public repository history at commit `ca21a733` dated 4 August 2026; commit `85cdead2` repointed the existing public K3P project page to that combined source directory. The full draft was therefore already present in public repository history before this clarification. This record is additive: no history was rewritten. The pre-clarification paper, summary, certificates, and original verifier modules remain in the parent directory; its navigation and provenance files were updated to identify this clarification.

The source authors have been contacted and are auditing the construction. No journal or arXiv submission of this work has occurred.

## Revision lineage

This package incorporates an earlier K2P reproduction audit and the prior K3P-only package. The K3P-only repository version is recoverable at commit `d60581d1`. The separate K2P audit directory and the earlier first-contact memo were not included in this repository, so the present two-page clarification note was reconstructed from the exact public certificate and unified paper.

## Independent recomputation

Before editing, the complete pre-clarification verifier suite was replayed successfully. The new verifier does not begin with the four-term formula for `M`. It starts from the ten rooted arcs and the explicit edge placement, retains one incoming arc at each reticulation, and calculates all labelled descendant sets and Fourier labels from the resulting graphs.

For the simple witness it independently checks:

- the four graph-derived core monomials;
- the common `K_x^2 K_y K_z` factor;
- all sixteen entries of `M`, including the two diagnostic entries;
- all exact `4 x 4` transition matrices;
- all 64 Fourier-coordinate equalities;
- all 64 ordinary-state network/tree probability equalities;
- equality with Fourier inversion and every corresponding stored certificate entry.

The complete suite additionally replays the strict continuous-time K2P witness, induction-order audit, all-six-order negative-sign point, K2P ranks and collision family, and all K3P collision, Jacobian, and analytic implicit-function data.

## Exact arithmetic and source conventions

The focused verifier uses exact arithmetic in `Q(sqrt(71))` and only the Python standard library. The source-convention checker uses exact rational test vectors to confirm order `(A,C,G,T)`, Klein addition `C+G=T`, the K2P identification `a_C=a_T`, the five explicit Lemma 4.1 coordinates, and the favorable-order factorization of `Q`.

## AI assistance

AI-assisted mathematical research, symbolic exploration, code generation, auditing, and editorial tools contributed to discovery and preparation. Claims are exposed through proofs, exact certificates, source code, and replayable computations. No external communication was initiated by the automated revision process.
