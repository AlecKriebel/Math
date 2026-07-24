# Complete remaining-search estimate for the order-three LP(333) route

**Checkpoint date:** 2026-07-24

## Executive conclusion

The five classified `h=2` profiles are finite all the way to an exact
Legendre pair, but the present generic solvers do not make their complete
search feasible.  The decisive transition is not the abundant second
placement digit.  It is the next layer:

```text
36 affine variables
18 digit-2 quadratic equations
19 genuine digit-3 carry equations.
```

A neutral independence model leaves `1/3` point per profile at digit 3,
then essentially none at exactness.  This is a heuristic, not a
nonexistence proof.  The measured bounded runs have neither found a
digit-3 point nor proved one impossible.

There is a rigorous finite endpoint.  Every nonstructural displayed
residual is a signed sum of at most 135 Eisenstein units.  Therefore
vanishing through digits `0,...,8`, equivalently divisibility by
`lambda^9`, forces exact zero.  A solver should impose the exact signed
histogram equations directly; constructing the current pairwise-one-hot
digit-8 CNF would waste essentially all 16 GB of RAM.

Most importantly, failure of all five `h=2` lifts would **not** finish the
order-three route.  The `h=1` and `h=0` profile shells remain incompletely
classified.  A production prefix has now found and exactly replayed one
`h=0` profile orbit, but the unfinished census gives no total orbit count.
The two shells contain exactly 510,384 and 107,476 legal unsigned
medium-support masks.  Their mandatory local equation reduces the relevant
raw signed-medium-skeleton counts to 59,743,488 and 47,730,304, but a
straight 729-character calculation still costs between 78.35 billion
character evaluations with maximal reuse and 426.77 billion if the nine
one-high positions are processed separately.  That front end is a credible
optimized C++/symmetry project; it is not a credible Python loop.

Thus:

1. a complete generic search of the five `h=2` affine cubes is infeasible;
2. a compact, row-margin-sharded exact digit-3 attack is memory-feasible
   but has unproved runtime;
3. the compiled `h=1,0` character kernel clears its four-week throughput
   gate by more than 700 times, so end-to-end classifier orchestration is
   the best finite computation to implement next;
4. neither task presently supports a four-week forecast of `H(668)`;
5. an exact digit-3 obstruction or a complete dense-shell classification
   would itself be a credible theorem-level result.

Throughout this report, **theorem**, **upper bound**, and **heuristic** are
kept separate.

## 1. What exact completion means

For a fixed exact profile, the 54 active fibers are signed Eisenstein
phases.  Put

```text
u=(U_A0,U_A1,U_A2,U_B0,U_B1,U_B2)
```

in `Z[omega][C_37]^6`, and let

```text
P(U_0,U_1,U_2)=(U_1,U_2,omega^2 U_0)
```

on each channel.  The complete primitive-nine layer is exactly

```text
E0 = sum_i U_i U_i^*       = 167 e,
E1 = sum_i (P U)_i U_i^*   = 0.                         (1)
```

`E0` contributes 13 independent integer conditions and `E1` contributes
26, for 39 in total.  Fixed energy and the exact row-direction equations
account for three of them, leaving 36 genuinely mixed integer conditions.

The profile equation `D_t=0` supplies the `Phi_3` layer.  A compatible
physical row-margin word supplies the trivial-character/row layer.
Equation (1) supplies the `Phi_9` layer.  A decoded survivor must still be
replayed through all 333 periodic correlations before it is called an
`LP(333)`.

There are two lossless finite formulations of (1).

### Exact signed histograms

For one displayed row, let `n_j` be the signed number of phase terms with
exponent `j` and let `T` be its target.  Define

```text
A = n_0-n_2-T,
Q = (n_0+n_1-2n_2-T)/3.
```

Then

```text
F = n_0+n_1 omega+n_2 omega^2-T
  = A+(3Q-A)omega,                                      (2)

F=0  iff  A=Q=0.
```

