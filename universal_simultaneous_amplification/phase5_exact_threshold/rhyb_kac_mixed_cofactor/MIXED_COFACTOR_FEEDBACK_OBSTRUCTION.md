# Poisson-gauged mixed cofactors and the two-rule feedback obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph enumeration, ansatz search, literature search, or external
communication was used.

## Status

**PROVED EXACT DETERMINANT REDUCTION AND SCOPED ROUTE OBSTRUCTION.**  This
note does not prove the one-root Kac inequality

\[
 r^3\psi_{B,i}\psi_{D,i}\leq 1.                    \tag{D-KAC}
\]

It gives a single bordered determinant whose sign is exactly `(D-KAC)`.
The construction retains the signed density reward before applying an
exact determinant-one Poisson gauge.  On the active branch the gauged
matrix is sign-similar to a `Z`-matrix, but that matrix is an `M`-matrix if
and only if `(D-KAC)` already holds.

This closes the canonical route

1. turn the signed mark into a positive determinant by Poisson gauge; then
2. invoke Hadamard--Fischer, generic `M`-matrix positivity,
   Alexandrov--Fenchel, or a stable-polynomial coefficient inequality.

Before the gauge, the standard cone hypotheses fail.  After the gauge, the
unknown inequality is literally the last two-by-two principal minor.  The
Poisson gauge preserves the first determinant derivative but not the
higher coefficients needed by a stable-polynomial argument.

This is deliberately a scoped obstruction.  It does not rule out a new
cross-rule forest identity, or a physical supersolution proving that the
feedback matrix is an `M`-matrix.

## 1. A determinant-one Poisson gauge

Let `Q` be the row generator of a finite irreducible continuous-time
Markov chain on `Omega`, put

\[
 L=-Q,
\]

and fix a root `i`.  Write `R=Omega\setminus\{i\}` and

\[
 A=L_{RR},\qquad \tau_Q(i)=\det A.                  \tag{1}
\]

The killed matrix `A` is a nonsingular `M`-matrix.  For an arbitrary real
column mark `g`, define the killed Poisson column

\[
 z_i=0,\qquad z_R=A^{-1}g_R                         \tag{2}
\]

and its root residue

\[
 \boxed{\kappa_i=g_i-L_{iR}A^{-1}g_R.}              \tag{3}
\]

Since `Q=-L`, one has

\[
 g+Qz=g-Lz=\kappa_i e_i.                            \tag{4}
\]

For the density mark, (3) is exactly the Kac reward

\[
 \kappa_i=g(i)+Q(i,R)(-Q_{RR})^{-1}g_R=\psi_i.      \tag{5}
\]

Let

\[
 \mathcal T_Q(g)=
 \left.\partial_t\det\{L+t\operatorname{diag}(g)\}
 \right|_{t=0}
 =\sum_a\tau_Q(a)g_a.                               \tag{6}
\]

There is an exact rank-one determinant representation

\[
 \boxed{
 \det(L+g e_i^T)=\mathcal T_Q(g)
                   =\tau_Q(i)\kappa_i.}             \tag{7}
\]

Indeed, `adj(L)=mathbf 1 tau_Q^T`, so the rank-one determinant formula
gives the first equality.  For the second equality, put

\[
 E_i=I-z e_i^T.                                     \tag{8}
\]

Because `z_i=0`, `det E_i=1`, and direct multiplication gives the stronger
matrix identity

\[
 \boxed{
 (L+g e_i^T)E_i=L+\kappa_i e_i e_i^T.}              \tag{9}
\]

Thus the signed mark has not been replaced by a positive part or absolute
value.  It has been transported by an exact determinant-one column gauge.
If `mathcal T_Q(g)>0`, then `kappa_i>0`, and the last matrix in (9) is a
nonsingular `M`-matrix obtained by pinning one vertex of the singular
irreducible `M`-matrix `L`.

Equation (9) is stronger than the usual first-order Poisson invariance
`mathcal T_Q(g+Qz)=mathcal T_Q(g)`: it is an identity of two full rank-one
determinants.  It is not an identity of the diagonal pencils
`det(L+t diag(g))` and `det(L+t diag(g+Qz))`.

## 2. One bordered determinant for the Kac diagonal gap

