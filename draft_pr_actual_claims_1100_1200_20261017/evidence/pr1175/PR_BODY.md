## Accepted prior partial results; unconditional improved lower bound on hold

This AI-assisted, unrefereed audit retains credit for Stijn Cambie's 5/8
construction, Dmitry Khanukov's corrected upper certificate and lower padding
argument, Donald Della Pietra's upstream structured construction and analytic
developments, and the earlier authors cited in the complete audit.

For the maximum f(N) of a subset of {1,...,N} avoiding three pairwise distinct
positive integers with 1/a = 1/b + 1/c, the recorded audit accepts:

- liminf f(N)/N >= 5/8 from Cambie's elementary construction. Thus the subsidiary
  half-density conjecture is false.
- limsup f(N)/N <= 140803024/163562355 = 0.860852266403232... from Khanukov's
  corrected certificate, independently regenerated/checked finite inputs and
  the audited disjoint-multiplier transfer.
- Khanukov's padding implication conditional on the exact structured upstream
  witness. The implication yields a positive delta; it does not independently
  establish the full upstream analytic witness.

**H-L1/H-L2 remain uncleared for unconditional independent acceptance of the
5/8 + delta lower improvement.** The full upstream human analytic closure and
separate EP327 formal analytic chain have not been independently verified end
to end. No local Lean build, upstream source rebuild, fresh Lean-kernel replay,
or local transitive axiom-report reproduction was performed. The human and
Lean routes use different quantitative parameters and must not be conflated.
This is a verification hold, not a counterexample or an assertion that the
source's theorem is stated with an extra assumption. The upper acceptance does
not rely on clearing the lower hold.

No full resolution, convergence theorem, exact limiting density, novelty,
priority, external human peer review, journal acceptance, or new explicit
numerical lower improvement above 5/8 is claimed.

The principal source is [Khanukov's corrected 0.2.0-preprint release](https://github.com/khanukov/erdos302/releases/tag/v0.2.0-corrected-preprint),
pinned to commit 3e400a3807d22f711c7998f9537f49991925231a, dated 13 September
2026, preliminary and unrefereed. The complete ten-page manuscript and TeX
were inspected in the recorded audit. The [official problem record](https://www.erdosproblems.com/302)
records the target and Cambie's construction.

The historical independent checker regenerated 719 nontrivial divisors and
12,675 reciprocal triples; solved all 47 base prefixes; certified 2,016 scaled
configurations; checked 271 rational packings and 274 cover levels; and obtained
the exact upper fraction. Normal Python, -O and -OO historical result identities
agree. Sixteen certificate corruptions were rejected and 320 small-hypergraph
brute-force cross-checks passed. These are historical audit results. Edition
preparation did not rerun mathematical programs, execute Lean or third-party
code, install dependencies, or retrieve new scholarly sources.

The pinned upstream source inspection covered 26 EP301 and 92 EP327 Lean
modules, with 131 file Git-identity matches. The lexical guard is not a parser,
compiled proof replay, transitive axiom audit or complete mathematical review.
Successful exact-release author-side CI is explicitly distinguished from local
formal verification. Full toolchain, dependency and public-source identities
are recorded, together with inspection limits and the two lower holds.

Exactly seven authored audit/acceptance and public metadata files are proposed
as additions under unsolved_math_prioritization/attempts/2037/. The substantive
mathematical arguments are preserved with editorial framing and historical
labels. No executable code, Lean/library module, copied source document,
source-derived image, raw certificate/data, detailed result ledger, private
source, personal data or private coordination material is included. This is
not a self-contained executable reproduction package. No existing file or
QUEUE entry is changed. No publication has been performed by this local
preparation step.

## Exact public-file identities

- `ACCEPTANCE.md`: 3,312 bytes; SHA-256 `3f12a3bdc47a0de5a452c2561f88bc59459de4aee398d8f15fb847cb298e711f`.
- `MANIFEST.json`: 1,590 bytes; SHA-256 `7539edd1f7ac03686b0c63b2876b352c89241f32a49e74214441c25cf9e7d4b2`.
- `MATHEMATICAL_AUDIT.md`: 18,304 bytes; SHA-256 `e1211ed9012651fec86533301b0ebd2f6aa4f160a91c4bd0de7344a0e59aafe5`.
- `README.md`: 2,891 bytes; SHA-256 `8a3d7dc8611f0db9b76bf37d0fa54f438c9f2ea2e2b0bb5a017fdc4d6632df21`.
- `SOURCE_METADATA.json`: 82,889 bytes; SHA-256 `d882bfa8791f31a31d73cc6fd64160f46c3f1c5cf020f8487b37304cf8ec8c77`.
- `STATUS.json`: 1,682 bytes; SHA-256 `479688163a9f2a0b731283816afbee872b88ca29c0c458d9a4e16f8e3ad1014d`.
- `VERIFICATION_SUMMARY.md`: 4,436 bytes; SHA-256 `19f05cce04fc2af38d4fe3df98567161899a99b89b45efabecb954e8b03c307d`.

MANIFEST.json lists all seven public members and hashes the other six; its digest is independently pinned above.

