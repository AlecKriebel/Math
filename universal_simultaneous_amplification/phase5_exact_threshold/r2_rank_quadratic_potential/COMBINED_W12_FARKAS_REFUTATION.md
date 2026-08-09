# Exact refutation of the combined rank-`H,K_0` certificate

Date: 2026-08-08 (America/Los_Angeles)

## Status

The fitness-two certificate using arbitrary rank constants, arbitrary
rank-labelled vertex coefficients, and **independent coefficients of both
stationary internal conductance and the two-request covariance `K_0` on
every rank** is **EXACTLY REFUTED**.

The witness is a connected complete-support twelve-vertex undirected
integer-weighted graph.  This result refutes only the restricted potential
space.  It does not refute the full rank-pair certificate or the universal
fitness-two fixation bound.  Indeed, an independent exact harmonic solve
proves that the witness graph itself is strictly dB-suppressing at fitness
two.

## 1. Restricted primal

Let `P` be the loopless reversible request kernel, `pi` its stationary
distribution, `Pi=diag(pi)`, and

\[
 K_0=\Pi-P^T\Pi P,\qquad
 E_\pi(S)=\sum_{\{i,j\}\subseteq S}\pi_iP_{ij}.            \tag{1}
\]

For `k=|S|` and mutant indicator `s`, the refuted potential space is

\[
 F(S)=a_k+\sum_{v\in S}b_{k,v}
      +\lambda_kE_\pi(S)+\theta_k s^TK_0s.                 \tag{2}
\]

The two quadratic columns are affine in the vertex columns at ranks one
and `n-1`, so independent copies are required only on ranks two through
`n-2`.  With `F(empty)=0`, define

\[
 p_{W_{12}}(P)=\min {1\over n}\sum_iF(\{i\})              \tag{3}
\]

subject to

\[
 F(V)=1,\qquad LF(S)\le0\quad(empty\ne S\ne V).           \tag{4}
\]

The proposed combined certificate would require

\[
 p_{W_{12}}(P)\le\rho_{\rm dB}(K_n,2)                    \tag{5}
\]

for every finite reversible loopless kernel.

## 2. Exact graph and quotient

Partition the vertices into five classes of sizes

\[
 (1,1,2,3,5),                                              \tag{6}
\]

and assign every edge between distinct vertices in classes `i,j` the
integer weight

\[
W=\begin{pmatrix}
1000&5000000000&10000&30&3\\
5000000000&2500&350&44&1200\\
10000&350&26000&4800&80000000\\
30&44&4800&6000000&30000000\\
3&1200&80000000&30000000&10000000
\end{pmatrix}.                                              \tag{7}
\]

The five weighted degrees are

\[
5000020105,\quad5000006832,\quad400050750,\quad
162009674,\quad290001203.                                  \tag{8}
\]

Every intervertex weight is positive.  Within-class automorphisms reduce
the subset chain exactly to 286 transient count states.  The invariant
affine span has five columns on each of ranks one through eleven, while the
two quadratic columns contribute on ranks two through ten.  With the full
boundary column, the exact dimension is

\[
 5\cdot11+2\cdot9+1=74.                                   \tag{9}
\]

The verifier separately constructs the twelve labelled vertices and
checks every quotient drift row against the labelled update rule.

## 3. Exact primal/dual pair

Let `D` be the exact 286-by-74 normalized drift matrix, `c` the uniform
singleton objective, and `f` the full-state boundary.  The primal and dual
are

\[
 \min c^Tx\quad\text{subject to }Dx\le0,\ f^Tx=1,         \tag{10}
\]

\[
 \max z\quad\text{subject to }y\ge0,\ c+D^Ty-zf=0.        \tag{11}
\]

The exact verifier stores 73 active count states.  The corresponding 74
dual unknowns solve a nonsingular rational system, and all 73 state weights
are strictly positive.  Independently, the active rows plus the boundary
reconstruct a rational primal potential.  Every one of its 286 drift
inequalities is nonpositive and its objective equals the dual value.
Consequently

\[
 p_{W_{12}}(P)=0.4600442069423893447745517\ldots.          \tag{12}
\]

The complete baseline is

\[
 \rho_{\rm dB}(K_{12},2)={2816\over6141}
 =0.45855723823481517668\ldots.                            \tag{13}
\]

Exact subtraction gives

\[
 \boxed{
 p_{W_{12}}(P)-\rho_{\rm dB}(K_{12},2)
 =0.001486968707574168093229390\ldots>0.}                 \tag{14}
\]

The reduced numerator and denominator in `(14)` have 3485 and 3487
decimal digits.  The SHA-256 identifier of canonical
`numerator/denominator` text is

```text
0cc5256b94a446ce0a8d2f8174e8cc081f5c3a0b25ea683d977808f044f94a22
```

The digest is only an identifier; the verifier checks the sign by exact
integer comparison.

## 4. Exact non-conflation with true fixation

The same replay independently builds and solves the full 286-state
quotient harmonic system.  Uniform-singleton fixation is

\[
 \rho_{\rm dB}(G,2)=0.4215620895939539989012090\ldots,     \tag{15}
\]

and exact subtraction proves

\[
 \rho_{\rm dB}(K_{12},2)-\rho_{\rm dB}(G,2)
 =0.03699514864086117778011324\ldots>0.                   \tag{16}
\]

The canonical SHA-256 identifier of the exact margin in `(16)` is

```text
15fdf227d4184ee288596e3d92f7ea65be17c0e0e87b9d60a01ecd1d8d190ae1
```

Thus the witness graph is exactly dB-suppressing at fitness two.  The
failure is solely a failure of the compressed proof space.

## 5. Consequence

The exact dual description of `W_12` consists of rank mass, every
rank-labelled one-mark balance, and the two rank storage recurrences for
`E_pi` and `K_0`.  The counterexample proves that these balances do not
imply the complete endpoint bound.  In particular, no Schur or Riccati
argument using only those two scalar pair contractions can close the
universal theorem.

The smallest live quadratic certificate is now the full rank-pair matrix,
equivalently every rank-labelled two-mark balance.  A successful proof must
retain at least one genuinely additional pair direction beyond `E_pi` and
`K_0`; identifying the minimal universal enlargement remains open.

## 6. Replay

From the repository root:

```text
.venv/bin/python universal_simultaneous_amplification/phase5_exact_threshold/r2_rank_quadratic_potential/verify_combined_w12_farkas_refutation.py
```

The replay checks all labelled and quotient drift rows, reconstructs the
strictly positive rational dual and matching rational primal, verifies all
drift signs, proves the strict restricted excess over `2816/6141`, and
solves the true fixation system exactly.