This is the smallest known endpoint encoding: expose the sparse phase
forms and impose two signed-cardinality equalities per displayed row.

### Prime-167 group ring

On the support-167 phase shell,

```text
E0=167e  iff E0=0 modulo 167,
E1=0     iff E1=0 modulo 167.
```

The equality cases are excluded by the 37-, 3-, and 111-cycle support
orbits.  Splitting the invariant algebra gives exactly 39 `F_167` scalar
conditions.  This is an excellent independent verifier.  Enumerating the
factorwise finite-field norm cone backwards is not practical: the sparse
zero/unit inverse-CRT intersection remains the bottleneck.

These facts are proved and replayed in
`LP333_ORDER3_PHASE_FACTOR.md`,
`LP333_ORDER3_PHASE_PRIME167.md`, and
`digit3_carry_algebra/README.md`.

## 2. The five classified `h=2` profiles

### 2.1 Certified state space

There are five exact profile-zero orbits:

```text
h2-222222-0
h2-422220-0
h2-422220-1
h2-422220-2
h2-422220-3.
```

For every representative:

```text
placement trits                         54
first placement-digit rank             18
first-digit affine dimension            36
points after the first digit          3^36
                                      =150,094,635,296,999,121.
```

Thus a blind enumeration of all five spaces contains

```text
5*3^36 = 750,473,176,484,995,605 points.                (3)
```

Even at an unrealistically optimistic one billion complete exact point
tests per second, (3) takes 23.78 years.

### 2.2 Correct equation count at digits 2 and 3

**Theorem.**  Digit 2 consists of 18 nonzero quadratic equations on
`F_3^36`.  The two displayed origin rows are identically zero at this
digit.

**Theorem.**  Digit 3 has 19 genuine equations, not 18.  The delayed
`E1(origin)` row becomes a nonzero linear equation.  It is independent of
the rank-18 first-digit system, so imposing it first leaves dimension 35.
The other digit-3 conditions are ternary carry cubics in the affine
coordinates.

At the certified digit-2 witness, the combined digit-2/digit-3 Jacobian has
full column rank 36 and its linearized correction is inconsistent.  This
is a local negative result, not a global obstruction.

The exact search levels and neutral counts are:

| last zero digit | equations newly used | neutral expected points per profile |
|---:|---|---:|
| 1 | rank-18 affine system | `3^36` |
| 2 | 18 quadrics | `3^18 = 387,420,489` |
| 3 | 19 carry equations | `3^-1 = 1/3` |
| 4 | modelled as 19 further independent conditions | `3^-20` |
| 5 | same heuristic | `3^-39` |
| 6 | same heuristic | `3^-58` |
| 7 | same heuristic | `3^-77` |
| 8, exact | same heuristic | `3^-96` |

Only the equation counts through digit 3 and the exact digit-8 endpoint are
theorems.  Every expected count in the last column after the first row is
an independence heuristic.  In particular, `5*3^-96 =
7.8583e-46` is a planning signal, not a probability theorem.

The certified second-digit witness is therefore evidence that the
instrument works, but not evidence of convergence: the neutral model
expects hundreds of millions of such points per profile.

### 2.3 Rigorous exact cutoff at digit 8

Let `lambda=1-omega`.  For every nonstructural displayed residual across
the five profiles, cancellation leaves a signed sum of at most 135 units.
The `E0` origin residual is structurally zero.  Hence

```text
|F| <= 135,
Norm(F) <= 135^2 = 18,225 < 3^9 = 19,683.               (4)
```

If digits `0,...,8` vanish, then `lambda^9` divides `F`, so `3^9` divides
`Norm(F)`.  Inequality (4) forces `F=0`.  The exact verifier also exhausts
all nonzero Eisenstein integers in the norm ball and finds maximum
`lambda`-valuation exactly 8.

In the `(A,Q)` coordinates of (2), the endpoint prefix is

