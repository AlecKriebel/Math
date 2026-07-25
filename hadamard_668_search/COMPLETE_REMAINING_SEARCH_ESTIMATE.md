# Complete remaining-search estimate for the order-three LP(333) route

**Checkpoint date:** 2026-07-25

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
order-three route.  The `h=1` shell remains unclassified.  The formerly
open `h=0` census is now complete: all 729 shards cover 47,730,304 raw
decorations and 25,368,365,895,696 weighted primitive leaves, and detached
integer replay proves that exactly 18 inequivalent canonical profile orbits
survive.  Twelve have orbit size 24 and six have orbit size 12.  All
eighteen have first-placement rank/nullity `18/36`; that is a classification
of profile inputs, not a classification of their physical lifts.

The two dense shells contain exactly 510,384 and 107,476 legal unsigned
medium-support masks.  Their mandatory local equation reduces the relevant
raw signed-medium-skeleton counts to 59,743,488 and 47,730,304.  The
completed `h=0` run validates the compiled, symmetry-aware approach.  The
remaining `h=1` front end has 59,743,488 signed medium skeletons and an
additional high-position/high-phase layer; its complete cost still depends
on how much of those nine positions can be reused.

Thus:

1. a complete generic search of the five `h=2` affine cubes is infeasible;
2. a compact, row-margin-sharded exact digit-3 attack is memory-feasible
   but has unproved runtime;
3. the `h=0` profile census has finished and yielded a complete 18-orbit
   theorem with an independent 666-correlation certificate;
4. the six half-turn orbits have a complete two-layer low-anti-weight
   exclusion: 7,178 digit-two points, zero row-margin matches, and zero
   digit-three points;
5. the quadratic antipodal rank-two family is exhausted on all eighteen
   frozen canonical gauges: 3,663,754,254 states give seven digit-two
   controls and zero row-margin or consecutive lifts, but the
   action-noninvariant law leaves 342 labelled images unenumerated;
6. all nine Eliahou short-block cases are exactly excluded after
   3,710,853,316,608 join rows and 88,927,740 physical replays; twenty long
   cases remain open;
7. neither the remaining `h=1` classification nor the eighteen unrestricted
   physical phase lifts presently supports a four-week forecast of `H(668)`;
8. the completed `h=0` classification is a credible theorem-level result,
   while an exact digit-3 obstruction for a whole profile would materially
   strengthen it.

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

### 2.7 Completed structured action closure

The earlier `structured_phase_families/` certificate was exact on the five
canonical orbit representatives, not on every labelled image: its feature
laws depend on the selected class coordinates.  The separate action-closure
certificate now covers all `24+12+12+12+24=84` distinct images for the
three nontrivial opposite families and the `F_27` minimal-submodule family.

The exact attained first-digit counts are:

| family | attained first-digit placements | digit-two survivors |
|---|---:|---:|
| opposite planar | 72,900 | 0 |
| opposite twisted | 3,542,940 | 0 |
| opposite helical | 2,278,854 | 5 |
| `F_27` minimal submodules | 5,325 | 0 |
| **total** | **5,900,019** | **5** |

The five helical points remain five distinct classes under exact common
`C6`-rotation replay.  Every point is fixed by minimal proper multiplier
supergroup ID8; their digit-three defects are `5,6,7,8,12`, and zero
survive digit three.  Hence this complete finite census does not satisfy the
progress gate.  It also shows why representative-only testing was
insufficient for coordinate-dependent families.

The independent `five_orbit_family_audit/` anti-tensor result remains an
exact audit of the five canonical representatives; it was already scoped
that way and has not been action-closed.

## 3. The dense `h=1` and `h=0` profile shells

The remaining dense shells are

```text
h=1: (n_9,n_3,n_0)=(1,15,8),
h=0: (n_9,n_3,n_0)=(0,18,6).
```

The five `h=2` objects do not cover them.  The `h=0` profile classification
is now complete, but its eighteen physical phase lifts remain open.  The
`h=1` profile classification and lifts both remain open.

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
physical phase cube is always `3^54`.  Rank 18 at the first digit is
certified for the five `h=2` profiles and all eighteen classified `h=0`
profiles; it must not be assumed for a future `h=1` profile.  The universal
1,756-word row-margin catalog and trivial-character transfer have now been
applied exactly to every `h=0` orbit, leaving 45--96 compatible rows per
profile before the nonlinear placement digits.

No honest complete phase-lift cost can be assigned to `h=1` until its
classification gives the number and first-digit ranks of its exact orbits.
For `h=0`, the orbit count and first-layer ranks are now known, but the
decisive unrestricted quadratic/cubic completion cost remains unbounded.
One delimited rank-two family is fully costed below.

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

