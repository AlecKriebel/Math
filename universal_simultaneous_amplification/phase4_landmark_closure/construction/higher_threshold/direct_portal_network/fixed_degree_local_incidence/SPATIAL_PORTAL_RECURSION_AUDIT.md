# Fixed-degree spatial portals and local incidence

Date: 2026-08-08 (America/Los_Angeles)

Status: **the exact local multitype portal recursion is derived.  A broad
degree-one knife-edge obstruction is proved, and the natural independent
tree/cavity closure is exactly refuted before any graph cycle is encountered.
No simultaneous-establishment lead was found.  The full fixed-degree
high-girth sign problem remains open.**

No literature search or external contact was used.  All rates are derived
from the atomic Bd and dB rules.  Numerical searches are discovery evidence
only.

## 1. Spatial construction regime

Let the portal graph `R_Q` be `Delta`-regular.  Give every portal edge weight

\[
 \eta={H\over\Delta},                                  \tag{1}
\]

so each portal has total portal load `H`.  Balanced local blade incidence
gives every portal blade load `B`, hence weighted portal degree

\[
 d=B+H.                                                \tag{2}
\]

Unlike the diffuse regime, `Delta` is fixed and `eta` remains order one.
A portal child and its parent therefore retain an order-one shared edge.

Let `f_at` be the fraction of portal `a`'s blade load assigned to blade type
`t`, with

\[
 f_{at}\ge0,\qquad\sum_t f_{at}=1.                    \tag{3}
\]

The rows may be tied to fixed-radius portal neighborhoods or to a radius
growing slowly with `Q`; they need not be portal independent.  Undirected
incidence makes the seeding distribution of a type-`t` parent

\[
 g_{ta}={f_{at}\over c_t},\qquad c_t=\sum_a f_{at}.    \tag{4}
\]

For a translation-invariant local kernel on a vertex-transitive portal
graph, types and portals can both be indexed spatially and (4) is the reverse
kernel.

## 2. Exact local multitype recursion

For a mutant portal set `A`, let

\[
 j_A(a)=|N(a)\cap A|.                                  \tag{5}
\]

The exact Bd rates are

\[
 \delta^B_a(A)=B+{\{\Delta-j_A(a)\}\eta\over d}
 \quad(a\in A),                                       \tag{6}
\]

\[
 \upsilon^B_b(A)={rj_A(b)\eta\over d}
 \quad(b\notin A).                                    \tag{7}
\]

For dB they are

\[
 \delta^D_a(A)=
 {B+\{\Delta-j_A(a)\}\eta\over
  B+\{\Delta-j_A(a)\}\eta+rj_A(a)\eta},             \tag{8}
\]

\[
 \upsilon^D_b(A)=
 {rj_A(b)\eta\over
  B+\{\Delta-j_A(b)\}\eta+rj_A(b)\eta}.             \tag{9}
\]

For a prospective descendant-survival vector `s`, put

\[
 m_a=\sum_t f_{at}s_t.                                 \tag{10}
\]

The retained-child killing rates in portal state `A` are

\[
 \kappa_B(A;s)={r^2B\over(r+1)d}\sum_{a\in A}m_a,
 \qquad
 \kappa_D(A;s)={rB\over2}\sum_{a\in A}m_a.           \tag{11}
\]

Let `H^U_A(s)` be the probability that at least one retained child is born
before the portal set reaches empty.  With `H_empty=0`, the exact local
multitype recursion is

\[
 \left[\sum_{a\in A}\delta^U_a(A)
       +\sum_{b\notin A}\upsilon^U_b(A)
       +\kappa_U(A;s)\right]H^U_A
 =\kappa_U(A;s)
  +\sum_{a\in A}\delta^U_a(A)H^U_{A\setminus\{a\}}
  +\sum_{b\notin A}\upsilon^U_b(A)H^U_{A\cup\{b\}}.\tag{12}
\]

The parent blade survival maps are

\[
 S^B_t(s)={R^B_t(s)\over1+R^B_t(s)},\qquad
 R^B_t(s)=r(r+1)d\sum_a g_{ta}H^B_{\{a\}}(s),        \tag{13}
\]

\[
 S^D_t(s)={R^D_t(s)\over1+R^D_t(s)},\qquad
 R^D_t(s)={2r^2\over d}\sum_a g_{ta}H^D_{\{a\}}(s).\tag{14}
\]

Equations (5)--(14), rather than a scalar Galton--Watson equation, are the
correct fixed-degree local portal-episode recursion.

At the two requested fitnesses the exact constants in (11), (13), and (14)
are

\[
\begin{array}{c|ccc}
r&r^2/(r+1)&r/2&r(r+1)\\ \hline
3/2&9/10&3/4&15/4\\
31/20&961/1020&31/40&1581/400
\end{array},                                          \tag{15}
\]