```text
A=0 mod 81,   Q=0 mod 81.
```

It is smaller still to assert `A=Q=0` directly.  There is no reason to
build digit 9 or a large residue automaton.

### 2.4 Row-margin joins

The exact trivial-character transfer has already been intersected with the
universal 1,756-word row-sum catalog:

| profile | compatible catalog rows | accepted assignments in the raw `3^54` phase cube | accepted fraction | reduction factor |
|---|---:|---:|---:|---:|
| `h2-222222-0` | 72 | 272,797,926,089,102,312,850 | `4.6913e-6` | 213,160 |
| `h2-422220-0` | 72 | 272,288,106,061,230,283,920 | `4.6825e-6` | 213,560 |
| `h2-422220-1` | 72 | 289,168,460,981,590,208,256 | `4.9728e-6` | 201,093 |
| `h2-422220-2` | 96 | 368,409,083,453,963,639,136 | `6.3355e-6` | 157,840 |
| `h2-422220-3` | 93 | 336,046,930,024,774,681,314 | `5.7790e-6` | 173,041 |

These are exact counts over `3^54`; their intersections with the
rank-18 affine spaces and the 18 quadrics have not been counted.

Multiplying the digit-2 neutral count by the raw row-gate fractions gives
about 1,814 to 2,455 points per profile, 10,252 in total.  This is only a
rough independence calculation.  It must not be promoted to a count:
the row gate and the digit equations are functions of the same phases and
no independence theorem is known.  They also must not be conflated.  The
row gate enforces the **augmentation**, or trivial column character, of
`E1`; the delayed displayed `E1(origin)` equation is the **coefficient at
column lag zero**.  No implication in either direction has been proved.
The correct implementation is to impose both a compatible margin and the
displayed digit equations during the search, not multiply two post hoc
selectivities.

There are 405 profile/margin shards in total.  Stabilizers and duplicate
margin signatures should be handled before launching all 405 as unrelated
jobs.

### 2.5 Current model sizes

The present generic prefix CNF uses pairwise exactly-one clauses for every
residue state.  Candidate `h2-222222-0` has the following exact projected
sizes:

| last zero digit | residue moduli used | Boolean variables | clauses | pairwise one-hot clauses |
|---:|---|---:|---:|---:|
| 2 | `3,3,9` | 37,260 | 214,418 | 91,896 |
| 3 | `9,9` | 43,824 | 297,302 | 157,536 |
| 4 | `9,9,27` | 102,900 | 1,243,166 | 925,524 |
| 5 | `27,27` | 122,592 | 1,909,886 | 1,535,976 |
| 6 | `27,27,81` | 299,820 | 9,528,098 | 8,625,096 |
| 7 | `81,81` | 358,896 | 15,254,582 | 14,178,240 |
| 8, exact | `81,81,243` | 890,580 | 81,171,086 | 78,512,004 |

Across the five candidates, the endpoint ranges are 887,652--899,124
variables and 80,911,012--81,950,382 clauses.

On the local CPython runtime, the 78.5 million two-literal clause lists
alone require approximately 10.7 GB when their list bodies, outer
references, and freshly allocated negative integers are counted.  The
remaining clauses, phase-form objects, and the solver's internal copy push
the job beyond a safe 16 GB envelope.  This encoding should not be built.

A standard sequential exactly-one replacement projects to approximately
1,770,156 variables and 5,291,246 clauses at digit 8.  It fits, but no
solve-time evidence says it will finish.

The signed-histogram CP model is much smaller.  On
`h2-422220-0`, its digit-3 instance has:

```text
993 distinct sparse phase forms
8,221 allowed table rows
2,099 variables
1,052 constraints.
```

An earlier version peaked near 517 MB.  Exact mode changes the modular
prefix to `A=Q=0` and stays in the same compact architectural class.
This is the correct endpoint representation under 16 GB.

### 2.6 Measured bounded solver rates

