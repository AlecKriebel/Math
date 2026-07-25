# All-orbit quadratic rank-two conic dimension gate

> **Scope correction, 2026-07-25.**  The historical term “all-orbit” in
> this v1 folder means all 18 **frozen canonical representative gauges**,
> not every image under the 24-element classification action.  The
> feature law is not action-invariant: six classes have gauge-dependent
> physical dimensions.  Thus the five exhaustive results below cover
> five canonical gauges only; 342 noncanonical action images were not
> tested.  The v1 verifier and certificate remain byte-for-byte frozen.
> See `SCOPE_CORRECTION.json` and the superseding
> `../h0_witt_conic_rank_two_full_18/` certificate and action audit.

## Scope

For each of the 18 frozen canonical representative gauges in the exact
dense-shell `h=0` classification, this folder analyzes the quadratic
antipodal center family

```text
t_X(j,s) = P_X(x,s,p_X,j(s)) + h_j Q_X(x,s,p_X,j(s)),
u_X(j,s) = -p_X,j(s)t_X(j,s),
```

where `x=j mod 3`, `h_j=+1` for `j<6` and `-1` otherwise, and all four
polynomials `P_A,P_B,Q_A,Q_B` are arbitrary total-degree-at-most-two
polynomials over `F_3`.

The two correction rows `Q_A,Q_B` are arbitrary ten-coordinate vectors,
so every rank-zero, rank-one, and rank-two correction in this quadratic
antipodal feature space is included.  Degree-three and non-antipodal
center laws are outside the family.

## Exact quotient census

Every profile has 40 raw coefficients, first-layer constraint rank 18,
and hence `3^22=31,381,059,609` valid coefficient descriptions.  Exact
evaluation-kernel quotienting gives:

| profile | feature rank | kernel dim. | physical dim. | physical denominator | status |
|---|---:|---:|---:|---:|---|
| `orbit-01` | 36 | 4 | 18 | 387,420,489 | deferred |
| `orbit-02` | 35 | 5 | 17 | 129,140,163 | deferred |
| `orbit-03` | 35 | 5 | 17 | 129,140,163 | deferred |
| `orbit-04` | 35 | 5 | 17 | 129,140,163 | deferred |
| `orbit-05` | 34 | 6 | 16 | 43,046,721 | **exhaustive** |
| `orbit-06` | 36 | 4 | 18 | 387,420,489 | deferred |
| `orbit-07` | 32 | 8 | 14 | 4,782,969 | **exhaustive** |
| `orbit-08` | 35 | 5 | 17 | 129,140,163 | deferred |
| `orbit-09` | 34 | 6 | 16 | 43,046,721 | **exhaustive** |
| `orbit-10` | 35 | 5 | 17 | 129,140,163 | deferred |
| `orbit-11` | 36 | 4 | 18 | 387,420,489 | deferred |
| `orbit-12` | 36 | 4 | 18 | 387,420,489 | deferred |
| `orbit-13` | 36 | 4 | 18 | 387,420,489 | deferred |
| `orbit-14` | 34 | 6 | 16 | 43,046,721 | **exhaustive** |
| `orbit-15` | 36 | 4 | 18 | 387,420,489 | deferred |
| `orbit-16` | 35 | 5 | 17 | 129,140,163 | deferred |
| `orbit-17` | 34 | 6 | 16 | 43,046,721 | **exhaustive** |
| `orbit-18` | 36 | 4 | 18 | 387,420,489 | deferred |

Thus the dimension distribution is:

```text
dimension 14: 1 profile
dimension 16: 4 profiles
dimension 17: 6 profiles
dimension 18: 7 profiles
```

No larger image was enumerated.  This follows the frozen gate exactly:
exhaust every image of size at most `3^16`, and record a delimited fallback
for every larger image.

## Exhaustive result

The five permitted profiles contain

```text
4*3^16 + 3^14 = 176,969,853
```

distinct first-layer physical placements.  All were enumerated after
symbolically restricting the 18 second-digit quadrics to their exact
physical images.

| profile | placements | maximum score | 17/18 points | exact digit-two |
|---|---:|---:|---:|---:|
| `orbit-05` | 43,046,721 | 17/18 | 4 | 0 |
| `orbit-07` | 4,782,969 | 17/18 | 5 | 0 |
| `orbit-09` | 43,046,721 | 17/18 | 12 | 0 |
| `orbit-14` | 43,046,721 | 17/18 | 15 | 0 |
| `orbit-17` | 43,046,721 | 17/18 | 4 | 0 |
| **total** | **176,969,853** | **17/18** | **40** | **0** |

Consequently, within the exhausted profiles:

```text
exact second-digit survivors                 0
two-consecutive-digit survivors              0
margin-compatible second-digit survivors     0
```

The verifier reconstructs the exact 1,756-word margin catalog and is
written to replay the following digit and exact row margin for every
digit-two survivor.  The certified survivor set is empty, so those two
counts are rigorously zero.

## Explicit coverage denominator

Across the 18 canonical gauges, the per-gauge physical quotients contain
exactly

```text
7*3^18 + 6*3^17 + 4*3^16 + 3^14
  = 3,663,754,254 placements.
```

The exhaustive physical-state coverage is therefore

```text
176,969,853 / 3,663,754,254 = 37 / 766
                                      ~= 4.8303%.
```

Because every profile has the same `3^22` valid coefficient descriptions,
the coefficient-law-weighted profile coverage is separately `5/18`.
These fractions must not be conflated: the tested profiles were selected
by the physical-dimension gate and have smaller quotient images.

The result is complete for all five exhausted canonical-gauge families.
It makes no survivor or exclusion claim for the thirteen deferred
canonical gauges or for any of the 342 noncanonical action images.

## Deferred-family fallback and estimate

A dimension-17 image has exactly 129,140,163 states and 3,942 batches of
32,768.  Its dense restricted-quadratic work proxy is exactly

```text
3 * (17/16)^2 = 867/256 ~= 3.3867
```

times one dimension-16 sweep.

A dimension-18 image has exactly 387,420,489 states and 11,824 batches.
Its corresponding proxy is

```text
9 * (18/16)^2 = 729/64 ~= 11.3906.
```

The six dimension-17 and seven dimension-18 cases total about 100.055
dimension-16 work units.  Calibrating only as an empirical estimate
against the completed single-core run gives roughly 3.3 additional CPU
hours; wall time can be materially longer under contention.  No such run
was launched.

The rigorous fallback recorded in the certificate is to obtain an
additional exact quotient, a quadratic-character zero-fiber certificate,
or a lossless meet-in-the-middle split before enumerating any deferred
image.  Until then their status is `DEFERRED_DIMENSION_GATE`.

## Verification

Run:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 \
/Users/alec/Documents/Math/tmp/hadamard-env/bin/python \
  verify_all_orbit_rank_two.py
```

The verifier uses only tracked certificates and source files.  It
reconstructs the quotient dimensions of all 18 canonical gauges,
re-enumerates the five safe images, replays physical representatives,
rebuilds the margin catalog, and compares every result with
`all_orbit_rank_two_certificate.json`.

The detached reference replay took 578.53 wall seconds, 485.47 user
seconds, and 56,492,032 bytes maximum resident memory.  The certificate
semantic hash is:

```text
a12dbd72d6e0546f6f6eadf911116b2d83ac349ac0965bba2082263865e5b346
```

This is a delimited canonical-gauge structured-family result, not a
classification-orbit, `LP(333)`, or `H(668)` exclusion.
