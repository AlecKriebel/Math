# Priority audit for the 22 July 2026 milestone

This is a provisional mathematical-priority review, not a legal opinion and
not a guarantee that every unpublished manuscript has been found.  It records
the searches made, separates new-looking claims from known or incremental
material, and identifies what must be strengthened before submission.

## Executive verdict

It is worth drafting a short computational paper now, but it is not yet ready
to submit or post as a theorem-level preprint.

The strongest likely-new result is the solver-backed exclusion of every exact
`BS(84,83)` in the raw labelled Hamming ball of radius 18 around Eliahou's
published seed.  The fixed-`q` reduction to the empty class `TU(41)` is the
strongest mathematical companion.  The inversion-type Legendre obstructions
and the large finite local-neighborhood audits are useful supporting results,
not convincing standalone papers.

Two issues should be closed before public theorem claims:

1. replace or independently certify the 1,284 retained CP-SAT
   `INFEASIBLE` statuses used through radius 18;
2. inspect the full 2026 Eliahou update and the complete recent
   `LP(333)` literature, then circulate the draft privately to the closest
   authors for overlap checking.

## A. Radius-18 exclusion around Eliahou's seed

**Priority assessment: strongest result; likely new, with moderate
confidence.**

Eliahou's 2025 paper constructs and verifies the 64-modular matrix and exposes
the structured seed, but does not report a Hamming-ball repair exclusion.
The current SageMath construction table still lists 668 as unknown, and the
recent public `LP(333)` status report pursues a different compression route.
No located source reports the same `BS(84,83)` radius-18 theorem.

The repository's finite decomposition is unusually reproducible: it checks
the margin images, quad quotient, hashes, parent edges, root witnesses, and
the final primitive-7/14 eliminations.  Its important limitation is also
explicit.  OR-Tools CP-SAT does not emit independently replayable SAT/PB proof
transcripts here.  The artifact checker confirms that the recorded
`INFEASIBLE` statuses and all surrounding arithmetic are internally
consistent; it does not prove those statuses without trusting the solver.

Before submission, regenerate these finite instances in a proof-producing
format (for example CNF plus DRAT/LRAT, or pseudo-Boolean plus VeriPB) or have
an independent exact solver reproduce every infeasible case.  Preserve the
proof files, solver versions, commands, checksums, and a small proof checker.

## B. Fixed-`q` reduction to `TU(41)`

**Priority assessment: likely new reduction; suitable as a theorem inside the
same paper.**

The parity telescope from a hypothetical fixed-`q` repair to
`BS(42,41)` and then `TU(41)` was not found in the searched literature.
Nonexistence at the endpoint is not new: Edmondson, Seberry, and Anderson
totally enumerated inequivalent Turyn sequences of long length below 43, and
their classification has none of long length 42.

The checker verifies the new symbolic reduction but deliberately imports that
published classification.  A previous draft also gave an invalid
sum-of-two-squares shortcut.  That shortcut has been removed:
for `BS(42,41)` the relevant identity is
`C^2+D^2=162=9^2+9^2`.  This correction does not affect the reduction, but it
makes an independent modern certificate for the `TU(41)` endpoint desirable.

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
3. the certified radius-18 exclusion ladder;
4. the Legendre inversion lemmas and local searches as appendices or
   supplementary experiments.

Use a title that states the local scope, such as *Exact local obstructions
around a 64-modular Hadamard matrix of order 668*.  Do not imply a
nonexistence theorem for `H(668)`, `BS(84,83)`, or `LP(333)`.

Before posting:

- inspect the full text of Shalom Eliahou's 2026
  [update on modular Hadamard matrices](https://doi.org/10.1007/s10801-026-01544-5);
- ask Eliahou, the `LP(333)` authors, and the database authors whether they
  know overlapping unpublished work;
- upgrade the solver statuses to independently replayable certificates;
- obtain or construct a modern independent `TU(41)` certificate;
- freeze a tagged release with all inputs, hashes, versions, and checkers.

## Sources checked

- Shalom Eliahou,
  [A 64-modular Hadamard matrix of order 668](https://ajc.maths.uq.edu.au/pdf/93/ajc_v93_p422.pdf),
  *Australasian Journal of Combinatorics* 93(2) (2025), 422-427.
- Shalom Eliahou,
  [An update on modular Hadamard matrices](https://doi.org/10.1007/s10801-026-01544-5),
  *Journal of Algebraic Combinatorics* 64 (2026).
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
