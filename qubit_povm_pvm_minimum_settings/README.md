# Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation

The principal results concern complex local Hilbert spaces of dimension at most two, finite input-dependent output alphabets, and ordinary finite shared randomness selecting complete strategies:

1. With two inputs per party, the POVM and PVM behavior convex hulls coincide.
2. A physical 3×2 POVM strategy strictly exceeds the bound for every PVM strategy and its convex hull.
3. Consequently the minimum separating input architecture is (3,2), up to exchanging the parties.

The Lean source includes explicit basis/dimension, finite-label, and stochastic-output bridges. Read [the certificate](bell_lean/CERTIFICATION.md), [claim-to-declaration map](bell_lean/docs/CERTIFIED_COVERAGE.md), and [source-model conventions](bell_lean/docs/MODEL_CONVENTIONS.md) for exact scope and evidence. The conclusion does not assert same-state simulation, equality of raw strategy sets, or a global POVM optimum.

## Version 2 local package

[VERSION_2.md](VERSION_2.md) describes the concrete review package and complete clean-extraction reproduction. It is prepared locally; no new immutable release or DOI is claimed.

- `paper/`: LaTeX source, bibliography, publication PDF and line-numbered review PDF.
- `artifacts/`: exact symbolic certificates and machine-readable data.
- `bell_lean/`: Lean proofs, pinned environment, compiled statement contracts and run-specific receipts.
- `referee_2026-09-11/` and `referee_response_20260911/`: historical public review evidence.
- `version2_completion_20260921/`: current direct archive comparison and independent semantic review.
- `reproduce.py`: shipment integrity, exact checks, fresh Lean verification and PDF builds.

From a clean extraction of the staged package, after installing prerequisites:

```sh
python reproduce.py --bootstrap
```

For exact symbolic checks only, use `./run_all.sh`; for only the Lean build, use `python scripts/run_lean.py --serial` from `bell_lean`. Neither subset is the complete release verification.

The formal proof follows some different routes from the manuscript. The remaining auxiliary manuscript-only mathematics is listed explicitly in the coverage map. Formal checking does not establish bibliographic priority or replace review of the translation from scientific conventions into the stated mathematical models.

Alec Kriebel, Independent Researcher. ORCID: <https://orcid.org/0009-0001-9320-500X>.

Manuscript/data: CC BY 4.0. Verification code and Lean sources: MIT. See [LICENSE](LICENSE).
