# Independent proof audit for the frozen v1 construction

This document audits the non-computational implications behind clean-room
checks 1–17 and gives independent proofs of checklist items 18–20.  It was
written against only the frozen network data and theorem statement.  It does
not use the proof text or certificates from the original verifier.

Run the companion exact verifier from the Version 1.0 release directory with

```text
./reproduce.sh
```

## Logical certificates behind checks 9, 11, and 13

For check 9, quotienting by the linear polynomial

\[
L=z-x-y+1
\]

eliminates one variable.  The remaining homogeneous projective conic has
symmetric matrix

\[
\begin{pmatrix}7&-1&-8\\-1&7&-8\\-8&-8&16\end{pmatrix}
\]

and determinant \(-256\).  It is therefore nonsingular over the algebraic
closure.  A reducible projective conic is the union of two lines (possibly the
same line), and is singular at their intersection.  Thus this conic is
absolutely irreducible.  The quotient by \((L,Q)\) is a domain of dimension
one, so \((L,Q)\) is prime of height two.

For check 11, on \(L=0\) put \(a=x-y\) and \(s=x+y=z+1\).  Exact reduction
gives

\[
4a^2+3z^2-10z+3=0
\]

and hence

\[
(3z-1)(3-z)=4a^2\ge0.
\]

It follows that \(1/3\le z\le3\).  Also

\[
s^2-4a^2=4(z-1)^2\ge0.
\]

Since \(s=z+1\ge4/3\), this implies \(|a|\le s/2\), and therefore

\[
x=\frac{s+a}{2}\ge\frac{s}{4}\ge\frac13,
\qquad
y=\frac{s-a}{2}\ge\frac{s}{4}\ge\frac13.
\]

Finally,

\[
4a^2+3\left(z-\frac53\right)^2=\frac{16}{3}
\]

is a bounded ellipse, and \((x,y,z)\) is an affine function of \((a,z)\).
Thus every real conic point is strictly positive and the real locus is
compact.

For check 13, use the following field-extension lemma.

**Lemma.** Let \(k\subseteq K\) be fields with \(k\) of characteristic zero,
and let
\(f_1,\ldots,f_r\in k[X_1,\ldots,X_n]\).  If their gcd over \(k\) is one,
then their gcd over \(K\) is one.

**Proof.** It is enough to pass first to an algebraic closure \(\bar k\): any
factorization of a polynomial over a larger algebraically closed extension
already exists over \(\bar k\), since a normalized factorization is a finite
system of polynomial coefficient equations over \(\bar k\).  If an
irreducible \(h\in\bar k[X]\) divided every \(f_i\), every Galois conjugate of
\(h\) would do the same.  The product of its distinct conjugates, with the
common multiplicity occurring in the rational polynomials, descends up to a
unit to a nonconstant polynomial in \(k[X]\) dividing every \(f_i\), a
contradiction.  Hence no common factor appears after extension.  Applying the
lemma to \(k=\mathbb Q\) and \(K=\mathbb R,\mathbb C\) proves the claim. ∎

## Checks 15–17: independently recomputed decomposition

The clean-room verifier does not import or copy the original large
Gröbner-basis factors.  It obtains the residual ideal by the saturation

\[
\mathfrak q=K:D^\infty
=\bigl(K+(1-uD)\bigr)\cap\mathbb Q[x,y,z],
\]

where \(D\) is derived by eliminating \(x\) between \(L\) and \(Q\).  It then
uses a second auxiliary variable to recompute

\[
\mathfrak p\cap\mathfrak q
=\bigl(v\mathfrak p+(1-v)\mathfrak q\bigr)
  \cap\mathbb Q[x,y,z].
\]

The unique reduced lexicographic basis of this intersection agrees term for
term with the independently computed basis of \(K=(F_1,F_2,F_3)\).  The
residual basis is triangular,

\[
x+r_x(z),\qquad y+r_y(z),\qquad R(z),
\]

with irreducible, squarefree \(R\in\mathbb Q[z]\) of degree fifteen.  Thus
\(\mathfrak q\) is maximal over \(\mathbb Q\), and after algebraic closure it
is fifteen distinct reduced points.  A direct Gröbner-basis computation gives
\(\mathfrak p+\mathfrak q=(1)\), so these points are disjoint from the conic.
The equality

\[
K=\mathfrak p\cap\mathfrak q
\]

then proves that \(K\) is radical and that the conic prime is a minimal
component.

## Check 18: three species are necessary

For one species, a positive-dimensional positive equilibrium set contains an
interval.  A univariate polynomial vanishing on an interval is zero, so the
vector field is the excluded zero field.

Now consider two species.  If the stoichiometric rank is zero, the field is
zero.  If it is one, choose a nonzero rational vector \(v\) spanning the
stoichiometric subspace.  Every reaction vector is a rational scalar multiple
of \(v\), hence

\[
F=v f
\]

for one \(f\in\mathbb Q[x,y]\).  A nonzero constant \(f\) has no equilibrium,
whereas \(f=0\) gives the zero field.  In every remaining case \(f\) is a
nonconstant common factor of all nonzero coordinate polynomials.