None of these measurements is a complete-search rate.  Branches,
conflicts, and tabu updates are not unique phase points.

| instrument | bounded result | measured activity |
|---|---|---:|
| five 300-second digit-3 tabu runs | all `UNKNOWN`, best 5--9 bad rows | 1,032,219 updates total, about 688 updates/s |
| direct prefix-2 CP-SAT, 120 s | `UNKNOWN` | 191,572 branches, 6,473 conflicts |
| direct prefix-3 CP-SAT, 300 s | `UNKNOWN` | 3,549,810 branches, 475,442 conflicts |
| sparse histogram CP-SAT, 180 s, older model | `UNKNOWN`, about 517 MB peak | 1,341,326 branches, 18,835 conflicts |
| three codimension-12 CDCL slices | no digit-2 point before cutoff | 100,000 conflicts in 28.67--33.62 s |

The fastest observed CP-SAT branch counter was about 11,833 branches/s.
If branches were unique raw points—which they are not—scanning (3) at
that rate would still take about two million years.  The only credible
path is algebraic elimination, strong decomposition, or a proof-producing
constraint search that prunes astronomical subcubes at once.

## 3. The unclassified `h=1` and `h=0` profile shells

The remaining dense shells are

```text
h=1: (n_9,n_3,n_0)=(1,15,8),
h=0: (n_9,n_3,n_0)=(0,18,6).
```

The five `h=2` objects do not cover them.  Even an exact exclusion of all
five `h=2` phase lifts leaves both shells open.

### 3.1 Exact support and signed-skeleton counts

In one opposite quartet, the mandatory lower equation permits no singleton
medium support.  The unsigned local support polynomial is

```text
U(x)=1+6x^2+4x^3+x^4.
```

Here is the complete local derivation.  Order the quartet as

```text
(A_j,A_(j+6),B_j,B_(j+6))
```

and write an active medium sign as `s_i in {+1,-1}` and an inactive slot
as zero.  The mandatory signed-skeleton equation is

```text
-s_0+s_1+s_2-s_3=0 modulo 3.                            (5a)
```

For each fixed support subset, direct enumeration of its `2^m` signings
gives:

| medium occupancy `m` | support subsets | legal signs per fixed subset | signed local states |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 |
| 1 | 4 | 0 | 0 |
| 2 | 6 | 2 | 12 |
| 3 | 4 | 2 | 8 |
| 4 | 1 | 6 | 6 |

The second and fourth columns give `U(x)` and

```text
S(x)=1+12x^2+8x^3+6x^4,                                (5b)
```

respectively.  This is independently pinned as the local histogram
`(1,0,12,8,6)` by
`shell_two_exact/verify_shell_two_partition_theory.py`; it is not inferred
from the later global counts.

The exact support counts are therefore

```text
[x^15] U(x)^6 = 510,384,
[x^18] U(x)^6 = 107,476.                               (5)
```

Thus the relevant raw signed-medium-skeleton counts, in the same convention
as the completed `h=2` enumeration, are

```text
[x^15] S(x)^6 = 59,743,488,
[x^18] S(x)^6 = 47,730,304.                            (6)
```

For comparison, the deliberately loose bounds obtained by assigning all
medium signs before the mandatory local equation are

```text
510,384 * 2^15 = 16,724,262,912,
107,476 * 2^18 = 28,174,188,544.
```

Equation (6), not these loose products, is the correct starting count.

The `h=1` support leaves nine nonmedium positions.  Choosing the high
position gives a factor nine.  Its three phases are indistinguishable at
the first quadratic digit and enter one digit later.  Consequently:

```text
h=1 signed skeleton/high-position states
  <= 59,743,488 * 9
   = 537,691,392,

h=1 fully high-oriented skeleton states
  <= 59,743,488 * 9 * 3
   = 1,613,074,176.
```

These are upper bounds before aggregate targets and exact correlations.

