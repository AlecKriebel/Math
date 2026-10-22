# Delone cluster groups: five bounded proof attempts

Problem 20001782 / AIM-GEOMETRY-0120. Checked 3 October 2026.

**Status: the original group-order problem is unresolved after 5/5 attempts.**
No full solution, general counterexample, or novelty claim is made. These
are AI-assisted research notes, not a refereed paper.

## Original question

For fixed d>=4, bound the order of the centered 2R-cluster group of every
2R-regular Delone set in R^d by a constant depending only on d. The exact
packing and covering radii are r and R. The bound must be independent of
R/r. Cluster equivalences preserve their marked centers.

See [SOURCE_GATE.md](SOURCE_GATE.md) for the original AIM source, current
primary literature, conventions, retrieval limits, and prior-attempt check.
The catalogue's displayed title describes earlier partial work, not this
full target. The exact live catalogue page returned 403 during this check.

## Results and failed routes

1. [Attempt 1](ATTEMPT_1.md): rectangular lattices show that no dimension-only
   multiple of r forces even rank two of the local cluster. Their exact
   symmetry groups remain bounded, so this is a failed-route certificate,
   not a counterexample to the original question.
2. [Attempt 2](ATTEMPT_2.md): if the ar-cluster has rank k, its restricted
   group has order at most (a+1)^(k^2), leaving a finite kernel in O(d-k).
   In particular, rank d-1 gives |S_x(2R)|<=2(a+1)^((d-1)^2).
3. [Attempt 3](ATTEMPT_3.md): real character pairing sharpens a conditional
   Jordan reduction to a factor of order m^floor(d/2). A direct metric
   packing argument independently proves bounded element orders suffice.
   The required uniform element-order bound is still absent.
4. [Attempt 4](ATTEMPT_4.md): a rank plateau propagates short-span directions
   along short-neighbor components. A globally regular paired-layer example
   has ladder components that fail to cover their affine spans, blocking
   direct inheritance of a lower-dimensional Delone problem.
5. [Attempt 5](ATTEMPT_5.md): an invariant rank-d lattice would give an
   explicit mod-3 bound. An irrational two-coset regular set shows that the
   canonical cluster-generated additive module need not be such a lattice.
   This does not show that the symmetry group lacks a different rational form.

These elementary lemmas and examples are not advertised as new. The known
full-span estimate and Jordan strategy are background; the useful output
is a more precise conditional reduction and explicit exclusion of unjustified
intermediate claims. The general Delone-specific compatibility step remains
unproved. There is no claimed resolution of the sufficiently-large-d
2^d d! conjecture, either.

## Verification

Run `python verify_examples.py`. It uses only Python's standard library and
reproduces [checks.json](checks.json):

- 30 rectangular-lattice parameter/rank/group-count controls
- 12 paired-layer rank and centered-equivalence controls
- 11 exact quadratic-field inequalities for the irrational two-coset family
- 100 conjugated finite-order matrix controls for the mod-3 certificate
- 480 exact checks of the real-character maximum formula

These are finite regression checks, not substitutes for the written proofs
or evidence of a general solution. The irrationality and nondiscreteness
arguments are analytic, not inferred from floating-point computation.

The [research log](RESEARCH_LOG.md) records all five attempts. Retrieval,
checks, review, and packaging are not additional proof-attempt turns.
