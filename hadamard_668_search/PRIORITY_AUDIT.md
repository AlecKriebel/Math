# Priority audit for the 22 July 2026 milestone

This is a provisional mathematical-priority review, not a legal opinion and
not a guarantee that every unpublished manuscript has been found.  It records
the searches made, separates new-looking claims from known or incremental
material, and identifies what must be strengthened before submission.

## Executive verdict

It is worth privately circulating a short computational paper now, but it is
not yet ready to submit or post as a theorem-level preprint.

The strongest theorem-sized likely-new result is the fixed-`q` reduction to
the empty class `TU(41)`.  Its 1994 endpoint has now also been reproduced by
an independent 461-shard enumeration.  The solver-backed radius-18 exclusion
around Eliahou's seed is promising and likely new, but remains a
computational claim until all 1,296 infeasible leaves are independently
certified.  The inversion-type Legendre obstructions and the large finite
local-neighborhood audits are useful supporting results, not convincing
standalone papers.

Two issues remain before public radius-18 theorem claims:

1. replace or independently certify all 1,296 retained CP-SAT
   `INFEASIBLE` statuses used through radius 18: 1,284 at the
   primitive-root layer and 12 at the primitive-7/14 compression layer;
2. inspect the body of Eliahou's 2026 update if it becomes lawfully accessible
   without outreach, and obtain independent expert review before submission.

The openly available recent `LP(333)` papers and March 2026 status report
have been inspected.  The symmetric/symmetric observation is prior; the
skew/skew and mixed equations were not located but are incremental
specializations, not paper-leading results.  Project policy prohibits all
external outreach; no contact drafts or recipient lists are retained.

## A. Radius-18 exclusion around Eliahou's seed

**Priority assessment: strongest computational result; likely new, with
moderate confidence.**

Eliahou's 2025 paper constructs and verifies the 64-modular matrix and exposes
the structured seed, but does not report a Hamming-ball repair exclusion.
The current SageMath construction table still lists 668 as unknown, and the
recent public `LP(333)` status report pursues a different compression route.
No located source reports the same `BS(84,83)` radius-18 computation.

The repository's finite decomposition is unusually reproducible: it checks
the margin images, quad quotient, hashes, parent edges, root witnesses, and
the final primitive-7/14 eliminations.  Its important limitation is also
explicit.  OR-Tools CP-SAT does not emit independently replayable SAT/PB proof
transcripts here.  The artifact checker confirms that the recorded
`INFEASIBLE` statuses and all surrounding arithmetic are internally
consistent; it does not prove those statuses without trusting the solver.

Before submission, regenerate all 1,296 finite instances in a proof-producing
format (for example CNF plus DRAT/LRAT, or pseudo-Boolean plus VeriPB) or have
an independent exact solver reproduce every infeasible case.  Preserve the
proof files, solver versions, commands, checksums, and a small proof checker.
The existing checker independently validates the twelve decoded root
witnesses, but that witness replay does not certify the twelve subsequent
compression-target infeasibility claims.

The first certification prototype is complete.  Four representative leaves
(radius 16, shell 17, shell 18, and shell-18 primitive 7) regenerate to
deterministic CNF and pass `drat-trim`; final replay used 250 MB peak RSS.
This is 4/1,296 coverage.  One known feasible root model also passes an
independent positive-model checker with the symmetry quotient enabled.  In
addition, all twelve stored root witnesses extend to SAT models of their
exactly pinned, unquotiented v2 CNFs and pass every clause plus independent
mathematical checks.  A separate exhaustive contribution-signature regression
reconstructs all 83 endpoint quads and verifies the exporter's global root
orbit partition for every even four-bit mask.  The exporter also has small
exhaustive regressions.

A naïve batch is not currently responsible.  One hard raw-bit proof grew to
388 MB without finishing; z7+z14 strengthening timed out at 60 seconds and
peaked at 1.785 GB RSS.  The next bounded step is an exact orbit-count CNF for
the six hard root leaves, followed by a proof-size audit before any corpus run.

## B. Fixed-`q` reduction to `TU(41)`

**Priority assessment: likely new reduction; suitable as a theorem inside the
same paper.**

The parity telescope from a hypothetical fixed-`q` repair to
`BS(42,41)` and then `TU(41)` was not found in the searched literature.
Nonexistence at the endpoint is not new: Edmondson, Seberry, and Anderson
totally enumerated inequivalent Turyn sequences of long length below 43, and
their classification has none of long length 42.

The symbolic checker verifies the new reduction.  A separate independent
outside-in enumerator now reproduces the published endpoint: 461/461
canonical depth-five shards, 57,543,021 nodes, and zero solutions.  An
independent Python program exhausts all `2^19` assignments defining the shard
cover; ASan/UBSan regressions reproduce the known small cases at short
lengths 3, 7, and 9.  The computation supports the theorem while continuing
to credit the 1994 classification.

