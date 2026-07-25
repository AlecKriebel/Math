# Lift triage for new exact `h=0` profile orbits

This folder turns the continuing exhaustive `h=0` profile census into an
exact, record-driven lift audit.  It contains genuine second-digit placement
witnesses and a new quadratic-retraction theorem, but **not** a Legendre pair
of length 333 or a Hadamard matrix of order 668.

## Main result

The first three new production orbits all have first-lift rank 18 and
nullity 36.  Their eighteen active second-digit equations are independent
dense quadrics.  A retracted Newton method found and directly replayed an
exact second-digit placement for every one:

| orbit | second-digit witness | following digit defect | exact row-margin word |
|---|---:|---:|---:|
| `c90c2887b652140a` | yes | **6** | no |
| `6e45edfb0bfb0974` | yes | 13 | no |
| `533a4ccf9d6a91d8` | yes | 11 | no |
| `e6860f056b3ae483` (provisional) | yes | 10 | no |

Here “following digit defect” is the number of nonzero displayed
`lambda^3` rows among the exact 20-row replay.  Zero would be the next
consecutive lift.  The selected `c90c` point satisfies every row through
`lambda^2`, but its digit-3 carry residual on displayed rows 1 through 19
is

```text
(1,2,0,1,1,0,0,0,0,2,0,0,0,0,1,0,0,0,0).
```

The direct base-`lambda` digit is the negative (the unit multiple two) of
this vector over `F_3`, so the support and defect are identical.

## Radical-translation retraction

For the active quadrics

```text
(q_0,...,q_17) = (Q_1,...,Q_6,Q_8,...,Q_19),
```

put

```text
g_i = q_i + q_(i+6) + q_(i+12),       0 <= i < 6.
```

For any selected forms

```text
f_i(x) = c_i + l_i x + 2 x^T B_i x,
```

let

```text
R = intersection_i ker(B_i).
```

There is a translation matrix `V` giving an exact quadratic retraction

```text
Phi(x) = x - V (f_1(x),...,f_k(x))^T
```

if and only if the restriction of the linear terms to `R` has rank `k`.
Equivalently,

```text
B_i V = 0       for every i,
L V   = I_k.
```

Then `f_i(Phi(x))=0` identically.  This criterion is exact, not a
linearization.

All 364 five-dimensional hyperplanes in the six-dimensional span of the
`g_i` were exhausted:

| orbit | retractable 5-space | common radical | full-six radical / linear rank |
|---|---|---:|---:|
| `c90c...` | unique: omit `g_2` | 5 | `2 / 2` |
| `6e45...` | none | — | `1 / 1` |
| `533a...` | unique: omit `g_1` | 5 | `2 / 2` |

Thus five is the exact maximum for `c90c` and `533a` in the entire
structured span; six is impossible.  The exact maximum for `6e45` is four.
This is stronger than checking the six coordinate omissions or trying a
favorable equation order.

## Exact character calibration

The same six forms have the following projective character data:

| orbit | exceptional lines among 364 | exact `g^(-1)(0)` |
|---|---:|---:|
| `c90c...` | 2 | 205,891,132,094,649 |
| `6e45...` | 11 | 205,891,128,906,003 |
| `533a...` | 4 | 205,891,138,471,941 |

Exact zero populations after adjoining four original quadrics remain close
to the random-map expectation:

| orbit | 6 equations | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|
| `c90c...` | 205891132094649 | 68630383742175 | 22876798418910 | 7625599217091 | 2541867639165 |
| `6e45...` | 205891128906003 | 68630375593413 | 22876785487179 | 7625594493171 | 2541866182623 |
| `533a...` | 205891138471941 | 68630382856440 | 22876797296979 | 7625598036111 | 2541864568617 |

These counts support abundance at digit 2.  They do not estimate the
row-margin-compatible digit-3 population.

## Exact physical row-margin interaction

The pinned 1,756-word catalog gives:

| orbit | compatible rows | raw compatible assignments |
|---|---:|---:|
| `c90c...` | 93 | 355,022,758,986,962,757,600 |
| `6e45...` | 77 | 285,625,803,284,684,292,024 |
| `533a...` | 72 | 270,619,555,920,772,805,460 |

Every pinned digit-2 witness misses the catalog.

The five-form retraction cannot silently preserve a fixed catalog target.
After composing the six physical phase sums with the 36 affine
coordinates, their 54 nonzero Fourier characters span all 36 dual
coordinates for both five-form orbits.  Hence the global translation
invariance space has dimension zero.  Each canonical correction direction
changes many characters (`34,38,32,38,37` for `c90c` and
`42,31,40,24,33` for `533a`).

A fixed row-margin target can still be incorporated, but only as a
separate nonlinear allowed-table gate (or as a post-filter) on
`Phi(x)`.  The retraction itself supplies no target-preserving direction.

