# Bytsko characteristic-matrix and antisymmetrizer audit

**Date:** 2026-07-29

**Status:** exact normalization/reduction; no new divisibility obstruction

## 1. Translation of conventions

Bytsko studies orthogonal projections \(P\in M_{n^2}(\mathbb C)\)
satisfying
\[
Q^2(P_1P_2P_1-P_2P_1P_2)=P_1-P_2.
\tag{1}
\]
Thus the exceptional relation is his case
\[
n=d,\qquad r=\operatorname{rank}P=\frac{d^2}{2},
\qquad Q=\sqrt3.
\tag{2}
\]

His Hecke generator is
\[
R_{\mathrm B}=q_{\mathrm B}I-QP,
\qquad q_{\mathrm B}+q_{\mathrm B}^{-1}=Q.
\]
Taking \(q_{\mathrm B}=e^{i\pi/6}\) gives
\[
e^{i\pi/6}R_{\mathrm B}
=e^{i\pi/3}I-(1+e^{i\pi/3})P,
\]
which is exactly the present \(R\).  The two conventions therefore differ
only by an overall phase.

## 2. The parameter \(k\)

Bytsko defines
\[
k=\frac12\operatorname{rank}(P_1-P_2).
\tag{3}
\]
His trace formula at \(m=1\) is
\[
\operatorname{Tr}(P_1P_2)
=rn+(Q^{-2}-1)k.
\tag{4}
\]
Automatic standardness gives
\[
\operatorname{Tr}(P_1P_2)
=\operatorname{Tr}\!\left(
 P_1\,\operatorname{Tr}_3(P_2)\right)
=\frac{d^3}{4}.
\tag{5}
\]
Substituting (2) into (4) therefore yields
\[
\frac{d^3}{4}
=\frac{d^3}{2}-\frac23k,
\qquad
\boxed{k=\frac{3d^3}{8}}.
\tag{6}
\]
For \(d=2s\), this is \(k=3s^3\).  Hence the rank parameter itself
requires exactly \(2\mid d\), but it does not require \(2\mid s\).

Equation (6) is the same multiplicity obtained from the canonical
two-projection decomposition: \(P_1-P_2\) has the two nonzero eigenvalues
\(\pm\sqrt{2/3}\), each with multiplicity \(3d^3/8\).

## 3. The characteristic matrix

Choose a Hilbert--Schmidt orthonormal basis
\(\mathcal T=\{V_1,\ldots,V_r\}\) of the operator subspace corresponding
to \(\operatorname{ran}P\).  Bytsko defines the \(rn\times rn\) block
matrix
\[
W_{\mathcal T}
=\sum_{s,m=1}^r E_{sm}^{(r)}\otimes V_m\overline{V_s},
\qquad
A_{\mathcal T}=W_{\mathcal T}W_{\mathcal T}^*.
\tag{7}
\]
His characteristic-matrix criterion says that a non-Temperley--Lieb
solution has
\[
\sigma(A_{\mathcal T})
=\{1^{\,rn-k},Q^{-2\,k}\}.
\tag{8}
\]
In the exceptional case,
\[
\boxed{
\sigma(A_{\mathcal T})
=\left\{
1^{\,d^3/8},
\left(\frac13\right)^{\,3d^3/8}
\right\}.
}
\tag{9}
\]
Equivalently, the singular values of \(W_{\mathcal T}\) are
\[
1\quad\text{with multiplicity }s^3,
\qquad
\frac1{\sqrt3}\quad\text{with multiplicity }3s^3.
\tag{10}
\]

At \(d=6\), the multiplicities are \(27\) and \(81\).  They are both
integral, and the smaller singular-value multiplicity is odd.  Thus the
characteristic-matrix theorem contains no implicit even-degeneracy
condition that would exclude \(d=6\).

Bytsko's general rank and trace-norm inequalities are also automatic here.
For example, his inequality
\[
rn-k+Q^{-1}k\le r^2
\]
reduces to
\[
\frac{1+\sqrt3}{8}d^3\le\frac14d^4,
\]
which holds for every \(d\ge2\).

## 4. Antisymmetrizer relation

In Bytsko's Hecke convention the relevant phase is
\(q_{\mathrm B}=e^{i\pi/6}\).  His positivity argument for the
\(q\)-antisymmetrizer then forces the five-strand antisymmetrizer to vanish.
This is consistent with the already established \(H_n(3,6)\) trace
quotient and its admissible Young graph.  The resulting projector ranks
are exactly the Markov-trace ranks already audited in
`track_hecke_multiplicity.md`; they impose only \(2\mid d\).

## 5. Scope

The characteristic matrix is a useful exact reformulation of the full
three-site relation and may be a better discovery parametrization than
dense \(216\times216\) residuals.  It does **not**, by itself, add a
four-divisibility obstruction.  Any such obstruction must use structure
not present in its two-point singular spectrum, for example the special
tensor placement of the operator subspace on both adjacent pairs.

## Sources checked

- A. Bytsko, *On orthogonal projections related to representations of the
  Hecke algebra on a tensor space*, arXiv:2212.13116.
- A. Bytsko, *Two relations for the antisymmetrizer in the Hecke algebra*,
  arXiv:2203.08664.

The downloaded PDFs and arXiv source archives are retained under
`tmp_literature/`.
