# Odd leg projections force divisibility by four

**Date:** 2026-07-28

**Status:** PROVED
**Scope:** arbitrary exceptional solutions with a projection in a one-leg
commutant.  The theorem is not a divisibility result for solutions whose two
one-leg commutants contain only even-rank projections.

## 1. Setup

Let \(V\) be a complex Hilbert space of dimension \(d\), and let
\[
P=P^*=P^2\in\operatorname{End}(V\otimes V),\qquad
\operatorname{rank}P=\frac{d^2}{2},
\tag{1}
\]
satisfy
\[
P_{12}P_{23}P_{12}-P_{23}P_{12}P_{23}
=\frac13(P_{12}-P_{23}).
\tag{2}
\]
The automatic-standardness theorem already proved in
`track_structural_projection.md` gives
\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I_V.
\tag{3}
\]
The only external input to (3) is Lechner's no-opposite-spectrum/Markov
theorem.  The argument below is otherwise elementary finite-dimensional
linear algebra.

Define the two one-leg commutants
\[
\mathcal C_L(P)=
\{x\in\operatorname{End}(V):(x\otimes I)P=P(x\otimes I)\},
\tag{4}
\]
\[
\mathcal C_R(P)=
\{x\in\operatorname{End}(V):(I\otimes x)P=P(I\otimes x)\}.
\tag{5}
\]

## 2. The abstract two-projection count

We use the following special case of the two-projection lemma.

### Lemma 2.1

Let \(a,b\) be orthogonal projections on a \(D\)-dimensional Hilbert space
such that
\[
aba-bab=c(a-b),\qquad 0<c<1.
\tag{6}
\]
If
\[
\operatorname{rank}a=\operatorname{rank}b=\frac D2
\quad\text{and}\quad
\operatorname{Tr}(ab)=\frac D4,
\tag{7}
\]
then, when \(c=1/3\),
\[
\dim(\operatorname{ran}a\cap\operatorname{ran}b)
=
\dim(\ker a\cap\ker b)
=\frac D8.
\tag{8}
\]
In particular, \(8\mid D\).

### Proof

Put
\[
z=aba-ca=bab-cb.
\tag{9}
\]
Then \(az=za=z\) and \(bz=zb=z\).  Thus the range of \(z\) lies in
\(\operatorname{ran}a\cap\operatorname{ran}b\).  On this intersection,
\(z=(1-c)I\).  Self-adjointness shows that
\[
z=(1-c)e,
\tag{10}
\]
where \(e\) is the orthogonal projection onto the common range.  Consequently
\[
\begin{aligned}
\operatorname{Tr}e
&=\frac{\operatorname{Tr}(aba)-c\operatorname{Tr}a}{1-c}\\
&=\frac{D/4-cD/2}{1-c}.
\end{aligned}
\tag{11}
\]
For \(c=1/3\), this is \(D/8\).

The usual two-projection decomposition has a common-one sector, a
common-zero sector, and two-dimensional generic sectors.  Equal half ranks
make the common-one and common-zero dimensions equal.  This proves (8).
Equivalently, the latter equality follows by applying the same argument to
\(I-a,I-b\).  Since (8) is the dimension of a Hilbert space, it is an
integer. \(\square\)

## 3. Invariant leg-commutant theorem

### Theorem 3.1

Let \(P\) satisfy (1)--(3).  If \(z\) is a projection of rank \(r\) in
either \(\mathcal C_L(P)\) or \(\mathcal C_R(P)\), then
\[
\boxed{8\mid r d^2.}
\tag{12}
\]
More precisely, restricting the three-site pair to the \(z\)-sector on the
spectator site gives common-one and common-zero multiplicities
\[
\boxed{\frac{r d^2}{8}.}
\tag{13}
\]

### Proof for \(z\in\mathcal C_L(P)\)

Put \(W=zV\), so \(\dim W=r\), and restrict \(P\) to \(W\otimes V\):
\[
Q=(z\otimes I)P\big|_{W\otimes V}.
\tag{14}
\]
Because \(z\otimes I\) commutes with \(P\), \(Q\) is an orthogonal
projection.  Its rank is
\[
\begin{aligned}
\operatorname{rank}Q
&=\operatorname{Tr}((z\otimes I)P)\\
&=\operatorname{Tr}\!\left(
z\,\operatorname{Tr}_2P\right)
=\frac{rd}{2}.
\end{aligned}
\tag{15}
\]

