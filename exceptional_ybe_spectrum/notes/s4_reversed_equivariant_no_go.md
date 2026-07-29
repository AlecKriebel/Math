# Exact exclusion of the reversed \(S_4\)-equivariant heterogeneous branch

**Date:** 2026-07-29 PDT

**Status:** `PROVED` (finite exact character calculation and exact
coordinate-row certificate)

**Scope:** the heterogeneous spectator construction with
\[
 A=V_3,\qquad B=V_2,
\]
where \(V_3\) is the standard three-dimensional representation of
\(S_4\), \(V_2\) is the two-dimensional irreducible representation, and
the active operator on \(A\otimes B\otimes A\) commutes with the
diagonal \(S_4\)-action.

This is the reversed factor ordering relative to the previously excluded
\(V_2\otimes V_3\otimes V_2\) branch.  The two branches have different
dimensions, commutants, and overlap spaces, so the earlier result did not
imply the theorem below.

This note does **not** exclude an arbitrary \(d=6\) Yang--Baxter matrix,
an arbitrary heterogeneous operator, or an operator with another
symmetry.

## 1. Theorem

Let
\[
 H\in\operatorname{End}(A\otimes B\otimes A)
\]
be a trace-zero Hermitian involution commuting with diagonal \(S_4\).
On
\[
 A\otimes B\otimes A\otimes B\otimes A
\]
put
\[
 H_1=H\otimes I_{B\otimes A},\qquad
 H_2=I_{A\otimes B}\otimes H.
\]

> **Theorem.**  No such \(H\) satisfies
> \[
> H_1H_2H_1-H_2H_1H_2=\frac13(H_1-H_2).
> \]

Thus the complete diagonal-\(S_4\)-equivariant, half-rank
\((3,2,3)\) heterogeneous branch is empty.

## 2. Exact module decomposition

Use the conjugacy-class order
\[
 1,\quad(12),\quad(12)(34),\quad(123),\quad(1234),
\]
whose class sizes are \(1,6,3,8,6\).  In the irrep order
\[
 1,\quad\epsilon,\quad V_2,\quad V_3,\quad V_3',
\]
the character table is
\[
\begin{array}{c|rrrrr}
 &1&(12)&(12)(34)&(123)&(1234)\\ \hline
1       &1& 1& 1& 1& 1\\
\epsilon&1&-1& 1& 1&-1\\
V_2     &2& 0& 2&-1& 0\\
V_3     &3& 1&-1& 0&-1\\
V_3'    &3&-1&-1& 0& 1
\end{array}
\]
and
\[
 \chi_{A\otimes B\otimes A}
 =\chi_{V_3}^2\chi_{V_2}
 =(18,0,2,0,0).
\]
Taking exact character inner products gives
\[
 A\otimes B\otimes A
 \cong
 1\oplus\epsilon\oplus2V_2\oplus2V_3\oplus2V_3'.
 \tag{2.1}
\]
Consequently
\[
 \operatorname{End}_{S_4}(A\otimes B\otimes A)
 \cong
 \mathbb C\oplus\mathbb C
 \oplus M_2(\mathbb C)^{\oplus3},
 \tag{2.2}
\]
of complex dimension \(14\).  This is the full equivariant commutant,
not a smaller ansatz.

For an exact matrix realization, take the rational sum-zero bases
\[
\begin{aligned}
V_3&=\operatorname{span}
\{e_1-e_4,e_2-e_4,e_3-e_4\},\\
V_2&=\operatorname{span}
\{f_1-f_3,f_2-f_3\},
\end{aligned}
\]
where \(S_4\) acts on the four letters and on the three perfect matchings.
The product-basis Gram matrix is
\[
 G=G_3\otimes G_2\otimes G_3.
\]
Character sums construct the five central projectors, of ranks
\[
 1,\quad1,\quad4,\quad6,\quad6.
 \tag{2.3}
\]

