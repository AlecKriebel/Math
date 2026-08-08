# Rank-moment Green flows and the exact quadratic barrier

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external contact was used.

## Status

This note records two **PROVED reductions** and two **EXACT ROUTE
REFUTATIONS**.  It does not prove or refute the endpoint fixation separator.

1. The signed part `T+C` of the balanced endpoint identity is exactly a
   within-rank Johnson Dirichlet pairing.  This identifies the missing
   quantity as the nonuniform part of the two Green occupations.
2. Projecting the full Green equations onto all rank-labelled Boolean
   moments of degree at most two gives a finite linear-programming upper
   bound on each normalized fixation probability.
3. Scalar cross-rank flow, even with the exact state geometry entering its
   rates, cannot prove the separator: an exact order-three relaxed witness
   violates it by `22686/13685` in normalized-sum units.
4. The entire degree-two moment LP also cannot prove the separator: an exact
   positive order-seven primal witness violates the normalized-sum bound.

The order-seven graph itself satisfies the fixation separator strictly.  It
is the relaxation, not the evolutionary process, that violates the target.

## 1. Exact weak Green formulation

Fix a rule `U`, and let `L_U` be its continuous type-changing generator on
the transient sets.  Give every test function value zero at the two
absorbing states.  If `z_U` is the Green occupation from the uniform
singleton law `mu`, then

\[
 \sum_S z_U(S)[-L_Uf](S)=\sum_S\mu(S)f(S).             \tag{1}
\]

Let `a_U(S)` be the rate from `S` directly to the all-mutant state.  Then

\[
 \rho_U(G)=\sum_Sz_U(S)a_U(S).                         \tag{2}
\]

For an integer `d>=0`, define the rank-labelled degree-`d` space

\[
 \mathcal F_d=
 \operatorname{span}\left\{
 {f1}_{\{|S|=k\}}{f1}_{\{I\subseteq S\}}:
 1\le k\le n-1,\ |I|\le d
 \right\}.                                             \tag{3}
\]

The degree-`d` projected Green LP for rule `U` is

\[
 \begin{array}{ll}
 \text{maximize}&
 \displaystyle {1\over\rho_U(K_n)}\sum_S z(S)a_U(S),\\[4pt]
 \text{subject to}&z(S)\ge0,\\
 &\displaystyle
 \sum_Sz(S)[-L_Uf](S)=\langle\mu,f\rangle
 \quad(f\in\mathcal F_d).
 \end{array}                                           \tag{P_d^U}
\]

The actual Green occupation is feasible by (1).  Therefore

\[
 {\rho_U(G)\over\rho_U(K_n)}\le \operatorname{val}(P_d^U). \tag{4}
\]

This is a theorem over exact rational arithmetic; no optimization heuristic
is used in (4).

The dual is equally concrete.  It minimizes the uniform-singleton mean of a
rank-labelled degree-`d` potential `f` subject to

\[
 [-L_Uf](S)\ge {a_U(S)\over\rho_U(K_n)}
 \quad\hbox{for every transient }S.                    \tag{D_d^U}
\]

Thus a proof that

\[
 \operatorname{val}(P_2^{\rm Bd})+
 \operatorname{val}(P_2^{\rm dB})\le2                 \tag{5}
\]

would have proved the balanced separator.  The exact witness below refutes
(5).

## 2. Why order five looked promising

On five vertices, degree two spans every function on every transient rank:

\[
 5+10+10+5=30=2^5-2.
\]

One may use singleton indicators on ranks one and four and pair indicators
on ranks two and three.  Hence `P_2^U` is the full Green system and its dual
potential is exactly the normalized fixation harmonic.

For the weakly completed star with center--leaf weight `1000` and every
leaf--leaf weight `1`, the exact normalized optima are

\[
 \operatorname{val}(P_2^{\rm Bd})
 ={2353272239601190666793731\over2061729368416890045332005}
 =1.1414069545\ldots,
\]

