# Exact small-state prefix for the LP(333) diagonal phase frame

## Status

The three-fiber phase factor turns each of the 22 pinned ideal-compatible
profile tuples into exactly 54 signed cube-root phase variables.  A direct
phase search has size

```text
3^54 = 58,149,737,003,040,059,690,390,169.
```

The first two necessary projections of the diagonal frame admit a much
smaller exact decomposition.  Each of the six fiber sequences can be
collapsed independently to:

```text
(its exact augmentation norm,
 its first characteristic-37 logarithmic norm coefficient).
```

Across all 22 profile tuples, the largest one-sequence summary has only 444
states.  After joining all six sequences and discarding partial norms above
167, the largest final state table has 666 states.

Exact enumeration shows that all 22 fixed profile tuples survive this
prefix.  This is a reproducible state-compression theorem and count, not a
complete diagonal-frame assignment, an `LP(333)`, or a Hadamard matrix.
All 22 tuples already fail the stronger placement-independent gate `D_t=0`,
so these counts are diagnostic validation of a reusable decomposition, not
live candidate counts.  Apply the prefix next only to a profile that passes
the zero gate.

## 1. Diagonal frame and augmentation

Let the six Eisenstein sequences be

```text
U_(A,0), U_(A,1), U_(A,2),
U_(B,0), U_(B,1), U_(B,2).
```

The diagonal equation is

```text
sum_i U_i U_i^* = 167 e                 in Z[omega][C_37].     (1)
```

For one sequence, write its fixed zero-column phase as `u(0)` and its
value on the nonzero order-three class `C_j` as `u_j`.  Every active `u_j`
has three possible signed unit values and every inactive value is zero.
Because each class has size three, evaluation at the trivial column
character is

```text
S = u(0) + 3 sum_(j=0)^11 u_j.                              (2)
```

Applying the augmentation to (1) gives the exact integer condition

```text
sum_i Norm(S_i) = 167.                                      (3)
```

For one sequence with at most twelve active classes, the possible exact
sums in (2) form a small two-dimensional triangular lattice.  This already
collapses most of its `3^n` phase assignments.

## 2. First characteristic-37 coefficient

Reduce (1) modulo 37 and use the logarithmic coordinate from the existing
characteristic-37 transfer.  With `v=u^3`, the first nonconstant coefficient
of one sequence is

```text
L = 19 sum_(j=0)^11 8^j u_j                 in Z[omega]/37.  (4)
```

The coefficient of `v` in `U U*` is

```text
tau = L conjugate(S) - S conjugate(L).                       (5)
```

It is anti-self-conjugate and therefore carries one scalar over `F_37`.
Equation (1) requires

```text
sum_i tau_i = 0.                                             (6)
```

Both (3) and (6) are additive across the six sequences.  Thus each sequence
is enumerated once and collapsed to the finite summary

```text
(Norm(S), tau) -> exact multiplicity.
```

No pair or triple of raw phase assignments is ever enumerated.

## 3. Exact state widths

For the 22 pinned profile tuples:

```text
active phases per tuple                         54
largest raw one-sequence space              3^12 = 531,441
largest collapsed one-sequence summary           444
largest six-sequence joined summary               666
distinct sequence signatures checked              129
peak verifier RSS on the reference replay       30 MB
swaps                                               0
```

The summary discards a one-sequence state immediately when its exact norm
already exceeds 167.  This is safe because all six norms are nonnegative.

## 4. Exact survivor counts

All 22 profile tuples have positive counts after both (3) and (6).

Before the characteristic-37 condition, the exact augmentation-survivor
counts range from

```text
209,362,382,441,060,450,385,168
```

to

```text
233,232,723,804,553,256,004,480.
```

After imposing (6), the exact prefix-survivor counts range from

```text
5,658,442,768,663,401,171,882
```

to

```text
6,303,587,129,843,385,773,508.
```

All 44 per-tuple counts are pinned directly in the verifier.  The ratio
between the two counts is extremely close to 37 for every tuple:

```text
36.99999999991419 ... 37.000000001458545.
```

This near-uniformity is an observed exact-count pattern only.  The counts
are **not** generally in the exact ratio 37, and no independence theorem is
claimed.

The compact hash of the active-count vectors, all six sequence summaries,
joined state widths, and exact survivor counts is

```text
443d0e733f5c383d5d5ed14d5ec98b458becf9d7dd9e64c08d9d07c2b625a81a.
```

## 5. Tractability boundary

The next characteristic-37 coefficient can still be summarized separately
for one sequence.  In a bounded row-zero census its one-sequence tables had
at most 16,096 states.  A naïve dictionary join of those tables was not a
small computation and was stopped without a result.

Consequently:

- the augmentation-plus-`T_1` layer is retained as an exact small-state
  theorem;
- no `T_2` survivor count, exclusion, or timeout inference is retained;
- a future `T_2` implementation should use a dense convolution over
  `F_37^2`, an equivalent transform, or a further algebraic factorization.

## Reproduction

```text
python3 verify_lp333_order3_diagonal_frame_prefix.py
python3 -m unittest -v test_lp333_order3_diagonal_frame_prefix.py
```

The verifier uses the Python standard library and exact integer arithmetic.
It independently compares 129 sequence formulas against the general
characteristic-37 transfer before replaying the counts.
