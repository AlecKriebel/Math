# The two remaining two-block leg types in dimension six

**Date:** 2026-07-29
**Status:** PROVED common-leg obstruction and exact assumption audit; no
unrestricted no-go for either one-sided algebra type
**Scope:** arbitrary exceptional projections in base dimension six

## 1. Conclusion

Write
\[
\mathcal C_L(P)=\{x\in M_6:[x\otimes I,P]=0\},\qquad
\mathcal C_R(P)=\{x\in M_6:[I\otimes x,P]=0\}.
\]
The two nontrivial two-block types left by the one-leg arithmetic audit are
\[
\mathcal A_{4+2}=\mathbb C I_4\oplus\mathbb C I_2
\tag{1}
\]
and
\[
\mathcal A_{2,2;2}
=(M_2(\mathbb C)\otimes I_2)\oplus\mathbb C I_2.
\tag{2}
\]

There is a clean exact obstruction, stronger than the earlier
three-color shared-atom statement:

> **Trivial-intersection theorem.**  Every dimension-six exceptional
> projection satisfies
> \[
> \boxed{\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb C I_6.}
> \tag{3}
> \]

Consequently, neither (1) nor (2) can occur in an aligned form on the two
legs.  In particular, an exceptional solution with a non-scalar leg
commutant cannot be invariant under tensor flip.

This does **not** exclude either type as a one-sided leg commutant.  Exact
permutation models below show that two copies of either algebra can be put
in relative position with scalar intersection.  Exact abstract
three-strand models also satisfy every endpoint rank and cubic-block
condition for all four ordered pairs of (1)--(2).  The missing condition
is still the existence of one two-site projection whose two shifted copies
realize that abstract pair.

## 2. No rank-two projection can reduce both legs

### Theorem 2.1

Let \(P\in\operatorname{End}(V\otimes V)\), \(\dim V=6\), be an
exceptional projection, and put \(H=I-2P\).  There is no rank-two
projection
\[
z\in\mathcal C_L(P)\cap\mathcal C_R(P).
\tag{4}
\]

### Proof

Assume that (4) holds and put \(W=zV\), so \(\dim W=2\).  Since \(z\)
reduces both tensor legs of \(H\), the cell
\[
K=H\big|_{W\otimes W}
\tag{5}
\]
is a Hermitian involution and \(W^{\otimes3}\) is invariant under its two
adjacent copies.  Hence
\[
K_{12}K_{23}K_{12}-K_{23}K_{12}K_{23}
=\frac13(K_{12}-K_{23}).
\tag{6}
\]

Let \(Q=(I-K)/2\), with rank \(r\in\{0,1,2,3,4\}\).

- If \(r=1\), write
  \(Q=|\operatorname{vec}S\rangle\langle\operatorname{vec}S|\), normalized
  by \(\operatorname{Tr}(S^*S)=1\).  Relation (6) forces the two
  eigenvalues of the compression of \(Q_{23}\) to
  \(\operatorname{ran}Q_{12}\) to lie in \(\{1,1/3\}\), so its determinant
  is at least \(1/9\).  Direct vectorization gives determinant
  \(|\det S|^4\), while the arithmetic--geometric mean inequality gives
  \[
  |\det S|^4\leq\frac1{16}<\frac19.
  \]
  Thus \(r=1\) is impossible.
- Complementation gives the same contradiction for \(r=3\).
- The case \(r=2\) is precisely the established empty exceptional class
  in base dimension two.

It follows that \(r=0\) or \(4\), and therefore
\[
K=\varepsilon I_{W\otimes W},
\qquad \varepsilon\in\{+1,-1\}.
\tag{7}
\]

