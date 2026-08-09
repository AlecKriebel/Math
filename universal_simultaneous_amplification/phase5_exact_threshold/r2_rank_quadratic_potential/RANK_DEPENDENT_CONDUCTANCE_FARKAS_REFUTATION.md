# Exact refutation of the rank-dependent-conductance certificate

Date: 2026-08-08 (America/Los_Angeles)

## Status

The fitness-two certificate using arbitrary rank constants, arbitrary
rank-labelled vertex coefficients, and **one independent coefficient of
reversible internal conductance on every rank** is **EXACTLY REFUTED**.

The counterexample is a connected complete-support nine-vertex undirected
integer-weighted graph.  This result refutes only the restricted potential
space.  It is not a fixation counterexample and does not refute either the
larger rank-`H` plus rank-`K_0` certificate or the full rank-pair conjecture.

## 1. Restricted primal

For a reversible loopless graph, put

\[
 E_\pi(S)=\sum_{\{i,j\}\subseteq S}\pi_iP_{ij}.
\]

The refuted potential space is

\[
 F(S)=a_k+\sum_{v\in S}b_{k,v}+\lambda_kE_\pi(S),
 \qquad k=|S|,                                               \tag{1}
\]

where `lambda_k` is independent on every rank.  With `F(empty)=0`, define

\[
 p_{\rm rank-H}(P)=\min {1\over n}\sum_iF(\{i\})             \tag{2}
\]

subject to

\[
 F(V)=1,\qquad LF(S)\le0\quad(empty\ne S\ne V).             \tag{3}
\]

A universal certificate in this space would require

\[
 p_{\rm rank-H}(P)\le\rho_{\rm dB}(K_n,2).                  \tag{4}
\]

## 2. Exact graph and quotient

Partition the vertices into five classes of sizes

\[
 (1,1,2,2,3),                                               \tag{5}
\]

and assign every edge between distinct vertices in classes `i,j` the
integer weight

\[
W=\begin{pmatrix}
10^9&10^{22}&2\cdot10^9&5\cdot10^{10}&3000\\
10^{22}&10^9&4\cdot10^8&2500000000&1\\
2\cdot10^9&4\cdot10^8&4\cdot10^{16}&45\cdot10^{15}&450000\\
5\cdot10^{10}&2500000000&45\cdot10^{15}&4\cdot10^8&1750000000\\
3000&1&450000&1750000000&8\cdot10^9
\end{pmatrix}.                                              \tag{6}
\]

The five weighted degrees are

\[
\begin{aligned}
&10000000000104000009000,\quad10000000000005800000003,\\
&130000002401350000,\quad90000058150000000,\quad19500903001.
\end{aligned}                                                \tag{7}
\]

All intervertex weights are positive, so the graph is connected.  Its
within-class automorphisms reduce the subset chain exactly to 142 transient
count states.

On each rank the invariant affine vertex span has dimension five.  The
internal-conductance column is zero/redundant at rank one and is affine in
the missing-vertex class at rank eight; it contributes one independent
column on ranks two through seven.  Including the full-state boundary gives

\[
 5\cdot8+6+1=47                                             \tag{8}
\]

independent function columns.  The verifier also reconstructs every
quotient drift row directly from the nine labelled vertices.

## 3. Exact primal/dual pair

Let `D` be the exact 142-by-47 normalized drift matrix, `c` the uniform
singleton objective, and `f` the full-state boundary.  The primal and dual
are

\[
 \min c^Tx\quad\text{subject to }Dx\le0,\ f^Tx=1,           \tag{9}
\]

\[
 \max z\quad\text{subject to }y\ge0,\ c+D^Ty-zf=0.          \tag{10}
\]

The exact verifier stores 46 active count states.  The corresponding 47
dual unknowns (46 weights and `z`) solve a nonsingular rational system, and
all 46 weights are strictly positive.  Independently, the same active drift
rows plus the boundary reconstruct a rational primal potential.  Every one
of its 142 drift inequalities is nonpositive and its objective equals the
dual value.  Therefore

\[
 p_{\rm rank-H}(P)
 =0.4463122484779187239833287\ldots.                        \tag{11}
\]

The complete baseline is

\[
 \rho_{\rm dB}(K_9,2)={1024\over2295}
 =0.44618736383442265795\ldots.                             \tag{12}
\]

Exact subtraction gives

\[
 \boxed{
 p_{\rm rank-H}(P)-\rho_{\rm dB}(K_9,2)
 =0.0001248846434960660312589405\ldots>0.}                 \tag{13}
\]

The reduced numerator and denominator in `(13)` have 2875 and 2879 decimal
digits.  The SHA-256 of canonical `numerator/denominator` text is

```text
54157ebc0d0153a2d86dc928f47495f688d2104b3971ff5cf0127e838ccb9f76
```

The digest is only an identifier; the verifier checks the sign by exact
integer comparison.

## 4. Consequence

One graph-natural pair direction per rank is still not sufficient, even
when every vertex correction is retained.  The live compressed route must
now contain at least one additional independent pair direction.  The
canonical next space is rank constants plus rank-labelled vertices plus
both

\[
 E_\pi(S),\qquad s^T(\Pi-P^T\Pi P)s                         \tag{14}
\]

on every rank.  Numerically, the `K_0` direction repairs this exact witness
with large slack, but that observation is not a universal theorem.

## 5. Replay

From the repository root:

```text
.venv/bin/python universal_simultaneous_amplification/phase5_exact_threshold/r2_rank_quadratic_potential/verify_rank_dependent_conductance_farkas_refutation.py
```

The replay checks the labelled update rule against all quotient rows,
reconstructs the strictly positive rational dual and matching rational
primal independently, verifies all drift signs, and compares the objective
with `1024/2295` exactly.
