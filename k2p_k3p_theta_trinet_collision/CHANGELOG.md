# Changelog

## Version 1.2.0 theorem expansion -- 26 August 2026

- Reordered the logical narrative: the compact K2P collision already refutes
  K3P tree--theta disjointness by model inclusion.
- Distinguished the quartic point's genuinely K3P network parameters from its
  relabeled-K2P shared output, then used the rank-15 restricted submersion to
  prove nearby genuinely K3P collision distributions.
- Added local product geometry and 11-/14-dimensional fixed-output network
  fibers, while retaining the 17-/23-dimensional collision loci.
- Promoted the full-rank calculations to Zariski-density corollaries in the
  effective affine K2P and K3P three-leaf Fourier spaces.
- Proved one-blob common-subtree grafting on every labelled unrooted binary
  tree topology for every `n >= 3`, with strict-interior, edgewise
  continuous-time, and genuinely K3P variants.
- Added an independent exact four-leaf graft verifier covering all 256 Fourier
  coordinates and all 256 ordinary-state probabilities.
- Completed independent post-edit proof, verifier, and release-metadata audits;
  rebuilt and visually inspected all PDFs; and replayed all exact checks in
  normal and optimized modes.
- Froze annotated tag `k2p-k3p-theta-v1.2.0` at commit
  `7570a4a0f7051a607ee6eb4ef7ed43e54e805322` and retained the validated ZIP,
  tar.gz, checksums, and replay record under `releases/`.
- Deliberately left multi-blob composability, common-generator/clock models,
  genuine four-attachment blobs, JC collisions, and complete classification to
  follow-up work.

## Version 1.1.0 response and release isolation -- 25 August 2026

- Updated the canonical manuscript for arXiv:2607.12919v3, which removes the
  Version 2 arbitrary-level K2P claim, records the leaf-order obstruction, and
  leaves high-level K2P/K3P questions open.
- Qualified continuous-time results as edgewise, corrected `Theta_0`, added
  global nongenericity and non-tree-child scope, and expanded related work.
- Moved the coherent superseded parent package under
  `legacy/DO_NOT_SUBMIT-pre-clarification/` and the immutable version `1.0.0`
  archive under `legacy/releases/`.
- Prepared venue-neutral release version `1.1.0` and tag
  `k2p-k3p-theta-v1.1.0` without moving the prior tag.
- Froze tag `k2p-k3p-theta-v1.1.0` at commit
  `d71493d1c188cc78ede27fed1744373272ffb220` and retained validated ZIP and
  tar.gz replay archives plus checksum sidecars under `releases/`.

## Canonical bioRxiv and archival preparation -- 23 August 2026

- Designated `k2p_k3p_theta_clarified/` as the sole current manuscript,
  verification, submission, and release subtree.
- Marked the similarly named parent files and parent ZIP as historical inputs
  that must not be submitted or redeposited.
- Added bioRxiv official-requirements notes, an upload-metadata worksheet, and a
  permanence-aware final approval checklist.
- Added citation metadata, explicit mixed-material licensing boundaries, and an
  MIT license for executable verifier/build code only.
- Added a Zenodo metadata template with unresolved author-license, release,
  commit, and DOI placeholders.
- Added a deterministic Git-subtree release builder that excludes untracked
  caches and the legacy parent package and performs a two-build byte comparison.
- Published canonical source/replay tag `k2p-k3p-theta-biorxiv-v1.0.0` at full
  commit `4100ec6524054cef1e78441587abc9487d689d0b`.
- Removed the stale unversioned parent ZIP and sidecar (recoverable from Git
  history) and replaced them with the clean commit-pinned version `1.0.0` ZIP
  and checksum sidecar.
- Corrected newline preservation for generated archive manifests/provenance and
  added byte-for-byte checks of both generated files inside ZIP and tar.gz.
- Replayed the complete suite normally and with Python optimization from a clean
  extraction; both passed, and rebuilt PDF text and pixels matched.

## Displayed-tree clarification revision

The additive `k2p_k3p_theta_clarified/` release makes the existing construction unambiguous without changing any mathematical parameter or conclusion.

- States explicitly that both arcs out of `p` carry `S` and both arcs out of `q` carry `T`.
- Derives the common `K_x^2 K_y K_z` factor and the four-switching matrix from labelled descendants.
- Adds literal retained-edge graph reconstruction and exact ordinary-state pruning for the simple witness.
- Records the exact five-coordinate Lemma 4.1 convention cross-check.
- Corrects the technical summary and public-repository/provenance wording.
- Preserves the pre-clarification paper, summary, certificates, and original verifier modules in this parent directory; parent navigation and provenance files now point to the clarification.

## Widened scope: added the K2P collision

This directory supersedes the earlier K3P-only `k3p_theta_trinet_collision` package. The construction, verifiers, and manuscript now cover both K2P and K3P.

- Added the compact K2P collision over `Q(sqrt(71))`, its exact minimum site-pattern probability, and its status as a counterexample to the K2P conclusion of Lemma 5.6 and the K2P branch of Corollary 5.8 in arXiv:2607.12919v2.
- Added a separate edgewise strictly continuous-time K2P witness, checked independently by direct ordinary-state Markov pruning.
- Added the fixed-order induction diagnosis: a relabeling step in the source paper's proposed K2P induction is not compatible with the fixed coordinate order used in the parent expansion.
- Added an independent rational theta point with `Q<0` in all six leaf orders.
- Added the exact K2P rank-9 minors at both witnesses, the local dimension-17/codimension-3 collision locus, and an exact six-dimensional symmetric collision family.
- Retained and re-verified the K3P collision, rank-15 determinant, local dimension-23 collision locus, and the real-analytic implicit-function extension into the edgewise strictly continuous-time K3P cone.
- Unified the K2P and K3P material into a single `combined-paper.tex`/`.pdf` and a single two-page `technical-summary.tex`/`.pdf`.
- Tightened the algebraic isolating intervals used by the exact verifier so the displayed child-invariant decimals are rigorously certified:
  - `-1.919971072382827... x 10^-9`, and
  - `3.428488326525925... x 10^-9`.

## Mathematical and textual corrections

- Included the exact short clause from Lemma 5.6 that the invariant is "zero on M1 and strictly positive on M2," and stated Corollary 5.8 precisely in paraphrased mathematical form.
- Corrected the discovery narrative: AI-assisted analysis of a K3P follow-up first flagged a possible sign/leaf-order issue and a numerical collision candidate in the source paper's K2P invariant, after which the exact witnesses, rank calculations, family, and verifiers were constructed and independently checked.
