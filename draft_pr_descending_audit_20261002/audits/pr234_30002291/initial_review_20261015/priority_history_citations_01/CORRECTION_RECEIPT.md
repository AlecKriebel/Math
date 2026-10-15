# Correction receipt — priority-history lane

Completed 2026-10-15T05:48:05.964091+00:00; scoped correction completion 100%. The historical/scientific disposition is unchanged.

## Exact changes

- Normalized the two DOI paths to `10.1214/16-AOP1170` and `10.15559/18-VMSTA111`. Six malformed occurrences were repaired across REPORT.md (two), SOURCE_READ_LEDGER.md (two), and QUERY_LEDGER.md (two). The query-ledger repair restores the exact original search string.
- Replaced the all-real-line volatility example with σ_s=2 for s<0 and σ_s=2+sin(L_s) for s≥0. Negative-time adaptation now follows from constancy. Nonnegative-time Lévy levels are adapted, and L_0=0 makes the definitions agree at 0, preserving càdlàg paths.
- Replaced the monotonicity phrase with “|g′| is eventually decreasing.”

## Validation and seals

All 69 unique source URLs in authored source/provenance artifacts passed static whitespace and URL-parse checks; SOURCE_URL_VALIDATION.json records every URL. The two DOI identifiers were cross-checked against cached primary publisher metadata and the primary journal PDF. Previously recorded 403/server access limitations remain; this check does not claim universal URL reachability.

The prior completed seal was preserved privately at `private/prior_completed_seal_20261015T054646Z/`, including its original manifest and every file it lists. All eight preserved artifact hashes match that original manifest.

- Prior manifest SHA-256: `5eb873b495dfd909b91cba101b049799fc7a93e7c9a6b3d0aa6c62ed03796f3f`
- Prior report SHA-256: `930b33fd006396c29d3f90dc2f6aea5eae404f11758b0277ed539f8388141273`
- Corrected report SHA-256: `d15a20f200c52c8252ae44f1ba3e73ad885ba713aabca93c71d156862a0a8258`

The refreshed safe manifest includes this receipt and SOURCE_URL_VALIDATION.json. No candidate, parent-folder artifact, Git/index/ref, or provider was mutated. No external individual was contacted.
