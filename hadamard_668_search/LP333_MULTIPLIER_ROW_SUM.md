# LP(333) multiplier row-sum obstruction

## Status

The fixed-compression multiplier families with subgroup sizes

```text
h = 18, 9, 6
```

are empty. This closes the column-only order-18 family, the order-9
(`quartic`) quotient, and the order-6 (`sextic`) quotient.

The same projection is feasible for `h=3`. That is the sharp viable boundary
among these four subgroup sizes, but the retained `h=3` object is only a
length-nine row-sum witness. It is **not** a Legendre pair, a Hadamard matrix,
or evidence that the remaining column equations can be solved.

All claims below are checked with exact integer arithmetic by
`verify_lp333_multiplier_row_sum.py`.

## 1. Summing all column lags

Let `H` be the subgroup of order `h` in the quadratic residues of
`F_37^*`, where

```text
h in {18,9,6,3},       m = 36/h.
```

The nonzero elements split into the `m` classes

```text
C_j = 2^j H,           j=0,...,m-1.
```

Write the `H`-invariant QPSK quotient as

```text
x_0(r), x_1(r), ..., x_m(r),       r in Z/9.
```

The fixed Legendre-symbol compression is

```text
sum_r x_0(r)     = 1,
sum_r x_{j+1}(r) = -3 i (-1)^j.
```

Because `m` is even, the pointwise nonzero-class sum

```text
t_r = sum_{j=1}^m x_j(r)
```

satisfies

```text
sum_r t_r = 0.
```

For the partition sizes

```text
w = (1,h,...,h),
```

let `D=diag(w)`, and let `M_j` be the transition matrix for one column
lag in `C_j`. Direct finite-field counting gives the exact matrix identity

```text
D + h sum_j M_j = w w^T.                         (1)
```

Indeed, for fixed source and target columns there is exactly one column lag
taking the source to the target. The verifier reconstructs every class and
transition matrix and checks (1) entry by entry for all four values of `h`.

Define the complete CRT-row sum

```text
s_r = x_0(r) + h t_r.
```

Summing the QPSK Legendre-pair equations over all 37 column lags now gives

```text
Re PAF_s(0) = 333 + 36(-1) = 297,
Re PAF_s(a) = 37(-1)       = -37,   a=1,...,4.   (2)
```

Thus every candidate in any of these multiplier families must project to a
length-nine Gaussian sequence satisfying (2).

## 2. The zero word is forced to be an LP(9) core

At zero column lag, for each nonzero row lag,

```text
R_0(a) + h sum_{j=1}^m R_j(a) = -1.
```

Consequently `R_0(a)+1` is divisible by `h`. Exact enumeration of the
`4^9` QPSK words with sum one shows, independently for
`h=18,9,6,3`, that this necessary divisibility condition leaves exactly the
same 972 words, all with

```text
R_0(1)=R_0(2)=R_0(3)=R_0(4)=-1.
```

The standard 972 row-normalization actions form one free orbit on this
catalog. We may therefore use the canonical exponent word

```text
x = (0,0,0,1,2,3,1,3,2).
```

The verifier additionally replays the obstruction over all 972 cores.

## 3. A small exact integer projection

Use the sign-pair representation

```text
x = (A+B + i(B-A))/2.
```

At a fixed row, `t_r` is a sum of `m` fourth roots. Equivalently, its two
sign sums are independent values

```text
p_r,q_r in {-m,-m+2,...,m}.
```

The real sign coordinates of `s_r` are then

```text
U_r = A_r + h p_r,
V_r = B_r + h q_r.
```

The condition `sum t=0` is exactly

```text
sum p_r = sum q_r = 0.
```

After subtracting the norm nine of `x`, the zero-lag equation in (2) becomes

```text
C_A(p) + C_B(q) = 288/h,                         (3)
```

where

```text
C_A(p) = sum_r ((h/2) p_r^2 + A_r p_r),
C_B(q) = sum_r ((h/2) q_r^2 + B_r q_r).
```

Every summand is a nonnegative integer. This makes (3) a very small finite
enumeration, despite being a relaxation of the full quotient.

The canonical exact census is:

| `h` | classes `m` | states in each real channel | paired sum/energy states | distinct PAF profiles | target profiles |
|---:|---:|---:|---:|---:|---:|
| 18 | 2 | 1 | 0 | 0 | 0 |
| 9 | 4 | 21 | 40 | 29 | 0 |
| 6 | 6 | 589 | 2,376 | 971 | 0 |
| 3 | 12 | 102,869 | 46,503,026 | not exhausted here | at least 1 |

