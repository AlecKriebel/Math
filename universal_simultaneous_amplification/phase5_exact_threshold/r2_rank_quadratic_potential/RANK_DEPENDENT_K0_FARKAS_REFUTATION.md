# Exact refutation of the rank-dependent-`K_0` certificate

Date: 2026-08-08 (America/Los_Angeles)

## Status

The fitness-two certificate using arbitrary rank constants, arbitrary
rank-labelled vertex coefficients, and **one independent coefficient of
the two-request covariance form `K_0` on every rank** is **EXACTLY
REFUTED**.

The counterexample is a connected complete-support nine-vertex undirected
integer-weighted graph.  This result refutes only the restricted potential
space.  It is not a fixation counterexample and does not refute either the
larger rank-`H` plus rank-`K_0` certificate or the full rank-pair conjecture.

## 1. Restricted primal

Let `P` be the loopless reversible request kernel, let `pi` be its
stationary distribution, put `Pi=diag(pi)`, and define

\[
 K_0=\Pi-P^T\Pi P.                                        \tag{1}
\]

For a mutant indicator `s`, reversibility gives the nonnegative form

\[
 s^TK_0s=\sum_v\pi_vx_v(1-x_v),\qquad x=Ps.              \tag{2}
\]

The refuted potential space is

\[
 F(S)=a_k+\sum_{v\in S}b_{k,v}+\lambda_k s^TK_0s,
 \qquad k=|S|.                                             \tag{3}
\]

The quadratic column is affine in the vertex columns on ranks one and
`n-1`, so only ranks two through `n-2` need independent copies.  With
`F(empty)=0`, define

\[
 p_{\rm rank-K_0}(P)=\min {1\over n}\sum_iF(\{i\})        \tag{4}
\]

subject to

\[
 F(V)=1,\qquad LF(S)\le0\quad(empty\ne S\ne V).           \tag{5}
\]

A universal certificate in this space would require

\[
 p_{\rm rank-K_0}(P)\le\rho_{\rm dB}(K_n,2).             \tag{6}
\]

## 2. Exact graph and quotient

Partition the vertices into five classes of sizes

\[
 (1,1,2,2,3),                                              \tag{7}
\]

and assign every edge between distinct vertices in classes `i,j` the
integer weight

\[
W=\begin{pmatrix}
10^6&3\cdot10^{11}&7\cdot10^{10}&4\cdot10^5&3\cdot10^7\\
3\cdot10^{11}&10&4\cdot10^5&5\cdot10^{10}&5\\
7\cdot10^{10}&4\cdot10^5&3\cdot10^6&11\cdot10^5&9\cdot10^{10}\\
4\cdot10^5&5\cdot10^{10}&11\cdot10^5&17\cdot10^{10}&5\cdot10^{10}\\
3\cdot10^7&5&9\cdot10^{10}&5\cdot10^{10}&36\cdot10^9
\end{pmatrix}.                                             \tag{8}
\]

The verifier stores these weights as integers only.  The five weighted
degrees are

\[
\begin{aligned}
&440090800000,\quad400000800015,\quad340005600000,\\
&370002600000,\quad352030000005.
\end{aligned}                                               \tag{9}
\]

All intervertex weights are positive, so the graph is connected.  Its
within-class automorphisms reduce the subset chain exactly to 142 transient
count states.

On each rank the invariant affine vertex span has dimension five.  The
`K_0` column is redundant at ranks one and eight and contributes one
independent column on ranks two through seven.  Including the full-state
boundary gives

\[
 5\cdot8+6+1=47.                                           \tag{10}
\]

The verifier also reconstructs every quotient drift row directly from the
nine labelled vertices.

## 3. Exact primal/dual pair

Let `D` be the exact 142-by-47 normalized drift matrix, `c` the uniform
singleton objective, and `f` the full-state boundary.  The primal and dual
are

\[
 \min c^Tx\quad\text{subject to }Dx\le0,\ f^Tx=1,         \tag{11}
\]

\[
 \max z\quad\text{subject to }y\ge0,\ c+D^Ty-zf=0.        \tag{12}
\]

The exact verifier stores 46 active count states.  The corresponding 47
dual unknowns (46 weights and `z`) solve a nonsingular rational system, and
all 46 weights are strictly positive.  Independently, the same active drift
rows plus the boundary reconstruct a rational primal potential.  Every one
of its 142 drift inequalities is nonpositive and its objective equals the
dual value.  Therefore

\[
 p_{\rm rank-K_0}(P)
 =0.4539329228798728451964329\ldots.                       \tag{13}
\]

The complete baseline is

\[
 \rho_{\rm dB}(K_9,2)={1024\over2295}
 =0.44618736383442265795\ldots.                            \tag{14}
\]

Exact subtraction gives

\[
 \boxed{
 p_{\rm rank-K_0}(P)-\rho_{\rm dB}(K_9,2)
 =0.007745559045450187244363190\ldots>0.}                 \tag{15}
\]

The reduced numerator and denominator in `(15)` have 1798 and 1800 decimal
digits.  The SHA-256 of canonical `numerator/denominator` text is

```text
49230606abeb30eafdf1dbe7bfd96b7e35f80bdff7eb7b15efbd759706c4534c
```

The digest is only an identifier; the verifier checks the sign by exact
integer comparison.

## 4. Consequence

Neither canonical quadratic direction is sufficient alone, even when it
is rank dependent and every vertex correction is retained:

- rank-`H` alone is refuted by the independent exact graph in
  `RANK_DEPENDENT_CONDUCTANCE_FARKAS_REFUTATION.md`;
- rank-`K_0` alone is refuted by `(7)--(15)`.

The smallest surviving compressed space must retain both directions on
every rank,

\[
 E_\pi(S),\qquad s^T(\Pi-P^T\Pi P)s,                       \tag{16}
\]

together with all rank-labelled one-marks.  The present certificate says
nothing about feasibility of that combined space.  The full rank-pair
matrix remains the fallback.

## 5. Replay

From the repository root:

```text
.venv/bin/python universal_simultaneous_amplification/phase5_exact_threshold/r2_rank_quadratic_potential/verify_rank_dependent_k0_farkas_refutation.py
```

The replay checks the labelled update rule against all quotient rows,
reconstructs the strictly positive rational dual and matching rational
primal independently, verifies all drift signs, and compares the objective
with `1024/2295` exactly.