A previous draft also gave an invalid
sum-of-two-squares shortcut.  That shortcut has been removed:
for `BS(42,41)` the relevant identity is
`C^2+D^2=162=9^2+9^2`.  This correction does not affect the reduction.

A promising unproved extension is to test whether the same telescope works
for Eliahou's apparent family
`q_k=(16k+3,2,16k+1,1)`, reducing fixed-`q_k` repair to `TU(8k+1)`.
That is a research direction, not a claim in this milestone.

## C. Legendre-pair symmetry and profile results

**Priority assessment: mixed; supporting material only in its current form.**

The symmetric/symmetric obstruction is already subsumed by the public
modulo-3 multiplier obstruction: inversion is a multiplier congruent to 2
modulo 3.  It should not be presented as a new result.

No explicit prior statement was located for the normalized skew/skew
certificate `v^2+w^2=222` or the mixed certificate
`x^2+3y^2=667`.  These are clean and may be new specializations, but they are
elementary and narrow.  A general theorem for lengths divisible by three
would be more publishable than the isolated `333` cases.

The 21 compressed profiles are sampled, not exhaustive, and are a tiny subset
of a landscape for which the March 2026 status report claims an exhaustive
9-compression computation with 12,017,243 compatible configurations.  The
profile-4 and profile-19 finite-neighborhood results are independently
verified and computationally substantial, but they prove only local
minimality in explicitly defined move graphs.  They are useful validation
data and negative search evidence, not evidence that `LP(333)` is globally
impossible.

## Recommended paper and release plan

Draft one compact paper organized around:

1. Eliahou's structured quadruple and its exact translation to `BS(84,83)`;
2. the fixed-`q` parity telescope and reduction to `TU(41)`;
3. the radius-18 solver report and proof-certification ladder;
4. the Legendre inversion lemmas and local searches as appendices or
   supplementary experiments.

Use a title that states the local scope, such as *Exact local obstructions
around a 64-modular Hadamard matrix of order 668*.  Do not imply a
nonexistence theorem for `H(668)`, `BS(84,83)`, or `LP(333)`.

Before posting:

- obtain and inspect the full text of Shalom Eliahou's 2026
  [update on modular Hadamard matrices](https://doi.org/10.1007/s10801-026-01544-5);
- upgrade the solver statuses to independently replayable certificates;
- freeze a tagged release with all inputs, hashes, versions, and checkers.

The independent `TU(41)` enumeration is complete.  Full-text access to the
2026 article was not lawfully available during this audit.  No author contact
will be attempted; priority language must remain provisional unless public
sources or independent review resolve the overlap question.

## Sources checked

- Shalom Eliahou,
  [A 64-modular Hadamard matrix of order 668](https://ajc.maths.uq.edu.au/pdf/93/ajc_v93_p422.pdf),
  *Australasian Journal of Combinatorics* 93(2) (2025), 422-427.
- Shalom Eliahou,
  [An update on modular Hadamard matrices](https://doi.org/10.1007/s10801-026-01544-5),
  *Journal of Algebraic Combinatorics* 64 (2026); metadata and abstract
  checked, full body unavailable in the audit environment.
- G. M. Edmondson, Jennifer Seberry, and M. R. Anderson,
  [On the existence of Turyn sequences of length less than
  43](https://documents.uow.edu.au/~jennie/WEBPDF/1994_03.pdf),
  *Mathematics of Computation* 62 (1994), 351-362,
  [doi:10.1090/S0025-5718-1994-1203733-8](https://doi.org/10.1090/S0025-5718-1994-1203733-8).
- Dragomir Ž. Đoković,
  [Classification of base sequences `BS(n+1,n)`](https://arxiv.org/abs/1002.1414),
  enumerating `n <= 30`, not the present `n=83` case.
- Przemysław Chojecki,
  [Computational Search for a Hadamard Matrix of Order 668 via Legendre
  Pairs of Length 333](https://www.ulam.ai/research/frontier-had.pdf),
  status report, March 2026.
- Ilias Kotsireas, Roberto Gallardo-Cava, Ana Isabel Gómez, and Domingo
  Gómez-Pérez,
  [On the search of binary Legendre pairs of length
  `pq^2`](https://doi.org/10.1016/j.jsc.2026.102606),
  *Journal of Symbolic Computation* 138 (2027), article 102606.
- Matteo Cati and Dmitrii V. Pasechnik,
  [A database of constructions of Hadamard
  matrices](https://arxiv.org/abs/2411.18897), 2024.
- [SageMath's current Hadamard construction
  documentation](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/matrices/hadamard_matrix.html),
  which lists 668, 716, 892, and 1132 as unknown in its implemented range.