For `h=9` and `h=6`, every paired state was checked against all four
nonzero equations in (2), and none matched. For `h=18`, even the energy
equation has no state.

Across all 972 zero cores the exact totals are:

```text
h=18             0 states, 0 hits
h=9         38,880 states, 0 hits
h=6      2,309,472 states, 0 hits.
```

This is a complete obstruction for the stated multiplier families, not a
bounded solver outcome.

## 4. The viable boundary at h=3

For `h=3`, the energy-and-sum projection contains exactly `46,503,026`
states. The following Gaussian row sum satisfies the complete target (2):

```text
s = [(4,-3), (1,6), (-2,-3), (12,1), (-1,0),
     (-6,-1), (-6,1), (0,-1), (-1,0)].
```

Relative to the canonical `x`, it gives

```text
t = [(1,-1), (0,2), (-1,-1), (4,0), (0,0),
     (-2,0), (-2,0), (0,0), (0,0)].
```

The verifier checks

```text
sum s                   = 1,
sum |s_r|^2             = 297,
Re PAF_s(1..4)          = (-37,-37,-37,-37),
sum t                   = 0,
each t_r is a sum of 12 fourth roots.
```

This proves only that the row-sum obstruction stops at `h=3`. A genuine
order-3-multiplier construction must still split every `t_r` into twelve
class phases with the prescribed class sums and satisfy every individual
column-lag equation.

The dependency-free C++ enumerator
`enumerate_lp333_order3_row_sums.cpp` completes this boundary census. It
checks all `46,503,026` energy-and-sum states and finds exactly `1,756`
row-sum words satisfying all four nonzero equations in (2). The emitted
catalog is

```text
output/lp333_order3_row_sum_catalog.csv
```

with `1,757` lines including its header and SHA-256

```text
e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea.
```

Every catalog word passes the two Gale--Ryser tests needed to realize its
row sums by the twelve fixed-weight binary class columns. This margin test
does not impose the class-word autocorrelations or any nonzero-column
equation, so it is a compatibility check rather than a construction.

Pairing the twelve order-three classes into the six classes of the excluded
sextic quotient gives a useful distance-from-symmetry statistic. Minimize,
row by row, the number of paired class phases that must differ. Across the
`1,756` words, the resulting rigorous lower-bound histogram is

```text
paired splits   2   3   4    5    6    7    8    9
words           8  11  62  194  411  530  406  134.
```

Thus every surviving order-three row-sum word must genuinely break the
closed sextic symmetry, although the relaxed minimum is only two cells.

Reproduce the exhaustive catalog with:

```sh
c++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  enumerate_lp333_order3_row_sums.cpp \
  -o ../tmp/hadamard_668_build/enumerate_lp333_order3_row_sums

../tmp/hadamard_668_build/enumerate_lp333_order3_row_sums \
  --emit-words output/lp333_order3_row_sum_catalog.csv
```

## 5. Phi-3 corollary inside the sextic equations

The earlier order-three row Fourier projection of the `h=6` quotient also
collapses exactly. If `G_{j,a}` is the sum of class word `j` over rows
congruent to `a modulo 3`, and

```text
T_a = sum_{j=1}^6 G_{j,a},
```

then the summed nonzero-class equations and the zero-column equation imply

```text
T = (-2i, i+epsilon, i-epsilon),
epsilon in {1,-1,i,-i}.                              (4)
```

For completeness, write `T_0=u=a+bi`, `T_1=v=c+di`, and
`T_2=-u-v`. The Gaussian norm shell is

```text
6(a^2+b^2+c^2+d^2+ac+bd) + a + 3b = 18.             (5)
```

Completing squares bounds the quadratic term by four. Reducing (5) modulo
three and using that bound gives `a=0`; the remaining equation forces
`b=-2` and

```text
c^2 + (d-1)^2 = 1,
```

which yields exactly the four states in (4). The verifier checks this finite
shell too. Since the stronger row-sum theorem already proves that the
sextic family is empty, (4) is retained as an algebraic cross-check rather
than as a new solver channel.

## Consequences and scope

- The order-18 column-only multiplier family is closed.
- The order-9/quartic fixed-compression quotient is closed.
- The order-6/sextic fixed-compression quotient is closed; its exact CP-SAT
  search should not be resumed.
- The order-3 row-sum projection is feasible and is the next multiplier lane
  not excluded by this theorem.
- None of these exclusions proves that `LP(333)` or `H(668)` is impossible
  without the corresponding multiplier and fixed-compression assumptions.

Run the complete dependency-free replay with:

```sh
python3 verify_lp333_multiplier_row_sum.py
python3 -m unittest -v test_lp333_multiplier_row_sum.py
```