The same finite calculation has now been extended across all six
half-turn-fixed `h=0` profiles.  In aggregate, 244 signed anti-words give
242 consistent slices and 7,178 exact digit-two points.  None meets an
exact row margin and none survives the complete next digit; the best has
digit-three defect six.  This closes the two lowest anti-code shells on
every half-turn orbit.  It does not enumerate the remaining anti spaces or
the twelve generic profiles.

The independent Witt-conic lane first gave a second exact denominator.  The
complete quadratic antipodal rank-two closure on orbit 07 has 40 polynomial
coefficients, first-layer solution dimension 22, evaluation-kernel dimension
eight, and therefore exactly

```text
3^(22-8) = 3^14 = 4,782,969
```

distinct physical placements.  Exhaustive replay leaves zero full
digit-two points, zero row-margin-compatible points, and zero
two-consecutive-digit points; five placements reach 17 of 18 digit-two
equations.  This is the entire stated family, but only a `3^-22` fraction
of the ambient `F_3^36` first layer.  It demonstrates how a theorem can make
a rank-two family finite without making unrestricted lifting feasible.

The same family has now been exhausted on all eighteen **frozen canonical
representative gauges**.  Their physical quotient denominators sum to

```text
3,663,754,254 states.
```

Seven ordinary digit-two controls survive, with following-digit defects
`10,10,11,13,13,14,14`.  None survives full digit three or two consecutive
digits, and none meets the exact row-margin catalog.

This is not an all-orbit result.  The feature law is not invariant under the
24-element profile action.  Across all 360 distinct labelled images the
physical dimensions are

```text
dimension 14:  12 images
dimension 15:   8 images
dimension 16:  56 images
dimension 17:  96 images
dimension 18: 188 images.
```

Only eighteen canonical gauges were enumerated.  Independent enumeration of
all action images would have workload sum

```text
all 360 images       87,815,310,840 states
completed 18          3,663,754,254 states
remaining 342        84,151,556,586 states.
```

At the observed rate, the remaining raw sweep projects to roughly 89
single-core wall hours before verification overhead or contention.  These
are workload sums, not disjoint placement counts.  The noninvariance makes
the canonical census a finite-family theorem and makes another
undifferentiated action-image sweep a poor construction priority.

### 3.7 Complete `h=0` census and all-canonical-representative lift audit

The first heavy production prefix also found the distinct exact profile

```text
A IDs = 1,2,6,1,5,1,4,5,1,5,7,4
B IDs = 2,4,2,4,4,6,5,5,8,1,5,8
target  = (-3,0,0,3).
```

Its stabilizer is trivial, its orbit has size 24, and all 37 integer
profile correlations replay exactly. Its first placement layer has
rank/nullity `18/36`; the next layer is eighteen quadrically independent
dense forms. A bounded search reaches defect one, but exact enumeration of
the complete 137,724,625-point ternary Hamming ball through radius six finds
no digit-two point. This gives local geometry, not a global obstruction or
a useful completion-rate estimate.

Exact character compression now calibrates the global system. Six
structured triple-sums of the quadrics have zero fiber

```text
3^30 - 7*3^13 = 205,891,120,934,388,
```

and the first four have an explicit quadratic parametrization by
`F_3^32`. After adjoining four original quadrics, the exact ten-equation
zero fiber is 2,541,863,158,002, within roughly one part per million of
the random-map expectation `3^26`. Thus the new structure is a useful
coordinate reduction, but the global population has not contracted
anomalously through ten constraints. Continuing the random-rate calibration
through the remaining eight equations predicts about `3^18` full
digit-two points, reinforcing that digit two alone is not a progress gate.

The classifier was upgraded from stop-on-first discovery to exhaustive
exact-orbit retention.  Every exact hit was canonicalized, target-labelled,
deduplicated, and replayed on all 37 lags.  Atomic shards and a hash-pinned
manifest made the computation resumable; the stopped v1 discovery output
was not migrated into v2.

The current v2 enumeration path processes the first connected positive-work
prefix, containing 19,131,876 primitive phase leaves, with a five-run median
of 0.744369 seconds after the redundant diagnostic fallback was removed.
Applying that one measured rate to the rigorous primitive-leaf upper bounds
gives:

```text
h=0:     19.27 single-core hours
h=1:     32.45 single-core hours
combined 51.72 single-core hours.
```

That projection was subsequently replaced by the completed run.  The
strict aggregate covers:

