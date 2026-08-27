# Provenance and reproducibility

## Canonical and public status -- 27 August 2026

This directory is the sole current K2P/K3P manuscript, verification,
submission, and archival subtree. The pre-clarification paper, summary,
certificates, and verifiers are isolated under the parent
`legacy/DO_NOT_SUBMIT-pre-clarification/` directory. The immutable version 1.1.0
release is under the parent `releases/` directory, while version 1.0.0 remains
under `legacy/releases/`. All earlier materials are excluded from new
submission/release instructions.

This repository is public. The pre-clarification combined K2P/K3P directory
first appears in public repository history at commit `ca21a733`, dated 4 August
2026; commit `85cdead2` repointed the existing public K3P project page to that
combined source directory. The full early draft was therefore already public
before the clarification. This record is additive and no history was rewritten.

The current frozen submission/replay snapshot is version `1.2.5`, identified by
the Git tag `k2p-k3p-theta-v1.2.5`. The earlier tags
`k2p-k3p-theta-v1.2.4`, `k2p-k3p-theta-v1.2.3`,
`k2p-k3p-theta-v1.2.2`, `k2p-k3p-theta-v1.2.1`, `k2p-k3p-theta-v1.2.0`,
`k2p-k3p-theta-v1.1.0`, and
`k2p-k3p-theta-biorxiv-v1.0.0` remain immutable.
Versions 1.2.4, 1.2.3, 1.2.2, 1.2.1, 1.2.0, and 1.1.0 are retained under the parent
`releases/` directory; version 1.0.0 remains under `legacy/releases/`. Exact upload-time
status and unresolved author choices are recorded in `submission/biorxiv/`.
No GitHub release, bioRxiv submission, Zenodo deposit, DOI, or external
communication was initiated by the automated revision process.

Version `1.2.0` distinguishes the source paper's history explicitly. The
removed arbitrary-level K2P lemma and corresponding global conclusion are
cited at arXiv:2607.12919v2. The corrected arXiv:2607.12919v3 removes that
formal lemma and the K2P part of the corresponding global corollary, records
the leaf-order obstruction, and leaves high-level K2P and K3P questions open. Since K2P is
nested in K3P, the compact K2P collision answers both questions negatively.
The separate quartic theta parameter breaks every globally character-relabeled
K2P edge symmetry, although its exact shared distribution is openly identified
as globally character-relabeled K2P; the rank-15 submersion supplies nearby
shared distributions outside all three globally character-relabeled K2P
strata. None of these statements affects the source paper's JC
or level-one results.

Version 1.2.0 additionally records the 11- and 14-dimensional fixed-output
fibers, Zariski-dense effective theta images, and the common-subtree theorem
that inserts one theta blob at any selected internal vertex of any labelled
unrooted binary tree. It does not claim simultaneous multi-blob composition.

Version 1.2.1 makes no mathematical change. It removes overloaded topology and
manifold notation, defines globally character-relabeled K2P consistently,
states the comparison-tree and compatible theta rootings separately, qualifies
the nonreversible supermodel remark, and binds the three comparison-tree
half-time root checks into the exact replay suite.

Version 1.2.2 likewise makes no mathematical change. It records the source
paper's triangle and 2-blob qualifications exactly, writes the K3P local
section explicitly, narrows the arbitrary-taxon interpretation, and states
that contracting the inserted theta blob recovers the original labelled tree
topology.

Version 1.2.3 makes the already implicit rank-persistence step in the K3P
local-section proof explicit: the same selected $15\times15$ Jacobian minor
remains nonzero throughout the parameter neighborhood, so every selected
realization visibly has a 14-dimensional local fixed-output fiber. It changes
no theorem statement, parameter, certificate, or computational conclusion.

Version 1.2.4 responds to an independent referee audit without changing any
theorem, witness, or scientific conclusion. It binds K3P Jacobian, tangent,
reticulation-choice, and root-suppression labels to canonical executable
semantics; derives the formerly saturated K3P rate-margin derivatives from the
complete tangent; adds rejection tests for coordinated semantic mutations;
adds exact ordinary-state K3P pruning on all retained graphs; derives the K2P
dimension arithmetic in the replay; and distinguishes recomputed checks from
informational fields, regression transcripts, and unsigned integrity
manifests. It also makes the literature and source-version wording literal.

Version 1.2.5 closes the two bounded verifier-assurance gaps found by an
independent replay of version 1.2.4. The K3P checker now binds the canonical
vertex table, complete ten-arc endpoint/vector map, and every reticulation
descriptor relationally before constructing graph dictionaries, with four new
coordinated mutation regressions. The compact K2P checker now consumes the
previously redundant stored `K_odot_K` transition row, with a dedicated
negative test. The coverage inventory distinguishes canonical, release-archive,
and referee-packet integrity artifacts. No mathematical claim, witness,
certificate value, title, abstract, or theorem statement changes.

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

The complete suite additionally replays the edgewise strictly continuous-time
K2P witness, induction-order audit, all-six-order negative-sign point, K2P
ranks and collision family, the exact K3P parameter/output symmetry distinction,
the K3P Jacobian and edgewise continuous-time analytic implicit-function data,
the direct ordinary-state K3P pruning comparison and semantic-mutation guards,
and the 11/14 fixed-output fiber counts. A focused four-leaf verifier checks one
single-theta graft using all 256 Fourier coordinates and all 256 ordinary-state
probabilities. The universal all-tree result rests on the manuscript's
common-kernel proof, not finite enumeration. Edgewise embeddability does not
assert a common generator, rate ratio, molecular clock, or globally compatible
node times.

## Exact arithmetic and source conventions

The compact simple-witness verifier uses exact arithmetic in `Q(sqrt(71))`.
The continuous-time K2P and four-leaf graft verifiers use the isolated field
`Q(ell,sqrt(1423))`, and the K3P verifier uses `Q(h)` with `5 h^4=1`.
All require only the Python standard library. The source-convention checker uses
exact rational test vectors to confirm order `(A,C,G,T)`, Klein addition
`C+G=T`, the K2P identification `a_C=a_T`, the five explicit Lemma 4.1
coordinates, and the favorable-order factorization of `Q`.

## AI assistance

AI-assisted mathematical research, symbolic exploration, code generation, auditing, and editorial tools contributed to discovery and preparation. Claims are exposed through proofs, exact certificates, source code, and replayable computations. No external communication was initiated by the automated revision process.

`CERTIFICATE_FIELD_COVERAGE.md` records which certificate groups are
recomputed or semantically bound and which are descriptive or consistency-only.
Stored transcripts and K3P sidecars are regression/transport copies, not
independent mathematical oracles. Included unsigned SHA-256 manifests support
internal path and byte consistency but do not authenticate themselves.

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
