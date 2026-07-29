# Overlap-space Kramers parity audit

**Date:** 2026-07-29

**Status:** exact limitation theorem; no four-divisibility conclusion

## 1. Question and conclusion

Put \(d=2s\), and let
\[
p=P_{12},\qquad q=P_{23}
\]
for an arbitrary exceptional projection.  On \(\operatorname{ran}p\),
the compression \(pqp\) has eigenvalues
\[
1\quad\text{with multiplicity }s^3,\qquad
\frac13\quad\text{with multiplicity }k=3s^3.
\tag{1}
\]
When \(s\) is odd, \(k\) is odd.  It is therefore tempting to seek an
antiunitary of square \(-1\) on the \(1/3\)-eigenspace and invoke Kramers
degeneracy.

The exact audit gives a negative delimitation:

1. the canonical complex structure furnished by \(p,q\) acts on the
   full \(2k\)-dimensional generic sector and exchanges its two
   \(k\)-dimensional halves;
2. an antiunitary of square \(-1\) commuting with the two-projection
   algebra exists **if and only if \(k\) is already even**;
3. Bytsko's cyclic overlap matrix maps two generally different
   \(k\)-dimensional singular subspaces, rather than furnishing an
   endomorphism of one of them;
4. for the published exact \(d=4\) witness those two subspaces are
   demonstrably different, the cyclic overlap is nonnormal, adjoint
   closure fails, outer reversal fails, and the available real
   conjugation has square \(+1\).

Thus no Kramers parity follows from the abstract overlap algebra, its
polar map, conjugation, transpose/adjoint, or bare tensor reversal.  A
positive parity theorem would need genuinely new spatial data that
canonically closes the two singular subspaces and proves an alternating
or quaternionic structure there.

This is not a counterexample to four-divisibility: the exact odd-\(k\)
model in Section 4 is an abstract three-strand representation, not a
tensor-local \(d=6\) projection.

## 2. Canonical generic sector

For \(c=1/3\), let \(e\) and \(f\) be the common-one and common-zero
projections of \(p,q\), and set
\[
g=I-e-f.
\]
On \(g\mathcal H\), the standard two-projection decomposition is
\[
g\mathcal H\cong\mathbb C^2\otimes\mathbb C^k,
\tag{2}
\]
with
\[
p=p_0\otimes I_k,\qquad q=q_0\otimes I_k,
\]
where
\[
p_0=
\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
q_0=
\begin{pmatrix}
c&\sqrt{c(1-c)}\\
\sqrt{c(1-c)}&1-c
\end{pmatrix}.
\tag{3}
\]
In particular,
\[
C^*(p,q)|_{g\mathcal H}=M_2(\mathbb C)\otimes I_k.
\tag{4}
\]

The \(1/3\)-eigenspace of \(pqp\) is
\[
K=(p-e)\mathcal H
\cong\mathbb C\binom10\otimes\mathbb C^k.
\tag{5}
\]
Every complex-linear word \(x\in C^*(p,q)\), when compressed to \(K\),
therefore satisfies
\[
(p-e)x(p-e)=\lambda_x(p-e)
\tag{6}
\]
for some scalar \(\lambda_x\).  No word in the two projections acts
nontrivially on the multiplicity factor.

The normalized commutator
\[
\mathcal J=\frac{pq-qp}{\sqrt{c(1-c)}}
\tag{7}
\]
is a canonical skew-adjoint complex structure on \(g\mathcal H\):
\[
\mathcal J^*=-\mathcal J,\qquad
\mathcal J^2=-g.
\tag{8}
\]
But
\[
(p-e)\mathcal J(p-e)=0,\qquad
\mathcal J(p-e)\mathcal J^*=(I-p)g.
\tag{9}
\]
It exchanges the two halves of every generic block.  It is not a
complex or quaternionic structure on \(K\).

## 3. Classification of antiunitary symmetries

Choose the standard conjugation \(C_0\) in (2)--(3).  It commutes with
\(p\) and \(q\) and has square \(+1\).

### Proposition 3.1

Every antiunitary \(\Theta\) on \(g\mathcal H\) that commutes with both
\(p\) and \(q\) has the form
\[
\Theta=(I_2\otimes u)C_0
\tag{10}
\]
for a unitary \(u\in U(k)\).  Moreover,
\[
\Theta^2=I_2\otimes u\overline u.
\tag{11}
\]
Consequently, such a \(\Theta\) with \(\Theta^2=-I\) exists if and only
if \(k\) is even.

### Proof

The product \(\Theta C_0\) is a complex-linear unitary commuting with
\(p,q\).  By (4), it equals \(I_2\otimes u\).  This proves (10), and
(11) follows directly.  If \(u\overline u=-I_k\), determinants give
\[
1=\det(u\overline u)=\lvert\det u\rvert^2=(-1)^k,
\]
so \(k\) is even.  Conversely, for even \(k\), take \(u\) to be a
direct sum of real matrices
\(\left(\begin{smallmatrix}0&1\\-1&0\end{smallmatrix}\right)\).
\(\square\)

There is an identical conclusion if one asks \(\Theta\) to interchange
\(p\) and \(q\).  Indeed, the real involution
\[
S_0=\frac{p_0+q_0-I}{\sqrt c}
\tag{12}
\]
interchanges them.  Thus \(S_0\Theta\) commutes with both projections,
and Proposition 3.1 applies.