```text
729 / 729 shards
47,730,304 raw decorations
1,999,128 canonical decorations
25,368,365,895,696 weighted primitive leaves
19,986 characteristic-two/modulo-nine hits
64 post-modulo-nine lambda hits
18 canonical exact-zero profile orbits
360 weighted exact-zero objects.
```

A detached dependency-free verifier checks 666 exact integer-Eisenstein
correlations, the faithful 24-element action, canonicality, stabilizers,
and all 153 pairwise-disjointness comparisons.  The orbit-size distribution
is twelve at 24 and six at 12.

The exact all-eighteen canonical-representative follow-up finds first-layer
rank/nullity `18/36` and quadratic-span rank 18 for every profile.  It audits 6,552 structured
characters and 6,552 hyperplanes; the maximum retraction dimensions split
nine profiles at five and nine at four, with none at six.  Exact transfer
through all 1,756 row-sum words leaves 45--96 compatible words per profile.
These numbers replace the earlier statement that the number and first-digit
ranks of the dense profiles were unknown.  They still do not price the
complete nonlinear physical lifts.

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

The exact physical-margin plus characteristic-37 `T1/T2` convolution now
prices the next additive prefix without extrapolation.  Across all 405
targets it reduces

```text
1,538,710,506,610,661,125,476
```

physical-margin assignments to

```text
1,123,966,766,238,638,605.
```

Every target survives; the reduction factor `1369.0000032296` is essentially
the random `37^2` expectation.  Even an unrealistic rate of one billion
complete assignments per second would require about 35.6 years.  The
simultaneous primitive-unit theorem changes the search coordinates to the
ratio torus `R R*=-1`, but it does not change this candidate count.  A
complete remaining search is therefore still unpriced until a nontrivial
multiplicative inverse-CRT sieve is proved.

The completed 84-image structured closure should not be rerun or enlarged
by cosmetic variants of the same coordinate laws.  It already costs only
555.84 summed single-process image seconds and approximately 36.4 MB peak
resident memory, so additional hardware would add no mathematical
information.  Its five ID8-fixed digit-two points all fail the next digit.
Any new bounded family should supply a genuinely different invariant and
the same exact action-image denominator.

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

That microbenchmark alone does **not** estimate full classification time.
The later connected audit measures complete support and signed-skeleton
streaming, order-24 canonicalization, lower gates, witness handling, and
detached replay on one positive-work prefix.  Its 51.72-single-core-hour
combined projection was the operational planning number.  The completed
729-shard `h=0` run now replaces the `h=0` part of that estimate with a
runtime certificate and 18 exact profile orbits.  The `h=1` projection
remains distribution-sensitive, and neither calculation prices the
subsequent physical phase lifts.

**RAM.**  Streaming one support orbit at a time should stay well below
16 GB.  Storing one byte for all 450,419,940 support-character pairs costs
about 450 MB; eight bytes costs 3.60 GB; a 32-byte decomposition costs
14.4 GB before indexing.  Full decompositions should therefore be streamed
or cached by orbit/type, not retained globally.

**Disk.**  Never write the 78--427 billion character results.  Even one
byte per result is 78--427 GB.  Store only aggregate counts, positive
fibers, canonical witnesses, and resumable shard checkpoints.  A few GB is
enough for the intended streaming design.

### 4.3 Independent construction-family budgets

The short-block Eliahou boundary now has an exact finite work count.  Each
of the nine canonical cases 21--29 has 262,144 parity quotients and normally
requires

```text
412,316,860,416 principal join rows.
```

Cases 24 and 27 use an exact fallback gauge for 786,432 additional rows
each.  The total nine-case work is therefore

```text
3,710,853,316,608 principal join rows.
```

The complete run is now finished.  Across all nine cases, 88,927,740 joint
modulo-six supports were replayed as physical integer polynomials and
bit-packed correlations, with zero exact support.  The eight cases beyond
the original case-26 run used 145,055.25557 summed kernel seconds.  Unlike
the `3^36` lift projections, this is an exhaustive, bounded calculation with
a detached strict aggregate.  It closes all nine short-block cases only;
the twenty long-block cases remain outside this engine.

The long-case endpoint-orientation layer now has a sharp local cost but no
global enumeration.  Case 1 has exactly

```text
25,953,942,447,362,002
```

weight-39 supports at the anti-fold characteristic-two layer before root
profile conditioning.  For a supplied support, the new positive-fold lift
typically reduces `2^39` endpoint choices to `2^17`, then imposes 21 exact
quadratics.  A deterministic 200-support control processed 26,607,616
mod-16 orientation points in about 94 seconds and left 22 mod-32 points,
one with the exact roots and none modulo 64.  These are bounded observations,
not a whole-space survival rate.

