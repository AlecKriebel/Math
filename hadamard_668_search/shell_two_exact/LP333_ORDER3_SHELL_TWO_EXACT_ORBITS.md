# Complete exact profile classification of the two-high shell

## Status

The order-three `LP(333)` profile sector

```text
(n_9,n_3,n_0)=(2,12,10)
```

has exactly five orbits of exact profile-zero solutions under the established
order-24 symmetry group.  Their orbit sizes are

```text
24, 12, 12, 12, 24,
```

so the five representatives account for 84 raw symmetry images.

This is a profile-level theorem.  The five objects solve the exact
length-37 Eisenstein complementary-autocorrelation equation obtained from
the three-row quotient.  They are **not** labelled `LP(333)` objects, do not
yet solve the primitive-nine placement equations, and are not Hadamard
matrices of order 668.

## 1. Uniformizer descent

Put

```text
lambda=1-omega,              omega^2+omega+1=0.
```

The ten profile letters are

```text
0,
sigma lambda omega^u          (sigma in {+1,-1}, u in F_3),
3 omega^v                     (v in F_3).
```

After fixing the signs of the twelve medium letters at phase zero, every
medium phase change and every insertion of one of the two high letters is
divisible by `lambda^2`, which is associated to 3.  If `m` is the signed
base word and the one-slot changes are `delta_i`, bilinearity gives the
lossless identity

```text
D(m+sum_i delta_i)
 =
D(m)+sum_i [D(m+delta_i)-D(m)]                 (mod 9).  (1)
```

All omitted cross products are divisible by 9.  Thus (1) is an exact
quotient theorem, not a heuristic linearization.

For an opposite-class quartet

```text
(A_j,A_(j+6),B_j,B_(j+6)),
```

the signed skeleton equation is

```text
-s_A,j+s_A,j+6+s_B,j-s_B,j+6=0 in F_3.                 (2)
```

The legal local counts by number of medium positions are

```text
m=0,1,2,3,4:       1,0,12,8,6.
```

Consequently twelve media in six quartets have only seven support
partitions:

```text
222222, 332220, 333300, 422220, 433200, 442200, 444000.
```

At the first quotient flag, a nonempty `m`-medium quartet imposes one
nonzero affine equation on its phase trits and hence leaves exactly
`3^(m-1)` local records.  An empty quartet is instead a gate on the
two-high support.  The global search therefore joins small local tables of
size at most 27 against:

```text
12 correlation coordinates modulo 9,
4 exact aggregate coordinates,
2 high-support positions,
2 high phases.
```

Only the joined records are evaluated modulo 27 and with exact Eisenstein
arithmetic.

## 2. Complete partition census

The enumerator uses one representative of every signed-skeleton orbit.
Every modulo-nine survivor is detachedly replayed.  The exact counts are:

| partition | raw skeletons | canonical skeletons | modulo-9/exact-aggregate survivors | modulo-27 survivors | exact survivors |
|---|---:|---:|---:|---:|---:|
| `222222` | 2,985,984 | 124,612 | 2,054,918 | 12 | **1** |
| `332220` | 6,635,520 | 277,120 | 4,568,708 | 23 | 0 |
| `333300` | 61,440 | 2,880 | 49,152 | 0 | 0 |
| `422220` | 3,732,480 | 156,880 | 2,590,579 | 17 | **4** |
| `433200` | 829,440 | 35,520 | 591,921 | 2 | 0 |
| `442200` | 466,560 | 20,520 | 341,206 | 6 | 0 |
| `444000` | 4,320 | 256 | 4,554 | 1 | 0 |
| **total** | **14,715,744** | **617,788** | **10,201,038** | **61** | **5** |

The five exact hits lie on five different canonical signed skeletons.
For each hit, the stabilizer of the full profile equals the stabilizer of
its skeleton.  Hence no orbit is counted twice.  The other 56 modulo-27
points have visibly nonzero residuals in multiples of 27.

## 3. Exact orbit representatives

Profile IDs index the lexicographically ordered compositions of three:

