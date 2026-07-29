# Operator-Schmidt rank four: a Clifford-frame parity theorem and its limit

**Date:** 2026-07-29
**Scope:** arbitrary local dimension in the theorem below; exact \(d=4\)
limitation model in the audit
**Status:** exact conditional theorem; no classification of all
operator-Schmidt-rank-four exceptional solutions

## 1. Executive conclusion

Operator-Schmidt rank four is the first rank at which the general
bipartite-unitary structure theorem used at rank three stops.  Rank-four
unitaries need not be locally equivalent to controlled unitaries: the
two-qubit swap is the elementary counterexample.  Consequently there is no
valid route

\[
\operatorname{OSR}(H)=4
\Longrightarrow
\text{controlled}
\Longrightarrow
4\mid d.
\]

There is nevertheless an exact parity theorem for the most natural
rank-four Clifford branch.

> **Four-product Clifford-frame theorem.**
> Let \(d\) be even.  Suppose
> \[
> H=\sum_{j=1}^4 c_j A_j\otimes B_j,
> \qquad c_j\in\mathbb R\setminus\{0\},
> \tag{1}
> \]
> where all \(A_j,B_j\in M_d(\mathbb C)\) are traceless Hermitian
> involutions and the four product involutions
> \[
> T_j=A_j\otimes B_j
> \tag{2}
> \]
> anticommute pairwise.  Then
> \[
> \boxed{4\mid d.}
> \tag{3}
> \]

If \(\sum_jc_j^2=1\), then (1) is automatically a Hermitian involution.
If the two local families are linearly independent, it has
operator-Schmidt rank four.  Thus (3) excludes every \(d\equiv2\pmod4\)
solution in this rigorously defined four-term Clifford-reflection ansatz,
independently of the cubic relation.

The theorem does **not** extend to arbitrary operator-Schmidt-rank-four
involutions.  In a Hermitian Schmidt decomposition the local Schmidt
operators need not be involutions, and the four product terms need not
anticommute.  An exact \(d=4\) calibration below further shows that
Hermiticity, involutivity, trace zero, both scalar partial traces,
operator-Schmidt rank four, and scalar leg commutants do not themselves
supply a nontrivial true one-leg control projection or the exceptional
cubic.  No claim about four-local equivalence of this calibration is
needed.

## 2. Why the rank-three structure theorem cannot simply be reused