A literal support-first pass at the measured 0.47 seconds per support would
take roughly 390 million single-core years.  Even one million complete
supports per second would take about 823 years for this first layer.  The
exact fold-plus-causal ternary model still uses all 5,928 quadratic products,
so neither additional local hardware nor a syntax-only solver rewrite makes
this a production search.  The required advance is a global support
obstruction or a coupled parametrization that avoids enumerating supports.

The near-Williamson length-167 route has a much worse exact front end.  Its
one-defect identity removes one block, but the 33 unique gauge-fixed `A,B`
shards contain exactly

```text
5,389,321,893,816,717,644,217,498,408,040,941,405,747,563,982,000
```

states, about `10^48.73`, before completing the remaining blocks.  More
cores do not make this a search program.  It requires a new parametrization,
spectral classification, or other theorem that removes dozens of effective
binary dimensions.

### 4.4 Would more hardware change feasibility?

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

### Resolved priority: publish/pivot

The four-family 84-image action closure, the all-eighteen canonical-gauge
rank-two census, and the all-nine short-block Eliahou census have completed.
None passes the gate.  The rank-two family supplies seven more digit-two
controls but zero row-compatible consecutive lift, and its action
noninvariance leaves a large mechanically enumerable scope rather than a new
contraction.

Preserve the five-orbit and eighteen-orbit classifications with these finite
lift obstructions as a scoped paper project.  Stop headline `H(668)` search
on the present lifts.  Any future restart must begin with a genuinely new
construction principle or quotient, not another digit-two witness, cosmetic
structured family, or undifferentiated sweep of the remaining 342 images.

### Optional paper-scoped continuation, not headline `H(668)` work

1. Preserve the completed 18-orbit `h=0` certificate as the fixed profile
   input.
2. For `h=1`, measure batching across the nine high positions before
   authorizing its complete census.
3. Canonicalize complete decorated `h=1` objects under the order-24 group
   and exact-replay every positive profile.
4. Do not resume `h=0` lifting unless a genuinely new construction principle
   first yields an algebraically bounded family or proof decomposition with
   an explicit coverage denominator.
5. Require exact row margins and two consecutive higher digits in the same
   physical point; another isolated digit-two point is not a milestone.

### Stop/go interpretation

- **Go:** an algebraic digit-3 reduction, a certified digit-3 point, or a
  new lift family with a rigorous coverage denominator and a surviving
  row-compatible consecutive lift.  The dense `h=0` profile classifier has
  already passed and completed; its output is now an 18-orbit theorem, not
  a reason to extrapolate physical-lift feasibility.
- **Publish/pivot:** this condition is met by the completed 18-orbit `h=0`
  classification with its finite lift obstructions and the empty all-nine
  short-block Eliahou census.
- **Stop headline search:** only more digit-2 witnesses, repeated
  `UNKNOWN` runs without increasing certified coverage, or proposed
  families whose complete denominators remain astronomically uncosted.

## 6. Scope warning

This report estimates the **order-three invariant LP(333) construction
program** and compares two independent construction families.  Eliminating
the five `h=2` lifts does not eliminate `h=1` or the eighteen `h=0` lifts.
Eliminating all of these profile shells would close this order-three profile
route, not prove that no unrestricted Legendre pair of length 333 exists
and not prove that no Hadamard matrix of order 668 exists by some other
construction.  Likewise, exhausting the nine Eliahou short-block cases
leaves twenty long-block boundary cases open.

The mechanically verified five-orbit shell-two classification and
eighteen-orbit dense-shell classification remain valuable regardless of
the phase-lift outcome.

## 7. Arithmetic replay

From `hadamard_668_search`, the first two commands are dependency-free; the
environment-pinned commands then audit the final certificates:

```text
python3 verify_complete_remaining_search_estimate.py
python3 -m unittest -v test_complete_remaining_search_estimate.py
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  eliahou_short_block_census/verify_nine_case_completion.py
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  h0_witt_conic_rank_two_full_18/verify_canonical_representative_certificate.py
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  h0_witt_conic_rank_two_full_18/verify_action_noninvariance.py
```

Together these commands recompute both local generating functions, all support and signed-skeleton
coefficients, the counts by nonempty quartet, every affine upper bound, all
three 729-character work totals, the 405 row-margin shards, the five-cube
volume, and the exactness inequality.  Its semantic hash is

```text
c4eddd59d76d36f5c1b133a972e8e451afd6ed3bdadf95e8b3ebcffe54fffa56
```
