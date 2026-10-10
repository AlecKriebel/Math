# EP302: audit of credited partial results

This AI-assisted, unrefereed edition records a bounded audit of known results
for the maximum size f(N) of a subset of {1,...,N} containing no three pairwise
distinct positive integers a,b,c satisfying 1/a = 1/b + 1/c.

## Disposition

- Stijn Cambie's construction: accepted; liminf f(N)/N >= 5/8. This disproves
  the subsidiary half-density conjecture.
- Dmitry Khanukov's corrected upper result: accepted by the historical
  independent exact certificate checks and audited mathematical transfer;
  limsup f(N)/N <= 140803024/163562355 = 0.860852266403232...
- Khanukov's padding argument: accepted conditional on the precisely stated
  structured witness from Donald Della Pietra's upstream work.
- Unconditional 5/8 + delta lower improvement: independent acceptance remains
  on H-L1/H-L2 hold for the upstream analytic closure/formal replay. This is a
  verification hold, not a counterexample or an allegation that the author's
  theorem is stated conditionally.
- No convergence, exact limiting density, full resolution, novelty, priority,
  or new explicit numerical improvement above 5/8 is claimed.

The principal source is Khanukov's [corrected 0.2.0-preprint release](https://github.com/khanukov/erdos302/releases/tag/v0.2.0-corrected-preprint),
pinned to commit 3e400a3807d22f711c7998f9537f49991925231a. It is preliminary
and unrefereed. The [official problem record](https://www.erdosproblems.com/302)
records the target and Cambie's construction. Credit also remains with Della
Pietra and the earlier authors identified in the full audit.

## Reading this edition

- MATHEMATICAL_AUDIT.md preserves the substantive construction, exact-check
  account, upper transfer, conditional padding proof, semantic audit, holds,
  and prior-result distinctions, with tracked editorial framing.
- ACCEPTANCE.md states the accepted implications and exact remaining gap.
- VERIFICATION_SUMMARY.md distinguishes historical independent tests, source
  inspection, author-side CI, and checks not performed.
- SOURCE_METADATA.json gives public source identities and historical
  retrieval/inspection metadata without reproducing source contents.
- STATUS.json is the machine-readable disposition.
- MANIFEST.json lists the seven public files and hashes the other six.

No executable program, Lean source, raw certificate, copied source document,
source-derived image, or detailed test dataset is distributed. The recorded
mathematical tests were not rerun during edition preparation. Source hashes
and successful public CI metadata do not clear the lower verification hold.
This is not a self-contained executable reproduction package or an external
human referee report. Historical observations refer to 10 October 2026;
this edition does not certify the present state of upstream repositories or
provide an exhaustive literature/priority search.
