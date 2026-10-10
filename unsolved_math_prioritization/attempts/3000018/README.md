# Simple directed chip-firing halting is NP-complete

Problem 3000018 / AMR-029-0018 has a complete authored proof accepted by
the accompanying independent mathematical audit on 10 October 2026.
Halting of nonnegative configurations on finite loopless simple strongly
connected conservative digraphs is NP-complete under polynomial-time
many-one reductions. The separately accepted appendix proves the same
result for oriented graphs with no antiparallel arcs. Hardness persists
when deleting one specified vertex leaves a depth-at-most-one DAG and when
all initial chip counts, including their total, are polynomially bounded
in the SAT input length.

The reduction builds a genuine simple graph from modular banks and a
Boolean/CRT encoding of 3-SAT. Its legal checkpoint evolution, least-action
argument, and all output and chip bounds are proved in full. NP membership
is credited to Farrell and Levine, *CoEulerian graphs*, Section 3, and the
report supplies a self-contained specialization of their certificate method.
Farrell and Levine are also credited for the original simple-graph question
and the stable-capacity observation. No Eulerian-multigraph halting claim or
first-in-literature priority claim is made.

This is an AI-assisted, unrefereed manuscript. Acceptance means the written
proof and the separate oriented appendix passed the accompanying audit;
it does not mean external human peer review, journal acceptance, formal
proof-assistant certification, or certification of bibliographic priority
or preexisting present-day openness. The analytic arguments depend on no
omitted program or computation.

## Contents

- [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): complete modular-bank
  reduction, legal dynamics, bounds, edge cases and NP certificate
- [ORIENTED_APPENDIX.md](ORIENTED_APPENDIX.md): separately accepted
  strengthening, exact graph counts and three-cycle preprocessing
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): independent analytic audit
  of both arguments and recorded aggregate supporting checks
- [ACCEPTANCE.json](ACCEPTANCE.json): complete decisions, public mathematical
  file identities, aggregate checks and review limits
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): credited prior results, original
  question, exact language and recorded source-inspection limits
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public citations, hashes,
  sizes, locators and historical retrieval/inspection/search observations
- [STATUS.json](STATUS.json): complete accepted scope and its limitations
- [MANIFEST.json](MANIFEST.json): all nine members and exact hashes of the
  eight other files; the draft PR body independently pins the manifest

## Editorial record

The mathematical report changes its title and provisional theorem labels,
replaces pending-audit language with completed acceptance and review limits,
and updates the obsolete oriented-scope disclaimer to refer to the separately
accepted appendix. Its modular identity, CRT encoding, construction, legal
checkpoint schedule, least action, all polynomial bounds, membership proof
and trivial cases are preserved. The appendix changes only its title,
status/public-report reference and obsolete audit condition; its construction,
counts, checkpoint argument and directed three-cycle cases are unchanged.

The audit binds the distributed mathematical files, updates report and
appendix designations, and marks computational and source observations as
recorded historical evidence. All analytic review and aggregate check counts
are retained. Acceptance uses public mathematical file identities rather
than provisional input or unavailable-program references. Source metadata
retains the audit observations and adds matching public bibliography and
proof-review history, distinguishing the earlier Egres access error from
the later successful audit inspection. Status, this README, source review
and manifest are authored edition documents. No proof correction was required.

Programs, raw generated outputs, datasets, source PDFs, copied third-party
source text or images, and private coordination material are excluded.
Finite checks are supporting metadata only. Edition preparation performed
no new scholarly-source retrieval, source-file rehash, source inspection,
literature search, or mathematical test rerun. No QUEUE entry or unrelated
repository content is changed; editorial preparation adds no substantive
proof-attempt response and resets no historical accounting. No merge,
release, DOI, journal submission, or outside outreach is implied.