\[
 \operatorname{val}(P_2^{\rm dB})
 ={217581384729692915165\over286584406535154503216}
 =0.7592226924\ldots.
\]

Their balanced mean is `0.9503148235...<1`.  The exact dual multipliers have
eight orbit types for each rule:

- rank one: center and leaf;
- ranks two and three: center--leaf and leaf--leaf pair;
- rank four: center and leaf.

The verifier prints every multiplier as an exact rational and checks
`A z=b`, `A^T y=c`, positivity, and equality of the primal and dual values.
This finite success is not evidence that degree two remains complete or
sufficient at growing order.

## 3. Exact scalar-flow obstruction

On the path `0--2--1` with weights `1,17`, retain only the scalar rank-cut
currents and boundary flow.  The following nonnegative artificial Green
occupations satisfy every retained equality exactly:

\[
 z_B(\{0\})={72\over85},\quad
 z_B(\{0,1\})={27\over85},\quad
 \widehat\rho_B={81\over85},                           \tag{6}
\]

and

\[
 z_D(\{2\})={55\over161},\quad
 z_D(\{1,2\})={106\over161},\quad
 \widehat\rho_D={106\over161}.                        \tag{7}
\]

The normalized relaxed values are

\[
 {\widehat\rho_B\over\rho_B(K_3)}={171\over85},
 \qquad
 {\widehat\rho_D\over\rho_D(K_3)}={265\over161},      \tag{8}
\]

and their excess sum is

\[
 {171\over85}+{265\over161}-2={22686\over13685}>0.     \tag{9}
\]

Thus no argument using only nonnegativity, scalar rank currents, and local
rate/geometry identities can prove the endpoint separator.  Vertex- or
configuration-resolved conservation is indispensable.

## 4. Exact degree-two obstruction

Use seven vertices with center `0` and blades `(1,2),(3,4),(5,6)`.  The only
edges and their positive integer weights are

| edge | weight |
|---|---:|
| `01` | `1,000,000` |
| `02` | `100,000,000,000` |
| `12` | `20,000,000` |
| `03` | `3,000,000,000` |
| `04` | `20,000,000` |
| `34` | `1` |
| `05` | `50,000,000` |
| `06` | `30,000,000` |
| `56` | `100` |

The support is connected.  On seven vertices, a deterministic basis for
`F_2` consists of singleton indicators at ranks one and six and all pair
indicators at ranks two through five.  It has

\[
 7+4\binom72+7=98
\]

elements, whereas the transient state space has dimension `126`.  The
middle-rank modes missing from this projection are the first place where
the relaxation can depart substantially from the true Green measure.

The exact verifier supplies 98 positive rational occupation atoms for each
rule.  They solve all 98 projected equations over `QQ`.  Their normalized
objectives are

\[
 \widehat x=1.5776282393105\ldots,
 \qquad
 \widehat y=0.46353137239207\ldots,                    \tag{10}
\]

so

\[
 \widehat x+\widehat y-2
 =0.041159611702588\ldots>0.                           \tag{11}
\]

The sign in (11) is checked as one exact rational.  Its reduced numerator
and denominator have respectively 10,931 and 10,935 bits; the SHA-256 hash
of the decimal-free string `numerator/denominator` is

```text
06ac21529788bdf11f01dd0b5a7d28f5aa97cbaffae9f5d92a045ae40d399855
```

This closes every universal degree-two projected-flow proof, including a
graph-dependent choice of all pair coefficients in the dual.  It is
strictly stronger than failure of a radial or aggregate `(A,B)` ansatz.

For avoidance of doubt, the actual exact fixation ratios of this graph are

\[
 x=1.12589339050480\ldots,
 \qquad y=0.463531356469192\ldots,                     \tag{12}
\]

whose balanced mean is about `0.79471237`.  The graph is not an endpoint
fixation counterexample.

## 5. Exact Johnson form of the remaining obstruction

