# Independent audit: irrational Seshadri constants

Problem 30003978 / OWR-16628-010, rank 743. Audited 5 October 2026.

**PASS: prior-literature resolution supported by an independent ordinary mathematical audit.** The audited scope is every r >= 9, complex plane blowups at very general centers, ample integral polarizations, and one very general evaluation point. This supplies the conclusion of the original Nagata-only implication without proving or assuming Nagata.

The decisive results are [Laface–Ugaglia, arXiv:2609.26521v2, Theorem 2](https://arxiv.org/abs/2609.26521v2), for r=9, and [Malara–Merta–Szpond–Zielinski, arXiv:2610.01783v1, Theorem 1.2](https://arxiv.org/abs/2610.01783v1), for r>=10 through n=2r-13. Both remain recent preprints in the sources checked. Their constructions are credited prior work. This is neither an original solution nor a formal verification or peer-review endorsement.

GEOMETRIC_AUDIT.md records the full scrutiny: actual birational maps, limiting nefness, normal-bundle computation, the specialized reflection proof, Cartier quotient normalization, cyclic resolution and plane marking, very-general-center/evaluation quantifiers, and ampleness. It identifies the exact standard geometric inputs and the broader abstract assertions not needed for this application.

SOURCE_PINS.json records freshly retrieved PDF hashes and sizes, inspected pages, current version status, and independently checked public dataset metadata. REPLAY.json records the author freeze and exact replay results. The original packet was not edited.

Reproduce the independent arithmetic with Python 3 and SymPy 1.14.0:

    python3 independent_verify.py > /tmp/seshadri-independent.json
    cmp /tmp/seshadri-independent.json independent_results.json
    python3 test_packet_integrity.py > /tmp/seshadri-integrity.json
    cmp /tmp/seshadri-integrity.json integrity_results.json
    python3 verify_packet.py

The independent verifier records 32,975 exact assertions; the author output replays with 85,787. Neither count proves geometry. Universal reasoning, rather than finite test coverage, carries the all-r conclusion. The arithmetic verifier includes eight adverse controls; the independent inventory checker has fourteen acceptance/rejection controls.

Only authored analysis, authored code, exact outputs, manifests, and public verification metadata are included. PDFs, extracted source text, source screenshots, raw datasets, selected dataset records, and private coordination files are excluded. No remote write was made.