```text
0:(0,0,3)  1:(0,1,2)  2:(0,2,1)  3:(0,3,0)  4:(1,0,2)
5:(1,1,1)  6:(1,2,0)  7:(2,0,1)  8:(2,1,0)  9:(3,0,0).
```

| label | partition | aggregate target | orbit / stabilizer | A profile IDs | B profile IDs |
|---|---|---|---:|---|---|
| `h2-222222-0` | `222222` | `(2,-2,-2,2)` | `24 / 1` | `2,5,8,1,7,9,5,8,5,5,5,7` | `2,5,3,6,5,5,5,4,7,5,4,7` |
| `h2-422220-0` | `422220` | `(2,-2,-2,2)` | `12 / 2` | `2,5,7,8,6,5,2,5,7,8,6,5` | `5,8,5,0,1,5,5,8,5,0,1,5` |
| `h2-422220-1` | `422220` | `(2,-2,-4,-2)` | `12 / 2` | `2,8,8,5,5,5,2,8,8,5,5,5` | `2,5,5,4,1,3,2,5,5,4,1,3` |
| `h2-422220-2` | `422220` | `(4,2,-2,2)` | `12 / 2` | `4,9,8,5,5,5,4,9,8,5,5,5` | `2,7,5,1,5,6,2,7,5,1,5,6` |
| `h2-422220-3` | `422220` | `(-3,0,-3,-3)` | `24 / 1` | `8,5,4,5,9,1,6,8,5,5,2,6` | `2,3,5,5,1,5,1,4,7,5,5,5` |

For every representative, two independent implementations verify:

```text
D(0)=(167,0),
D(t)=(0,0) for every t=1,...,36,
the exact aggregate target,
the (2,12,10) norm census,
all six local signatures,
canonicality and the complete G-orbit.
```

## 4. The next placement layer

Each exact profile has 54 active within-residue placement trits:

```text
12 medium letters * 2 active fibers
+10 zero letters * 3 active fibers
+ 2 high letters * 0 active fibers
=54.
```

Thus the raw labelled phase space for each representative is

```text
3^54 = 58,149,737,003,040,059,690,390,169.
```

The first placement Hensel digit has the same exact census on all five:

```text
variables                         54
displayed equations               20
identically zero rows              2
coefficient/augmented rank     18/18
nullity                            36
consistent                        yes
```

The trivial column-character transfer and exact row-margin catalog give:

| label | compatible transfer signatures | compatible row-margin rows | accepted root-character assignments |
|---|---:|---:|---:|
| `h2-222222-0` | 64 | 72 | 272,797,926,089,102,312,850 |
| `h2-422220-0` | 64 | 72 | 272,288,106,061,230,283,920 |
| `h2-422220-1` | 64 | 72 | 289,168,460,981,590,208,256 |
| `h2-422220-2` | 87 | 96 | 368,409,083,453,963,639,136 |
| `h2-422220-3` | 46 | 93 | 336,046,930,024,774,681,314 |

These counts solve only the row-direction/root-character gate.  The
nontrivial column characters and the upper primitive-nine digits remain.

## 5. Certificates and reproduction

The semantic SHA-256 of the complete generated certificate is

```text
36099444b32f88869557a6f510f06cfa3b6eaa7a876b26cf62a0796ca4232565.
```

The compact stored certificate has file SHA-256

```text
8e7579d6361ffda0187c10e8e4fef654c8288e51e87e41432c178725cec40614.
```

The first independently detached representative certificate has semantic
SHA-256

```text
4bb83d560f3b80fc765374f44480bf30d94c515a694a10f6867003cf1c9ada02.
```

Run the light independent audits with:

```sh
python3 shell_two_exact/verify_shell_two_partition_theory.py
python3 shell_two_exact/verify_shell_two_exact_orbits.py
python3 -m unittest -v \
  shell_two_exact/test_shell_two_partition.py
```

Compile the exact enumerator with:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  shell_two_exact/verify_shell_two_partition.cpp \
  -o /tmp/verify_shell_two_partition
```

Then run it once for each of the seven partition strings using
`--partition`.  A complete run automatically checks every pinned count.
The reference runs peaked below 4 MB resident memory; the longest
partition took about 22.6 minutes of CPU time.  No SAT solver and no
timeout inference is used.
