# Consecutive higher-digit lift audit

## Status

One placement on profile `h2-422220-0` has now been independently found and
certified through lambda digit 2.  It is fixed by the base multiplier
`<10>` and by none of the five minimal proper common-multiplier supergroups.
Its exact twenty displayed Eisenstein residuals have digits

```text
digit 0:  0 nonzero rows
digit 1:  0 nonzero rows
digit 2:  0 nonzero rows
digit 3: 17 nonzero rows
```

This is a useful search seed, not a milestone toward `LP(333)`: the
second-digit heuristic predicts about `3^18` such points per profile.

No point through digit 3 or digit 4 has been found.  In particular, the
unique second-digit survivor in the exhaustively tested
`opposite_helical_c4` family fails digit 3 in five displayed rows.  That
control point is additionally fixed by the recently excluded supergroup
ID8, so it cannot be a final construction.

A later exact-replay census found two partial **stage-2.5** points: they
satisfy all eighteen active digit-2 quadrics and also the delayed
`E1(origin)` digit-3 linear equation.  They occur on profiles
`h2-222222-0` and `h2-422220-1` and leave respectively 11 and 16 of the
other displayed digit-3 rows nonzero.  Thus the tempting implication
“digit 2 forces the delayed row nonzero” is decisively false, but neither
point is a digit-3 lift.  Moreover, neither point's six phase sums occurs
in its profile's compatible exact row-margin corpus.  They are therefore
algebraic probes of the placement-digit variety, not viable partial
`LP(333)` lifts.  On the first point the delayed row alone actually
survives through digit 4 and first fails at digit 5; the other rows still
fail digit 3, so this row-specific fact is not a consecutive global lift.

## 1. Integral form of every later digit

Put `lambda=1-omega`; then

```text
lambda^2 = -3 omega.
```

Write one displayed residual as

```text
F = a+b omega.
```

Vanishing of its first `k` lambda digits means exactly
`lambda^k | F`.  Since powers of `lambda^2` differ from powers of `3` by a
unit, the conditions are

```text
digits 0..(2m-1) vanish
    iff a == b == 0 mod 3^m,

digits 0..(2m) vanish
    iff a == b == 0 mod 3^m
        and a+b == 0 mod 3^(m+1).
```

Consequently the two consecutive digits requested by the sprint have the
particularly simple exact form

```text
through digit 3:  a == b == 0 mod 9,
through digit 4:  a == b == 0 mod 9 and a+b == 0 mod 27.
```

There is no hidden high-degree approximation in these tests.  The SAT,
CP-SAT, and tabu instruments all impose these exact integral congruences,
and every candidate is replayed by repeated exact division by `lambda`.

## 2. Nine digits are already exact

The `E0` origin residual is structurally zero: it consists of 167 positive
unit diagonal terms minus 167.  Across all five profiles, every other
displayed residual is a signed sum of at most 135 unit roots.  Hence

```text
|F| <= 135,
N(F)=a^2-ab+b^2 <= 135^2 = 18,225 < 3^9 = 19,683.
```

If a nonzero `F` were divisible by `lambda^9`, its norm would be a positive
multiple of `3^9`, a contradiction.  Therefore digits `0,...,8` all zero
already imply `F=0`; digit 9 is unnecessary.

The verifier separately exhausts every nonzero Eisenstein integer of norm
at most `135^2`.  The maximum valuation is exactly 8 (six associates attain
it), mechanically confirming the cutoff.

## 3. Certified second-digit witness

The compact certificate is `full_second_digit_witness.json`.  Its placement
hash is

```text
1ee7e540ecfac7433e9f99f8291639b769740336e798d15f546399603d82f909.
```

It was found by incremental ternary tabu repair on the eighteen active
quadratic forms after 2,952,653 updates.  Search provenance is not used in
verification.  The verifier independently checks:

- the profile identifiers and 36-to-54 affine lift;
- all twenty symbolic first and second digits;
- all twenty exact Eisenstein coefficients and digits through 9;
- hashes of the affine and placement points;
- invariance under multiplier 10;
- noninvariance under generators `64,112,46,7,16`;
- the 135-term modulus bound and exact nine-digit cutoff.

The verification has passed with both system Python and the repository's
Python 3.9 environment, with semantic hash

```text
c0448791a4012ede6575fbb0af76efa0ff83463f1566ff27be028d3ae66b3415.
```