### 3.2 Affine phase upper bounds before the six quadratic equations

If `r` quartets are nonempty, the lower local and channel rows have rank
`r+1`, so the medium-phase affine dimension is

```text
d=n_3-(r+1).
```

The signed-skeleton counts by `r` are:

| shell | `r` | signed skeletons | `d` |
|---|---:|---:|---:|
| `h=1` | 4 | 103,680 | 10 |
| `h=1` | 5 | 12,085,248 | 9 |
| `h=1` | 6 | 47,554,560 | 8 |
| `h=0` | 5 | 1,296,000 | 12 |
| `h=0` | 6 | 46,434,304 | 11 |

These rows are the coefficient extractions

```text
[x^n y^r] (1+12 y x^2+8 y x^3+6 y x^4)^6,              (6a)
```

with `(n,r)=(15,4),(15,5),(15,6),(18,5),(18,6)`.
They sum to the two values in (6), and substituting
`d=n-(r+1)` reproduces the affine upper totals below.  This provides a
detached source check on every by-`r` number rather than distributing the
global totals heuristically.

If every affine system were consistent, summing `3^d` over these skeletons
would give the rigorous loose upper bounds

```text
h=1 medium-phase points                  556,001,604,864
h=1 after 9 high positions             5,004,014,443,776
h=1 after the 3 later high phases     15,012,043,331,328
h=0 medium-phase points                8,914,445,186,688
combined fully oriented upper         23,926,488,518,016. (7)
```

Aggregate targets and quadratic/exact correlations can only reduce (7).
It is not a survivor count.

### 3.3 The 729-character cost

For a fixed affine quadratic map

```text
Q:F_3^d -> F_3^6,
```

all six first quadratic equations can be counted exactly using the 729
additive characters of `F_3^6`.  Each character requires only small
`d<=12` linear algebra.  A positive fiber can be self-reduced to a witness;
a zero fiber excludes that skeleton at this digit.

The raw character counts are:

| shell/work unit | work units | 729-character evaluations |
|---|---:|---:|
| `h=1`, one transform per legal signed medium skeleton | 59,743,488 | 43,553,002,752 |
| `h=0`, one transform per legal signed medium skeleton | 47,730,304 | 34,795,391,616 |
| **maximum reuse subtotal** | 107,473,792 | **78,348,394,368** |
| `h=1`, if nine high positions require separate transforms | 537,691,392 | 391,977,024,768 |
| `h=0` as above | 47,730,304 | 34,795,391,616 |
| **unbatched high-position subtotal** | 585,421,696 | **426,772,416,384** |

The polar restriction depends on the unsigned support, not on every sign
or high phase.  Precomputing its 729 pencil reductions for all supports
would require

```text
(510,384+107,476)*729 = 450,419,940
```

support-character reductions.  Sign, target, and high-position effects can
then reuse those reductions while changing affine/linear data.  The
implementation should benchmark how much of the nine-position factor can
be batched.

**Heuristic only.**  Treating the six coordinates as independent would
divide the upper (7) by 729, leaving about 32.82 billion first-quadratic
points.  The existing theorem proves only that one particular sum of the
six forms is surjective with large fibers; it neither proves uniformity of
the six-map nor predicts its zero fibers.  The 729 transform must be
evaluated.

### 3.4 Symmetry caveats

The certified profile group has order 24:

```text
C6 x C2_A x C2_B.
```

It gives at most a factor-24 reduction.  Stabilizers occur: the five
`h=2` profile orbits already have sizes 12 and 24.  Therefore raw counts
cannot simply be divided by 24 and called orbit counts.

For `h=1`, a support or medium skeleton stabilizer need not fix its high
position or later high phase.  Canonicalization must be performed on the
complete decorated object, or every full group image must be expanded and
deduplicated.  Quotienting the support first and multiplying by an assumed
orbit size can miss or double-count profiles.

