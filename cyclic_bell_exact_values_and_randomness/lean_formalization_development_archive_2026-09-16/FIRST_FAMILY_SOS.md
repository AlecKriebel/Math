# An exact d=4 polynomial SOS for the first family

This is an alternative proof route written for the companion. It is not a
formalization of the manuscript's all-dimensional polar proof, a manuscript
revision, or a bibliographic novelty claim. The exact identities below passed
supplementary symbolic checks; their Lean scripts remain uncompiled.

## Constants

Set

\[
k=\sqrt2,\quad s=\sin(\pi/8),\quad c=\cos(\pi/8),\quad
\alpha=(c+s)/2,\quad\beta=(s-c)/2.
\]

The source proves, from the actual trigonometric constants,

\[
s>0,\ k>0,\quad s^2=(2-k)/4,\ c^2=(2+k)/4,\ sc=k/4,
\quad c=(1+k)s,
\]

\[
\alpha=(2+k)s/2,\quad\beta=-ks/2,\quad k\alpha=c,\quad k\beta=-s,
\quad 4(2+k)s=2/s=:M_4.
\]

See `ScalarData.lean`. The upper-bound modules import these scalar facts but do
not import the explicit witness, target projectors, or target probability table.

## Operator identity

Let A and U be arbitrary unitaries on a finite coordinate space. Let B_y,
0≤y<4, be unitaries satisfying U B_y=B_y U. There is no assumed finite order,
no equality-root spectral restriction, and no same-party commutation.
Put T_y=i^y U, and define the operator polynomials

\[
P(T)=sI+2\alpha T+sT^2=s\bigl[I+(2+k)T+T^2\bigr],
\]
\[
Q(T)=\beta I+\alpha T+\alpha T^2+\beta T^3
=\frac{s}{2}\bigl[-kI+(2+k)T+(2+k)T^2-kT^3\bigr].
\]

These polynomial names P,Q are distinct from the manuscript's polar residuals.
Define

\[
F_y=(I+T_y)A^\dagger-P(T_y)B_y,\qquad
G_y=T_yA^\dagger-Q(T_y)B_y.
\]

Then

\[
\boxed{M_4 I-\sum_{y=0}^3\operatorname{Re}[A(I+T_y)B_y]
=\frac{s}{2}\sum_{y=0}^3(F_y^\dagger F_y+kG_y^\dagger G_y).}
\]

Here Re is the Hermitian part (T+T†)/2. The principal source declaration is
`CyclicBell.FirstSOS.reduced_gap_identity`.

## Why the expansion works

The cross term is fixed by the exact identity

\[
s\bigl[(I+T)^\dagger P(T)+kT^\dagger Q(T)\bigr]=I+T
\quad(T^\dagger T=I).
\]

The coefficients of T† and T² are s(s+kβ)=0. The coefficients of I and T are
s(s+2α+kα)=1. This is `cross_factorization`, not an assumed interpolating
identity or a certificate imported from Python.

Four-point Fourier orthogonality gives

\[
\sum_y(I+T_y)^\dagger(I+T_y)=8I,\qquad
\sum_y T_y^\dagger T_y=4I,
\]

\[
\sum_yP(T_y)^\dagger P(T_y)=8I,\qquad
\sum_yQ(T_y)^\dagger Q(T_y)=4I.
\]

For P the sum of squared coefficients is 2; for Q it is 1. Matrix-valued
Parseval is proved without commuting the coefficient matrices. Commutation of
U with B_y implies commutation of both polynomials with B_y. Consequently,
B_y cancels from each right energy term. A cancels from the summed left energy
terms by unitarity. Each diagonal side contributes
s(8+4k)I=M_4 I; the cross terms contribute twice the Hermitian Bell operator.
Dividing the expansion by two gives the displayed identity.

The augmentation adds the separate unitary identity

\[
I-\operatorname{Re}(AB_4)
=\tfrac12(I-AB_4)^\dagger(I-AB_4).
\]

No commutation of A and B_4 is required for that identity. In the actual tensor
model all cross-party commutations hold automatically.

## Physical interpretation and arbitrary mixed states

For an arbitrary `Strategy 2 nA nB`, lift the original PVM-encoded A₀,A₁ and
Bob observables to the joint tensor space, and take
A=A₀⊗I and U=(A₀⊗I)†(A₁⊗I). `PhysicalBounds.lean` derives unitarity and the
required commutation from PVM axioms and tensor entries. It does not specialize
the Hilbert dimension to four.

For any positive trace-one density ρ, the Gram term has nonnegative expectation:

\[
\operatorname{Tr}(\rho T^\dagger T)
=\operatorname{Tr}(T\rho T^\dagger)\ge0.
\]

This direct trace argument does not require ρ to be pure or to commute with T.
It avoids a missing purification or spectral-decomposition bridge. Together
with s,k>0 it proves the intended finite-dimensional bound

\[
\langle\overline{\mathcal I}_4\rangle\le 2/\sin(\pi/8)+1.
\]

The explicit witness and its attainment are a separate chain in
`Witness.lean` and `Attainment.lean`. The latter obtains reduced value 8α=M₄
from the first two Fourier modes, and aligned value 1.

## Supplementary checks and limits

`first_sos_preflight.py` expands the identity using exact cyclotomic coefficients
and two free party algebras. `partial_commutation_preflight.py` uses a different
word reduction implementation with only U/B₀,…,B₃ commutation. It retains
noncommutation of A with U or any Bob generator and of distinct Bob generators.
Both implementations reject a doubled prefactor. The weaker-commutation check
supports the exact hypotheses of the matrix lemma, rather than only its tensor
specialization. They share coefficient arithmetic and are not independent-agent
reviews. Neither is in the trusted Lean proof chain.

No all-dimensional d theorem, arbitrary-Hilbert-space theorem, or qc supremum
statement is claimed by this finite-matrix Lean source. Such extensions need
their own typed model and proof, even though polynomial identities suggest a
possible route.
