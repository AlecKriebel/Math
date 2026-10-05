# Independent audit packet: 9500009

Status: **PASS for limited claims; full problem UNRESOLVED.**

`AUDIT_REPORT.md` gives the mathematical review, exact counts, source boundaries,
and one nonblocking verifier-hardening issue. The original author freeze remains
unchanged. This additive packet makes no novelty or publication claim.

## Replay

Requires Python 3 and an installed C++17 `g++` compiler. No network is used.

    python3 code/verify.py
    python3 -O code/verify.py

Both commands must exit zero and print status PASS. Default replay does not
rewrite files. The following deliberate false reference must fail with exit 1:

    python3 -O code/verify.py --negative-control

`--write` regenerates derived mathematical outputs only. Do not use it when
checking an existing freeze. The independent verifier uses explicit exceptions;
its checks are not removed by Python optimization.

## Contents

- `code/`: independently written counting and checking implementations
- `results/`: independent computed counts, verification summary, harness controls
- `reference/`: exact authored computational outputs copied from the original
  freeze, used only as comparison targets and certificate inputs
- `SOURCE_PROVENANCE_AUDIT.json`: public source, dataset, review-hash and bounded
  prior-attempt verification metadata
- `FREEZE_INTEGRITY.json`: integrity checks on the unchanged author packet
- `CORRECTIONS.md`: additive provenance completion and replay caveat
- `MANIFEST.json`: hashes and byte counts of this audit payload

All 162 pair counts for n=2,3,4 match; direct permutation and edge-orientation
checks cover n=2,3; 122 forest bounds also match independent poset counts.
Finite checks and an exponential rarity bound do not resolve the large-n limit.

Excluded: source PDFs, source extracts, HTML, images, raw datasets, downloaded
repository responses, private coordination, executables, and temporary files.
