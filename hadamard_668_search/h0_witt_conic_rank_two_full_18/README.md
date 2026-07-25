# Canonical-gauge quadratic rank-two census

## Result

The arbitrary-quadratic antipodal rank-at-most-two center family has been
exhausted on all 18 **frozen canonical representative gauges** in the
complete dense-shell `h=0` classification.

The exact census is:

```text
canonical representative gauges exhausted       18 / 18
physical quotient states exhausted        3,663,754,254
exact second-digit survivors                           7
two-consecutive-digit survivors                       0
margin-compatible second-digit survivors              0
```

The family is

```text
t_X(j,s) = P_X(x,s,p_X,j(s)) + h_j Q_X(x,s,p_X,j(s)),
u_X(j,s) = -p_X,j(s)t_X(j,s),
```

where `x=j mod 3`, `h_j=+1` for `j<6` and `-1` otherwise, and
`P_A,P_B,Q_A,Q_B` are arbitrary total-degree-at-most-two polynomials over
`F_3`.  This contains every rank-zero, rank-one, and rank-two opposite
correction in this 40-parameter quadratic antipodal feature space.  It
does not contain degree-three or non-antipodal laws.

Per canonical gauge:

| gauge | quotient dimension | states | maximum score | exact digit two | following-digit defects |
|---|---:|---:|---:|---:|---|
| `orbit-01` | 18 | 387,420,489 | 18/18 | 1 | 10 |
| `orbit-02` | 17 | 129,140,163 | 17/18 | 0 | — |
| `orbit-03` | 17 | 129,140,163 | 17/18 | 0 | — |
| `orbit-04` | 17 | 129,140,163 | 18/18 | 1 | 13 |
| `orbit-05` | 16 | 43,046,721 | 17/18 | 0 | — |
| `orbit-06` | 18 | 387,420,489 | 18/18 | 1 | 10 |
| `orbit-07` | 14 | 4,782,969 | 17/18 | 0 | — |
| `orbit-08` | 17 | 129,140,163 | 18/18 | 1 | 14 |
| `orbit-09` | 16 | 43,046,721 | 17/18 | 0 | — |
| `orbit-10` | 17 | 129,140,163 | 17/18 | 0 | — |
| `orbit-11` | 18 | 387,420,489 | 18/18 | 1 | 13 |
| `orbit-12` | 18 | 387,420,489 | 17/18 | 0 | — |
| `orbit-13` | 18 | 387,420,489 | 18/18 | 1 | 14 |
| `orbit-14` | 16 | 43,046,721 | 17/18 | 0 | — |
| `orbit-15` | 18 | 387,420,489 | 17/18 | 0 | — |
| `orbit-16` | 17 | 129,140,163 | 17/18 | 0 | — |
| `orbit-17` | 16 | 43,046,721 | 17/18 | 0 | — |
| `orbit-18` | 18 | 387,420,489 | 18/18 | 1 | 11 |

Every one of the seven digit-two assignments is embedded in the
certificate.  The detached verifier physically reconstructs it, confirms
all 18 active second-digit equations, evaluates the following digit, and
checks membership in the exact 1,756-word row-margin catalog.  The
following-digit defects are distributed as

```text
defect 10: 2
defect 11: 1
defect 13: 2
defect 14: 2
```

so none is close to a consecutive higher-digit lift.

## Critical action-scope correction

The structured feature law is **not invariant** under the 24-element
action used to classify the shell profiles.  A separate exact linear
audit reconstructs all `18*24=432` action incidences and the 360 distinct
profile images.  Six classification orbits have different physical
feature dimensions in different gauges:

| classification orbit | canonical dimension | dimensions across its action images |
|---|---:|---|
| `orbit-02` | 17 | 16, 17 |
| `orbit-04` | 17 | 17, 18 |
| `orbit-05` | 16 | 15, 16, 18 |
| `orbit-08` | 17 | 16, 17, 18 |
| `orbit-10` | 17 | 17, 18 |
| `orbit-17` | 16 | 16, 17, 18 |

These rank changes are decisive counterexamples to action invariance.
The remaining 12 classification orbits have constant dimension, but
constant dimension alone does not prove covariance of their feature
spaces.

Across all 360 distinct action images, the exact dimension distribution
is:

```text
dimension 14:  12 images
dimension 15:   8 images
dimension 16:  56 images
dimension 17:  96 images
dimension 18: 188 images
```

Therefore the completed expensive census covers exactly 18 canonical
gauges, not the other 342 action images.  It is not a shell-orbit,
`LP(333)`, or `H(668)` exclusion.

## Complete remaining workload

If every gauge-dependent image were enumerated independently, the exact
sum of its physical quotient denominators would be

```text
all 360 action images        87,815,310,840 states
completed canonical 18        3,663,754,254 states
remaining 342 images         84,151,556,586 states
```

These numbers are an enumeration-workload sum, not a claim that the
ambient placement sets are disjoint.  At the observed continuation
throughput, the remaining raw sweep projects to about 89 single-core wall
hours before verification overhead or machine contention.  That
projection is empirical, not a mathematical lower bound.  The size and
the gauge defect make another undifferentiated sweep a poor next research
move; a covariant construction law or a new quotient is preferable.

## Certificates and verification

`canonical_18_rank_two_certificate.json` is detached from the ignored
production output.  It embeds all 18 records, all score histograms, the
seven full assignments, and the semantic hashes of the 13 atomic
continuation results.  It also pins the complete loaded project-local
replay dependency bundle, including the rank-one, second-digit, Hensel,
trit-lift, row-margin, classification, action, and final-scan sources.

`ACTION_NONINVARIANCE_CERTIFICATE.json` records every action image,
dimension, quotient hash, stabilizer, and explicit rank-change witness.

From this folder, run with a NumPy-capable Python:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python3 verify_canonical_representative_certificate.py

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
python3 verify_action_noninvariance.py
```

The first command does not read `output/` and does not rerun the
3.66-billion-state enumeration.  It reconstructs all 18 quotient ranks,
validates every histogram and survivor bin, replays all seven controls,
rebuilds the margin catalog, and reruns the lightweight action audit.  It
uses about 41 MB and takes about six seconds on the research machine.

To rebuild the detached certificate from retained atomic output:

```text
python3 freeze_canonical_representative_certificate.py --write-certificate
```

To resume or independently reproduce one continuation gauge:

```text
python3 run_deferred_rank_two.py --orbit orbit-01
```

Existing results are skipped only after their complete semantic and input
hashes validate.  New output is written atomically.  The thirteen
continuation runs totaled 13,248.53 wall seconds and stayed below
60,866,560 bytes maximum resident memory under one-thread limits.

The current semantic hashes are:

```text
canonical census   963a4cb24217fa1a58afa7d7840cf965821c76177c6c6711d33862c00355dc7a
action audit       029ae4f1b6186435d2f1b445f88da1d7e69479b4a65bac9e179e9cb2a8aafcad
```