If the stoichiometric rank is two, the positive compatibility class is the
whole positive orthant.  A positive-dimensional algebraic or semialgebraic
common-zero set implies

\[
\dim \mathbb Q[x,y]/(F_1,F_2)\ge1;
\]

semialgebraic dimension cannot exceed the Krull dimension of its Zariski
closure, and dimension is preserved by extending the coefficient field from
\(\mathbb Q\) to \(\mathbb R\).  If the ideal is zero, the field is zero.
Otherwise a minimal prime of dimension at least one has height exactly one.
Since \(\mathbb Q[x,y]\) is a UFD, this prime is generated by a nonconstant
irreducible polynomial dividing both coordinates.  Thus no one- or
two-species system satisfies the target, while the verified construction uses
three species.

**Audit result for 18: PASS.** The argument uses the stipulated algebraic or
semialgebraic positive dimension; it does not purport to cover arbitrary
non-semialgebraic fractal sets.

## Check 19: one-linkage rank-two obstruction

Let a three-species network have one linkage class and stoichiometric rank
two.  Choose a primitive integral vector \(w\) spanning \(S^\perp\).  For
each reaction \(y\to y'\),

\[
w\mathbin\cdot(y'-y)=0.
\]

Connectivity of the undirected complex graph therefore makes \(w\cdot y=d\)
constant on all complexes.  For \(\lambda>0\), define

\[
T_\lambda(x)_i=\lambda^{w_i}x_i.
\]

Every source monomial is multiplied by \(\lambda^d\), so

\[
F(T_\lambda x)=\lambda^dF(x).
\]

The scaling action preserves the positive equilibrium set.  At a positive
point \(p\), its infinitesimal direction is

\[
u(p)=(w_1p_1,w_2p_2,w_3p_3).
\]

A compatibility class has tangent space \(S=w^\perp\), while

\[
w\cdot u(p)=\sum_iw_i^2p_i>0.
\]

Thus the orbit direction is transverse to the class.  Choose a smooth
one-dimensional stratum of the stipulated algebraic or semialgebraic
equilibrium continuum.  Acting on this stratum gives a two-dimensional
semialgebraic subset of the ambient equilibrium variety.  Therefore

\[
\dim\mathbb Q[x,y,z]/(F_1,F_2,F_3)\ge2.
\]

If the dimension is three, the steady ideal is zero.  Otherwise a minimal
prime of dimension two has height one and, by factoriality of
\(\mathbb Q[x,y,z]\), is generated by a nonconstant irreducible divisor of
every coordinate.  Hence rank two forces either the zero field or a common
factor.  Rank one already has the form \(F=vf\), so under one linkage class a
three-species gcd-one example must have full rank.

**Audit result for 19: PASS.** One linkage class and positive concentrations
are essential: they give, respectively, the common weighted degree and the
strict transversality inequality.

## Check 20: four complexes cannot work

Assume one linkage class, weak reversibility, four distinct complexes, and
stoichiometric rank three.  Let \(Y\) be the \(3\times4\) complex matrix and
let \(A_\kappa\) be the kinetic matrix, with column sums zero, so that

\[
F(x)=Y A_\kappa\Psi(x),
\qquad
\Psi_i(x)=x^{y_i}.
\]

Weak reversibility plus one linkage class makes the directed complex graph
strongly connected.  The kinetic matrix has rank three.  One direct proof is
to apply the maximum principle to its transpose: if
\(A_\kappa^Th=0\), choose an index where \(h\) is maximal.  The corresponding
equation is a positive weighted sum of terms \(h_j-h_i\le0\); all outgoing
neighbors have the same value, and strong connectivity propagates that value
to every vertex.  Thus \(\ker A_\kappa^T=\operatorname{span}(1,1,1,1)\), so
\(\operatorname{rank}A_\kappa=3\) and
\(\operatorname{im}A_\kappa=1^\perp\).

The map \(Y:1^\perp\to S\) is onto because the images of incidence vectors
are the reaction differences.  Both spaces have dimension three, so it is an
isomorphism.  At a positive equilibrium,

\[
YA_\kappa\Psi(x)=0
\]

therefore implies \(A_\kappa\Psi(x)=0\): every positive equilibrium is
complex-balanced.  Since \(\ker A_\kappa\) is one-dimensional, two positive
equilibria \(x,x'\) have proportional monomial vectors.  Consequently, for
every pair of complexes,

\[
(y_i-y_j)\cdot(\log x-\log x')=0.
\]

The complex differences span \(S=\mathbb R^3\), so
\(\log x=\log x'\), hence \(x=x'\).  There is at most one positive
equilibrium and no continuum.  At least five complexes are necessary.

**Audit result for 20: PASS.** Weak reversibility is essential to the stated
rank argument.  This is a lower bound only; it does not assert that five
complexes suffice.

## Final audit disposition

All checklist items 1–20 pass under their stated hypotheses.  No logical gap
was found.  The only scope qualifications are those explicitly noted above:
the continua are algebraic or semialgebraic, the rank-two obstruction assumes
one linkage class, and the four-complex lower bound assumes weak reversibility
and full stoichiometric rank.
