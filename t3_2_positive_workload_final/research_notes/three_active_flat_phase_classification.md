# Exact classification of affine-feasible three-active tier failures

## 1. Scope and claim status

This note classifies every **all-active** tier obstruction that remains after
the finite structural branches, the universal Anderson--Kim tier test, and
the affine-stoichiometric feasibility test. Here all three populations tend
to infinity and the capped availability vector is therefore \((2,2,2)\).

The classification and the directional generator estimate in Section 5 are
proved. They are deliberately not stated as a recurrence theorem. The
remaining interface is a multiple-cone/Green-occupation gluing theorem: a
state sequence on which one member of a finite family of proper linear
functions has negative drift does not, by itself, supply one global Foster
function.

The exact enumeration is implemented in
*src/three_active_flat_phase.py* and tested by
*tests/test_three_active_flat_phase.py*.

## 2. Definitions

Let

\[
 \mathcal C_2=\{0,A,B,C,2A,2B,2C,A+B,A+C,B+C\}
\]

and let \(P=(L_0,L_1)\) be an ordered pair of linkage supports from the
residual atlas. Each actual reaction graph on \(L_i\) is assumed strongly
connected and all its rate constants are positive. For a tier descriptor
\(d\), let \(G_d(P)\) be the global top D-tier restricted to
\(L_0\cup L_1\), and let \(E_d(P)\) be the global top S-tier.

For an all-active descriptor, every complex is eventually enabled. Hence

\[
 E_d(P)=G_d(P).
\tag{2.1}
\]

Choose the primitive positive integral representative
\(w=(w_A,w_B,w_C)\) of the descriptor and put

\[
 H_w(x)=w\cdot x.
\tag{2.2}
\]

The finite descriptor construction is exact for arbitrary multiscale tier
sequences: equal blocks encode finite positive monomial ratios, and strict
blocks encode ratios tending to infinity. The vector \(w\) is only a
rational representative of that preorder; no assumption of polynomially
related population scales is made.

## 3. Whole-top geometry

### Proposition 3.1 (unique whole-top linkage)

For every affine-feasible all-active failed incidence \((P,d)\), exactly one
of the two linkages is contained in \(G_d(P)\), and the other is disjoint
from \(G_d(P)\).

#### Proof

For a linkage \(L\), write \(K_L=L\cap G_d(P)\). Because of (2.1), the
universal arbitrary-orientation condition is satisfied whenever

\[
 \varnothing\ne K_L\subsetneq L.
\]

Consequently failure implies, separately for each linkage,
\(K_L=\varnothing\) or \(K_L=L\). The global top tier is nonempty, so at
least one linkage is wholly top.

The exact certificate finds full stoichiometric rank three for all 1,269
incidences. If both linkages were wholly top, every reaction vector
\(y'-y\) would satisfy \(w\cdot(y'-y)=0\). The full stoichiometric space
would then lie in the two-dimensional plane \(w^\perp\), contradicting rank
three. Thus exactly one linkage is wholly top. \(\square\)

Call this linkage \(T\), and call the other linkage \(R\). Proposition 3.1
immediately gives

\[
 H_w(y)=h_*\quad(y\in T),
 \qquad
 H_w(z)<h_*\quad(z\in R).
\tag{3.1}
\]

In particular every reaction in \(T\) is exactly \(H_w\)-neutral, for every
orientation and every rate vector. Also \(H_w\) is a strictly positive
proper workload on the full state space. The isolated \(T\)-dynamics stays
on the finite shell

\[
 \{x\in\mathbb N_0^3:H_w(x)=m\}.
\tag{3.2}
\]

Finiteness of (3.2) is a structural fact, but it is not a uniform mixing or
Poisson-corrector estimate as \(m\to\infty\).

## 4. Exact enumeration

There are 1,269 affine-feasible failed incidences on 403 distinct ordered
support pairs:

| class | incidences | distinct pairs |
|---|---:|---:|
| positive-active-invariant residual | 1,263 | 401 |
| signed residual | 6 | 2 |
| total | 1,269 | 403 |

They use 39 distinct all-positive descriptor weights. The whole-top side is
the shielded linkage in 1,233 incidences and the available linkage in 36.
Every full network has stoichiometric rank three. Its full deficiency
histogram is