Restrict (2) on its first site to
\[
\mathcal K=W\otimes V\otimes V.
\]
The two projections appearing there are
\[
a=Q\otimes I_V,\qquad b=I_W\otimes P.
\tag{16}
\]
Restriction preserves (2), so
\[
aba-bab=\frac13(a-b).
\tag{17}
\]
The dimension of \(\mathcal K\) is \(D=rd^2\), and (1), (15) give
\[
\operatorname{rank}a=\operatorname{rank}b=\frac{rd^2}{2}.
\tag{18}
\]

The overlap trace is fixed by (3), not assumed:
\[
\begin{aligned}
\operatorname{Tr}_{W\otimes V\otimes V}(ab)
&=\operatorname{Tr}_{W\otimes V}
\left[
Q\left(I_W\otimes\operatorname{Tr}_2P\right)
\right]\\
&=\frac d2\operatorname{Tr}Q
=\frac{rd^2}{4}.
\end{aligned}
\tag{19}
\]
Lemma 2.1 now gives both multiplicities in (13), hence (12).

If \(z\in\mathcal C_R(P)\), apply the proved case to the tensor-flipped
projection \(FPF\).  Tensor reversal interchanges \(P_{12}\) and \(P_{23}\)
and multiplies both sides of (2) by \(-1\), so the relation is preserved.
It also exchanges the two leg commutants. \(\square\)

### Corollary 3.2

If \(d\equiv2\pmod4\), then every projection in both one-leg commutants has
even rank.

Indeed, \(v_2(d^2)=2\), so (12) forces \(v_2(r)\geq1\).

There is a useful finite-dimensional \(C^*\)-algebra formulation.  If a
unital \(*\)-subalgebra \(\mathcal A\) of either leg commutant is represented
as
\[
V\cong\bigoplus_\alpha
\left(\mathbb C^{m_\alpha}\otimes\mathbb C^{n_\alpha}\right),
\qquad
\mathcal A\cong\bigoplus_\alpha
\left(M_{m_\alpha}(\mathbb C)\otimes I_{n_\alpha}\right),
\tag{20}
\]
then a minimal projection in the \(\alpha\)-summand has ordinary rank
\(n_\alpha\).  Hence
\[
8\mid n_\alpha d^2
\tag{21}
\]
for every \(\alpha\).  In a hypothetical dimension \(d\equiv2\pmod4\)
solution, every representation multiplicity \(n_\alpha\) is therefore even.

If \(g\) is the greatest common divisor of the ranks of all nonzero
projections in \(\mathcal A\), then (20) gives
\[
g=\gcd_\alpha n_\alpha.
\tag{22}
\]
The simultaneous content of all the divisibilities (21) is exactly
\[
8\mid g d^2.
\tag{23}
\]
Thus taking several projections, sums, meets, or complements produces no
stronger arithmetic consequence by this argument.  For example, at \(d=6\)
the condition is satisfied whenever all \(n_\alpha\) are even.

## 4. Rank-one and block-controlled consequences

### Corollary 4.1

Suppose that, in some orthonormal basis of one leg,
\[
H=I-2P=\sum_{x=1}^d |x\rangle\!\langle x|\otimes A_x
\tag{24}
\]
or the tensor-flipped form.  Then
\[
4\mid d.
\tag{25}
\]
Moreover, every \(A_x\) is a trace-zero Hermitian reflection.

### Proof

Equation (24), Hermiticity, and \(H^2=I\) make each \(A_x\) a Hermitian
involution.  Equivalently,
\[
P=\sum_x|x\rangle\!\langle x|\otimes p_x,
\qquad p_x=\frac{I-A_x}{2},
\tag{26}
\]
with every \(p_x\) a projection.  Taking the second partial trace in (3)
coefficient by coefficient gives
\[
\operatorname{rank}p_x=\operatorname{Tr}p_x=\frac d2,
\qquad
\operatorname{Tr}A_x=0.
\tag{27}
\]
Every rank-one \(|x\rangle\langle x|\) belongs to
\(\mathcal C_L(P)\).  Theorem 3.1 gives \(8\mid d^2\).  Since \(d\) is an
integer, this is equivalent to \(4\mid d\). \(\square\)

The invariant hypothesis behind (24) is:

> one of the one-leg commutants contains a maximal abelian
> \(*\)-subalgebra of \(M_d(\mathbb C)\).

Every MASA is unitarily conjugate to the diagonal algebra, so its minimal
rank-one projections give (24), and conversely (24) supplies such a MASA.

There are two distinct meanings of “higher-rank controlled blocks”:

