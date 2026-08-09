# Exact refutation of the single-global-conductance certificate

Date: 2026-08-08 (America/Los_Angeles)

## Status

The fitness-two certificate using arbitrary rank constants, arbitrary
rank-labelled vertex coefficients, and **one global coefficient** of the
reversible internal conductance is **EXACTLY REFUTED**.

The counterexample is a connected complete-support 17-vertex undirected
integer-weighted graph.  Its true dB fixation probability is below the
complete baseline, as independently proved in the additive Farkas audit.
Thus this result refutes only the restricted potential space.  It is not a
fixation counterexample and does not refute the full rank-pair conjecture.

## 1. Restricted primal

Let `P` be the row-stochastic replacement kernel of a reversible loopless
graph, let `pi` be its stationary law, and put

\[
 E_\pi(S)=\sum_{\{i,j\}\subseteq S}\pi_iP_{ij}.
\]

On every nonempty rank `k`, consider

\[
 F(S)=a_k+\sum_{v\in S}b_{k,v}+\lambda E_\pi(S),             \tag{1}
\]

where `lambda` is one scalar shared by all ranks.  Fix `F(empty)=0` and
solve

\[
 p_{\rm glob}(P)=\min {1\over n}\sum_iF(\{i\})              \tag{2}
\]

subject to

\[
 F(V)=1,\qquad LF(S)\le0\quad(empty\ne S\ne V).             \tag{3}
\]

No separate constraints `F(S)>=0` are imposed.  They follow from the
maximum principle, but omitting them makes the refutation stronger.  A
certificate of complete-graph maximality in this space would require

\[
 p_{\rm glob}(P)\le\rho_{\rm dB}(K_n,2).                    \tag{4}
\]

In the optional coordinates `G(S)=2^{|S|}F(S)`, the last term in `(1)` is
the single geometric conductance profile.  Thus `(1)` is precisely the
corrected global-`H` conjecture, not the earlier mistyped `2^k` version in
the original fixation coordinates.

## 2. Exact graph and quotient

Partition the vertices into classes of sizes

\[
 (m_1,m_2,m_3)=(2,5,10),                                   \tag{5}
\]

and assign each edge between distinct vertices in classes `i,j` the weight

\[
 W=\begin{pmatrix}
 20000000&15&5\\
 15&9&4500\\
 5&4500&150
 \end{pmatrix}.                                             \tag{6}
\]

The three weighted degrees are

\[
 20000125,\qquad45066,\qquad23860.                           \tag{7}
\]

All intervertex weights are positive.  The graph is connected and its
automorphism group contains `S_2 x S_5 x S_10`.

Average any feasible labelled potential over this automorphism group.
Writing a state as the mutant-count triple `(s_1,s_2,s_3)`, this gives 196
transient state orbits.  On a fixed rank,

\[
 s_3=k-s_1-s_2,
\]

so the invariant rank-labelled affine space is spanned by `1,s_1,s_2`.
There are three columns on each rank `1,...,16`, one full-rank boundary
column, and one global internal-conductance column.  The restricted invariant
function space therefore has exact dimension

\[
 3\cdot16+1+1=50.                                          \tag{8}
\]

The verifier reconstructs every quotient drift row independently from all
17 vertex labels and checks exact agreement.

## 3. Exact primal/dual pair

Let `D` be the 196-by-50 matrix of generator rows, each divided by its
positive total type-change rate.  Let `c` be the uniform-singleton objective
and `f` the full-state boundary row.  The primal is

\[
 \min c^Tx\quad\hbox{subject to}\quad Dx\le0,\quad f^Tx=1. \tag{9}
\]

Its weak dual is

\[
 \max z\quad\hbox{subject to}\quad
 y\ge0,\qquad c+D^Ty-zf=0.                                 \tag{10}
\]

Indeed `(10)` and `(9)` imply

\[
 c^Tx=z-y^TDx\ge z.                                        \tag{11}
\]

The exact verifier stores a 49-state support.  The 50 equations in `(10)`
for its 49 weights and `z` form a nonsingular rational system.  Exact FLINT
elimination gives all 49 weights strictly positive.  Independently, the 49
active drift equalities together with `f^Tx=1` give a nonsingular 50-by-50
primal system.  Its solution satisfies all 196 drift inequalities and has
the same objective as the dual.

Thus strong equality is verified directly, without relying on a floating
optimizer:

\[
 p_{\rm glob}(P)
 =0.4767015236181397039926\ldots.                           \tag{12}
\]

The complete baseline is

\[
 \rho_{\rm dB}(K_{17},2)={524288\over1114095}
 =0.47059541601030432719\ldots.                             \tag{13}
\]

Exact rational subtraction gives

\[
 \boxed{
 p_{\rm glob}(P)-\rho_{\rm dB}(K_{17},2)
 =0.006106107607835376264719\ldots>0.}                     \tag{14}
\]

The numerator and denominator of the reduced rational in `(14)` have 719
and 721 decimal digits.  Its canonical `numerator/denominator` SHA-256 is

```text
343421077b046ee95de10f433f0c385b6242bebae9f28e5bb28a2a258339ed13
```

The digest is only an identifier.  The strict sign is checked by exact
integer comparison in the verifier.

## 4. Consequence for the live route

The geometric conductance coboundary is structurally canonical, but one
global coefficient does not close the endpoint theorem even after every
rank constant and every rank-labelled vertex correction is allowed.  Any
surviving low-degree certificate must retain at least one of:

1. a genuinely rank-dependent conductance/internal-edge coefficient;
2. more than one graph-natural pair statistic; or
3. the full rank-labelled pair moment matrix.

This exact refutation also explains why the full matrix collision balance
cannot be replaced by its single fixed conductance contraction.

## 5. Replay

From the repository root:

```text
.venv/bin/python universal_simultaneous_amplification/phase5_exact_threshold/r2_rank_quadratic_potential/verify_global_conductance_farkas_refutation.py
```

The replay performs both verification paths:

- labelled update rule to 196-row quotient, followed by exact positive dual
  substitution;
- independent exact matching primal reconstruction, all-state drift checks,
  and exact comparison with the complete baseline.