## 4. Bounded digit-3 search

Five independent 300-second low-memory tabu runs imposed the exact digit-2
and digit-3 residuals simultaneously.  The completed checkpoints were:

| profile | updates | restarts | best nonzero digits 2+3 | status |
|---|---:|---:|---:|---|
| `h2-222222-0` | 210,120 | 3 | 9 | UNKNOWN |
| `h2-422220-0` (excluded structured seed) | 202,936 | 3 | 5 | UNKNOWN |
| `h2-422220-1` | 206,616 | 3 | 8 | UNKNOWN |
| `h2-422220-2` | 213,436 | 3 | 8 | UNKNOWN |
| `h2-422220-3` | 199,111 | 2 | 9 | UNKNOWN |

`UNKNOWN` is literal: none of these runs is an exclusion theorem.
The stored points are independently replayable candidate checkpoints, but
the files do not contain the full stochastic trajectories or enough
provenance to reproduce the searches themselves.

A separate fast census optimized only the eighteen digit-2 quadrics for
300 seconds on each profile.  It exactly replayed nine distinct digit-2
points: five on `h2-222222-0` and four on `h2-422220-1`.  One point on each
profile also zeroed the delayed nineteenth linear row.  Their full digit-3
residual counts were 11 and 16.  These two witnesses are independently
replayed by `verify_stage_2_5_witnesses.py`; the census totals remain
bounded search observations rather than counts of the solution varieties.
An exact trivial-character audit found that all nine census points miss
their compatible row-margin corpora.  In particular, phase-only localized
searches from either saved point are diagnostic unless the row-margin join
is added to their objective.  The five raw bounded census records and all
nine hit coordinates are retained under `digit2_row7_census/`; the
dependency-free `verify_digit2_row7_census.py` exactly replays every hit and
all nine failed joins.  It does not reproduce the stochastic trajectories.

The full Hamming ball of radius 5 around the better candidate-0 stage-2.5
point contains `13,065,937` affine points.  Exhaustive quadratic evaluation
finds only two digit-2 points there: the center and one point at exact
radius 5.  The neighbor has 13 nonzero digit-3 rows, fails the delayed row
at digit 3, and also misses the row-margin corpus.  Thus the center is
isolated from the digit-2 variety through radius 4 and has no improving
digit-2 neighbor through radius 5.  This is a certified local statement,
not a global exclusion.

A 600-second hyperplane-preserving tabu run from that center, weighting
each broken digit-2 row by 30, completed 287,990 updates and retained the
center's objective 11 as its best point.  Its status is `UNKNOWN`.  Because
the center misses the row-margin corpus, this was a local phase-variety
diagnostic rather than a viable-lift search.

An exact row-margin-aware sparse CP-SAT model was then added.  On candidate
0, the union of all 72 compatible six-sum targets remained `UNKNOWN` after
300 seconds, 1,694,753 branches, and 49,821 conflicts.  Eight evenly spaced
fixed-target shards (`0,9,...,63`) each remained `UNKNOWN` after 30 seconds.
These runs show substantial solver hardness already at digit 2; they do not
exclude any target or prove that a row-margin-compatible digit-2 point
exists.

As a structurally different control, a pair-permutation tabu instrument
keeps one exact six-sum target invariant at every move and repairs the
first and second digits lexicographically.  A 60-second target-0 run made
26,173 moves and reached `(2,9)` nonzero first-/second-digit rows, with
status `UNKNOWN`.  The instrument is a potentially useful resumable lane,
but this bounded run did not even enter the first-digit affine space and is
not evidence of convergence to digit 2.

Generic CNF and CP-SAT were also tested as bounded instruments.  Even the
abundant second digit remained hard for those encodings:

```text
quadratic PySAT/CaDiCaL:       UNKNOWN after about nine minutes
direct prefix-2 Glucose:      UNKNOWN at 60 seconds
direct prefix-2 CP-SAT:       UNKNOWN at 120 seconds,
                              191,572 branches, 6,473 conflicts
direct prefix-3 CP-SAT:       UNKNOWN at 300 seconds,
                              3,549,810 branches, 475,442 conflicts
```

The stochastic exact-quadratic repair was decisively better for producing a
second-digit point.  At digit 3, however, the system has reached the
expected square-plus-one regime and no comparable convergence has appeared.