Now restrict the three-site cubic relation to
\[
W\otimes W\otimes V.
\]
This subspace is invariant: the first copy of \(H\) is (7), and the second
copy preserves \(W\otimes V\) because \(z\in\mathcal C_L(P)\).  On this
subspace put
\[
X=\varepsilon I,\qquad
Y=I_W\otimes H\big|_{W\otimes V}.
\]
Both are involutions.  Hence
\[
XYX-YXY=Y-X.
\]
Comparison with the cubic relation gives
\[
Y-X=\frac13(X-Y),
\]
so \(Y=X\).  Thus
\[
H\big|_{W\otimes V}=\varepsilon I_{W\otimes V}.
\tag{8}
\]

Automatic standardness says \(\operatorname{Tr}_2H=0\).  Restricting this
operator identity to \(W\) and using (8) instead gives
\[
0=z(\operatorname{Tr}_2H)z
=\operatorname{Tr}_V(H|_{W\otimes V})
=6\varepsilon I_W,
\]
a contradiction. \(\square\)

### Corollary 2.2

For every dimension-six exceptional projection,
\[
\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb C I_6.
\]

Indeed, a non-scalar finite-dimensional \(C^*\)-subalgebra of \(M_6\)
contains a nontrivial projection.  The controlled-leg divisibility theorem
forces every such projection in either leg commutant to have even rank.
Its rank is therefore \(2\) or \(4\); in the latter case its complement
has rank \(2\).  Either possibility contradicts Theorem 2.1.

### Corollary 2.3

If \(FPF=P\), where \(F\) is tensor flip, then
\[
\mathcal C_L(P)=\mathcal C_R(P)=\mathbb C I_6.
\tag{9}
\]
Thus neither (1) nor (2) survives a flip-symmetric ansatz.

## 3. Exact normal forms for the one-sided branches

Theorem 2.1 must not be turned into an unrestricted no-go by silently
identifying the two leg algebras.

For (1), write \(V=U\oplus W\), with \(\dim U=4\), \(\dim W=2\).
Commutation on the left gives
\[
P=Q_U\oplus Q_W
\quad\text{on}\quad
(U\otimes V)\oplus(W\otimes V).
\tag{10}
\]
Automatic standardness gives exactly
\[
\operatorname{Tr}_VQ_U=3I_U,\qquad
\operatorname{Tr}_VQ_W=3I_W,
\tag{11}
\]
\[
\operatorname{Tr}_UQ_U+\operatorname{Tr}_WQ_W=3I_V.
\tag{12}
\]
In particular,
\[
\operatorname{rank}Q_U=12,\qquad \operatorname{rank}Q_W=6.
\tag{13}
\]
Neither block is a smaller ordinary Yang--Baxter solution: on the middle
site, \(P_{12}\) need not preserve \(U\) or \(W\), because (10) controls
only the *left* tensor leg.

For (2), write
\[
V=(A\otimes B)\oplus W,\qquad
\dim A=\dim B=\dim W=2.
\]
Then
\[
P=(I_A\otimes Q)\oplus S,
\tag{14}
\]
where \(Q,S\) are rank-six projections on \(B\otimes V\) and
\(W\otimes V\), respectively, and
\[
\operatorname{Tr}_VQ=3I_B,\qquad
\operatorname{Tr}_VS=3I_W,
\tag{15}
\]
\[
2\operatorname{Tr}_BQ+\operatorname{Tr}_WS=3I_V.
\tag{16}
\]
If \(X=\operatorname{Tr}_BQ\), positivity of \(S\) and \(I-S\) yields the
nontrivial but compatible interval
\[
\boxed{\frac12I_V\leq X\leq\frac32I_V,\qquad
\operatorname{Tr}X=6.}
\tag{17}
\]

Writing the reflection \(I-2Q\) in the Pauli basis of \(B\) gives
\[
I\otimes B_0+X\otimes B_1+Y\otimes B_2+Z\otimes B_3.
\tag{18}
\]
Unlike the excluded \(M_3\otimes I_2\) factor branch, (16) does not force
\(B_0=0\): its contribution is cancelled by the \(W\)-block.  The
involutivity equations are
\[
B_0^2+B_1^2+B_2^2+B_3^2=I,
\tag{19}
\]
\[
\{B_0,B_1\}+i[B_2,B_3]=0
\tag{20}
\]
and the two cyclic analogues.  They do not force the \(B_j\)'s to commute.
Thus the Pauli argument proving the full-factor no-go does not extend to
(2).