\[
 \delta=1:668,\quad
 \delta=2:410,\quad
 \delta=3:155,\quad
 \delta=4:33,\quad
 \delta=5:3.
\tag{4.1}
\]

There are only 35 whole-top supports, or 15 orbits under permutation of the
three species. If \(r_T\) and \(\delta_T\) denote the internal rank and
deficiency of the one-linkage top phase, exactly five shapes occur:

| \(r_T\) | \(\delta_T\) | \(|T|\) | incidences | top supports |
|---:|---:|---:|---:|---:|
| 1 | 0 | 2 | 966 | 8 |
| 1 | 1 | 3 | 279 | 3 |
| 2 | 1 | 4 | 17 | 17 |
| 2 | 2 | 5 | 6 | 6 |
| 2 | 3 | 6 | 1 | 1 |

### 4.1 Rank-one supports

The eight deficiency-zero two-node supports are

\[
\begin{gathered}
 \{2A,2B\},\ \{2A,A+B\},\ \{2A,B+C\},\
 \{2B,A+B\},\\
 \{A,B+C\},\ \{A+C,B+C\},\ \{B,2A\},\ \{B,A+C\}.
\end{gathered}
\tag{4.2}
\]

The three rank-one deficiency-one supports are

\[
 \{2A,2B,A+B\},\qquad
 \{2A,2C,A+C\},\qquad
 \{2B,2C,B+C\}.
\tag{4.3}
\]

### 4.2 Rank-two supports

Write

\[
 Q=\{2A,2B,2C,A+B,A+C,B+C\}.
\tag{4.4}
\]

The 17 four-node supports consist of every four-element subset of \(Q\),
together with exactly two nonquadratic exceptions,

\[
 \{A,2B,2C,B+C\},
 \qquad
 \{B,2A,2C,A+C\}.
\tag{4.5}
\]

The six five-node supports are exactly the five-element subsets of \(Q\),
and the unique six-node support is \(Q\) itself. Thus all rank-two top
supports are entirely quadratic except the two supports in (4.5).

No recurrence conclusion is inferred from a top support's deficiency. In
particular, the 279 rank-one deficiency-one incidences and the 24 rank-two
positive-deficiency incidences remain genuine analytic interfaces.

## 5. A proved directional physical-time estimate

The whole-top geometry yields more than a support classification. It gives
an exact drift estimate in the descriptor workload and automatically ignores
arbitrarily many faster neutral jumps.

### Proposition 5.1 (directional linear drift)

Fix one incidence \((P,d)\), any strongly connected orientations of its two
linkages, and any positive rate constants. Let \(x_n\) be any tier sequence
realizing \(d\). Then

\[
 \mathcal L H_w(x_n)\longrightarrow-\infty.
\tag{5.1}
\]

More precisely, let

\[
 m=\max_{y\in R}w\cdot y,
 \qquad M=\{y\in R:w\cdot y=m\},
\tag{5.2}
\]

choose \(y_0\in M\), and put \(r_n=x_n^{\underline{y_0}}\). There is a
constant \(\eta>0\), depending on the directed reaction graph, rates, and
the limiting tied-tier ratios of the sequence, such that

\[
 \mathcal L H_w(x_n)=-\eta r_n+o(r_n),
 \qquad r_n\longrightarrow\infty.
\tag{5.3}
\]

#### Proof

The contribution of \(T\) is identically zero by (3.1). For a source
\(y\in R\), define its total workload coefficient

\[
 b_y=\sum_{y\to z}\kappa_{yz}\,w\cdot(z-y),
\tag{5.4}
\]

where the sum runs over all outgoing reactions in the chosen orientation.
Every target of a source \(y\in M\) has workload at most \(m\), and hence
\(b_y\le0\).

The set \(M\) is a nonempty proper subset of \(R\). Indeed, if all of \(R\)
had the same \(w\)-workload, then both linkage stoichiometric spaces would
lie in \(w^\perp\), contradicting full rank three. Strong connectivity of
\(R\) forces at least one directed edge from \(M\) to \(R\setminus M\).
Its workload change is strictly negative, so \(b_y<0\) for at least one
\(y\in M\).

All complexes are enabled along an all-active sequence. Since the sources
in \(M\) occupy one D-tier,

