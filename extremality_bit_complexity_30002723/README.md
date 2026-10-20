# Rational one-row extremality in polynomial bit time

Problem ID 30002723, source key OWR-13353-006, row 1827. Prepared 20 October 2026.

## Status

**CLAIMED_SOLVED, five substantive attempts completed (5/5).** This authored proof passes the fresh full-theorem audit and exact saved-input replay; see [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md). It remains a claimed result, not externally peer-reviewed or independently certified for priority.

## Claimed theorem and exact scope

Given rational f in (0,1) and a periodic piecewise-linear minimal valid function for the one-row Gomory–Johnson infinite group problem, encoded by a sparse rational breakpoint list with rational point values and left/right limits, extremality is decidable in time polynomial in the total binary encoding length. Inputs may have two-sided discontinuities, including at zero. The definition uses unrestricted valid-function competitors.

The proof imports the Basu–Hildebrand–Köppe complete 4q-grid theorem, reduces its tight linear system to signed interval-pairing systems plus sparse endpoint equations, and uses the Agol–Hass–Thurston orbit-counting and weighted algorithms without expanding the numerical denominator.

This is a polynomial-bit-time **decision** claim. It is not a strong-polynomiality claim, a result for irrational representations or higher-dimensional group problems, or an implemented compressed solver. The included programs are dense finite validators, not runtime evidence for the claimed asymptotic algorithm.

## Reading order

- [ATTEMPT_5.md](ATTEMPT_5.md): theorem, complete algorithm, correctness assembly, and bit bounds.
- [ATTEMPT_3.md](ATTEMPT_3.md): full local proof, including discontinuities, limiting faces, and all 13 endpoint sectors.
- [ATTEMPT_4.md](ATTEMPT_4.md): signed lift, dimension cutoff, representative extraction, and weighted reconstruction.
- [ATTEMPT_1.md](ATTEMPT_1.md) and [ATTEMPT_2.md](ATTEMPT_2.md): exact input model, same-grid counterexample, and the continuous route.
- [AUDIT_ORBIT_COMPRESSION.md](AUDIT_ORBIT_COMPRESSION.md) and [structural/FULL_REDUCTION_REVIEW.md](structural/FULL_REDUCTION_REVIEW.md): completed independent mathematical reviews of the authored reduction.
- `structural/`: further complete lemma derivations and continuous-subclass proof.
- [AUDIT_FULL_THEOREM.md](AUDIT_FULL_THEOREM.md): fresh independent final audit, PASS for the complete theorem.
- `fresh_audit/`: 739 independent local row-space checks and 20 independent end-to-end decision simulations, including the dimension-cutoff branch.
- [provenance/SOURCE_GATE.md](provenance/SOURCE_GATE.md): bounded literature/source search completed before this authored proof. Its initial open-for-research finding is not a judgment on this later manuscript.

## Exact saved-input replay

Tested with Python 3.12.14 and the versions in `requirements.txt` (SymPy 1.14.0, NumPy 2.3.5, SciPy 1.17.0).

```sh
python -m pip install -r requirements.txt
python verify_manifest.py
python replay.py
```

The recorded run in [verification/REPLAY_REPORT.json](verification/REPLAY_REPORT.json) passed all eight suites, with byte-identical frozen outputs wherever a result file is regenerated.

The replay command copies the package to a temporary directory, runs only stored exact inputs or deterministic exact algebra tests, and checks byte-for-byte agreement with frozen result JSON files. It does not alter the published payload. It does not run floating-point LP discovery. A report can be saved with `python replay.py --report /path/to/report.json`; use a destination outside this directory if preserving the manifest is important.

NumPy and SciPy are declared dependencies because original modules import them, including when executing saved-input modes; the package is **not** standard-library-only. Floating-point LP is confined to optional candidate-discovery modes. The rank, minimality, and reconstruction assertions replayed here use exact integers and rational numbers.

The recorded 70-case continuous discovery run is retained in `structural/CONTINUOUS_TEST_RESULTS.json`. Its individual rational inputs were not saved, so it is **not part of exact saved-input replay**. Its generating script remains available as an optional discovery run. The separately stored all-covered, non-extreme rational example is replayed exactly.

## Payload and provenance boundaries

All mathematical prose and test fixtures are authored material. Provenance files contain public titles, URLs, source hashes/sizes, retrieval and inspection history, and dataset hash/count/match metadata only. Original problem datasets, dataset extracts, downloaded scholarly PDFs, extracted source text, images of source pages, private sources, personal data, and coordination files are excluded. The small rational test fixtures were constructed for validation and are not contents of the original problem datasets.

[MANIFEST.json](MANIFEST.json) covers every payload file except itself. Its own SHA-256 must be authenticated separately. Byte identity establishes artifact integrity, not mathematical correctness.
