# One-sided square invariance does not close at two sites

**Date:** 2026-07-29

**Status:** exact reduction and exact two-site limitation model; the
full Yang--Baxter implication remains open

**Scope:** arbitrary balanced exceptional projections up to the point
where the exact limitation model is introduced

## 1. The question

Let \(P\) be a balanced exceptional projection on \(V\otimes V\):
\[
P=P^*=P^2,\qquad
\operatorname{rank}P=\frac{d^2}{2},\qquad
\operatorname{Tr}_1P=\operatorname{Tr}_2P=\frac d2I_V. \tag{1}
\]
Suppose that a nonzero proper subspace \(W\subset V\) is
square-invariant,
\[
P(W\otimes W)\subseteq W\otimes W. \tag{2}
\]
The four-strand restriction theorem proves that \(r=\dim W\) is even
and that the restriction \(P_W=P|_{W\otimes W}\) is itself balanced:
\[
\operatorname{rank}P_W=\frac{r^2}{2},\qquad
\operatorname{Tr}_1P_W=\operatorname{Tr}_2P_W=\frac r2I_W. \tag{3}
\]

Put \(U=W^\perp\), \(u=\dim U=d-r\).  Does (1)--(3), together with the
Yang--Baxter cubic relation, force \(U\otimes U\) to be invariant?

This note isolates the exact missing quantity.  It also gives an exact
\(d=6,\ r=4,\ u=2\) projection satisfying every two-site condition in
(1)--(3), with the published exceptional \(d=4\) projection as its
restriction, for which \(U\otimes U\) is not invariant.  Thus
projection positivity, scalar partial traces, rank balance,
unitarity, the Hecke polynomial, and the complete restricted
Yang--Baxter equation do not suffice.  Any positive proof must use the
ambient three-site cubic relation in an essentially mixed-sector way.

## 2. The complement-variance reduction

Let \(e\) and \(f=I-e\) be the orthogonal projections onto \(W\) and
\(U\).  On \(V\otimes V\), put
\[
E=e\otimes e,\qquad
F=f\otimes f,\qquad
M=e\otimes f+f\otimes e. \tag{4}
\]
Since \(P\) is self-adjoint, (2) makes \(W\otimes W\) reducing:
\[
[P,E]=0. \tag{5}
\]
Thus
\[
P=P_W\oplus Q
\quad\text{on}\quad
E(V\otimes V)\oplus (M+F)(V\otimes V), \tag{6}
\]
where \(Q=(I-E)P(I-E)\) is a projection.

Subtracting the partial traces in (3) from (1) gives the exact
operator marginals
\[
\boxed{
\begin{aligned}
\operatorname{Tr}_2Q&=\frac u2e+\frac d2f,\\
\operatorname{Tr}_1Q&=\frac u2e+\frac d2f.
\end{aligned}} \tag{7}
\]
In particular,
\[
\begin{aligned}
\operatorname{Tr}(MQM)&=ru,\\
\operatorname{Tr}(FQF)&=\frac{u^2}{2}. 
\end{aligned} \tag{8}
\]
The two mixed cells separately have trace \(ru/2\).

Define the \(U\otimes U\) compression and its coupling to the mixed
sector by
\[
K=FQF=FPF,\qquad C=MPF. \tag{9}
\]
The \(F,F\) corner of \(Q^2=Q\) is
\[
K^2+C^*C=K. \tag{10}
\]
Consequently,
\[
\boxed{
\delta(P,W)
:=\frac{u^2}{2}-\operatorname{Tr}(K^2)
=\operatorname{Tr}(K-K^2)
=\|C\|_{\mathrm{HS}}^2
=\frac12\|[P,F]\|_{\mathrm{HS}}^2
\geq0.} \tag{11}
\]

This proves the following exact equivalences:
\[
\boxed{
\begin{aligned}
U\otimes U\text{ is invariant}
&\Longleftrightarrow [P,F]=0\\
&\Longleftrightarrow C=0\\
&\Longleftrightarrow K^2=K\\
&\Longleftrightarrow
\operatorname{Tr}(K^2)=\frac{u^2}{2}\\
&\Longleftrightarrow \delta(P,W)=0.
\end{aligned}} \tag{12}
\]