## 4. Relative position is genuine freedom

The following exact coordinate models show that scalar intersection is
not forbidden by the abstract algebra types.

Let \(\mathcal A_{4+2}\) be generated by the rank-two coordinate
projection onto \(\operatorname{span}\{e_5,e_6\}\).  If \(U\) is the
permutation with one-line notation
\[
(0,1,2,4,3,5),
\tag{21}
\]
then
\[
\mathcal A_{4+2}\cap U\mathcal A_{4+2}U^*
=\mathbb C I_6.
\tag{22}
\]
The same permutation gives scalar intersection between
\(\mathcal A_{4+2}\) and a conjugate of \(\mathcal A_{2,2;2}\).

In the coordinate realization
\[
\mathcal A_{2,2;2}
=\{(x\otimes I_2)\oplus\lambda I_2:x\in M_2,\lambda\in\mathbb C\},
\]
the permutation
\[
(0,2,1,4,3,5)
\tag{23}
\]
gives
\[
\mathcal A_{2,2;2}\cap
U\mathcal A_{2,2;2}U^*
=\mathbb C I_6.
\tag{24}
\]
Therefore Theorem 2.1 rules out alignment, not arbitrary relative
position.

There is also no hidden three-strand denominator.  Encode a simple
one-leg summand by
\[
M_m\otimes I_{2a}.
\]
For an ordered pair of endpoint summands \(a,b\), take a
\(24ab\)-dimensional two-projection block with
\[
\operatorname{rank}p=\operatorname{rank}q=12ab,
\]
\[
\dim(\operatorname{ran}p\cap\operatorname{ran}q)=3ab,
\]
\[
\text{\(9ab\) generic \(1/3\)-angle blocks,}
\]
and common-zero dimension \(3ab\).  It satisfies
\[
pqp-qpq=\frac13(p-q).
\tag{25}
\]
Tensoring this block with the endpoint matrix multiplicities gives exact
abstract \(216\)-dimensional models for all four ordered pairs of
(1)--(2), with total ranks \(108\), common-one and common-zero dimensions
\(27\), and overlap trace \(54\).

These are deliberately only abstract representations of the
three-strand two-projection algebra.  They need not have
\[
p=P\otimes I_6,\qquad q=I_6\otimes P
\]
for one common \(P\).  Their role is to prove that endpoint multiplicity
and the new trivial-intersection theorem do not by themselves exclude
either one-sided two-block type.

## 5. Exact status of the requested branches

The exact conclusions are:

1. A shared rank-two reducing subspace is impossible, without assuming
   three rank-two color decompositions.
2. Hence the two one-leg commutants of every \(d=6\) solution intersect
   only in scalars.
3. The types (1) and (2) are excluded in aligned and flip-symmetric
   ansätze.
4. Neither type is excluded as a one-sided commutant in arbitrary relative
   position.
5. The full-factor Pauli proof cannot be reused for (2), because its
   scalar Pauli coefficient is not forced to vanish.
6. Exact relative-algebra and abstract cubic-block models show precisely
   why the present invariants stop short of a no-go.

The remaining problem is spatial: use the equality of the two shifted
copies of one \(P\), rather than only their abstract Hecke block
decomposition, to rule out or construct a transverse pair.

## 6. Exact replay

Run:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_d6_two_block_leg_types.py
```

The verifier checks the determinant gap, scalar-cell propagation, exact
scalar intersections (22)--(24), every \(24ab\) abstract cubic block, and
the aggregate dimension/rank/overlap data for all four ordered pairs of
the two algebra types.
