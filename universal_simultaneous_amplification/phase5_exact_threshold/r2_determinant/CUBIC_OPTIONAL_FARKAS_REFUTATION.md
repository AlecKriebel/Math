# Exact Farkas refutations of cubic and quartic optional potentials

Date: 2026-08-08 (America/Los_Angeles)

## Status

The proposed cubic optional-potential lemma is **EXACTLY REFUTED** by a
seven-vertex connected undirected rational weighted graph.  A strict
degree-four potential exists on that first witness, so the failure is not a
normalization artefact.  However, the corresponding quartic lemma is also
**EXACTLY REFUTED** by a ten-vertex graph of the same two-class form.

These results close a sufficient proof route.  They do **not** refute the
universal fitness-two fixation inequality itself.

## 1. Exact optional-potential system

Let `P` be the row-stochastic replacement kernel of a connected loopless
weighted graph and put

\[
 x_v=P_{vS},\qquad
 g_v={2x_v\over1+x_v},\qquad
 \ell_v={1-x_v\over1+x_v}.                        \tag{1}
\]

At fitness two the dB chain adds `v` outside `S` with probability `g_v/n`
and removes `v` in `S` with probability `ell_v/n`.  For

\[
 F(S)=2^{-|S|}G(S),\qquad
 G(S)=1+\sum_{1\le |I|\le d}c_I1_{\{I\subseteq S\}},             \tag{2}
\]

the submartingale condition, after multiplication by the positive factor
`n2^(|S|+1)`, is

\[
 d_S+\sum_I a_{S,I}c_I\ge0,                       \tag{3}
\]

where

\[
 d_S=-\sum_{v\notin S}g_v+2\sum_{v\in S}\ell_v                  \tag{4}
\]

and the drift column has the particularly simple form

\[
 a_{S,I}=\begin{cases}
 d_S-4\sum_{i\in I}\ell_i,&I\subseteq S,\\
 g_v,&I\setminus S=\{v\},\\
 0,&|I\setminus S|\ge2.
 \end{cases}                                      \tag{5}
\]

The exact complete-baseline boundary conditions are

\[
 \sum_i c_{\{i\}}=1,\qquad
 \sum_{2\le|I|\le d}c_I=0.                       \tag{6}
\]

Equation `(5)` is derived directly from the two possible one-vertex moves.
The verifier also checks `(3)` against direct expected changes of `F`.

## 2. Farkas dual

Let `A=(a_(S,I))`, let `d=(d_S)`, and let `E` be the two boundary rows in
`(6)`, with target `b=(1,0)`.  The primal system is

\[
 -Ac\le d,\qquad Ec=b.                            \tag{7}
\]

Farkas' lemma gives the following exact obstruction.  If there are
`y_S>=0` and free `z_1,z_2` such that

\[
 -A^Ty+E^Tz=0                                     \tag{8}
\]

and

\[
 d^Ty+z_1<0,                                      \tag{9}
\]

then `(7)` is infeasible.  In moment language, `(8)` says that the
`y`-averaged drift is the same for every singleton column and the same for
every pair/triple column.  Thus the obstruction is a positive truncated
occupation law, not a numerical solver failure.

## 3. Cubic counterexample

Partition seven vertices into classes `A,B` of sizes two and five.  Give
each edge the integer weight

\[
 w_{uv}=\begin{cases}
 10000,&u,v\in A,\\
 100,&u,v\in B,\\
 1,&u\in A, v\in B\text{ or conversely}.
 \end{cases}                                      \tag{10}
\]

The graph has complete positive support and is therefore connected.  Its
automorphism group contains `S_2 \times S_5`.  If a cubic certificate
existed, averaging it over this group would produce an invariant one.
Invariant coefficients are indexed by the number `(a,b)` of `A` and `B`
vertices in the monomial:

\[
 (1,0),(0,1),(2,0),(1,1),(0,2),(2,1),(1,2),(0,3).                \tag{11}
\]

Transient states reduce to the sixteen count pairs
`0<=i<=2, 0<=j<=5`, with `(0,0)` and `(2,5)` removed.  The verifier builds
all 126 labelled rows independently and checks that their orbit aggregates
equal this reduced system.

An integer Farkas ray is supported on seven state orbits:

| state `(i,j)` | `y_(i,j)` |
|---|---:|
| `(0,1)` | `540627933005591230440428186696715600` |
| `(0,4)` | `429319667664502797137297911715830905` |
| `(1,0)` | `137468247559120961049408712647905728` |
| `(1,1)` | `1134179440520231288656990994323140` |
| `(2,0)` | `4237612806797289633945417624252880740` |
| `(2,1)` | `91732144491776328233927490827063760` |
| `(2,4)` | `171180400691387791097268387428693360` |

Take

\[
 z_1=-292949884113599470025054765354884048,
\]

\[
 z_2=-19087225856145491530878236546713200.         \tag{12}
\]

Exact rational substitution gives all eight balances in `(8)` identically
zero, while

\[
 \boxed{d^Ty+z_1
 =-16671847733465987326305780396702792<0.}         \tag{13}
\]

This proves that no degree-at-most-three potential of form `(2)` satisfies
all the submartingale inequalities on `(10)`.

## 4. The first witness is strictly quartic-feasible

The failure is genuinely about degree.  On the same graph `(10)`, the
verifier supplies invariant coefficients through degree four satisfying
`(6)` and every state inequality with exact minimum cleared drift

\[
 \boxed{
 {59103658221160944397237122483432978029271180\over
 2237974362268461704709634022056608788818134577}>0.}            \tag{14}
\]

It then reconstructs `G(S)` on all 128 labelled subsets and checks the
fitness-two dB expected change directly.  The full rational coefficient
vector is stored in `verify_cubic_optional_farkas.py`; the direct replay is
independent of the LP that discovered it.

Thus the cubic counterexample does not arise because the optional-stopping
normalization is inconsistent.

## 5. Quartic counterexample

Keep weights `(10)` but enlarge the classes to sizes two and eight.  This is
a connected complete-support graph of order ten.  The invariant
degree-four system has eleven coefficient types and twenty-five transient
state orbits.

There is an exact positive Farkas ray supported on

\[
 (0,1),(0,2),(0,7),(1,0),(1,2),(1,6),
 (2,0),(2,1),(2,2),(2,7).                         \tag{15}
\]

The primitive integer weights and the two boundary multipliers are recorded
in the verifier.  Exact substitution checks all eleven dual balances and
gives

\[
 \boxed{
 d^Ty+z_1=
 -591738467543996669461667803880418671550252755178182911237183584<0.}
                                                               \tag{16}
\]

Therefore no degree-at-most-four potential of form `(2)` exists on this
graph.

## 6. Scope

The following are now separated cleanly.

- **PROVED:** the optional-stopping reduction `(1)`--`(6)`.
- **EXACTLY REFUTED:** universal degree-three feasibility.
- **EXACTLY REFUTED:** universal degree-four feasibility.
- **PROVED FOR ONE GRAPH:** a strict quartic certificate repairs the first
  cubic witness.
- **NUMERICALLY OBSERVED:** in the two-class family with class sizes
  `(2,m)`, the minimum feasible degree increases as `m` and the scale
  separation grow.
- **OPEN:** whether any fixed degree works universally.
- **OPEN:** the universal fitness-two fixation inequality itself.

The last numerical observation is not used in either Farkas proof.
