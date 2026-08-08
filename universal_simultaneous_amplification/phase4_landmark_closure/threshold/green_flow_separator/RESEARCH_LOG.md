# Green-flow separator research log

Date: 2026-08-07 (America/Los_Angeles)

No literature search or external contact was used.

## Starting point

Take the exact endpoint identity

\[
 e_B+e_D=\mathsf T+\mathsf C-\mathsf E
\]

and the exact rank-cut Green-flow laws as proved.  The only target in this
branch is the genuinely global inequality

\[
 \mathsf T+\mathsf C\leq \mathsf E.
\]

Statewise signs, fixed-rank signs, separate aggregate signs, reach-two
balancing, and radial-plus-bilinear pointwise certificates are frozen as
false routes and are not reused.

## Exact Johnson centering

Put `t_i=sum_j P_ji` and `c_i=1-t_i`.  For a rank-`k` set,

\[
 c(S)=A(S)-B(S)=\sum_{i\in S}c_i,
 \qquad b(S)=B(S)-B_0(k).
\]

Both fields have exactly zero counting mean on every rank.  On the Johnson
graph `J(n,k)`, with positive Laplacian

\[
 (\mathcal Jf)(S)=\sum_{i\in S,j\notin S}
       \{f(S)-f(S-i+j)\},
\]

direct Boolean algebra gives

\[
 \mathcal Jc=nc,
 \qquad
 \mathcal Jb=2(n-1)b+(n-k-1)c.
\]

Consequently

\[
 \mathcal J^{-1}c={c\over n},\qquad
 \mathcal J^{-1}b={b\over2(n-1)}
 -{n-k-1\over2n(n-1)}c.                              \tag{J}
\]

This is a new exact cross-rank diagnostic: all favorable signed terms are
not rank means, but covariances between nonuniform Green occupations and
the first two Johnson eigenspaces.

## Next step

Insert (J) in `T+C`, perform exact Johnson summation by parts, and test
whether the resulting occupation-gradient pairing admits a coercive bound
by the dB tangent dispersion.  Any such estimate must use the full
cross-rank Green conservation; rank totals alone do not control the
within-rank gradients.

## 2026-08-08 -- projected Green-flow LP

- [PROVED] Froze the rank-labelled degree-`d` Green LP.  Actual Green
  occupations are feasible, so its objective is an upper bound on normalized
  fixation.  Its dual is a rank-labelled Boolean-polynomial supersolution.
- [EXACTLY VERIFIED] On the hard five-vertex weakly completed star, degree
  two spans the entire transient function space.  Exact primal and dual
  values are `1.1414069545...` for Bd and `0.7592226924...` for dB.  All
  eight orbit multipliers per rule are printed over `QQ`.
- [EXACT ROUTE REFUTATION] Scalar rank-cut flow fails on the weighted
  three-path by exact relaxed excess `22686/13685`.
- [NUMERICAL DISCOVERY, THEN EXACTLY CERTIFIED] The full degree-two
  relaxation fails on a positive integer weighted seven-vertex three-blade
  graph.  Exact positive 98-atom primal witnesses give normalized relaxed
  values `1.5776282393105...` and `0.46353137239207...`, with positive excess
  sum `0.041159611702588...`.  The actual graph has balanced normalized
  fixation about `0.79471237`, so this closes the relaxation route and is not
  a fixation counterexample.
- [PRECISE GLOBAL OBSTRUCTION] A proof must control higher Johnson modes of
  the within-rank Green occupations, or couple the two full flows before
  projection.  Every scalar and every graph-dependent degree-two projected
  certificate is now excluded.
- [EXACT BLOCK FORMULATION] Although the endpoint observable itself lies
  entirely in Johnson degrees at most two, its Green expectation is governed
  by high-mode Schur feedback.  The exact block equations are recorded in
  `QUADRATIC_FLOW_LP.md`.  A viable global theorem must sign or pair the two
  Schur feedback terms, rather than add another fixed number of moments.

## 2026-08-08 -- true-chain pivot from the LP witness

- [NUMERICALLY OBSERVED] Reoptimized the true full subset chains on the bare
  nine-edge three-blade support, varying all weights over many orders of
  magnitude.  The best simultaneous minimum found was
  `M=0.972429120923...`, with normalized ratios equal to displayed precision.
- [NUMERICALLY OBSERVED] Added all twelve missing support edges at one common
  weak-completion weight and reoptimized all ten parameters.  The maximum
  found was exactly the complete graph value `M=1`; no `M>1` candidate was
  observed.
- [NUMERICALLY OBSERVED] Freed all twenty-one complete-support weights and
  searched both from `K_7` and from weak completions of the bare optimum and
  the degree-two LP witness.  No point exceeded `M=1`; broad search returned
  `K_7`, while the targeted far start returned to a suppressing point.
- [EXACTLY COMPUTED DIAGNOSTIC] The first omitted equation that rejects the
  fake degree-two Bd occupation is the rank-three state-conservation equation
  at `{0,5,6}`, with exact residual `100.27630312762...`.  For dB the largest
  first-omitted triple residual is only `-0.001964602514...`, consistent with
  its relaxed and actual values being nearly equal.  This is a graph-specific
  third-order constraint, not an all-degree inequality, so the fixed-degree
  hierarchy is not being extended.
- No endpoint simultaneous amplifier was found.  These searches are
  discovery evidence only and do not prove the separator.
