# The generalized one-active 146-template common-potential theorem

**Proof-first composition theorem, 2026-08-12 PDT. Audit status: pending.**
This note composes three independently proved local kernels and one
invariant-face exclusion. It does not infer stochastic estimates from the
finite support table. The table is used only to prove the exhaustive,
disjoint partition

\[
                         146=17+111+6+12.                      \tag{1.1}
\]

All orientations are arbitrary strong orientations and all rate constants
are arbitrary fixed positive numbers. Constants may depend on these fixed
data and on a requested moment order.

## 1. Fixed-class marked scope

Use the normalized coordinates

\[
 U=\hbox{inactive spectator},\qquad
 V=\hbox{old active species},\qquad
 I=\hbox{unique top cofactor}.                                \tag{1.2}
\]

Fix a closed irreducible physical class, a reference marked state
\((x^\circ,0)\), and a historically reachable no-fast entrance

\[
                      x=(u,n,0),\qquad u=n^{o(1)},qquad D_V>0. \tag{1.3}
\]

Before the first crossing (V<n), reflection is inactive and

\[
                         D_V(t)=D_V(0)+V(t)-n.                 \tag{1.4}
\]

Hence a physical reaction first crossing (V<n) services one unit of the
incoming debt. Put

\[
 L_n=\left\lfloor{n^{1/3}\over\log(n+e)}\right\rfloor,
 \qquad
 G_\ell(x)=K_\ell+\sum_j\log(x_j!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4,                                     \tag{1.5}
\]

for any fixed correction vector \(\ell\) used by the containing pair.
Every local rule includes the terminal reaction and uses the common path
labels:

* (D): strict service;
* (E): a paid local defect;
* (P): an outer no-fast cutoff endpoint with (I=0,V=n,U\ge L_n);
* (B): every cutoff first crossed while a physical excursion is open.

Use priority (D), then (P/B), then (E). Thus the labels are disjoint,
and only (P) is an exact one-active-to-two-active chart handoff. The
population potential is unchanged at every endpoint reclassification.

## 2. Exhaustive structural partition

Delete (V+I), call (0,U,2U) base complexes and
(I,2I,U+I) cofactor complexes, and let (L_+) be the linkage containing
(V+I). The 146 normalized support templates split as follows.

1. **Exact cloud (17):**
   \(L_+=\{aU,V+I\}\), (a\in\{0,1,2\}\).
2. **Mixed nonexact (111):** after deleting (V+I), at least one linkage
   contains a base and a cofactor complex, and the row is not exact-cloud.
3. **Separated (6):**
   \(L_+\setminus\{V+I\}\) is base-only and the other linkage is
   cofactor-only.
4. **No-history (12):** every proper complex contains (I), while the
   other linkage is base-only.

These definitions are mutually exclusive. The frozen normalized support
table gives counts (17,111,6,12), hence (1.1).

On a no-history row, the face (I=0) is forward invariant: the proper
linkage is disabled, and every remaining reaction preserves (I=0,V).
It cannot be entered from (I>0), because every proper target contains
(I). The marked lift initialized at \((x^\circ,0)\) therefore has
(D_V=0) on this face. Consequently a no-history row never satisfies the
positive-debt hypothesis (1.3). This is an invariant proof, not a vacuous
declaration based on enumeration.

## 3. The three local theorem inputs

The following already-proved statements use exactly the common potential
in (1.5).

### 3.1 Exact cloud

The exact-cloud completion proves, for all 17 supports,

\[
 \begin{aligned}
 \mathbb P(D^c)&\le n^{-1+o(1)},\\
 \mathbb E[(1+U_\sigma+I_\sigma+|V_\sigma-n|)^p;E]
   &\le n^{-1+o(1)},\\
 \mathbb E[(1+U_\sigma+I_\sigma+|V_\sigma-n|)^p;B]
   &\le n^{-M},\\
 \mathbb E\sigma^p&\le n^{2p+o(1)},\\
 \mathbb E[W_\ell(X_\sigma)-W_\ell(x)+\sigma]
   &\le-cG_\ell(x)^3\log n.                                  \tag{3.1}
 \end{aligned}
\]

Its load-bearing inputs are the exact carrier product, sourcewise ordered
two-insertion Green bound, equality-trace compact minorization, actual
terminal entropy majorant, and time-marked additive-functional recursion.
The proof was independently replayed twice.

### 3.2 Mixed nonexact

The fast-Schur theorem proves the same conclusions for all 111 mixed
supports, with the stronger duration bound

\[
                         \mathbb E\sigma^p=n^{o(1)}.           \tag{3.2}
\]

Its ideal macro has only one or two fast (V+I)-sourced windows. A strong
cut makes the exact-return inverse geometric, the maximal-source killed
Green function controls all continuation visits, and the paid insertion
probability is sourcewise (n^{-1+o(1)}). The actual terminal entropy is
one-sided; any additional spectator descent helps the common Foster drift.
This theorem also received a strict independent replay.

### 3.3 Separated supports

The separated-six regenerative theorem proves (3.1), except with

\[
                         \mathbb E\sigma^p\le n^{p+o(1)}.      \tag{3.3}
\]

It regenerates the entire proper physical environment. Orientation-free
slack lifting makes every required order-one lower source accessible in
each residue class. The exact Feynman--Kac quotient uses the sharp two-mark
bound

\[
 \mathbb E[J_yJ_z]\le Cn^{-(\max(b_y,b_z)+1)},                \tag{3.4}
\]

which correctly permits \(\mathbb EJ_{2I}^2=\Theta(n^{-3})\).
An all-insertion weighted Neumann resolvent transfers the ideal return
chain to the full finite-(n) process. A strong lower cut gives a fixed
service chance per regenerative episode. This theorem received a strict
independent replay after both repairs.

## 4. Unified local theorem

For each of the 146 templates, select its unique category in Section 2.
No-history is impossible under (1.3). In each other category run the
corresponding physical stopping rule from Section 3. Because all three
rules use the identical (G_\ell,W_\ell), the same included endpoint
labels, and the same reflected debt coordinate, no switching cost or
Lyapunov comparison is introduced.

Taking the worst of (3.1)--(3.3), for every fixed (p,M),

\[
 \begin{aligned}
 \mathbb P(D^c)&\le n^{-1+o(1)},\\
 \mathbb E[(1+U_\sigma+I_\sigma+|V_\sigma-n|)^p;E]
   &\le n^{-1+o(1)},\\
 \mathbb E[(1+U_\sigma+I_\sigma+|V_\sigma-n|)^p;P\cup B]
   &\le C_{p,M}n^{-M},\\
 \mathbb E(1+U_\sigma+I_\sigma+|V_\sigma-n|)^p&=n^{o(1)},\\
 \mathbb E\sigma^p&\le n^{2p+o(1)},\\
 \mathbb E[W_\ell(X_\sigma)-W_\ell(x)+\sigma]
   &\le-cG_\ell(x)^3\log n.                                  \tag{4.1}
 \end{aligned}
\]

### Theorem 4.1

For every generalized Family-II one-active support template, every strong
orientation, every fixed positive rate vector, every fixed common
correction \(\ell\), and every historically reachable entrance (1.3),
there is a raw physical stopped block satisfying (4.1). It services one
unit of actual old-active reflected debt with probability
(1-n^{-1+o(1)}), charges every included defect and boundary endpoint, and
hands off only the path-labelled outer no-fast event (P) under the
identical common potential.

The theorem is a local row interface. It does not by itself certify any
pair: a pair theorem must still prove exhaustive coverage of its other
one-active, two-active, and all-active bad charts, and then apply the
fixed-class marked gluing theorem.

## 5. Frozen audited inputs

The analytic inputs are pinned to:

* exact-cloud common-(W) completion:
  `33dab04fba9d8f70b30f0ac43dffe7e432124867c51f5c647300f9e0bf80e6e4`;
* exact-cloud ordered Green theorem:
  `ea92e6c7a249f75a33d841682be2df620c4d0cab638f982ff40c7e4ca6bf50c2`;
* mixed-111 fast-Schur theorem:
  `50696e88cc6c195f106331f27cab4af8566a693f983947d486ad1cf9c903692e`;
* separated-six regenerative theorem:
  `6f63ac4272841d5901e35456ac38ac89c38665e05a2a99f8c4f649fa9bd9ecac`.

The present composition changes no pair or global flag until independently
replayed against those exact bytes and the frozen 146-template partition.
