# Hand-checkable proof supplement

## Review boundary

This separately authored publication supplement supplies the small amount of
finite arithmetic needed by the proof-only edition. It was written after the
original independent audit. That audit's acceptance does not cover this new
presentation. Independent review of this supplement is pending. No original
theorem is strengthened, and the non-complete-intersection classification
remains unresolved.

## 1. Apéry witness for the type-seven member

Let S = <32,48,40,21,49> and m = 21. For each residue r in {0,...,20},
the table gives d_r, an explicit expression in S, and the four integers

    Q_g(r) = (d_r + g - d_((r+g) mod 21))/21,
    for g = 32,48,40,49.

Every displayed expression has value d_r and residue r modulo 21. Each Q
entry is obtained by one addition, one table lookup, one subtraction and
division by 21, so all 84 Bellman inequalities are individually hand-checkable.
For the remaining generator g = 21 the corresponding Q is always 1.

| r | d_r | Membership expression | Q_32 | Q_48 | Q_40 | Q_49 |
|---:|---:|:---|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 64 | 2·32 | 0 | 3 | 0 | 0 |
| 2 | 128 | 48 + 2·40 | 3 | 3 | 8 | 5 |
| 3 | 129 | 2·40 + 49 | 3 | 5 | 5 | 2 |
| 4 | 88 | 48 + 40 | 0 | 0 | 0 | 5 |
| 5 | 89 | 40 + 49 | 0 | 5 | 0 | 2 |
| 6 | 48 | 48 | 0 | 0 | 0 | 0 |
| 7 | 49 | 49 | 0 | 0 | 0 | 0 |
| 8 | 113 | 2·32 + 49 | 5 | 3 | 5 | 2 |
| 9 | 72 | 32 + 40 | 0 | 0 | 3 | 0 |
| 10 | 136 | 2·48 + 40 | 8 | 3 | 3 | 5 |
| 11 | 32 | 32 | 0 | 0 | 0 | 0 |
| 12 | 96 | 2·48 | 0 | 3 | 0 | 5 |
| 13 | 97 | 48 + 49 | 0 | 5 | 5 | 2 |
| 14 | 98 | 2·49 | 2 | 2 | 2 | 7 |
| 15 | 120 | 3·40 | 3 | 8 | 3 | 5 |
| 16 | 121 | 32 + 40 + 49 | 5 | 5 | 3 | 2 |
| 17 | 80 | 2·40 | 3 | 0 | 0 | 0 |
| 18 | 81 | 32 + 49 | 0 | 0 | 0 | 2 |
| 19 | 40 | 40 | 0 | 0 | 0 | 0 |
| 20 | 104 | 2·32 + 40 | 0 | 3 | 3 | 5 |

**Why the table proves exactness.** We have d_0 = 0 and
d_((r+g) mod 21) ≤ d_r + g for every residue and generator. Induction on
the number of generators in a nonnegative factorization of s shows
d_(s mod 21) ≤ s for every s in S. Conversely, each d_r belongs to S by
its displayed expression, and every nonnegative integer congruent to d_r
and at least d_r is d_r + 21k for an integer k ≥ 0. It belongs to S.
Thus, for every integer s ≥ 0,

    s belongs to S if and only if s ≥ d_(s mod 21).

This proves that these are exactly the Apéry representatives, without a
search cutoff or an unpublished dataset.

The largest gap in residue r is d_r - 21, so the Frobenius number is
max_r d_r - 21 = 136 - 21 = 115. The number 7 is a gap since d_7 = 49,
and 108 is a gap since 108 is congruent to 3 and d_3 = 129. Their sum
is 115, so the semigroup is not symmetric.

**Complete pseudo-Frobenius set.** If f is pseudo-Frobenius then f + 21
belongs to S and f does not, so f = d_r - 21 for its residue r. For a
candidate d_r - 21, its sum with g belongs to S exactly when Q_g(r) ≥ 1.
The generator 21 always meets this test. All four displayed Q entries are
positive exactly for

    r = 2,3,8,10,14,15,16.

Subtracting 21 from their d_r values gives respectively

    107,108,92,115,77,99,100.

Every other row has a zero Q entry, explicitly identifying a generator
that rejects its candidate. Therefore

    PF(S) = {77,92,99,100,107,108,115},

and the Cohen–Macaulay type is seven. The use of the standard equivalence
between type, symmetry and Gorensteinness is unchanged from PROOF.md.

## 2. Finite matrix witness for the five-cycle example

For the matrix B displayed in PROOF.md §5 and the positive vector
a = (89,72,85,164,107), the five row products Ba are

    -356 + 85 + 164 + 107 = 0,
     89 - 360 + 164 + 107 = 0,
     89 + 144 - 340 + 107 = 0,
    178 + 144 + 170 - 492 = 0,
     72 + 85 + 164 - 321 = 0.

The columns sum to zero, the diagonal magnitudes are (4,5,4,3,3),
and the off-diagonal zero positions are exactly those in Theorem 4.
The cofactor deleting row 5 and column 5 is

    det [ -4   0   1   1 ]
        [  1  -5   0   1 ]
        [  1   2  -4   0 ]
        [  2   2   2  -3 ] = 107.

For example, expansion in the first row gives

    (-4)(-48) - 23 - 62 = 107.

Thus rank B = 4. Its right kernel is spanned by a and its left kernel
by the all-ones vector. Also gcd(89,72) = 1, hence a is primitive.
Consequently Adj(B) = h a·1^T; the computed (5,5) entry is
107 = h·107, so h = 1. In particular every adjugate column is exactly a.

To pass from a pseudo-principal matrix to a genuine principal matrix we
use the already credited Dey–Srinivasan Theorem 26: a rank-(n-1)
pseudo-principal matrix with column sums zero, primitive adjugate column,
diagonal magnitudes at least two and at most one off-diagonal zero per
column is principal for its positive primitive kernel generators. Every
hypothesis has just been checked for B. This use is precisely a
principality statement, not a claim that the source proves Theorem 4's
Gorenstein obstruction. Principality and diagonal magnitudes greater than
one also prove minimal generation.

Finally the formula of Lemma 3 gives

    v(2,4,5,3,1) = (-1,4,0,1,1),
    v(4,2,5,3,1) = (-1,2,0,2,1),

whose products with a are -89 + 288 + 164 + 107 = 470 and
-89 + 144 + 328 + 107 = 490. Lemma 3 proves both are pseudo-Frobenius
numbers, including all five membership conditions by cyclic rotation;
Theorem 4 proves their distinctness generally. No assertion about the
complete pseudo-Frobenius set of this example is needed or adopted in
this proof-only edition.