1. If
   \[
   H=\sum_\alpha E_\alpha\otimes A_\alpha
   \tag{28}
   \]
   with orthogonal control projections \(E_\alpha\), then every rank-one
   subprojection of every \(E_\alpha\) commutes with \(H\).  Thus (25) still
   follows, irrespective of the ranks of the \(E_\alpha\).
2. If one assumes only
   \[
   [E_\alpha\otimes I,H]=0
   \tag{29}
   \]
   while allowing a general operator on \(E_\alpha V\otimes V\), then the
   exact conclusion is only
   \[
   8\mid(\operatorname{rank}E_\alpha)d^2.
   \tag{30}
   \]
   An odd-rank block forces \(4\mid d\); an even-rank block does not.

Conflating (28) and (29) would overstate the theorem.

## 5. Operator-Schmidt rank audit

Chen and Yu prove in Theorem 11 of
[arXiv:1407.5464](https://arxiv.org/abs/1407.5464) that every bipartite
unitary of operator-Schmidt rank three is **locally equivalent** to a
controlled unitary.  Their definition allows independent local unitaries
before and after the controlled gate.  In the notation of their Figure 1,
\[
U=(Q\otimes I)
\left(\sum_j|j\rangle\!\langle j|\otimes V_j\right)
(R\otimes I),
\tag{31}
\]
or the tensor-flipped version.  The theorem is dimension-independent.
The analogous rank-two statement is Cohen--Yu,
[arXiv:1211.5201](https://arxiv.org/abs/1211.5201), again with local
equivalence rather than preservation of the original leg commutant.

This is not the same as (24).  Independent pre/post multiplication does
not preserve a one-leg commutant, and it does not preserve the
Yang--Baxter equation.  Therefore Theorem 11 by itself does **not** imply
that an exceptional solution of Schmidt rank at most three has a rank-one
leg-commutant projection.

The distinction persists even for traceless Hermitian involutions with both
scalar partial traces.  On
\[
V=\mathbb C^2\otimes\mathbb C^2
\]
put
\[
\begin{array}{lll}
A_1=X\otimes I,&A_2=Z\otimes I,&A_3=I\otimes Z,\\
B_1=Z\otimes I,&B_2=Z\otimes Z,&B_3=X\otimes I,
\end{array}
\]
and
\[
H_*=\frac1{\sqrt3}\sum_{j=1}^3 A_j\otimes B_j.
\tag{32}
\]
The three product terms in (32) are pairwise anticommuting Hermitian
involutions.  Hence
\[
H_*^*=H_*,\qquad H_*^2=I,\qquad
\operatorname{Tr}H_*=0,
\tag{33}
\]
and both one-site partial traces of \(H_*\) vanish.  The two triples
\(\{A_j\}\), \(\{B_j\}\) are linearly independent, so \(H_*\) has
operator-Schmidt rank exactly three.

Nevertheless,
\[
\mathcal C_L(H_*)=\mathcal C_R(H_*)
=I_2\otimes\operatorname{span}\{I_2,Z\}.
\tag{34}
\]
Every projection in either algebra has rank \(0,2\), or \(4\); neither
contains a MASA of \(M_4\).  Chen--Yu says that \(H_*\) is locally
equivalent to a controlled unitary, but it is not controlled in the
commutant sense needed above.

This example is only an assumption audit, not an exceptional solution:
its cubic \(H\)-residual has exact squared Hilbert--Schmidt norm
\[
\left\|
(H_*)_{12}(H_*)_{23}(H_*)_{12}
-(H_*)_{23}(H_*)_{12}(H_*)_{23}
-\frac13((H_*)_{12}-(H_*)_{23})
\right\|_2^2
=\frac{512}{3}.
\tag{35}
\]

Thus the currently justified conclusion is:

> A \(d\equiv2\pmod4\) exceptional solution cannot be directly controlled
> on either leg and cannot have any odd-rank leg-commutant projection.

It is **not** yet justified to claim operator-Schmidt rank at least four.
Such a corollary would require a new, exceptional-relation-specific bridge
from Chen--Yu local equivalence to an actual odd-rank leg-commutant
projection.

## 6. Exact replay

The independent verifier is

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_controlled_leg_divisibility.py
```

It checks:

- both control orientations on a non-Yang--Baxter exact test projection, so
  a vanishing residual cannot hide a sign or tensor-leg mistake;
- the overlap and abstract common-sector arithmetic;
- all four rank-one sectors of an exact controlled \(V_4\)-conference
  \(d=4\) witness;
- the operator-Schmidt-rank-three counter-audit (32), including its
  commutants and nonzero cubic residual.
