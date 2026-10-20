# Rainbow four-term APs: audited partial results

Status: **UNSOLVED**, research budget **5/5**. This package contains authored partial mathematics, an independent adversarial audit, reproducible standard-library code, and exact bounded test results. No novelty is claimed. It does not establish the asymptotic prime-modulus conjecture. See SCOPE.md for the exact target and public source citations.

## Results and boundaries

- analytic/COUNT_REDUCTIONS.md: exact counting/Walsh identities, an abstract pair-marginal obstruction, and a conditional U³-uniform sufficient criterion. The abstract pair law is NOT an actual cyclic coloring, and balance does NOT imply the required U³ bound.
- quartic/QUARTIC_COSET_LEMMA.md: a positive theorem for quartic multiplicative-coset colorings only, when p is prime, p≡1 mod 4, and p≥263681. The value assigned at zero is arbitrary. This does not cover arbitrary balanced colorings.
- computation/REPORT.md: exhaustive absence at primes 5,7,11,13,17,19,23,29, conditional on implementation correctness. These are not formal refutation certificates. Independent enumeration checks 5,7,11,13,17. Prime 31 is UNKNOWN (time-limited search), never an absence result. The interval seam argument concerns only its four explicit word families.
- STRUCTURAL_ATTEMPT.md: a conditional rainbow-three-AP seed yields a generalized arc-consistency fixed point for p≥17, using separate AP constraints, unary domains, and one exact cardinality constraint. This does not obstruct joint-relation reasoning, stronger consistency, or branching, and does not establish existence of the seed.
- The exact pair-link component/subset-sum reformulation is proved. The central missing step is a uniform large-component lemma for arbitrary disjoint quarter-density anchors. That lemma is NOT proved. The disconnected p=23 example does not refute the weaker large-component condition.
- AUDIT.md records the independent mathematical/implementation review and its acceptance boundaries; it is not a proof-assistant certificate or novelty assessment.

## Reproduce

Requirements: Python 3.10+ (standard library), g++ supporting C++17, and a typical Linux/macOS shell environment. No network, external datasets, or Python packages are required. The C++ program uses GCC-compatible headers/intrinsics. All paths in the replay driver are relative to its own location; invoke it from any working directory:

    python3 /path/to/package/reproduce.py --output /path/to/fresh-results

The driver builds the executable in a temporary directory outside this package. It replays analytic and independent audit checks, structural support checks, 400 interval checks, both exhaustive enumerations, validation of recorded relaxed witnesses, and a 20-second p=31 run. Each completed prime has a generous 120-second budget; a slower computer may still time out, which is explicitly reported as a replay failure rather than absence. Timeouts are checked every 1024 nodes and are not strict real-time limits. The p=31 run normally returns UNKNOWN; a different machine may finish, so the driver records its outcome without asserting that timeout is mathematically necessary.

Historical outputs reside beside their programs. replay/ contains the post-packaging replay, environment metadata, and comparisons against historical deterministic results. Timings and timeout node counts are machine dependent. The quartic verification metadata is supported by the independent audit program’s coefficient, threshold, and histogram checks. The global-cardinality support claim is proved in text, not enumerated by the structural script.

SHA256SUMS and MANIFEST.json record each included payload file’s relative path, bytes, and SHA-256; neither inventory includes itself or the other inventory. Verify from this directory with sha256sum -c SHA256SUMS.

## Packaging provenance

The mathematical source documents are preserved, except that the audit’s target pointer now names the self-contained SCOPE.md. The independent enumerator’s stale “<=13” docstring was corrected to its actual five-prime list. No mathematical code logic was altered. Old workspace-relative hash lists were replaced by the package inventory. Historical audit language describes the original review; replay records separately document the packaged version.

Excluded: source PDFs/images, dataset contents, internal coordination/status files, queue content, executable binaries, caches, and private material. This local package does not itself perform any publication or queue update.
