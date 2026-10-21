# Scoped existing-resolution record: fixed-dimensional loose embeddings

Record 30004262; source key OWR-17288-004; catalogue row 1849. Administrative classification: already_solved, turn 1/5, **only for the corrected same-N continuous loose-embedding question and the Riemannian finite-subset question**. This is not a blanket resolution of the historical uniform-embedding question.

The credited result is Alper Ferudun, *Loose Embeddings in a Fixed Euclidean Space: Countable Counterexamples and Flat Tori*, 20 October 2026, https://eulersolve.org/papers/owr-17288-004/paper.pdf (public page https://eulersolve.org/papers/owr-17288-004/ ; listed DOI https://doi.org/10.5281/zenodo.23513444). It is an **unrefereed, AI-assisted manuscript**, not our newly discovered result and not a peer-reviewed theorem certification. The included authored acceptance audit found no substantive mathematical error in the relevant proofs. It does not establish priority or exhaustive literature coverage.

## Definitions and scope

A loose embedding (LE) is a **continuous** map into Euclidean space that preserves the exact equality partition of distances in both directions: for every four points, the two image distances are equal if and only if the two source distances are equal. Comparisons include disjoint pairs and diagonal pairs. This forces injectivity. It is not order preservation, merely forward equality preservation, or a bi-Lipschitz condition.

H_N(X) means every finite subset, with its restricted original metric, has an LE into the **same fixed** R^N. Finite maps may differ without compatibility, uniform normalization, distortion bounds, or common continuity moduli. Finite-set continuity is automatic; global continuity is essential. The countable counterexamples have discontinuous global equality-pattern injections, which do not satisfy LE.

Read VARIANT_LEDGER.md before using any status. The original OWR wording says “uniformly embeddable” and leaves that new phrase undefined. The corrected dataset uses loose embeddability. The later primary question allows a larger finite target. These are different assertions.

## Files and verification

- ACCEPTANCE_AUDIT.md: authored full mathematical assessment of Theorems A/B/C, Corollary D, and Proposition 5.1, including all-index proof reasoning and scope limitations.
- VARIANT_LEDGER.md: exactly four principal variants and their separate outcomes.
- SOURCE_METADATA.json and DATASET_METADATA.json: public hashes, byte counts, retrieval history, and match results only. No copied source paper, dataset contents, or private coordination files are included.
- check_n1_original.py: preserved original authored exact rational finite sanity check, using Python assert statements. The acceptance audit refers to this same source by its original name, check_n1_independent.py; its bytes are unchanged.
- check_n1.py: AST-preserving hardened derivative with explicit runtime checks. run_checks.py supplies negative tamper controls.
- CHECK_PROVENANCE.json and CHECK_RESULTS.json: source derivation and normal/optimized execution results. These checks are finite sanity checks, not a general mathematical proof.
- PACKAGE_AUDIT.md: independent review of this package before freeze.
- MANIFEST.json: frozen file inventory with SHA-256 hashes and sizes; the manifest excludes itself to avoid a recursive hash.

Reproduce from this directory: python check_n1.py; python -O check_n1.py; python run_checks.py. The harness runs both baseline modes and two deliberately tampered variants in both modes. Untampered runs must exit 0; each tamper must exit 1 with AssertionError. The original check can be run normally, but its -O run disables assertions and is not verification evidence.

The Riemannian result uses intrinsic geodesic distance: every flat torus of intrinsic dimension at least two fails H_N for every finite target N. This disproves the universal Riemannian assertion, not H_N for every manifold. Circles are explicitly excluded: their standard planar chord realization is LE, so H_2 holds. For each target N the torus argument gives existence of some finite witness, not one finite subset failing all target dimensions and not an explicit general witness-size bound.