while `2r^2` is respectively `9/2` and `961/200`.

For a high-girth sequence, exhaustion by finite balls gives the minimal
bounded solution of (12) on the infinite `Delta`-regular tree.  The state is
still the entire finite mutant portal set: recovery, backtracking infection,
and reinfection prevent factorization into independent rooted branches.

## 3. Why the diffuse quadratic does not extend

A tempting cavity closure replaces (12) by

\[
 \{\delta_0+u_0+\beta(1-z)\}F(z)
 =\delta_0+u_0F(z)^2,                                 \tag{16}
\]

using the isolated-portal rates.  This is the correct diffuse equation, but
it is false at fixed portal degree.

The failure occurs before a cycle can be seen.  After one portal infects a
neighbor, the two adjacent mutants share an edge of weight `eta`.  Under Bd
their exact total loss and outward-birth rates are

\[
 2\left[B+{H-\eta\over d}\right],\qquad
 {2r(H-\eta)\over d},                                 \tag{17}
\]

not twice the isolated rates `B+H/d` and `rH/d`.  Under dB, each adjacent
mutant's loss probability is

\[
 {B+H-\eta\over B+H-\eta+r\eta},                     \tag{18}
\]

not one.  Thus the two portal descendants are not independent even on the
infinite regular tree.

An independent exact labelled audit makes the failure quantitative.  Take
the six-cycle, `B=H=1`, and start from one mutant portal.  At the complete
graph test marks, substituting the true singleton PGF into the left side of
(16) gives the following nonzero rational residuals:

\[
\begin{array}{c|cc}
 &\text{Bd}&\text{dB}\\ \hline
r=3/2&-502329/161086864&
-191801235170627729103007/48044549224070823098080898\\[1mm]
r=31/20&-3061735230854355/857582474922367922&
\text{a strictly negative exact rational}
\end{array}.                                          \tag{19}
\]

`verify_spatial_recursion_counterexample.py` reconstructs all 63 nonempty
labelled states, checks every row and rotational singleton identity exactly,
and certifies all four nonzero residuals.  Consequently, any proof or search
based on (16) in the fixed-degree regime is invalid.

## 4. A broad exact knife-edge obstruction

There is one topology-independent identity.  At the Bd establishment test
`q=1/r^2`, retained children are marked at rate

\[
 {|A|(r-1)B\over d}.                                  \tag{20}
\]

Let `W_partial(A)` be the total portal weight crossing from `A` to its
complement.  Substituting the product candidate

\[
 F_A=r^{-|A|}                                         \tag{21}
\]

into the exact first-step equation leaves residual

\[
 (r-1)|A|B\left({1\over d}-1\right);                 \tag{22}
\]

the entire boundary term cancels exactly.  Hence if

\[
 B+H=d=1,                                             \tag{23}
\]

(21) is the unique portal PGF on every finite regular portal graph.  The
parent equation then gives

\[
 D_B(1/r^2)=1/r^2,                                    \tag{24}
\]

so Bd establishment equals, rather than strictly exceeds, `1-1/r`.
Therefore no portal-transitive, translation-invariant local-incidence family
on the entire hypersurface `B+H=1` can be a strict simultaneous amplifier.
This identity holds for cycles, fixed-degree expanders, and arbitrary regular
portal topology.

## 5. Hostile search and status

The exact sparse subset solver searched one-to-one local incidence on cycles
and the cubic graph.  A translation-invariant neighborhood kernel has the
same scalar establishment test: by symmetry every type survival coordinate
is equal, so every row mark in (10) is the same.  Representative best minimum
PGF-test margins were

\[
\begin{array}{c|cc}
 &r=3/2&r=31/20\\ \hline
C_8&-0.03908&-0.05138\\
\text{cube portal graph}&-0.04361&-0.05620
\end{array}.                                          \tag{25}
\]

These are **NUMERICALLY OBSERVED**, not optimization certificates.  No
simultaneous-establishment lead appeared, so no post-establishment takeover
claim was made.

**PROVED:** the exact spatial multitype recursion (5)--(14); its high-girth
tree interpretation; failure of independent branching at the first adjacent
portal pair; and the topology-independent `B+H=1` Bd obstruction.

**EXACTLY COMPUTED:** four rational six-cycle counterexamples to the diffuse
quadratic at `r=3/2` and `r=31/20`.

**NUMERICALLY OBSERVED:** no simultaneous establishment in the bounded cycle
and cubic searches.

**OPEN:** the sign of the true infinite-tree resolvent away from `B+H=1`,
non-transitive colored incidence, growing local-incidence radius with fixed
portal degree, and a rigorous fixed-degree expander no-go.  The natural
scalar cavity route is **FALSIFIED**, not merely unproved.