If the action were free everywhere, the two character-cost subtotals would
fall to approximately 3.26 billion and 17.78 billion.  Those are
best-case planning figures, not certified orbit counts.

### 3.5 What follows a dense-shell profile hit

The 729-character layer is still a profile layer.  Every positive count
requires:

1. self-reduction to explicit profile phases;
2. all upper profile digits or detached exact `D_t=0` replay;
3. full order-24 orbit canonicalization;
4. a new 54-trit physical phase lift for every exact profile orbit.

The 54-active-fiber theorem applies to every norm-54 profile, so the raw
physical phase cube is always `3^54`.  The rank-18 first digit is measured
for the five `h=2` profiles only; it must not be assumed for new `h=1,0`
profiles.  The universal 1,756-word row-margin catalog and trivial-character
transfer remain available and should be applied immediately to each new
profile.

No honest complete phase-lift cost can be assigned to `h=1,0` until the
profile classification gives the number and first-digit ranks of its exact
orbits.

### 3.6 Measured lift geometry of the first exact `h=0` profile

The first production prefix found the exact profile

```text
A IDs = 1,1,2,4,4,5,1,1,2,4,4,5
B IDs = 5,5,1,7,4,1,5,5,1,7,4,1
target  = (2,-2,-4,-2).
```

It has a profile half-turn and first-layer splitting

```text
F_3^36 = V+ direct-sum V-,
dim(V+),dim(V-) = 21,15.
```

In the 27 natural opposite-class pairs, `V-` is a ternary `[27,15,4]`
code.  Its complete weight census has six weight-four words and fourteen
weight-five words.  The second digit splits into twelve even quadrics and
six odd bilinear equations.  The exact common-zero count of the six odd
equations is

```text
205,901,492,005,503.
```

This is essentially the generic `3^30` scale and is not a contraction.
Enumerating a generic fixed-anti slice currently takes about four seconds
in the exact NumPy prototype.  Applying that rate to all `3^15` anti words
would take roughly 664 one-core days, or 66 ideal ten-core days, merely to
reach digit two.  This is a measured implementation projection, not a
lower bound and not a forecast for optimized compiled algebra.

The two smallest anti-weight families have been exhausted:

| anti weight | signed words | signed digit-two points | exact row-margin intersection | best digit-three defect |
|---:|---:|---:|---:|---:|
| 4 | 6 | 266 | 0 | 6 rows |
| 5 | 14 | 392 | 0 | 7 rows |

The row-margin layer is not empty at minimum anti weight.  Anti weight zero
has no physical precursor, while one projective weight-four direction has
exactly 7,346 first-digit row-margin placements for each sign.  Its 87
digit-two points are disjoint from those 7,346 placements.  This is a
certified low-weight incompatibility, not a whole-profile obstruction.

A separate canonical asymmetric slice contains an exact digit-two point,
but it fails row margins and leaves 13 digit-three rows nonzero.  A
300-second compact digit-three solve on its 15 free trits returned
`UNKNOWN` after 4,340,808 branches.  The all-target row-margin-aware
digit-two model likewise returned `UNKNOWN` after 180 seconds and
2,065,449 branches.

An exact algebra audit also rules out the most direct spectral contraction.
The relative operators of the global `x` and `y` polar pencils generate
the full algebras `M_21(F_3)` and `M_15(F_3)`.  On the canonical
asymmetric slice the restricted operators again generate `M_15(F_3)`.
Neither system has a common affine recentering.  Therefore there is no
simultaneous invariant-block decomposition or ordinary one-field
trace/norm model of these quadrics.  This does not rule out nonlinear
elimination, but it removes the simplest route to making the full search
finite on this host.

Consequently the complete remaining search for this one `h=0` profile is
still unestimated at the decisive digit-three layer.  The half-turn
decomposition provides a natural sharding coordinate and exact low-weight
certificates, but no complete runtime bound.  Neither the isolated profile
nor its abundant digit-two points count as convergence toward `LP(333)`.

