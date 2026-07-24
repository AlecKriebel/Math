# Eliahou repair through the adjacent-42 fold

## Status

Eliahou's 13 residual base-sequence correlations are not independent.  After
folding the four rows modulo 42, they cancel into a cyclic complementary
frame of energy only 14.  An exact `BS(84,83)` must have the same cyclic
flatness with energy 334.

This gives three exact reductions.

1. Any exact repair of the published base rows changes at least 80 of their
   334 signs.
2. In the natural special coordinates `(s,q)`, any exact repair changes at
   least 41 of the 334 signs.  At distance 41, only one sharply classified
   two-`q`-flip family remains.
3. The complete minimum base-distance shell is an 80-sparse ternary norm
   equation in `Z[C_42]`.  The compulsory reciprocal `q` skeleton factors
   its first filter into 42 tiny transfer components.

The two cheapest Fourier roots reduce the 80 possible reciprocal `q` pairs
in the open special-distance-41 case to 39.  Each survivor has exactly two
possible joined ordinary/alternating row-sum profiles.

These are necessary conditions, not a construction.  No `BS(84,83)` or
Hadamard matrix is claimed.  The dependency-free checker
`verify_eliahou_adjacent42_repair.py` replays every finite claim.

A July 2026
[companion report](https://raw.githubusercontent.com/Arthur742Ramos/hadamard-668-multiplier-obstructions/main/mod64/report.md)
already states the basic equivalence between an exact lift in Eliahou's
special form and `BS(84,83)` and proves a raw-distance lower bound of 64.
That translation is therefore prior.  The base-distance bound 80 below is a
strict improvement; the adjacent-42 fold, special-distance-41 boundary, and
anti-fold continuation were not located in that release.

## 1. A third cyclic image of `BS(84,83)`

For a row `X` of length 84 or 83, fold it modulo 42:

```text
F_X(j) = X_j + X_(j+42),       0 <= j < 42,
```

where the missing second endpoint in a short row contributes zero.  If
`R_k` is the summed aperiodic correlation of the four base rows, the summed
periodic correlation `P_k` of their four folds is

```text
P_0  = R_0 + 2 R_42,

P_k  = R_k + R_(42-k) + R_(42+k) + R_(84-k),
                                      1 <= k <= 20,

P_21 = 2(R_21+R_63).                                  (1)
```

The other coefficients follow by cyclic reflection.  Equation (1) is
ordinary reduction of the four-row norm modulo `z^42-1`.

Thus every `BS(84,83)` gives a periodically complementary length-42
integer quadruple with energy 334.  This is a necessary cyclic image.  It is
not sufficient for the original aperiodic equations.

## 2. The seed is already 42-flat

For Eliahou's published base rows, the four folds are exactly

```text
F_A = -2 z^41,
F_B = 0,
F_C = 2 + z^41,
F_D = -2 z^40 + z^41.                                (2)
```

They obey

```text
sum_X N(F_X) = 14.                                    (3)
```

This is a complete cyclic norm identity: all 41 nonzero periodic
correlations vanish.

The 13 nonzero base residuals are

```text
k :   4    8    12   16   26  30  34  38   42   46   50   54   58
R : -256  192 -128   64  -32  64 -96 128 -160  128  -96   64  -32.
```

Under (1), they couple as

```text
R_4  + R_38 + R_46 = 0,
R_8  + R_34 + R_50 = 0,
R_12 + R_30 + R_54 = 0,
R_16 + R_26 + R_58 = 0,
R_0  + 2 R_42      = 14.                              (4)
```

The defect is therefore invisible at every 42nd root except through its
energy.  Repairing one bad lag independently destroys four exact coupled
relations in (4); a viable move must replace the whole cyclic frame.

## 3. Exact distance bound

Across the four rows there are

```text
42+42+41+41 = 166
```

disjoint separation-42 pairs, plus two unpaired short-row signs.  If `E`
of those pairs have equal endpoints, the folded zero-lag energy is

```text
2 + 4E.                                                (5)
```

An exact target has energy 334, hence exactly

```text
E_target = (334-2)/4 = 83
```

equal pairs.  The seed folds in (2) have only three equal pairs:

```text
A at 41,       C at 0,       D at 40.
```

Changing one base sign toggles at most one of the 166 pair products.
Therefore every exact repair has base-row Hamming distance at least

```text
83-3 = 80.                                             (6)
```

This is an algebraic global bound, not a bounded Hamming-ball computation.

The map from special coordinates to base rows is

```text
(s_i,q_i) -> (A_i,B_i) = (s_i,s_i q_i)
```

in each long or short block.  One special-coordinate sign change alters at
most two base signs.  Hence (6) first gives distance at least 40 in `(s,q)`.
Equality 40 would require all 40 changes to be `s`-only and would leave `q`
fixed.  The existing exact reduction in `FIXED_Q_OBSTRUCTION.md` excludes
that case via `TU(41)=empty`.  Consequently

```text
distance_(s,q) >= 41.                                  (7)
```

The use of the published `TU(41)` classification occurs only in the final
step from 40 to 41.  The base-row bound 80 is self-contained.

## 4. The complete base-distance-80 norm equation

Equality in (6) is rigid:

- all three seed-equal pairs retain their signs;
- the two short singleton signs are unchanged;
- exactly 80 of the 163 seed-opposite pairs become equal;
- exactly one endpoint is flipped in every selected pair;
- nothing else changes.

Write the target fold as

```text
F = F_0 + 2G,
```

where `F_0` is (2).  Then `G` is a four-row ternary word with exactly 80
nonzero coefficients, supported only on seed-opposite pair cells.  Conversely
the sign of a nonzero `G` coefficient uniquely tells which endpoint of its
seed-opposite pair must be flipped.

Expanding the cyclic norm gives the exact minimum-shell equation

```text
sum_r (F_(0,r) G_r* + G_r F_(0,r)*)
       + 2 sum_r N(G_r)
     = 160                         in Z[C_42].          (8)
```

Its constant coefficient is automatic from `|supp G|=80`; its 21
independent nonconstant coefficients couple the entire residual repair.
Solving (8) is only the adjacent-42 stage.  A survivor must still satisfy
the other adjacent cyclic fold, or equivalently all original aperiodic
equations.

## 5. Reciprocal-skeleton transfer factorization

Every exact special quadruple has the reciprocal `q` skeleton from
`NOVEL_LIFTING_64.md`.  Relative to the seed, let `f_A,f_B,f_C,f_D` be the
base-row flip bits.  The induced `q` change is

```text
p_i = f_A(i) + f_B(i)       or       f_C(i)+f_D(i)    in F_2.
```

The homogeneous reciprocal conditions are

```text
p_i = p_(83-i)       in the long block,
p_i = p_(82-i)       in the short block.              (9)
```

On the minimum shell, one half-pair in one row has only three local states:

```text
unchanged, flip lower endpoint, flip upper endpoint.
```

The separation-42 involution and (9) generate:

- 21 reflected components in the long block;
- 20 reflected components and one center component in the short block.

The generic reflected component has weight enumerator

```text
1 + 12 t^2 + 8 t^4.
```

Three boundary components remember the seed's three equal pairs:

```text
long exception     1 + 6 t^2,
short exception    1 + 2 t^2,
short center       1 + 4 t^2.
```

Hence the exact reciprocal-skeleton enumerator on the base minimum shell is

```text
(1+12t^2+8t^4)^39
 (1+6t^2)(1+2t^2)(1+4t^2).                           (10)
```

The coefficient of `t^80` is

```text
16,734,850,903,642,159,814,868,855,513,591,696,065,526,623,680.
```

This remains large, but the unrestricted shell has

```text
binom(163,80) 2^80
= 858,127,816,779,524,603,449,862,398,679,184,731,003,194,837,
  028,101,298,260,042,590,285,987,840
```

states.  The reciprocal transfer removes a factor of about `5.13e22`
without an optimizer or a search tree.  More importantly, (10) is
component-local and can be joined directly to the 21 coefficients of (8).

Modulo two, the short boundary part of (8) says that the XOR of the two
short equality masks is reflection invariant:

```text
v_j = v_(40-j).
```

The local transfer audit proves that (9) already enforces this condition on
the minimum shell.

## 6. Complete special-distance-41 split

At one coordinate, classify changes as:

```text
a = s-only,       b = q-only,       c = both.
```

Their special and base Hamming costs are

```text
H_special = a+b+2c,
H_base    = 2a+b+c.
```

Combining `H_special=41` with `H_base>=80` leaves exactly

```text
(a,b,c) = (41,0,0), (40,1,0), (39,2,0).              (11)
```

The first case keeps `q` fixed and is excluded by the fixed-`q` theorem.

The reciprocal skeleton has exactly one weight-one change: the center of
the short block, global index 125.  In the `(40,1,0)` case the 40 `s`
changes must generate 40 common fold coefficients `L,S`, with
`|supp L|+|supp S|=40`.  At the root `z=-1`, write

```text
lambda=L(-1),       sigma=S(-1).
```

The four folded row values force

```text
lambda(lambda+1) + sigma^2 = 41,
```

or equivalently

```text
(2lambda+1)^2 + (2sigma)^2 = 165.                    (12)
```

Equation (12) has no integer solution: the primes 3 and 11, both `3 mod 4`,
occur to odd exponent in 165.  Thus the unique one-`q`-flip case is
impossible.

The only open distance-41 case is therefore

```text
39 s-only changes + 2 q-only changes.                 (13)
```

The two `q` changes must form one reciprocal pair.  There are 83 such pairs:
42 long and 41 short.  Three short pairs cannot lie on the minimum base
shell: two hit a seed-equal `D` pair and the center reciprocal pair flips
both endpoints of one separation-42 pair.  Exactly 80 pairs remain before
spectral filtering.

## 7. Roots `+1` and `-1`: 80 pairs become 39

For a reciprocal `q` pair, let

```text
h_+ = H(1),       h_- = H(-1)
```

be its signed two-term fold.

The 42 long pairs have distribution

```text
(h_+,h_-)   count
(-2, 0)       6
( 0, 2)      15
( 0,-2)      15
( 2, 0)       6.
```

The 38 shell-compatible short pairs have

```text
(h_+,h_-)   count
( 2,-2)      10
( 0, 0)      18
(-2, 2)      10.
```

Imposing energy 334 at both roots, the parity of the 39 common `s`-flip
supports, and consistency between ordinary and alternating sums leaves only

```text
long:  (-2,0), (0,2)       6+15 = 21 pairs,
short: (0,0)                       18 pairs.
```

Thus exactly 39 reciprocal `q` pairs survive.

For each surviving pair there are exactly two joined profiles.  Writing a
profile as

```text
((L(1),S(1)), (L(-1),S(-1))),
```

they are:

```text
long (-2,0):
  ((-3, 4),(-5,-4)),  (( 6,-5),( 4, 5))

long (0,2):
  ((-4,-5),(-6, 5)),  (( 5, 4),( 3,-4))

short (0,0):
  ((-4,-5),( 4, 5)),  (( 5, 4),(-5,-4)).
```

This is the new exact frontier nearest the seed:

```text
39 q-pair choices x 2 root profiles,
```

followed by the group-ring equation (8) and the remaining cyclic/aperiodic
conditions.  No infeasibility is claimed for these 78 outer cases.

## Reproduction

From this directory:

```sh
python3 verify_eliahou_adjacent42_repair.py
python3 -m unittest -v test_eliahou_adjacent42_repair.py
```

The verifier uses only the Python standard library, reconstructs the seed
directly from its published run data, checks (1) on independent random
integer fixtures, and uses exact arithmetic throughout.