Chen--Yu prove that every bipartite unitary of operator-Schmidt rank three
is locally equivalent to a controlled unitary.  Their local equivalence
allows independent product unitaries on the input and output.  Rank four
has no analogous theorem.  Müller-Hermes--Nechita
([arXiv:1612.07616](https://arxiv.org/abs/1612.07616)) moreover prove that,
apart from the missing rank three on \(2\times2\), there are no
dimension-only obstructions on which operator-Schmidt ranks bipartite
unitaries can attain.  That is an existence theorem for ranks, not a
controlled or block-controlled normal form.

Indeed, on \(\mathbb C^2\otimes\mathbb C^2\),
\[
\mathsf F_2=\sum_{a,b=0}^1 |a\rangle\!\langle b|
 \otimes |b\rangle\!\langle a|
\tag{4}
\]
is a Hermitian involutive unitary of operator-Schmidt rank four.  Its
one-leg commutants are scalar, because
\[
(X\otimes I)\mathsf F_2=\mathsf F_2(X\otimes I)
\quad\Longrightarrow\quad
X\otimes I=I\otimes X
\quad\Longrightarrow\quad X\in\mathbb CI.
\tag{5}
\]
It is therefore not controlled on either leg, nor locally equivalent to a
two-qubit controlled unitary (whose operator-Schmidt rank is at most two).

The swap is not balanced and is not an exceptional solution.  Its role is
only to mark the exact failure point of the general low-Schmidt structure
theory.  Any rank-four theorem for the exceptional class must use new
information from the exceptional relations.

## 3. Commutation graphs forced by a Clifford frame

Assume (1)--(2).  For \(i\ne j\), pairwise anticommutation says
\[
(A_iA_j)\otimes(B_iB_j)
=-(A_jA_i)\otimes(B_jB_i).
\tag{6}
\]
Equality of two nonzero simple tensors gives a scalar
\(\zeta_{ij}\ne0\) such that
\[
A_iA_j=\zeta_{ij}A_jA_i,\qquad
B_iB_j=-\zeta_{ij}^{-1}B_jB_i.
\tag{7}
\]
Because \(A_i,A_j\) are involutions, multiplying the first identity on the
left and right by \(A_i\) gives
\[
A_jA_i=\zeta_{ij}A_iA_j.
\]
Comparing this with (7) gives \(\zeta_{ij}^2=1\).  Hence every local pair
either commutes or anticommutes, and the two legs have opposite choices.

Let \(G_A,G_B\in M_4(\mathbb F_2)\) be the alternating commutation matrices:
an off-diagonal entry is one exactly when the corresponding local
involutions anticommute.  If \(K\) is the adjacency matrix of the complete
graph \(K_4\), then
\[
\boxed{G_A+G_B=K.}
\tag{8}
\]

We use two elementary lemmas.

### Lemma 3.1: representation divisibility

If Hermitian involutions \(U_1,\ldots,U_4\in M_d(\mathbb C)\) commute or
anticommute according to an alternating binary matrix \(G\) of rank \(2r\),
then
\[
2^r\mid d.
\tag{9}
\]

**Proof.**  Symplectic Gram--Schmidt over \(\mathbb F_2\) transforms the
generators, using products and harmless phases, into \(r\) Weyl pairs
\[
X_kZ_k=-Z_kX_k
\]
which commute for different \(k\).  They generate a copy of
\(M_{2^r}(\mathbb C)\).  Every finite-dimensional unital representation of
this matrix algebra has dimension divisible by \(2^r\).  \(\square\)

### Lemma 3.2: the four-vertex complement lemma

If \(G\) and \(K+G\) are alternating \(4\times4\) binary matrices of rank
two, then at least one of their graphs has an isolated vertex.

**Proof.**  Write the six edge variables of \(G\) as
\[
a,b,c,d,e,f
\]
on \(12,13,14,23,24,34\).  Rank two implies vanishing Pfaffian
\[
af+be+cd=0.
\tag{10}
\]
The same condition for the complement expands to
\[
1+(a+b+c+d+e+f)+(af+be+cd)=0.
\tag{11}
\]
Thus \(G\) has an odd number of edges.  If it already has an isolated
vertex there is nothing to prove.  Otherwise it has three or five edges.
With five edges its complement has two isolated vertices.  With three
edges and no isolated vertex it is either a path on four vertices or a
three-leaf star.  The path has nonzero Pfaffian (its perfect matching is
unique), contradicting (10).  The star's center becomes isolated in the
complement.  \(\square\)

## 4. Proof of the four-product theorem

Suppose for contradiction that
\[
d=2s,\qquad s\ \text{odd}.
\tag{12}
\]
The matrix \(K\) in (8) has binary rank four.  Lemma 3.1 says that neither
\(G_A\) nor \(G_B\) can have rank four, since that would make \(4\mid d\).
Alternating ranks are even, so
\[
4=\operatorname{rank}K
\leq\operatorname{rank}G_A+\operatorname{rank}G_B
\leq4.
\tag{13}
\]
Consequently both local commutation matrices have rank two.

Lemma 3.2 gives an isolated generator on one of the two legs; call it
\(U_0\).  On that same leg, rank two supplies an anticommuting pair
\(C,D\).  A pair of anticommuting Hermitian involutions on
\(\mathbb C^{2s}\) is unitarily equivalent to
\[
C=Z\otimes I_s,\qquad D=X\otimes I_s.
\tag{14}
\]
Since \(U_0\) commutes with both, it has the form
\[
U_0=I_2\otimes L
\tag{15}
\]
for a Hermitian involution \(L\in M_s(\mathbb C)\).  But \(s\) is odd, so
the difference between the \(+1\) and \(-1\) multiplicities of \(L\) is
odd and cannot vanish.  Therefore
\[
\operatorname{Tr}U_0=2\operatorname{Tr}L\ne0,
\tag{16}
\]
contradicting the assumed tracelessness of every local factor.  This proves
\(4\mid d\).

## 5. Exact noncontrolled balanced calibration in \(d=4\)

The following matrix shows why the Clifford-frame theorem must not be
silently promoted to all rank-four involutions or to a controlled-unitary
theorem.  Put
\[
\begin{array}{llll}
A_1=XI,&A_2=IX,&A_3=ZI,&A_4=XZ,\\
B_1=XI,&B_2=ZI,&B_3=XZ,&B_4=ZY
\end{array}
\tag{17}
\]
on \(\mathbb C^4=\mathbb C^2\otimes\mathbb C^2\), and define
\[
H_\star=\frac12\sum_{j=1}^4A_j\otimes B_j.
\tag{18}
\]
The four product Pauli words anticommute pairwise.  Both local Pauli
families are linearly independent and generate \(M_4(\mathbb C)\).
Consequently
\[
\begin{gathered}
H_\star^*=H_\star,\qquad H_\star^2=I,\qquad
\operatorname{Tr}H_\star=0,\\
\operatorname{Tr}_1H_\star=\operatorname{Tr}_2H_\star=0,\qquad
\operatorname{OSR}(H_\star)=4,
\end{gathered}
\tag{19}
\]
and both leg commutants are scalar.  Thus
\(P_\star=(I-H_\star)/2\) is a rank-eight standard projection.

It is deliberately not exceptional.  Exact Pauli-word reduction gives
\[
\left\|
(H_\star)_{12}(H_\star)_{23}(H_\star)_{12}
-(H_\star)_{23}(H_\star)_{12}(H_\star)_{23}
-\frac13\bigl((H_\star)_{12}-(H_\star)_{23}\bigr)
\right\|_{\mathrm{HS}}^2
=\frac{1376}{9}.
\tag{20}
\]
This is an assumption audit: even all the two-site conditions in (19)
plus trivial leg commutants do not supply the missing exceptional
three-site relation.

## 6. Consequence for the unresolved branch

If a hypothetical \(d\equiv2\pmod4\) exceptional solution has
operator-Schmidt rank four, it cannot admit a Schmidt realization of the
form (1)--(2).  At least one genuinely non-Clifford feature is necessary:

- some local Schmidt factors are not involutions;
- or the product terms are not pairwise anticommuting;
- or involutivity results from cancellations among nonzero cross
  anticommutators.

The theorem therefore closes a natural rank-four construction mechanism,
but the unrestricted implication
\[
\operatorname{OSR}(H)=4\ \text{and exceptional}
\quad\Longrightarrow\quad4\mid d
\tag{21}
\]
remains open.

The published \(d=4\) witness and all of its identity amplifications have
operator-Schmidt rank three, so they neither prove nor contradict (21).

## 7. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_osr4_clifford_frame_parity.py
```

The verifier:

1. exhausts the \(64\) four-vertex commutation graphs and checks the
   complement lemma over \(\mathbb F_2\);
2. checks the Pauli commutation data and full local generation in (17);
3. checks (19) by exact Pauli-word algebra;
4. reproduces the \(38\)-word cubic residual and the exact norm
   \(1376/9\).

The finite graph replay is a check of Lemma 3.2, not a substitute for its
human proof.
