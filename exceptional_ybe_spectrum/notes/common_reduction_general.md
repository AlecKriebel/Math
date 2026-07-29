# Common one-leg reductions in arbitrary dimension

**Date:** 2026-07-29
**Status:** PROVED
**Scope:** arbitrary balanced exceptional solutions; no irreducibility,
Pauli, sparsity, or faithfulness hypothesis beyond the already proved
automatic standardness theorem

## 1. Result

Let \(V\) have even dimension \(d\), and let
\(q=e^{i\pi/3}\).  Suppose
\[
H=H^*=H^{-1}\in\operatorname{End}(V\otimes V),\qquad
\operatorname{Tr}H=0,
\]
satisfy
\[
H_{12}H_{23}H_{12}-H_{23}H_{12}H_{23}
=\frac13(H_{12}-H_{23}). \tag{1}
\]
Write
\[
\mathcal C_L(H)=\{x\in\operatorname{End}V:[x\otimes I,H]=0\},
\qquad
\mathcal C_R(H)=\{x\in\operatorname{End}V:[I\otimes x,H]=0\}.
\tag{2}
\]
The automatic-standardness theorem gives
\[
\operatorname{Tr}_1H=\operatorname{Tr}_2H=0. \tag{3}
\]

Suppose that \(z\) is a nonzero proper projection in
\(\mathcal C_L(H)\cap\mathcal C_R(H)\).  Put
\[
W=zV,\quad U=(I-z)V,\quad r=\dim W,\quad s=\dim U=d-r,
\tag{4}
\]
and let
\[
K_W=H|_{W\otimes W},\qquad K_U=H|_{U\otimes U}. \tag{5}
\]

> **Common-reduction theorem.**  Both \(K_W\) and \(K_U\) are non-scalar
> Hermitian involutions satisfying (1) on their respective base spaces.
> If \(a,b,c,e\) are the negative spectral multiplicities on
> \(W\otimes W,W\otimes U,U\otimes W,U\otimes U\), respectively, then
> exactly one of the following holds:
> \[
> \begin{array}{c|c|c|c}
> &a/r^2&e/s^2&(b,c)\\ \hline
> \text{balanced branch}&1/2&1/2&(rs/2,rs/2)\\
> \text{lower TL branch}&1/3&1/3&(2r^2/3,2r^2/3),\quad r=s\\
> \text{upper complementary branch}&2/3&2/3&(r^2/3,r^2/3),\quad r=s.
> \end{array}
> \tag{6}
> \]

The unbalanced alternatives in (6) are genuine local possibilities:
the dimension-three Gaussian Hecke matrix realizes \(1/3\), and
complementing its spectral projection realizes \(2/3\).

The result becomes sharper in the unresolved congruence class.

> **Corollary.**  If \(d\equiv2\pmod4\), only the balanced branch in
> (6) is possible.  Thus, with
> \[
> R_W=\frac{q-1}{2}I+\frac{q+1}{2}K_W,\qquad
> R_U=\frac{q-1}{2}I+\frac{q+1}{2}K_U,
> \]
> \[
> R_W\in[e^{i\pi/3},1/2,r],\qquad
> R_U\in[e^{i\pi/3},1/2,s]. \tag{7}
> \]
> In particular \(r,s\) are even, neither is two, and one of them is a
> strictly smaller dimension congruent to \(2\pmod4\).

Consequently:

1. a least-dimensional solution with \(d\equiv2\pmod4\) has
   \[
   \mathcal C_L(H)\cap\mathcal C_R(H)=\mathbb CI; \tag{8}
   \]
2. the dimension-six trivial-intersection theorem follows immediately;
3. a nontrivial common reduction in dimension ten would already produce
   a dimension-six exceptional solution.

This is a descent theorem, not a nonexistence theorem.  It identifies
precisely why the dimension-six proof does not propagate directly to
all \(d\equiv2\pmod4\): in larger common cells, a non-scalar balanced
exceptional compression can exist.

## 2. Which ranks can an unbalanced cubic involution have?

Let \(K\) be any Hermitian involution on \(X\otimes X\), where
\(\dim X=t\), satisfying (1), and put
\[
Q=\frac{I-K}{2},\qquad k=\operatorname{rank}Q. \tag{9}
\]
If \(K\) is scalar, then \(k=0\) or \(t^2\).  Otherwise
\[
S=-Q+q(I-Q),\qquad q=e^{i\pi/3}, \tag{10}
\]
is a unitary two-eigenvalue Hecke \(R\)-matrix.  The normalization is
\[
\frac{q}{(1+q)^2}=\frac13, \tag{11}
\]
so (1) is exactly the Hecke projection relation in this convention.

No standardness hypothesis on \(K\) is needed here.  The associated
two-eigenvalue matrix \(S\) has no opposite pair of eigenvalues, so
Lechner's Lemma 3.1 makes its normalized tensor-space trace a positive
Markov trace automatically.  Lechner's Theorem 3.4, using Wenzl's
positive-trace classification, then gives
\[
\frac{k}{t^2}\in\left\{\frac13,\frac12,\frac23\right\}. \tag{12}
\]
Equivalently, including the two scalar cases,
\[
\boxed{
k\in\left\{0,\frac{t^2}{3},\frac{t^2}{2},
\frac{2t^2}{3},t^2\right\}.
}
\tag{13}
\]
The divisibility consequences are
\[
3\mid t\quad\text{in the \(1/3\) and \(2/3\) cases},\qquad
2\mid t\quad\text{in the \(1/2\) case}. \tag{14}
\]