## 4. CPU, RAM, and disk planning

### 4.1 Five `h=2` lifts

**CPU.**  Raw enumeration is ruled out by (3).  The compact digit-3/exact
histogram model is small enough for aggressive sharding, but current
bounded rates give no basis for extrapolating a completion time.  The
search should be gated on either:

- a strong algebraic reduction of the 18 quadrics plus 19 carries;
- a proof-producing solve of a meaningful margin/profile shard; or
- a digit-3 witness that survives exact row margins.

Repeating generic 300-second stochastic runs is exploration, not progress
toward exhaustion.

**RAM.**  The sparse CP model's measured peak near 517 MB leaves room for
several workers within 16 GB.  Four concurrent workers would use roughly
2--3 GB for models before process/runtime overhead and are a conservative
local choice while other research programs run.  The pairwise digit-8 CNF
is unsafe.  More RAM would make that poor encoding loadable but would not
make its search tree small.

**Disk.**  Do not materialize the neutral `5*3^18=1,937,102,445`
second-digit points.  Their information-theoretic state payload is already
about 15.5 GB at eight bytes each; realistic 16--32-byte records require
31--62 GB.  Stream survivors into the next gate and checkpoint only shard
indices, solver seeds, hashes, and explicit best/witness assignments.
Proof logs for a genuine UNSAT shard need an explicit disk cap because
their size is presently unmeasured.

### 4.2 Dense profile shells

The 78.35-billion and 426.77-billion character totals translate into the
following throughput targets on ten ideally scaling cores:

| scope | per-core rate for 72 hours | per-core rate for 28 days |
|---|---:|---:|
| maximum-reuse subtotal, 78.35B | 30,227 characters/s | 3,239 characters/s |
| unbatched high-position subtotal, 426.77B | 164,650 characters/s | 17,641 characters/s |

At 100,000 character evaluations/s/core, the unbatched subtotal is about
49.4 single-core days or 4.94 ideal ten-core days.  At 10,000/s/core it is
about 49.4 ideal ten-core days.  These are arithmetic front-end times, not
end-to-end classification times; survivor self-reduction and exact replay
remain.

The required rates are plausible only for specialized compiled code with:

- support-level matrix-factorization reuse;
- batched right-hand sides and high positions;
- orbit canonicalization before expensive work;
- streaming aggregation with no per-character output.

### 4.2.1 Measured compiled follow-up

The proposed exact arithmetic kernel has now been implemented and
independently replayed in
`scratch_dense_shell_benchmark/`.  On one M1 Pro core, the conservative
three-run combined median is

```text
12,668,666 character evaluations/second/core.
```

This is 718 times the 28-day threshold and 76.9 times the 72-hour
unbatched threshold above.  A separate reference enumerates one real
`h=1` affine cube and one real `h=0` affine cube and agrees on all 1,458
exact Eisenstein character sums.  The optimized benchmark uses less than
5.1 MB resident memory.

Including the separately measured support-pencil factorization rate, the
arithmetic-only projections are about 1.86 one-core hours for the
78.35-billion maximal-reuse subtotal and 9.50 one-core hours for the
426.77-billion unbatched subtotal.  This decisively passes the narrow
compiled-rate gate and corrects the deliberately conservative
10,000--100,000/s planning examples.

It does **not** estimate full classification time.  Complete support and
signed-skeleton streaming, order-24 canonicalization, positive-fiber
self-reduction, upper-digit checks, row-margin joins, and exact replay are
outside the timed loop.  Those are now the bottleneck to measure.

**RAM.**  Streaming one support orbit at a time should stay well below
16 GB.  Storing one byte for all 450,419,940 support-character pairs costs
about 450 MB; eight bytes costs 3.60 GB; a 32-byte decomposition costs
14.4 GB before indexing.  Full decompositions should therefore be streamed
or cached by orbit/type, not retained globally.

