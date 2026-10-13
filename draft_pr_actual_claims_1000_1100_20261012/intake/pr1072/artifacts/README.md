# Ring loading: credited prior refutation of the 11D/10 bound

Problem 30002729 / OWR-13353-017, priority rank 1244. Accepted as a credited prior refutation, with zero new proof turns.

The target is the proposed universal inequality `L <= L* + 11D/10` for finite undirected rings, where `L` and `L*` are the optimal unsplittable and splittable maximum edge loads and `D` is the maximum complete demand. The audited prior construction yields `L-L*>1.119D>11D/10` after the required transfer to optimum values.

## Attribution and contents

The construction belongs to Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner's [AlphaEvolve work](https://arxiv.org/abs/2511.02864), Section 41. The transfer is credited to [Karl Däubel, Lemma 7](https://arxiv.org/abs/1904.02119). The original target is Skutella's Conjecture 1 in the [Oberwolfach report](https://doi.org/10.4171/owr/2014/51), printed page 2917.

- [PRIOR_REFUTATION_AUDIT.md](PRIOR_REFUTATION_AUDIT.md) supplies the complete authored transfer argument and mathematical audit: split-relative discrepancy versus an optimum-value gap; two- and four-edge demand-capped blocks; bottom-up maximum-load normalization; a weighted split-optimality certificate; preservation of the maximum full demand; and distinct nonzero demand endpoint pairs.
- [VERIFICATION_METADATA.json](VERIFICATION_METADATA.json) records the exact-check extent, public notebook and PDF identities, retrieval/inspection history, and manuscript-version/status limits.
- [STATUS.json](STATUS.json) records the accepted scope and limitations.
- [MANIFEST.json](MANIFEST.json) identifies every distributed member and hashes the other four files.

## External witness and review boundary

The [pinned public notebook](https://github.com/google-deepmind/alphaevolve_repository_of_problems/blob/8f447457957deac61e28bf1676746f0753b3b2f8/experiments/ring_loading_problem/ring_loading_problem.ipynb) is the external witness source. The reported exact witness verification is not distributed as a self-contained computational certificate. Reproduction requires independently obtaining that source and verifying its finite witness. Source notebook and PDF bodies, source-derived vectors and demand tables, programs, and raw computational outputs are not included. The complete written transfer proof is included.

All source checks recorded here belong to the completed audit. Edition preparation does not claim a new source retrieval, rehash, inspection, or literature search. In particular, the retained AlphaEvolve PDF is arXiv v1; the recorded latest-version check is v3. The Däubel inspection is arXiv v2. No journal-publication or peer-review assertion is inferred from those arXiv records.

This audit is AI-assisted and unrefereed. It makes no new-discovery, historical-priority, optimal-additive-constant, external-human-peer-review, or formal-proof-assistant-certification claim. Hashes and packaging checks establish byte integrity, not mathematical truth. This is an addition-only proof/audit edition; no queue or historical accounting is changed.