\[
 \frac{x_n^{\underline y}}{r_n}\longrightarrow\rho_y\in(0,\infty)
 \quad(y\in M),
 \qquad
 \frac{x_n^{\underline y}}{r_n}\longrightarrow0
 \quad(y\in R\setminus M).
\tag{5.5}
\]

Therefore

\[
 \frac{\mathcal L H_w(x_n)}{r_n}
 =\sum_{y\in M}\rho_yb_y+o(1)
 =-\eta+o(1),
 \qquad
 \eta=-\sum_{y\in M}\rho_yb_y>0.
\tag{5.6}
\]

Finally \(M\) cannot contain only the zero complex: \(w>0\), \(R\) has at
least two distinct complexes, and \(M\) is its maximal workload level.
Thus \(y_0\ne0\); since all three populations tend to infinity,
\(r_n\to\infty\). Equations (5.3) and (5.1) follow. \(\square\)

The estimate is unconditioned and is in physical time. It does not use a
trace, an embedded jump count, a finite inactive-coordinate box, a stationary
average of top-phase return durations, or deletion of reactions. Every top
reaction contributes exactly zero to \(H_w\), no matter how often it fires.

## 6. Why Proposition 5.1 is not yet a global recurrence theorem

The weight \(w\) in Proposition 5.1 is selected by the asymptotic tier cone.
A single network may have several feasible failed cones with different
weights. The proposition therefore establishes

\[
 \text{for every realizing divergent sequence, some proper }H_w
 \text{ has }\mathcal LH_w\to-\infty,
\tag{6.1}
\]

not the existence of one proper \(H\) satisfying a Foster inequality outside
a finite set.

The usual elementary combinations do not supply the missing implication:

- a positive linear combination introduces nonzero contributions from a
  linkage that was neutral only for its own descriptor weight;
- for \(H=\min_j H_{w_j}\), one has the useful inequality
  \(\mathcal LH(x)\le\mathcal LH_{w_j}(x)\) only when \(j\) minimizes at
  \(x\), and no certificate presently identifies that minimizer with the
  state's tier descriptor;
- a piecewise choice \(H_{w(x)}\) requires seam estimates, because changing
  the selected linear function can change its value by order \(|x|\), even
  though individual reaction jumps are bounded.

A continuous-time Green argument is promising here: all coordinates are
active, bounded jumps preserve an asymptotic descriptor, and the fastest
whole-top linkage is exactly neutral in the selected workload. But a valid
argument still has to construct and normalize a chart-local physical channel
flux, prove that restriction to a terminal cone loses no interface flux, and
apply the truncated \(H_w\) identity with controlled shell-boundary terms.
Those are precisely the occupation-localization steps challenged in the
independent audit. The finite support enumeration does not prove them.

The stronger construction in *three_active_shell_gluing_gate.md* uses the
fixed whole-top support of each pair to replace the cone-dependent linear
workloads by one constrained-shell entropy. It closes every failed
all-active cone of that pair, but an exact passing-cone example shows that
the shell entropy is not itself a global Foster function. Thus the
passing/flat interface, rather than the within-failure cone selection, is
the remaining gluing problem.

Accordingly the certified conclusion here is:

> Every affine-feasible three-active tier failure belongs to one of five
> explicit finite-shell top-phase shapes, and on each realizing descriptor
> sequence the proper descriptor workload has generator drift tending to
> minus infinity. A fixed shell potential removes the failed-cone switch,
> but global passing/flat interface gluing remains open.

## 7. Reproduction

From the project root run

    PYTHONPATH=src python3 src/three_active_flat_phase.py
    PYTHONPATH=src python3 -m unittest tests/test_three_active_flat_phase.py -v

The deterministic fingerprints are

    incidence_sha256   a662edcf046c5f759e21ff4a67e4041caf648d32f4ff8eee097bbcee517ac8b7
    certificate_sha256 9d43550b31e319a9bc8684877fd32c10502ffdd7979fefb3bdf552a2e9256fb1

The certificate is support/descriptor geometry only. Its JSON output
contains the explicit 35 supports, their ranks and deficiencies, incidence
counts, full-network deficiency histograms, and a minimum pair realizing
each of the five analytic shapes.
