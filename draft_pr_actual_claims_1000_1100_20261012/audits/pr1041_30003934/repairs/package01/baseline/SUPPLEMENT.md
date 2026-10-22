# Supplement and reproducibility boundaries

## Exact claim and proof boundary

The paper proves the entire accepted theorem, with source PARTITION nonempty and positive-integer. The target is exactly-one whole mixed-strategy pair in explicit rational matrices, variable positive dimensions, exact rank(A+B)=1, arbitrary degeneracy. No-instance uniqueness exhausts all auxiliary row minimizers and all opposing-strategy choices, including continua. Yes-instance existence comes from an actual retained half-bridge optimum. Numerical SSP experiments are supplementary; construction itself never executes an exponential SSP trajectory.

“Unrestricted optimum” means the fixed-demand network optimizer **after** the ternary cost perturbation and positive topological potential, **before** the simplex restriction. The quantified proof uses the full DS journal state/two-step argument and every legal SSP choice, comparison coupling in identical residual states, real-demand residual-cycle isolation, real fractional augmentation optimality, injective simplex encoding, and the uniform all-minimizer dual determinant penalty. These mechanisms are explicit in the paper; no historical PASS verdict serves as a mathematical premise.

## Included new computational interfaces

All code below is newly authored fresh-review code using Python standard-library exact rational arithmetic. It is not the historical omitted `computation/verify_reduction.py`. Neither script is a general theorem verifier, an exhaustive equilibrium enumerator, or a portable replay of all reduction claims. A finite run can check its programmed cases and controls, while the paper proves the quantifiers.

- `evidence/reviews/flow_source_01/flow_check.py` constructs and inspects the source-flow stage. Its normal/optimized receipts are `CHECKS_NORMAL.json` and `CHECKS_OPTIMIZED.json`; they record 37 weight vectors, 660 augmentations/half-flow certificates and 864 small-instance cycles per mode, six original-choice searches, and four negative controls. It checks path comparisons in the same residual state, capacity/conservation, bridge reversal, exact residual-dual certificates, positive potentials, bounds and simplex witnesses. It does not verify game membership or enumerate all equilibria.
- `evidence/reviews/game_certificate_01/check_exact.py` constructs six full small games, the stated determinant-bound M, and exact network/simplex duals; checks 204 auxiliary pairs and strict defaults; and runs penalty, payoff-sign, rank, and rational-certificate negative controls. `EXACT_RESULTS.json` and `EXACT_STDOUT.json` are its frozen receipts. It does not independently prove the all-instance source interface, all-minimizer theorem, or enumerate the entire equilibrium set.

Each script resolves outputs relative to its own file. Rerunning it overwrites a receipt and changes timestamp/hash data. To preserve the frozen package, copy the relevant family directory outside this package and run there. Example commands in a disposable copy are:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 flow_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -O flow_check.py
PYTHONDONTWRITEBYTECODE=1 python3 check_exact.py
```

The flow family uses explicit RuntimeError guards and records optimized-mode negative-control probes. The game family uses ordinary assertion checks, so use normal Python, as in its recorded run. These are documented actual interfaces, not claims of an independently provided CLI for arbitrary PARTITION inputs. This preparation does not count a rerun of either script as a replay of the absent historical six-game/39-network computations.

## Evidence, pin history, and current integrity

The original head is `ad138ddd5bd1a51c0f225f03342c0c058873f790`; the original full tree has eleven authored theoretical files. `evidence/root/SUBMITTED_PINS.json` stores their repository paths, original snapshot paths, sizes, and hashes. They are copied to `evidence/original/<snapshot_path>` without any edits. Their historical acceptance and readiness text is preserved, not promoted to a statement about this new package.

The fresh flow, game, and priority families retain their authored derivations/reports, code/receipts where applicable, independence checkpoints, input/final/output pins, logs, and source receipt/catalogue metadata. Their paths in old pins were relative to their original review directory. `EVIDENCE_COPY_MANIFEST.json` explicitly maps each old audit-relative source path to its new package path and gives the current copied hash; thus relocation does not silently invalidate or rewrite historical evidence. Original pins that mention private raw sources are retained as historical identity records, while the private bodies remain absent.

`CURRENT_INTEGRITY.json` hashes every distributed content file except itself. Candidate archive and build/verification receipts are kept outside its self-reference domain. The deterministic archive uses a fixed 2026-10-13 UTC timestamp, sorted paths, fixed owner/group/modes and gzip mtime zero. `BUILD_RECEIPT.json` records content count, current-integrity hash, archive hash, and exclusion policy. Archive reproducibility means identical included bytes yield identical archive bytes; the PDF itself carries a build creation time and is pinned as a supplied artifact, so a newly compiled PDF may have a different binary hash.

Use `verify_package.py` to check current content hashes, the copy map, original eleven-file pins, historic fresh output pins for all distributed members, archive membership and archive SHA-256. It also enforces exclusions. It does not claim formal proof verification. `build_archive.py` refreshes integrity before creating the archive; after any editorial repair, new review, or status update, run it and verify again. Keeping the old pin manifests permits historical integrity comparison without confusing them with the current content manifest.

## Private-source exclusion and intellectual lineage

No third-party source bodies are redistributed: all raw/rawprivate material, PDFs other than the authored paper, extracted `.txt`, page images, caches, rendering intermediates, and citation-discovery response dumps are excluded. This specifically includes `reviews/game_certificate_01/sources/rawprivate`. Source receipts and authored summaries/catalogues provide public URLs, versions, identity hashes, and actual reading scopes instead. A report's link to an excluded raw source is a historical locator, not a broken promise that the attachment is distributed.

Credit belongs to DS for its source counter/bridge and activity/coNP hardness, Adsul and coauthors for the auxiliary zero-sum/scalar hyperplane method, Gilboa–Zemel for unrestricted uniqueness hardness and rational membership, Gilboa–Zemel/Conitzer–Sandholm for the default-plus-witness pattern, Erickson–Fox–Lkhamsuren (2018) for prior generic real-demand isolation context, and established LP duality/determinant/exact-penalty techniques. The specialized connecting proof is fully written, with no broad lemma-firstness claims. arXiv Adsul v4 Theorems 7/19/20/21 map to journal Theorems 1/4/5/6; journal Theorem 7 is a different result.

The bounded priority audit found no exact match in inspected bodies. Global priority remains unknown because Murty's complete 1980 body, the exact SODA 2015 body, Mehta's 2012 thesis, Patris's 2026 thesis, and additional bodies/forward leads were not completely recovered or inspected. Hash identity establishes provenance, not truth or exhaustive literature coverage. No first/current-worldwide-open/new-generic-isolation claim appears in the manuscript or prepared metadata.

## Review, authorship and publication boundary

Alec Kriebel, independent researcher, ORCID 0009-0001-9320-500X; version 1.0, 13 October 2026. Authored text/code/evidence is CC BY 4.0. Extensive AI assistance covered solving, verification, source investigation and writing; independent and adversarial AI reviews are unrefereed AI review, not human journal peer review or proof-assistant checking. The root accepted the underlying full theorem; NEW_WHOLE_01 review of this exact manuscript/package is pending. `publication_ready=false` until that review and root decision. No individual was contacted; no external service, submission, publication, release, DOI, PR, branch or Git index was changed by this preparation.