Thus the known rank and marginal identities determine the first
moment of \(K\), but the desired conclusion is precisely a second
moment, or zero-variance, identity.  If it holds, then \(K\) is the
balanced projection of the complementary restriction.  If it does
not, \(K\) is only a positive contraction of trace \(u^2/2\).

## 3. An exact \(d=6,\ 4+2\) two-site limitation model

We now show that the missing variance is genuine at the level of all
two-site data.

Let
\[
V=W\oplus U,\qquad
W=\operatorname{span}\{v_0,v_1,v_2,v_3\},\qquad
U=\operatorname{span}\{v_4,v_5\}. \tag{13}
\]
On \(W\otimes W\), take the published exceptional projection
\[
P_4=\frac{I-H_4}{2}, \tag{14}
\]
where
\[
\begin{aligned}
H_4={}&-\frac1{\sqrt6}ZIZZ
-\frac1{\sqrt6}ZIJJ
-\frac1{\sqrt6}JIZJ\\
&+\frac1{\sqrt6}JIJZ
-\frac1{\sqrt3}XIXX.
\end{aligned} \tag{15}
\]

On \((W\otimes W)^\perp\), start with the following eight mutually
orthogonal coordinate vectors:
\[
\begin{gathered}
|0,4\rangle,\ |1,4\rangle,\ |3,5\rangle,\ 
|4,0\rangle,\ |4,1\rangle,\\
|5,2\rangle,\ |5,3\rangle,\ |5,5\rangle,
\end{gathered} \tag{16}
\]
and add the two orthonormal vectors
\[
\psi_1=\frac{|4,4\rangle+|2,5\rangle}{\sqrt2},
\qquad
\psi_2=\frac{|4,5\rangle+|2,4\rangle}{\sqrt2}. \tag{17}
\]
Let \(Q\) be the rank-ten orthogonal projection onto the span of
(16)--(17), and define
\[
\widetilde P=P_4\oplus Q. \tag{18}
\]

The four cells in each superposition in (17) form a \(2\times2\)
rectangle.  The two occupied diagonal cells were replaced by two
balanced superpositions.  Every row and column sum is therefore
unchanged, while the off-diagonal matrix coefficients have zero
partial trace because both tensor coordinates differ.

Direct exact calculation gives
\[
\widetilde P=\widetilde P^*=\widetilde P^2,\qquad
\operatorname{rank}\widetilde P=18, \tag{19}
\]
\[
\operatorname{Tr}_1\widetilde P
=\operatorname{Tr}_2\widetilde P=3I_6. \tag{20}
\]
Moreover, \(W\otimes W\) reduces \(\widetilde P\), and its restriction
is exactly \(P_4\), including its full three-site cubic relation.

Nevertheless,
\[
\widetilde P|4,4\rangle
=\frac12\bigl(|4,4\rangle+|2,5\rangle\bigr), \tag{21}
\]
so \(U\otimes U\) is not invariant.  In the ordered basis
\[
|4,4\rangle,\ |4,5\rangle,\ |5,4\rangle,\ |5,5\rangle
\]
its compression is
\[
K=\operatorname{diag}\left(\frac12,\frac12,0,1\right). \tag{22}
\]
Hence
\[
\operatorname{Tr}K=2=\frac{u^2}{2},\qquad
\operatorname{Tr}K^2=\frac32,\qquad
\boxed{\delta(\widetilde P,W)=\frac12.} \tag{23}
\]

For
\[
\widetilde R=qI-(1+q)\widetilde P,\qquad
q=e^{i\pi/3}, \tag{24}
\]
unitarity and the Hecke polynomial follow exactly from (19).  The
only target axiom that this limitation model fails is the ambient
three-site Yang--Baxter relation.  To make that failure independently
visible, let
\[
\mathcal D(\widetilde P)
=\widetilde P_{12}\widetilde P_{23}\widetilde P_{12}
-\widetilde P_{23}\widetilde P_{12}\widetilde P_{23}
-\frac13(\widetilde P_{12}-\widetilde P_{23}). \tag{25}
\]
In lexicographic tensor coordinates,
\[
\left\langle 0,1,4\middle|
\mathcal D(\widetilde P)
\middle|0,0,4\right\rangle
=-\frac{\sqrt2}{48}\ne0. \tag{26}
\]