For reference, (12) is the specialization of Wenzl's positive traces
\[
\eta_{6,k}
=\frac{\sin(\pi(k-1)/6)}
{2\cos(\pi/6)\sin(\pi k/6)}
\quad(k=2,3,4), \tag{15}
\]
as used in Lechner, *The classification problem for unitary
\(R\)-Matrices with two eigenvalues*, Lemma 3.1 and Theorem 3.4.  No
trace-zero or scalar-partial-trace assumption on \(K\) is used.

## 3. Scalar compression is impossible

Because \(z\) reduces \(H\) on both tensor legs, \(W^{\otimes3}\) is
invariant under \(H_{12}\) and \(H_{23}\).  Hence \(K_W\) satisfies
(1).  The same argument applies to \(K_U\).

Assume \(K_W=\varepsilon I_{W\otimes W}\), where
\(\varepsilon\in\{+1,-1\}\).  Restrict (1) to
\[
W\otimes W\otimes V. \tag{16}
\]
This subspace is invariant.  On it set
\[
X=\varepsilon I,\qquad
Y=I_W\otimes H|_{W\otimes V}. \tag{17}
\]
Since \(X\) is a scalar involution and \(Y^2=I\),
\[
XYX-YXY=Y-X. \tag{18}
\]
Comparison with (1) gives
\[
Y-X=\frac13(X-Y),
\]
and therefore \(Y=X\).  Thus
\[
H|_{W\otimes V}=\varepsilon I_{W\otimes V}. \tag{19}
\]
But (3) now gives
\[
0=z(\operatorname{Tr}_2H)z
=\operatorname{Tr}_V(H|_{W\otimes V})
=d\varepsilon I_W, \tag{20}
\]
a contradiction.  Applying the same argument to \(I-z\) proves that
\(K_U\) is also non-scalar.

It follows from (12) that
\[
\eta_W:=\frac a{r^2},\quad
\eta_U:=\frac e{s^2}
\in\left\{\frac13,\frac12,\frac23\right\}. \tag{21}
\]

## 4. Ambient balance couples the two diagonal cells

Let \(P=(I-H)/2\), and decompose it into the four reducing cells
\[
W\otimes W,\quad W\otimes U,\quad
U\otimes W,\quad U\otimes U. \tag{22}
\]
Denote their ranks by \(a,b,c,e\), respectively.  Automatic standardness
for \(P\) is
\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I_d. \tag{23}
\]
Taking ordinary traces after restricting (23) to \(W\) gives
\[
a+b=\frac{rd}{2},\qquad
a+c=\frac{rd}{2}. \tag{24}
\]
The corresponding \(U\)-row equation gives
\[
c+e=\frac{sd}{2}. \tag{25}
\]
Consequently
\[
b=c,\qquad
\boxed{a-\frac{r^2}{2}=e-\frac{s^2}{2}.} \tag{26}
\]

For the three values in (21), the two sides of (26) belong to
\[
\left\{-\frac{r^2}{6},0,\frac{r^2}{6}\right\},
\qquad
\left\{-\frac{s^2}{6},0,\frac{s^2}{6}\right\}. \tag{27}
\]
Equality is possible only when both are zero, or when their signs agree
and \(r^2=s^2\).  In the balanced case, (24) gives
\(b=c=rs/2\).  In either equal-rank unbalanced case it gives
\(b=c=r^2-a\), producing the two off-diagonal ranks displayed in (6).
This proves the table.

## 5. The \(d\equiv2\pmod4\) descent

The controlled-leg divisibility theorem applies to \(z\), because \(z\)
belongs to either one-leg commutant:
\[
8\mid rd^2. \tag{28}
\]
If \(d\equiv2\pmod4\), then \(v_2(d^2)=2\), so (28) forces \(r\) even.
The complement \(I-z\) is also common, hence \(s\) is even as well.

The two unbalanced alternatives in (6) require
\[
r=s=d/2. \tag{29}
\]
But \(d/2\) is odd, contradicting the evenness just proved.  Therefore
both diagonal compressions are balanced, proving (7).

The established emptiness of the base-dimension-two balanced class shows
that \(r,s\neq2\).  Since \(r+s\equiv2\pmod4\), exactly one of \(r,s\)
is congruent to \(2\pmod4\); it is positive and strictly smaller than
\(d\).  If \(d\) were the least unresolved dimension admitting a
solution, this would be impossible.  Hence its common one-leg
intersection must be scalar.

## 6. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_common_reduction_general.py
```

The verifier independently:

1. constructs the exact dimension-three Gaussian \(1/3\)-rank witness
   and its \(2/3\)-rank complement;
2. checks the projection cubic relation on the full \(27\)-dimensional
   three-site space;
3. replays the finite rank-balance alternatives;
4. exhaustively audits the \(d\equiv2\pmod4\) arithmetic through
   \(d=202\);
5. checks the dimension-six and dimension-ten descent consequences.

The finite audit is a guard for the symbolic proof above, not a
replacement for it.
