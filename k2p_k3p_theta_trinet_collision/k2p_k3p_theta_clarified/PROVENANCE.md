# Provenance and reproducibility

## Canonical and public status -- 25 August 2026

This directory is the sole current K2P/K3P manuscript, verification,
submission, and archival subtree. The pre-clarification paper, summary,
certificates, and verifiers are isolated under the parent
`legacy/DO_NOT_SUBMIT-pre-clarification/` directory. Historical release archives
are under the parent `legacy/releases/` directory. All are excluded from new
submission/release instructions.

This repository is public. The pre-clarification combined K2P/K3P directory
first appears in public repository history at commit `ca21a733`, dated 4 August
2026; commit `85cdead2` repointed the existing public K3P project page to that
combined source directory. The full early draft was therefore already public
before the clarification. This record is additive and no history was rewritten.

The current frozen submission/replay snapshot is version `1.1.0`, identified by
the Git tag `k2p-k3p-theta-v1.1.0`. The earlier tag
`k2p-k3p-theta-biorxiv-v1.0.0` remains immutable. Exact upload-time status and unresolved
author choices are recorded in `submission/biorxiv/`. No bioRxiv or Zenodo
deposit and no external communication was initiated by the automated revision
process.

Version `1.1.0` distinguishes the source paper's history explicitly. The
removed arbitrary-level K2P statements are cited at arXiv:2607.12919v2. The
corrected arXiv:2607.12919v3 removes those statements, records the leaf-order
obstruction, and leaves high-level K2P and K3P questions open. The exact
collisions here answer both questions negatively without affecting the source
paper's JC or level-one results.

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

The complete suite additionally replays the edgewise strictly continuous-time K2P witness, induction-order audit, all-six-order negative-sign point, K2P ranks and collision family, and all K3P collision, Jacobian, and edgewise continuous-time analytic implicit-function data. Edgewise embeddability does not assert a common generator, rate ratio, molecular clock, or globally compatible node times.

## Exact arithmetic and source conventions

The focused verifier uses exact arithmetic in `Q(sqrt(71))` and only the Python standard library. The source-convention checker uses exact rational test vectors to confirm order `(A,C,G,T)`, Klein addition `C+G=T`, the K2P identification `a_C=a_T`, the five explicit Lemma 4.1 coordinates, and the favorable-order factorization of `Q`.

## AI assistance

AI-assisted mathematical research, symbolic exploration, code generation, auditing, and editorial tools contributed to discovery and preparation. Claims are exposed through proofs, exact certificates, source code, and replayable computations. No external communication was initiated by the automated revision process.

## Submission and archival metadata

Official bioRxiv scope, screening, formatting, funding, licensing, DOI, and
permanence guidance was rechecked on 23 August 2026 using only official
bioRxiv/openRxiv pages. The resulting audit and author worksheet are in
`submission/biorxiv/`. The repository intentionally leaves the bioRxiv
distribution option and the mixed-material Zenodo package license unresolved
for the author.

`CITATION.cff` records Alec Kriebel's ORCID and a preferred manuscript citation.
`LICENSE-CODE` applies MIT only to executable Python and shell source;
`LICENSES.md` defines the remaining boundaries. `submission/build_release.sh`
archives only the committed canonical subtree and embeds the selected Git
commit through Git's archive metadata.

`manifest.sha256` and the release builder use the same public-package boundary:
the author-only `submission/biorxiv/` worksheets are omitted, while the release
builder and all scientific source, certificates, transcripts, and PDFs are
included. Each built archive adds its own full-commit provenance record and an
exact manifest of the files actually archived.