Let

\[
 c(S)=A(S)-B(S),\qquad b(S)=B(S)-B_0(|S|).
\]

Both have zero counting mean at every rank.  On the rank-`k` Johnson graph,

\[
 \mathcal Jc=nc,
 \qquad
 \mathcal Jb=2(n-1)b+(n-k-1)c.                        \tag{13}
\]

Therefore

\[
 \mathcal J^{-1}c={c\over n},\qquad
 \mathcal J^{-1}b={b\over2(n-1)}
 -{n-k-1\over2n(n-1)}c.                              \tag{14}
\]

Writing the explicit potentials from (14) as `psi_B,psi_D`, exact summation
by parts gives

\[
 \mathsf T+\mathsf C
 =\sum_k\mathcal E_{J(n,k)}(z_B,\psi_B)
  +\sum_k\mathcal E_{J(n,k)}(z_D,\psi_D).             \tag{15}
\]

Thus the endpoint target is exactly

\[
 \sum_k\mathcal E_J(z_B,\psi_B)
 +\sum_k\mathcal E_J(z_D,\psi_D)\le\mathsf E.         \tag{16}
\]

The degree-two counterexample proves that (16) cannot follow from all Green
conservation laws tested only against the first two Johnson eigenspaces.
The missing ingredient must control the higher within-rank modes of the
occupation measures, or couple the two full Green flows before projection.
That is the **PRECISE NEW GLOBAL OBSTRUCTION** left by this branch.

There is a useful sharper formulation.  Let `Pi` be counting-measure
orthogonal projection, separately at every rank, onto Johnson degrees zero,
one, and two, and put `H=I-Pi`.  Both the source `mu` and the top absorption
flux lie in `range(Pi)`, and (13)--(15) show that the entire target functional
depends only on `Pi z_B,Pi z_D`.  Nevertheless those low projections are not
closed under either generator.  Writing `A_U=-L_U^T`, the exact Green system
has blocks

\[
 \begin{pmatrix}
  \Pi A_U\Pi&\Pi A_UH\\
  HA_U\Pi&HA_UH
 \end{pmatrix}
 \binom{\Pi z_U}{Hz_U}=\binom{\mu}{0}.                \tag{17}
\]

Whenever the high block is invertible, the actual low occupation is
therefore governed by the Schur operator

\[
 A_{U,\mathrm{eff}}
 =\Pi A_U\Pi-\Pi A_UH(HA_UH)^{-1}HA_U\Pi.             \tag{18}
\]

The projected LP retains only the first row of (17), allowing an arbitrary
nonnegative high occupation, and hence discards exactly the feedback term in
(18).  The order-seven witness proves that this feedback is not a negligible
technicality: for Bd its relaxed bound is `1.577628...`, while the exact
ratio after full feedback is `1.125893...`.

Accordingly, a viable endpoint proof may remain low-dimensional in its
*observable*, but it cannot be low-dimensional in its conservation laws.  It
needs a sign or paired estimate for the two high-mode Schur feedbacks.  This
is more specific than asking for additional rank moments and does not invite
another fixed-degree hierarchy.

## 6. Verification

From the repository root, run

```bash
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/green_flow_separator/verify_johnson_green_reduction.py --all
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/green_flow_separator/verify_quadratic_flow_lp_exact.py
```

The first script checks (13)--(16) on every exact hostile graph.  The second
checks the complete order-five primal/dual certificate and both exact LP
route counterexamples.

## Classification

| Claim | Status |
|---|---|
| Johnson--Green identity (15) | **PROVED** |
| projected Green LP upper bound (4) | **PROVED** |
| scalar rank-flow closure | **EXACTLY REFUTED AS A ROUTE** |
| universal degree-two closure (5) | **EXACTLY REFUTED AS A ROUTE** |
| balanced endpoint fixation separator | **OPEN** |
| no simultaneous amplification at `r=3/2` | **OPEN** |