Apply Section 1 to the recurrent Bd and dB dual generators.  Their state
spaces may have different sizes.  For `U in {B,D}`, put

\[
 L_U=-Q_U,\quad R_U=\Omega_U\setminus\{i\},\quad
 A_U=(L_U)_{R_UR_U},\quad b_U=(L_U)_{iR_U},          \tag{10}
\]

and let `g_U` be the restriction of the same density reward to
`Omega_U`.  Write `kappa_U` for (3).  In the block order

\[
                         (R_B,R_D,a,b),
\]

define

\[
 \boxed{
 \mathbb H_i=
 \begin{pmatrix}
 A_B&0&0&r^3g_{B,R_B}\\
 0&A_D&g_{D,R_D}&0\\
 b_B&0&1&r^3g_{B,i}\\
 0&b_D&g_{D,i}&1
 \end{pmatrix}.}                                    \tag{11}
\]

Schur complementation of `A_B direct-sum A_D` gives

\[
 \det\mathbb H_i
 =\det A_B\det A_D
   \det\begin{pmatrix}
       1&r^3\kappa_B\\
       \kappa_D&1
   \end{pmatrix}.                                   \tag{12}
\]

Using (1) and (7), this is the exact mixed-cofactor identity

\[
 \boxed{
 \det\mathbb H_i
 =\tau_B(i)\tau_D(i)
   -r^3\mathcal T_{Q_B}(g_B)\mathcal T_{Q_D}(g_D).} \tag{13}
\]

No positive-part operation is hidden in (13).  On the active branch both
tree functionals, and hence both `kappa` values, are positive.  Since

\[
 \mathcal T_{Q_U}(g_U)=\tau_U(i)\psi_{U,i},          \tag{14}
\]

the sign of (13) is exactly `(D-KAC)`.

The two Poisson column operations can be performed directly in (11):

- subtract `r^3 z_B` times the `R_B` columns from column `b`; and
- subtract `z_D` times the `R_D` columns from column `a`.

Both operations together form a unit upper-triangular right multiplier.
They transform (11) into

\[
 \mathbb N_i=
 \begin{pmatrix}
 A_B&0&0&0\\
 0&A_D&0&0\\
 b_B&0&1&r^3\kappa_B\\
 0&b_D&\kappa_D&1
 \end{pmatrix}.                                     \tag{15}
\]

This is the two-rule version of the exact signed Poisson gauge (9).

## 3. The master `M`-matrix condition is exactly the conjecture

On the active branch, apply the block signature which is positive on
`R_B,a` and negative on `R_D,b`.  It turns (15) into

\[
 \boxed{
 \mathbb Z_i=
 \begin{pmatrix}
 A_B&0&0&0\\
 0&A_D&0&0\\
 b_B&0&1&-r^3\kappa_B\\
 0&b_D&-\kappa_D&1
 \end{pmatrix}.}                                    \tag{16}
\]

This is a `Z`-matrix: `A_B,A_D` are killed `M`-matrices and
`b_B,b_D` are entrywise nonpositive.  It is block lower triangular, with
the final diagonal block

\[
 C_i=\begin{pmatrix}
 1&-r^3\kappa_B\\
 -\kappa_D&1
 \end{pmatrix}.                                     \tag{17}
\]

The first two diagonal blocks are already nonsingular `M`-matrices.
Therefore

\[
 \boxed{
 \mathbb Z_i\text{ is an `M`-matrix}
 \quad\Longleftrightarrow\quad
 C_i\text{ is an `M`-matrix}
 \quad\Longleftrightarrow\quad
 1-r^3\kappa_B\kappa_D\geq0.}                      \tag{18}
\]

The last equivalence is the elementary two-by-two `M`-matrix criterion.
Equality corresponds to a singular `M`-matrix.  Hence the desired theorem
has a single master `M`-matrix formulation, but generic `M`-matrix
positivity cannot prove it: the unknown sign is already the principal
minor

\[
                         \det\mathbb Z_i[\{a,b\}].   \tag{19}
\]

In particular, applying a Hadamard--Fischer or principal-minor inequality
to `mathbb Z_i` requires first knowing that `mathbb Z_i` is an `M`-matrix,
which by (18) is precisely `(D-KAC)`.  Applying such inequalities to the
two pinned matrices in (9) separately cannot compare the free positive
scalars `kappa_B` and `kappa_D`.

