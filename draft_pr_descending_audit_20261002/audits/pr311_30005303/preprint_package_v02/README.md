# Closedness and attractive approximation of binary MTP2 edge models

Alec Kriebel, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

This unrefereed research note proves that, on a fixed finite graph, binary MTP2 laws with finite unary/edge factors are exactly the limits of strictly positive attractive Ising laws on the same graph. It gives the exact edge-only closedness conclusion of Lauritzen's 2022 Conjecture 1, including isolated coordinates and empty graphs.

The historical comparison is qualified. Kahle–Sullivant (2024) already establishes natural-support limit-factorization; the general support reduction is an elementary extension. The zero-support attractive-approximation characterization is separately proved. No equivalent full characterization was established in the inspected primary bodies, but this is not a certificate of historical first discovery. The old C4 counterexample is credited to Gandolfi–Lenarda, published April 13, 2017. We do not claim a new counterexample.

AI tools were used extensively for derivation, primary-literature search, programming, and independent adversarial review. This package is not human peer reviewed or proof-assistant certified. Computations use exact integer/rational arithmetic and illustrate or falsify finite checks; the all-graph result rests on the written proof.

## Contents

- `output/pdf/mtp2_edge_closure.pdf`: five-page manuscript.
- `mtp2_edge_closure.tex`: standalone LaTeX source, with all bibliography entries inline.
- `SUPPLEMENT.md`: complete support-geometry comparison and verification scope.
- `REPRODUCE.py`, `verify_boundary.py`, `verify_priority_examples.py`: portable standard-library verification.
- `expected/`: deterministic expected boundary and exact-law results.
- `BUILD_RECEIPT.json`: recorded source/PDF hashes and native build/render evidence. Visual and adversarial approval are recorded separately when completed.
- `LICENSE.txt`: CC BY 4.0 for the original material in this package.
- `zenodo-deposit.json`: exact submission metadata; its filenames identify the two separately uploaded files.

The build receipt is historical. Its dated provenance correction identifies the original orchestration script hash; no historical executable-binary fingerprints are claimed. Current review decisions are recorded separately. The original law checker was authored independently; later count/provenance-label corrections do not assert that their editor had never read candidate code.

## Reproduce

Python 3.10 or newer, standard library only, with assertions enabled:

```text
python3 REPRODUCE.py --out-dir fresh-results
```

The output directory must not exist. It retains actual commands, timestamps, complete stdout/stderr and results, and compares generated results with `expected/`. No credentials, network, repository checkout, absolute workspace path or unpublished private source is required. The build receipt's recorded original workspace paths describe a past build and are not runtime requirements.

To rebuild the manuscript, use a LaTeX compiler supporting the listed standard packages; for example:

```text
tectonic mtp2_edge_closure.tex
```

This command produces a PDF beside the source. PDF metadata may differ by compiler/build time, so compare content and rendering rather than expecting identical PDF bytes from a later build. The verification JSON outputs are deterministic.

## Review limitations

This is an unrefereed preprint. Independent AI adversarial review is distinct from human peer review, and the exact finite checks are distinct from a formal machine proof. Review and publication decisions are recorded in separate dated audit receipts; this README itself supplies no approval or historical priority certificate.