There is also a canonical exact way to split each multiplicity-two
summand.  Couple the two outer \(V_3\) factors first:
\[
 V_3\otimes V_3\cong1\oplus V_2\oplus V_3\oplus V_3'.
\]
The outer \(1\)-channel splits the two copies of \(V_2\), while the
outer \(V_3\)-channel splits the two copies of both \(V_3\) and \(V_3'\).
Group-averaged intertwiners between each pair of copies then give exact
metric-Hermitian Pauli triples
\[
 (X_j,Y_j,Z_j),\qquad j=2,3,3',
 \tag{2.4}
\]
supported on the corresponding central projectors.  They obey
\[
 X_j^2=Y_j^2=Z_j^2=P_j,\qquad
 X_jY_j=iZ_j,
 \tag{2.5}
\]
and different triples have orthogonal central support.  The verifier
constructs these matrices from the group action and checks (2.3)--(2.5)
exactly; no numerical Clebsch--Gordan coefficients are used.

## 3. Complete list of balanced signatures

Let \(r_1,r_\epsilon\in\{0,1\}\) denote the ranks selected in the two
one-dimensional summands, and let
\[
 k_2,k_3,k_{3'}\in\{0,1,2\}
\]
denote the selected multiplicity-space ranks in the three
multiplicity-two summands.  A rank-nine projection has
\[
 r_1+r_\epsilon+2k_2+3k_3+3k_{3'}=9.
 \tag{3.1}
\]
The ten and only ten solutions are
\[
\begin{array}{c|ccccc}
 &r_1&r_\epsilon&k_2&k_3&k_{3'}\\ \hline
1&0&0&0&1&2\\
2&0&0&0&2&1\\
3&0&1&1&0&2\\
4&0&1&1&1&1\\
5&0&1&1&2&0\\
6&1&0&1&0&2\\
7&1&0&1&1&1\\
8&1&0&1&2&0\\
9&1&1&2&0&1\\
10&1&1&2&1&0
\end{array}
 \tag{3.2}
\]
Complementation sends
\[
 (r_1,r_\epsilon,k_2,k_3,k_{3'})
 \longmapsto
 (1-r_1,1-r_\epsilon,2-k_2,2-k_3,2-k_{3'})
 \tag{3.3}
\]
and \(H\mapsto-H\).  Since the shifted cubic residual changes sign
under \(H\mapsto-H\), it is enough to exclude the first five rows.

For \(k_j=0\) or \(2\), \(H\) is respectively \(-P_j\) or \(+P_j\) on
that central summand.  For \(k_j=1\), every Hermitian involution on its
multiplicity space is exactly
\[
 x_jX_j+y_jY_j+z_jZ_j,\qquad
 x_j^2+y_j^2+z_j^2=1,
 \tag{3.4}
\]
with real coefficients.  Equations (3.2)--(3.4) therefore parametrize
every balanced equivariant Hermitian involution.

## 4. Finite exact cubic certificate

For each of the five complement representatives, substitute the full
parametrization above into
\[
 D(H)=H_1H_2H_1-H_2H_1H_2-\frac13(H_1-H_2).
 \tag{4.1}
\]
In the rational product basis, multiplying every fixed central term and
every Pauli generator by \(24\) puts all entries in
\[
 \mathbb Z[\sqrt3,i].
\]
Thus every real-rational component of a matrix entry of \(24^3D(H)\)
is an integer polynomial of total degree at most three.

If one multiplicity block is noncentral, the full monomial space in its
three real coordinates has dimension
\[
 \binom{3+3}{3}=20.
\]
If all three blocks are noncentral, the corresponding nine-variable
monomial space has dimension
\[
 \binom{9+3}{3}=220.
\]

The exact certificate selects the following numbers of real-rational
matrix coordinates:
\[
\begin{array}{c|c|c}
(r_1,r_\epsilon,k_2,k_3,k_{3'})
&\text{selected coordinates}&\text{monomial columns}\\ \hline
(0,0,0,1,2)&8&20\\
(0,0,0,2,1)&8&20\\
(0,1,1,0,2)&10&20\\
(0,1,1,1,1)&59&220\\
(0,1,1,2,0)&10&20
\end{array}
 \tag{4.2}
\]
For each row of (4.2), form the integer matrix whose rows are the
coefficient vectors of those selected coordinate polynomials in the
ordered monomial basis.  Exact rational row reduction gives
\[
 (1,0,\ldots,0)
 \tag{4.3}
\]
in its row space, with the first column corresponding to the constant
monomial.

Equation (4.3) is a particularly short inconsistency certificate:
an exact rational linear combination of the selected entries of
\(24^3D(H)\) is the constant polynomial \(1\).  Hence those entries
cannot vanish simultaneously for any complex parameter values.  In
particular they cannot vanish on the real unit spheres (3.4).

The coordinate lists in the verifier are the replayable certificate.
The largest list has only \(59\) coordinates.  The program does not
infer nonexistence from optimizer residuals or floating-point rank; it
reconstructs all coefficient rows in
\(\mathbb Z[\sqrt3,i]\) and performs the final row reductions over
\(\mathbb Q\).

Together with complementation, this excludes all ten cases in (3.2) and
proves the theorem.

## 5. Replay and limitation

Run:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_s4_reversed_equivariant_no_go.py
```

The verifier checks:

1. the rational \(S_4\) actions and Gram metric;
2. the character projectors and decomposition (2.1);
3. the full \(14\)-dimensional commutant and three exact Pauli triples;
4. complete enumeration of the ten balanced signatures;
5. complement pairing;
6. the five exact coordinate-row certificates (4.2)--(4.3).

This closes the complete diagonal-\(S_4\)-equivariant reversed
\((3,2,3)\) branch.  It gives no obstruction to a genuinely
non-\(S_4\)-equivariant \(18\times18\) heterogeneous operator and hence
does not settle arbitrary local dimension six.