This identifies the circularity in the proposed Kramers argument:
constructing the desired antiunitary in the abstract multiplicity space
is equivalent to proving the parity one hoped to deduce from it.

The antiunitary \(\mathcal JC_0\) does square to \(-I\) on the full
generic sector, but (9) shows that it exchanges \(K\) with its partner.
Its Kramers degeneracy is exactly the already-visible factor \(2\) in
the dimension \(2k\).

## 4. Exact odd-multiplicity abstract countermodel

For \(s=3\), take
\[
a=b=s^3=27,\qquad k=3s^3=81,
\]
and form the direct sum of:

- \(a\) common-one one-dimensional blocks;
- \(b\) common-zero one-dimensional blocks;
- \(k\) copies of the generic block (3).

This gives exact projections on a \(216\)-dimensional space satisfying
\[
pqp-qpq=\frac13(p-q),
\]
with
\[
\operatorname{rank}p=\operatorname{rank}q=108,\qquad
\operatorname{Tr}(pq)=54.
\]
Thus it has precisely the balanced \(d=6\) three-strand dimensions and
Markov overlap, while its \(1/3\)-multiplicity is the odd number \(81\).
By Proposition 3.1 it has no commuting Kramers antiunitary.

This direct sum does not have the required common factorization
\[
p=P\otimes I_6,\qquad q=I_6\otimes P.
\]
It proves only that the relation, balance, standard trace, and complete
two-projection block data cannot supply the parity.

## 5. Cyclic overlap and Bytsko's matrix

Let \(L\) be cyclic left rotation,
\[
L(x\otimes y\otimes z)=y\otimes z\otimes x,
\qquad L^3=I.
\tag{13}
\]
Then
\[
q=L^*pL,\qquad r=LpL^*.
\tag{14}
\]
Under the usual vectorization
\(\operatorname{ran}P\subset M_d(\mathbb C)\), Bytsko's block matrix
\[
(W_{\mathcal T})_{sm}=V_m\overline{V_s}
\]
is the matrix of the cyclic compression
\[
W=pLp\big|_{\operatorname{ran}p}
\tag{15}
\]
in the basis \(\{|V_s\rangle\otimes|a\rangle\}\).  Hence
\[
WW^*=prp,\qquad W^*W=pqp.
\tag{16}
\]

The cubic relation fixes the singular values of \(W\), but it does not
identify its left and right singular subspaces.  Write
\[
K_q=p-e(p,q),\qquad K_r=p-e(p,r).
\tag{17}
\]
These are the \(1/3\)-spectral projections of \(W^*W\) and \(WW^*\),
respectively.  The polar unitary of \(W\) maps
\(\operatorname{ran}K_q\) to \(\operatorname{ran}K_r\).  It is an
endomorphism of one \(1/3\)-space only after an additional identification
is supplied.

Likewise, viewing \(\operatorname{ran}P\) as an operator subspace does
not provide an adjoint antiunitary automatically:
\[
\operatorname{ran}P\text{ is adjoint-closed}
\quad\Longleftrightarrow\quad
P=F\overline P F,
\tag{18}
\]
where \(F\) flips the two local tensor factors.  Neither (18), reality
\(\overline P=P\), nor flip symmetry \(FPF=P\) is part of the defining
relations.

## 6. Exact published-\(d=4\) stress test

For the published sparse real witness, exact arithmetic gives
\[
\operatorname{rank}K_q=\operatorname{rank}K_r=24,
\qquad
\operatorname{Tr}(K_qK_r)=18,
\tag{19}
\]
and hence
\[
\lVert K_q-K_r\rVert_{\mathrm{HS}}^2=12.
\tag{20}
\]
Equivalently, its cyclic overlap is nonnormal:
\[
\lVert WW^*-W^*W\rVert_{\mathrm{HS}}^2=\frac{16}{3}.
\tag{21}
\]
Thus even a valid exact exceptional solution does not make the two
\(1/3\)-singular spaces coincide.

The witness is real, so entrywise conjugation preserves \(p,q,K_q,K_r\),
but this antiunitary squares to \(+I\).  The adjoint/flip condition fails:
\[
\lVert P-FPF\rVert_{\mathrm{HS}}^2=8.
\tag{22}
\]
On three sites, bare outer reversal \(J_3\) also fails to preserve the
chosen overlap space:
\[
\operatorname{Tr}(K_qJ_3K_qJ_3)=9,\qquad
\lVert K_q-J_3K_qJ_3\rVert_{\mathrm{HS}}^2=30.
\tag{23}
\]

Equations (19)--(23) rule out the natural attempts to close the polar
overlap using normality, reality, adjoint, flip, or reversal.  They do
not rule out a deeper invariant constructed from additional tensor-local
data.

## 7. Remaining viable target

A parity proof through the overlap space would now have to establish a
new theorem of the following kind:

> The full tensor placement of an exceptional \(P\) canonically equips
> one of the \(3s^3\)-dimensional singular multiplicity spaces with a
> nondegenerate alternating form or an antiunitary of square \(-1\),
> using data beyond \(C^*(p,q)\), the cyclic polar overlap, and bare
> tensor permutations.

The published witness shows that such a theorem cannot be implemented
by simply identifying the left and right singular spaces, imposing
adjoint closure, or using ordinary conjugation.  At present this route
therefore supplies a sharp assumption audit rather than a proof that
\(2\mid s\).
