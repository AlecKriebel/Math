# Independent acceptance report

Problem 2800903 / AMR-027-0903, rank 989. Date: 2026-10-07 UTC.

## Decision

**Accepted as unresolved partial results, with two separate corrections supplied.** All five written mathematical routes pass independent review. No theorem-level correction is needed. This acceptance does not resolve the original unplanted random-model question, establish novelty, or represent human peer review.

The accepted mathematical claims are:

1. The six-point planar k = 2 feasible fractional witness is strictly cheaper than every integral solution, with certified gap at least 232103/400000. Its value is not asserted to be the exact LP optimum.
2. Systematic interval rounding proves an integral optimum for the ordinary data-point k-median LP on a line.
3. With six Gaussian points and k = 2, the failure probability has strictly positive liminf as dimension alone grows. Full support of the fixed-dimensional limiting distance vector is valid.
4. Gaussian distance concentration yields a near-one optimal-value ratio uniformly over k when log(n+1) = o(d); this is not exact LP integrality.
5. Replication yields positive finite-sample failure probability for n = 6r in every finite dimension at least two; its exhibited event does not give a uniform or joint-asymptotic lower bound.

## Corrections and their validation

- `VERIFY_HARDENING.patch`, embodied in `verify_hardened.py`, replaces Python's optimization-removable assertion with an explicit conditional `AssertionError`. The unpatched original is not accepted as an optimization-safe verifier.
- `SOURCE_SCOPE.patch`, embodied in `SOURCE_NOTES_corrected.md`, changes one unsupported abstract-only qualifier from planar to Euclidean. No mathematical result depends on that optional older reference.

Both patches are against the preserved original files and are intentionally supplied separately. Their presence does not mean the original frozen files were silently edited. Future corrected packaging should apply the patches or explicitly direct verification to the hardened copy, while retaining the original freeze and this audit provenance.

## Verified evidence

Frozen manifest SHA-256:

`58932d752e971ec0789b637ceab3ae3f0246927befb6bece2dcb1188ae034100`

All eight original file hashes and byte counts match. The original packet remains unchanged. All five archived scholarly-source byte/hash entries match their source manifest; only metadata and authored analysis are included here.

Python 3.12.14 validation:

- Original and hardened valid runs, normal / `-O` / `-OO`: six baseline passes, each producing exactly the frozen `verification.json` bytes.
- Original negative controls: all ten rejected normally; all ten falsely accepted under each optimized mode.
- Hardened negative controls: all ten rejected under every mode, before any report is written.
- Independent audit replay: 30,090 explicit checks. Normal, `-O`, and `-OO` audit execution produce identical `AUDIT_CHECKS.json` bytes.

The primary-source scope review preserves the distinction between Del Pia–Ma planted exact-recovery failure and a strict global LP/IP gap. It also preserves the unspecified n/d/k growth regime in the historical source question. No source-derived theorem was used beyond its checked hypotheses.

## Review artifacts

- `FULL_AUDIT.md`: complete claim-by-claim mathematical and source-scope analysis.
- `replay_audit.py`: source-free reproducible exact replay and mutation suite.
- `AUDIT_CHECKS.json`: complete baseline and mutation outcomes.
- `SOURCE_AUDIT_METADATA.json`: public source titles, URLs, hash/size checks, and inspection limits.
- Two correction patches and their corrected file copies.
- `AUDIT_MANIFEST.json`: byte counts and SHA-256 digests for the acceptance bundle.

No source PDFs, copied source text, external datasets, private sources, private personal information, or private coordination material are part of this acceptance bundle. No publication action was taken by this review.
