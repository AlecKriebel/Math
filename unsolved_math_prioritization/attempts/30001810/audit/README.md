# Independent audit of problem 30001810

Verdict: **ACCEPT AFTER LOCAL CLARIFICATIONS; PARTIAL-PROGRESS ONLY.**

The mathematical partials survive independent review. The supplied correction explicitly requires compatible standard face parametrizations in the pseudomanifold construction and distinguishes mixed-factor and same-factor shuffle boundary faces. The arbitrary-aspherical equality remains unresolved after five approaches.

Files:

- `AUDIT_REPORT.md`: complete independent proof audit, negative cases, accepted partials, and remaining gap
- `CORRECTION.patch`: actual unified patch against the frozen `MATHEMATICAL_REPORT.md`
- `CORRECTED_MATHEMATICAL_REPORT.md`: exact result of applying that patch
- `ACCEPTANCE.json`: machine-readable disposition and original/corrected fingerprints
- `SOURCE_METADATA.json`: inspected sources, hashes, retrieval limits, and dependencies
- `independent_checks.py`: independent exact mathematical and optimization controls
- `INDEPENDENT_CHECKS.json`: checked output including frozen-input verification
- `MANIFEST.json`: sizes and SHA-256 hashes of this audit packet

Run mathematical controls with `python independent_checks.py`. To reproduce every recorded input-integrity field, run `python independent_checks.py --input /path/to/original/frozen/public` and compare the output with `INDEPENDENT_CHECKS.json`.

Apply `CORRECTION.patch` only to a copy of the original report after verifying its SHA-256 is `b796c99ef3673687fcf40c3f3912b008fa6694d4b5eca996b1c1998f0e230062`. The resulting report must hash to `e8e396d4b4fb01a2319e95d4cd95fdd8c3e38ee971e155c27b398ee5be268683`. Rebuild the containing report-packet manifest if the corrected report replaces the original in a later package; the original manifest describes the original bytes only.

The tests use exact arithmetic, independent shuffle reconstruction, exhaustive finite primal/dual optimization, cover controls, and deliberate negative cases. They do not constitute a formal proof, an exhaustive manifold search, or a solution of the general comparison. The public audit packet contains authored mathematics and verification metadata only. Source PDFs, source extracts, datasets, and private coordination are excluded.