**Disk.**  Never write the 78--427 billion character results.  Even one
byte per result is 78--427 GB.  Store only aggregate counts, positive
fibers, canonical witnesses, and resumable shard checkpoints.  A few GB is
enough for the intended streaming design.

### 4.3 Would more hardware change feasibility?

More CPU cores would materially accelerate the dense support/skeleton
shards, which are naturally parallel, and would help independent
profile/margin CP shards.  A 32--64-core server or small cluster could
turn a successful compiled dense-shell benchmark into a practical
classification run.

More than 16 GB of RAM is secondary.  It permits larger caches and naive
CNFs, but the principal bottleneck is combinatorial pruning and arithmetic
throughput.  The exact histogram model and a streaming dense enumerator
already fit locally.  GPU acceleration may help batched small-field
arithmetic, but the M1 GPU shares the same 16 GB and no current exact
implementation demonstrates a useful rate.

For the five `h=2` cubes, additional commodity cores do not rescue blind
search.  They matter only after a decomposition creates genuinely
independent, strongly pruned shards.

## 5. Recommended finite gate

### First priority: exact `h=2` digit-3 gate

1. Use the sparse histogram variables, not high-modulus prefix automata.
2. Impose one compatible row-margin signature at a time, with symmetry
   deduplication across the 405 raw profile/margin pairs.
3. Include the delayed `E1(origin)` exact row at the start.
4. Seek either an explicit digit-3 survivor or a complete proof on a
   nontrivial collection of shards.
5. If a digit-3 point appears, switch immediately to `A=Q=0`; digits 4--8
   need not be searched sequentially.

A digit-3 point would be a meaningful milestone.  Another digit-2 point
would not.

### Parallel priority: compiled `h=1,0` profile classifier

1. Reproduce (5)--(6) and the counts by `r` in compiled code.
2. Benchmark all 729 characters with support-level factorization reuse.
3. Measure batching across the nine `h=1` high positions.
4. Canonicalize complete decorated objects under the order-24 group.
5. Run only if the measured rate meets the 28-day threshold or symmetry
   reduces it enough.
6. Exact-replay every positive profile and report counts, not sampled
   successes.

### Stop/go interpretation

- **Go:** an algebraic digit-3 reduction, a certified digit-3 point, or a
  dense-shell compiled rate comfortably above 17,641 character
  evaluations/s/core without exhausting RAM.  The arithmetic-only dense
  benchmark now meets this last condition at 12,668,666/s/core, while the
  end-to-end classifier remains unmeasured.
- **Publish/pivot:** a complete digit-3 obstruction for one or more
  `h=2` profiles, or a complete exact classification/exclusion of either
  dense shell.
- **Stop headline search:** only more digit-2 witnesses, repeated
  `UNKNOWN` runs without increasing certified coverage, or a dense-shell
  benchmark that misses the four-week rate by more than an order of
  magnitude.

## 6. Scope warning

This report estimates the **order-three invariant LP(333) construction
program**.  Eliminating the five `h=2` lifts does not eliminate `h=1,0`.
Eliminating all of these profile shells would close this order-three
profile route, not prove that no unrestricted Legendre pair of length 333
exists and not prove that no Hadamard matrix of order 668 exists by some
other construction.

The mechanically verified five-orbit classification remains valuable
regardless of the phase-lift outcome.

## 7. Arithmetic replay

From `hadamard_668_search`, the dependency-free audit

```text
python3 verify_complete_remaining_search_estimate.py
python3 -m unittest -v test_complete_remaining_search_estimate.py
```

recomputes both local generating functions, all support and signed-skeleton
coefficients, the counts by nonempty quartet, every affine upper bound, all
three 729-character work totals, the 405 row-margin shards, the five-cube
volume, and the exactness inequality.  Its semantic hash is

```text
c4eddd59d76d36f5c1b133a972e8e451afd6ed3bdadf95e8b3ebcffe54fffa56
```