The same circularity appears in semipositivity form.  The feedback block
has a positive supersolution `(t,1)^T` exactly when

\[
                    r^3\kappa_B\leq t\leq\kappa_D^{-1}.     \tag{20}
\]

Producing such a `t` from the cross-rule dynamics would prove the theorem;
generic matrix theory does not produce it.

## 4. Why the standard determinant cones do not survive the gauge

### 4.1 Before the gauge

At `R_hyb`, one has `3/2<r<2`.  On every module of order at least three,
the density mark is negative on singleton states and positive on
sufficiently high ranks.  In particular, on an order-three module

\[
 g_1={3-2r\over3r}<0,
 \qquad
 g_2={3-r\over3r}>0.                                \tag{21}
\]

Thus `diag(g)` is indefinite, and the reward columns in (11) contain both
signs.  The matrix (11) is not a `Z`-matrix, and positive diagonal
similarity cannot alter those signs.

The classical Alexandrov--Fenchel inequality for mixed discriminants
requires Hermitian positive-semidefinite matrices.  Here the directed
Laplacians are generally nonsymmetric and the mark `diag(g)` is indefinite.
Consequently its hypotheses do not apply to

\[
 \mathcal T_Q(g)
 =nD(L,\ldots,L,\operatorname{diag}(g)),             \tag{22}
\]

where `D` is the conventionally normalized mixed discriminant.  The
rank-one gauge (9) is a right equivalence, not a positive congruence, and
does not transport an Alexandrov--Fenchel cone.

### 4.2 After the gauge

After the gauge, each separate signed functional is indeed a determinant
of a pinned `M`-matrix.  But their proposed comparison has become exactly
the two-by-two feedback determinant (17).  There is no remaining mixed
discriminant inequality to invoke: its positivity is the statement to be
proved.

Stable-polynomial coefficient inequalities encounter a separate precise
failure.  The Poisson identity preserves only the coefficient linear in
the diagonal mark.  It is not an automorphism of the whole diagonal
determinant polynomial.

Take the symmetric two-state Laplacian

\[
 L=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}           \tag{23}
\]

and use the actual singleton/doubleton rank marks (21), with state one as
the root.  The active root residue is

\[
 \kappa=g_1+g_2={2-r\over r}>0.                     \tag{24}
\]

Nevertheless

\[
 \det\{L+t\operatorname{diag}(g_1,g_2)\}
 =t(g_1+g_2)+t^2g_1g_2,                             \tag{25}
\]

while the Poisson-gauged mark `(kappa,0)` gives

\[
 \det\{L+t\operatorname{diag}(\kappa,0)\}=t\kappa. \tag{26}
\]

The linear coefficients agree, as they must, but the quadratic
coefficient in (25) is strictly negative and disappears in (26).  Hence a
stable-polynomial or complete-log-concavity inequality cannot be applied
after silently replacing `g` by its Poisson gauge: the higher polynomial
data have changed.  Before replacement, the signed direction lies outside
the nonnegative directional cone used by those coefficient inequalities.

## 5. Exact conclusion

The signed Kac diagonal has the single determinant form (13).  The exact
Poisson gauge (9) is enough to make each separate signed factor positive,
but it exposes rather than resolves the cross-rule content: the remaining
matrix is the two-vertex positive-feedback loop (17).

Therefore the canonical AF/Hadamard--Fischer/generic `M`-matrix/stable-
polynomial architecture stops for a precise reason, not for lack of a
larger block ansatz.  A successful determinant proof must add genuinely
physical cross-rule information which proves that the feedback gain

\[
                         r^3\kappa_B\kappa_D
\]

is at most one.  Equivalently, it must construct the supersolution in
(20), or give a signed paired-forest expansion of (13).  Neither is proved
here.

## 6. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_kac_mixed_cofactor/verify_mixed_cofactor_feedback.py
```

The replay verifies (7)--(9), the bordered determinant (11)--(13), both
Poisson column operations, the signed block similarity, the exact
`M`-matrix feedback criterion on an active rational instance, and the
two-state failure of higher-coefficient gauge invariance.  It checks
identities only and does not assert `(D-KAC)` for physical duals.
