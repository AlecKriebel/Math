# Exact rational two-box branch intertwiners

## Result

Every local branch in the degree-three-to-degree-two DTH marginal now has an
explicit rational model.  Across the eight local (S_7) shapes and five local
(S_5) shapes there are exactly

\[
\boxed{30\text{ channels}=18\text{ horizontal}+12\text{ vertical}.}
\tag{1}
\]

For each channel the verifier constructs an integral intertwiner (J) and a
positive rational scalar (c_J) such that

\[
\rho_7(g)J=J\rho_5(g)
\qquad(g\in S_5),
\tag{2}
\]

\[
\rho_7((5\,6))J=
\begin{cases}
+J,&\text{horizontal},\\
-J,&\text{vertical},
\end{cases}
\tag{3}
\]

and

\[
\boxed{J^{\mathsf T}G_7J=c_JG_5.}
\tag{4}
\]

Thus (J/\sqrt{c_J}) is the physical isometric branch, but exact marginal
calculations never need to adjoin the square root: use the rational Kraus
matrix (J) and multiply its quadratic contribution by (1/c_J).

## Construction

Use integral standard-polytabloid bases in every local Specht module.  Their
Gram matrices (G_7,G_5) are integral and positive definite.  Exact physical
adjacent-transposition matrices are recovered from

\[
R_i=G^{-1}\bigl(\langle e_a,(i\ i+1)e_b\rangle\bigr)_{a,b}.
\]

All entries of every (R_i) are integers in the chosen bases.

For a source-target shape pair, apply the Reynolds projector to the
intertwiner space:

\[
\mathcal R(X)
=\sum_{g\in S_5}\rho_7(g)X\rho_5(g^{-1}).
\tag{5}
\]

Its image has dimension one or two according to the exact two-box branching
census.  Applying

\[
\frac{I\pm\rho_7((5\,6))}{2}
\]

gives the horizontal and vertical channels.  Primitive integer scaling is
chosen deterministically.  Schur's lemma implies (4); the verifier checks the
matrix identity itself rather than merely checking its trace.

## Exact normalization table

Indices refer to the established ordered lists

\[
\begin{aligned}
S_7:;&(7),(6,1),(5,2),(5,1,1),(4,3),(4,2,1),(3,3,1),(3,2,2),\\
S_5:;&(5),(4,1),(3,2),(3,1,1),(2,2,1).
\end{aligned}
\]

The deterministic primitive intertwiners have the following (c_J):

\[
\begin{array}{c|c|c|r@{\qquad}c|c|c|r}
S_7&S_5&\text{type}&c_J&S_7&S_5&\text{type}&c_J\\ \hline
0&0&H&1&1&0&H&70\\
1&0&V&2&1&1&H&1\\
2&0&H&150&2&1&H&30\\
2&1&V&2&2&2&H&1\\
3&0&V&70&3&1&H&140\\
3&1&V&4&3&3&H&1\\
4&1&H&18&4&2&H&6\\
4&2&V&2&5&1&H&2160\\
5&1&V&720&5&2&H&72\\
5&2&V&12&5&3&H&4\\
5&3&V&2&5&4&H&1\\
6&2&H&40&6&2&V&80\\
6&3&H&12&6&4&V&2\\
7&2&H&320&7&3&V&16\\
7&4&H&8&7&4&V&4
\end{array}
\tag{6}

## Consequence for the full rational map

Let (B_\Lambda) be the rational post-Omega source basis from the seed-Gram
construction and (K_\kappa) the existing rational target basis.  Replacing
each normalized branch by the primitive (J_p) above makes the exact
coefficient map

\[
C_{\Lambda,\kappa,p}
=(K_\kappa^{\mathsf T}G_\kappa K_\kappa)^{-1}
K_\kappa^{\mathsf T}J_p^{\mathsf T}G_\Lambda B_\Lambda
\tag{7}
\]

and its contribution carries the rational weight

\[
\frac{d_{\Lambda,\kappa}}
{c_{J_{p,1}}c_{J_{p,2}}c_{J_{p,3}}}.
\tag{8}
\]

Equations (7)--(8), the 720-term rational Grassmann projector, and the
rank-at-most-three rational Omega deflation together remove every algebraic
orthonormalization from the exact fixed-marginal system.

## Verification

`verification/verify_dth_level2_rational_branches.py` constructs all local
polytabloid modules and all 30 intertwiners from scratch, checks (2)--(4), and
prints the pinned normalization table (6).  It uses exact integer and SymPy
rational arithmetic; floating point is used only to select columns of a
rank-at-most-two Reynolds range, after which every claimed identity is
replayed exactly.