Thus \(\widetilde P\) is not a dimension-six witness.  Its purpose is
to prove sharply that the missing complementary invariance cannot be
deduced before using the spatial three-site equation.

## 4. Independent one-sided numerical falsifier

The general Grassmann search was extended by a
`one_sided_4plus2` symmetry.  It fixes the published \(H_4\) on the
16-dimensional \(W\otimes W\) cell and permits an arbitrary
signature-\((10,10)\) Hermitian involution on its full 20-dimensional
orthogonal complement.  In particular, it does **not** preserve
\(W\otimes U\), \(U\otimes W\), or \(U\otimes U\) separately.

The analytic gradient was checked by three finite differences.  The
errors decreased from \(1.04\cdot10^{-3}\) to
\(9.51\cdot10^{-6}\).  Nine reproducible complex runs were then made:

- six seeds \(26072982,\ldots,26072987\) with the pure cubic
  objective;
- three seeds \(26072988,\ldots,26072990\) with partial-trace penalty
  \(10\).

No run approached a witness.  The smallest final cubic Frobenius
residual was
\[
6.0108585346\ldots \tag{27}
\]
in the unpenalized runs; the penalized residuals were all larger than
\(6.32\).  These are failed searches, not evidence of nonexistence.
Their only role is adversarial: the broader one-sided branch did not
produce a counterexample to the possible implication
\(\delta=0\).

The complete JSONL traces include seeds, dependency versions, platform,
timestamps, raw diagnostics, and termination states:

```text
results/d6_one_sided_4plus2_runs.jsonl
results/d6_one_sided_4plus2_pt10_runs.jsonl
```

## 5. Consequence for the live proof route

For a hypothetical \(d=6\) exceptional solution containing a
square-invariant four-dimensional \(W\), the four-strand theorem gives
all hypotheses used in Section 2 with \(u=2\).  Therefore the desired
contradiction is now equivalent to proving
\[
\boxed{\delta(P,W)=0} \tag{28}
\]
from the ambient cubic relation.

No argument based only on:

- positivity or idempotence of \(P\);
- scalar one-site partial traces;
- the ranks of \(P\) and \(P_W\);
- unitarity or the two-eigenvalue Hecke polynomial; or
- the complete Yang--Baxter relation internal to \(W^{\otimes3}\)

can establish (27), because the exact model (18) has every one of
those properties and has \(\delta=1/2\).

This does not disprove the implication with the ambient cubic
relation.  It identifies the exact remaining target and prevents a
two-site multiplicative-domain or marginal-saturation argument from
silently assuming the conclusion.

## 6. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_one_sided_square_invariance.py
```

The verifier uses exact SymPy arithmetic and checks:

1. the published \(d=4\) restriction and its cubic relation;
2. the rank, projection, Hermiticity, and both scalar partial traces of
   \(\widetilde P\);
3. exact Hecke and unitarity identities for \(\widetilde R\);
4. invariance of \(W\otimes W\) and failure of invariance of
   \(U\otimes U\);
5. all four forms of the defect in (11);
6. the explicit nonzero ambient cubic coefficient (26).

The one-sided numerical gradient check is:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/d6_riemannian_search.py \
  --dimension 6 --seed 26072980 --field complex \
  --symmetry one_sided_4plus2 --initial h4_block \
  --gradient-check
```

Its raw output is in
`results/d6_one_sided_4plus2_gradient_check.txt`.  The two run families
use the same command without `--gradient-check`, with
`--max-iterations 400 --progress-every 400`, the seeds listed above,
and respectively
`--partial-trace-penalty 0` or `--partial-trace-penalty 10`.