## Bounded digit-3 manifold search

`search_c90c_digit3_manifold.py` starts from the defect-6 exact point,
takes moves in the kernel of the 18-row digit-2 Jacobian, biases those moves
with the 19-row digit-3 carry Jacobian, applies the five-form retraction, and
uses Newton restoration.  Only points restored to all eighteen quadrics are
scored.

The pinned run used 480.22 CPU seconds:

```text
tangent proposals             5,000
restoration attempts            726
successful restorations          12
distinct exact digit-2 points    13
best digit-3 defect               6
status                      UNKNOWN
```

This is neither an exclusion nor evidence that defect six is locally
minimal.  It is a mechanically replayable negative bounded experiment.

## Complete 18-orbit census scan

`scan_production_orbit_retractions.py` consumes completed production-v2
result JSON files, a result directory, or the strict production aggregate.
It deduplicates exact orbits by digest and derives, for every record:

- first-lift rank and nullity;
- all eighteen polar ranks and their coefficient-span rank;
- the complete 364-character structured audit and exact six-zero fiber;
- all 364 five-hyperplane retraction tests plus the full-six obstruction;
- the exact 1,756-row transfer intersection.

`FINAL_PRODUCTION_SCAN_18.json` freezes this audit for all 18 representatives
in the complete dense-shell classification.  The strict aggregate was read
once to create it.  Its aggregate SHA-256,
`3bccde87f456bfcd2f0c3da6ac8cf9cb3635538e831a95951003068ae87cae86`,
is pinned in every record.  Subsequent verification reconstructs the
representatives from the detached complete-classification certificate and
does not read ignored production output.

Across all 18 profiles:

- every first layer has rank 18 and nullity 36;
- every 18-quadric coefficient span has rank 18, while individual polar
  ranks range from 33 through 36;
- all \(18\cdot364=6,552\) structured characters and all 6,552
  five-hyperplanes were audited;
- nine profiles have exact maximum retraction dimension five and nine have
  exact maximum four; none retract all six structured forms;
- the nine five-retractable profiles have 11 successful hyperplanes in
  total, with at most two for any profile; and
- every profile was intersected with all 1,756 exact row-margin words.

Standout extrema are:

| invariant | minimum | maximum |
|---|---:|---:|
| exceptional structured lines | `orbit-13` / `e686...`: **0** | `orbit-01` / `8106...`: **18** |
| exact structured six-zero fiber | `orbit-07` / `86b1...`: 205,890,943,964,535 | `orbit-18` / `ac34...`: 205,891,433,421,696 |
| compatible catalog rows | `orbit-02` / `64ef...`: **45** | five profiles: **96** |
| accepted raw margin assignments | `orbit-02` / `64ef...`: 177,092,671,681,697,667,840 | `orbit-15` / `fdb6...`: **426,020,132,747,992,022,592** |

The earlier `CURRENT_PRODUCTION_SCAN_12.json` remains as a historical
mid-census snapshot.  Three priority boundaries from the complete scan are
important:

- `c90c...` has the best witnessed lift behavior (five-form retraction and
  observed digit-3 defect six);
- `e6860f056b3ae483` has zero exceptional structured character lines and a
  unique five-form retraction. A separately capped provisional run found
  nine digit-2 witnesses, but its best digit-3 defect was ten;
- `fdb6a5c865468e1f` has the largest physical transfer mass
  (426,020,132,747,992,022,592 assignments) but only a four-form retraction.

The production-level records without a detached all-correlation profile
certificate are explicitly provisional.

### Provisional `e686...` follow-up

The focused run consumed 280.65 CPU seconds inside a 300-second wall cap.
It found nine exact digit-2 witnesses with digit-3 defect histogram

```text
10:1, 11:2, 12:1, 13:1, 14:1, 15:1, 16:1, 17:1.
```

None of the nine witnesses met the exact row-margin catalog.  The best
point has defect ten, four rows worse than the certified `c90c` defect-six
point.  Thus the exceptionally clean six-character map did not translate
into better observed following-digit behavior in this bounded sample.
The result is frozen in `E686_PROVISIONAL_DIGIT2_CHECKPOINT.json`; its
profile status remains census-provisional.

## Verification

Run:

```text
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_new_orbits_lift_triage.py
```

The verifier independently re-derives the affine lifts and quadrics,
exhausts all 364 characters and 364 hyperplanes for every one of the 18
classified profiles, replays every 1,756-row transfer, recomputes the exact
character-prefix counts for the three detached witness profiles, checks the
fixed-margin Fourier obstruction, and validates both historical
bounded-search checkpoint hashes.  The final reference run took 154.07
seconds and peaked at 47.1 MB RSS.  It requires no ignored production
output.
