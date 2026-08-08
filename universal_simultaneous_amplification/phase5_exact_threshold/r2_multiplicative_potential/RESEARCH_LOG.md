# Rank-weighted multiplicative potential route

Date: 2026-08-08 (America/Los_Angeles)

## Exact reduction

For a real set function `G` define

\[
 F(S)=2^{-|S|}G(S).
\]

If

\[
 G(\varnothing)=1,\qquad G(V)=2,
 \qquad {1\over n}\sum_iG(\{i\})=1+{1\over n},
\]

and `F` is a submartingale for the fitness-two dB chain at every proper
nonempty state, optional stopping gives

\[
 \rho_{\rm dB}(G,2)
 \le { (n-1)/(2n)\over1-2^{1-n}}
 =\rho_{\rm dB}(K_n,2).
\]

This is exact: the complete finite-size correction is already present in
the two absorbing values and the uniform-singleton average.

Let `x_v=P_{vS}`, put

\[
 g_v={2x_v\over1+x_v},\qquad
 \ell_v={1-x_v\over1+x_v},
\]

and write `Delta_v G(S)=G(S)-G(S\setminus{v})` for `v in S`, with the
analogous add-one difference outside `S`.  After the common positive factor
`1/(n2^{|S|+1})` is removed, the submartingale condition is exactly

\[
 \sum_{v\notin S}g_v\{G(S+v)-2G(S)\}
 +2\sum_{v\in S}\ell_v\{2G(S-v)-G(S)\}\ge0. \tag{1}
\]

For

\[
 G(S)=1+\sum_{1\le |I|\le d}c_I1_{\{I\subseteq S\}},
\]

condition (1) is a finite linear feasibility problem.  The exact baseline
conditions are

\[
 \sum_i c_{\{i\}}=1,
 \qquad \sum_{2\le|I|\le d}c_I=0. \tag{2}
\]

The discovery implementation independently checks its linear rows against
direct evaluation of (1).

## Hostile status

- Degree one is infeasible already for the rational weighted triangle with
  edge weights `(1,1,2)`; the new route is not a disguised additive or
  rank-only potential.
- Degree at most two is frequently infeasible.
- Degree at most three is feasible in floating exact-structure LP screens
  on all 995 connected unweighted graphs through order seven; hundreds of
  dense, sparse, tree, nearly disconnected, and multiscale reversible
  graphs through order ten; random order-eleven and order-twelve graphs;
  all deterministic directed kernels through order five; and broad extreme
  directed screens through order eight.
- The degree-three certificates generally have a strict positive minimum
  drift when that margin is optimized.  This is evidence, not proof.
- A restricted scalar correction
  `sum_(v in S) P_(vS)(1-P_(vS))` is insufficient, as are independent
  vertex-weighted versions of that correction.

## Named open lemma

> **Cubic optional-potential lemma.**  For every finite connected loopless
> undirected weighted graph, the linear system (1)--(2) is feasible with
> `d=3`.

This lemma would prove the complete universal r=2 theorem immediately.  A
valid closure needs either an explicit graph-dependent coefficient formula,
a nonnegative factorization of (1), or a Farkas-dual proof.  Finite LP
feasibility is not a theorem.

The present bounded next tasks are:

1. derive the Farkas dual and identify its moment/flow meaning;
2. seek a fixed family of tight constraints yielding an explicit rational
   coefficient formula;
3. hostile-search symmetry-reduced weak-module and mesoscopic families at
   orders beyond the dense LP limit;
4. exactify representative rational certificates only after the universal
   algebraic mechanism is identified.