The next carry actually has nineteen genuine equations, not eighteen:
`E1` at the origin is structurally zero at digit 2 but becomes nontrivial
at digit 3.  An independent algebraic audit finds combined digit-2/digit-3
linearized rank 36 at the known second-digit point and an inconsistent
linearized correction.  This strengthens the interpretation of digit 3 as
the first genuinely overdetermined transition.

Two Newton displacement sheets from a 19/20 second-digit seed were also
tested.  The full linearized correction sheet had dimension 18; a relaxed
eleven-row correction sheet had dimension 25.  Exact restricted-quadratic
SAT returned UNKNOWN after about 2.5 minutes and 90 seconds respectively.
These were tangent-correction models, not random affine slices.

Random codimension-12 coordinate slices were then tested separately.
Three CDCL slices each reached 100,000 conflicts in 28.67, 29.69, and
33.62 seconds without a digit-2 point.  Five further slices received
500,000 restricted-variable tabu updates apiece, again without a digit-2
point.  Under the neutral count each slice should contain about `3^6`
digit-2 points, so this is evidence of solver hardness, not emptiness.

A direct digit-4 tabu objective was also run for 300 seconds from the best
structured digit-2 control.  It completed 209,203 updates and three
restarts, with best combined digit-2/3/4 objective 17 and status UNKNOWN.
Thus both consecutive higher digits were explicitly attempted, but neither
was reached.

The sparse-solver JSON files in the sibling digit-3 carry package are
historical benchmark records only.  Subsequent strengthening of the
explicit-row and exact-row-7 models means the current scripts need not
regenerate their recorded model sizes exactly; this does not change any
replayed witness or residual result here.

## 5. Complete-search estimate

This section estimates only the five `h=2` profiles in this placement
chart.  The separate
[`COMPLETE_REMAINING_SEARCH_ESTIMATE.md`](../../COMPLETE_REMAINING_SEARCH_ESTIMATE.md)
audits the remaining `h=1` and `h=0` profile classes and is the relevant
whole-program estimate.

The first placement digit leaves `3^36` points on each profile.  There are
eighteen active second-digit quadrics and nineteen genuine digit-3 carry
equations.  Extrapolating nineteen independent conditions per later digit
gives the following neutral model:

| last zero digit | expected points per profile |
|---:|---:|
| 1 | `3^36` |
| 2 | `3^18 = 387,420,489` |
| 3 | `3^-1 = 1/3` |
| 4 | `3^-20` |
| 5 | `3^-39` |
| 6 | `3^-58` |
| 7 | `3^-77` |
| 8 (exact) | `3^-96` |

This is a heuristic, not an independence theorem.  It explains why a
second-digit witness is abundant, why digit 3 is the real transition, and
why two consecutive further digits would be genuinely significant.

A blind complete enumeration is

```text
5 * 3^36 = 750,473,176,484,995,605 placements.
```

Even at one billion exact placements per second this is about 23.8 years.
A viable full lift therefore requires either:

1. an exact algebraic count or elimination of the digit-3 square system,
2. a structure that forces several subsequent digits together, or
3. a new construction family outside this placement chart.

The independence model assigns only about `5*3^-96` expected exact points
to the five profiles.  This is strong negative planning evidence, but not a
nonexistence result because the later digits may possess exceptional
dependencies.

## Reproduction

Dependency-free witness and checkpoint replay:

```bash
python3 phase_second_digit/higher_digits/verify_full_second_digit_witness.py
python3 phase_second_digit/higher_digits/verify_stage_2_5_witnesses.py
python3 phase_second_digit/higher_digits/verify_digit2_row7_census.py
python3 phase_second_digit/higher_digits/verify_bounded_search_checkpoints.py
```

The second command replays the saved best points; it does not reconstruct
the omitted stochastic search trajectories.

The tabu instrument additionally requires NumPy:

```bash
python3 phase_second_digit/higher_digits/search_lambda_prefix_tabu.py \
  --candidate 1 --maximum-digit 3 --seconds 300
python3 phase_second_digit/higher_digits/verify_stage_2_5_radius5.py
```

The CP-SAT instrument uses the repository's pinned OR-Tools environment.
`solve_lambda_prefix_sat.py` and `solve_full_second_digit_sat.py` use the
optional local Python-SAT research environment; they are not required for
certificate verification.
