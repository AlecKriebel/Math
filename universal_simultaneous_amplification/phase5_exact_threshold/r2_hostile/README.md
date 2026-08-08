# Exact hostile audit at fitness two

This directory is a bounded falsification package for the open conjecture

\[
\rho_{\rm dB}(G,2)\le \rho_{\rm dB}(K_n,2)
\]

on connected loopless undirected weighted graphs.  It does **not** prove that
conjecture.

## Canonical sign

At fitness two let

\[
m(G)=n\rho_{\rm dB}(G,2),\qquad
m_K=\frac{(n-1)2^{n-2}}{2^{n-1}-1}.
\]

The true stationary-collision target is

\[
F_0(G)=\frac1{m(G)}-\frac1{m_K}\ge0.
\]

This must be distinguished from the stronger marked-promotion margin

\[
F_{\rm prom}(G)=\frac1{m(G)}-U M_P^2\psi.
\]

`F_prom>=0` is sufficient for the true target, not equivalent to it.  The
searches report the two signs separately whenever both are evaluated.

## Exact outcomes

All primary calculations use rational arithmetic and solve the absorbing or
stationary equations over `QQ` with FLINT.

- `exact_fixation.py` independently reconstructs both update chains from the
  definitions and checks the complete baselines through order seven.
- `audit_unweighted_atlas.py` exactly checks all 995 connected unweighted
  graphs of orders two through seven.  No dB or simultaneous violation occurs;
  the complete graph is the unique dB equality in each order.
- `audit_structured_grid.py` exactly checks 9,471 rational multiscale graphs in
  51 dense-module, barbell, weak-completion, double-hub, core--satellite and
  ring templates.  No true-collision, simultaneous, or stronger-promotion
  violation occurs.
- `audit_weighted_trees.py --max-n 6` exactly checks 4,180 independently
  weighted tree instances, with ratios ranging from `10^-6` to `10^6` per
  nonanchor edge.  No violation occurs.
- `audit_reversible_f0.py` checks the genuine `F0` sign, not promotion, on
  2,300 seeded reversible rational graphs of orders five through seven with
  complete, sparse, nearly disconnected, core--periphery and multiple-hub
  structure.  No `F0<0` witness occurs.
- `audit_directed_kernels.py` checks the true collision and promotion signs on
  1,570 positive loopless nonreversible directed kernels.  Neither sign fails
  in this finite diagnostic corpus.  Directed kernels are not admissible
  graphs in the main problem.
- `audit_permutation_midpoint.py` exactly replays the failure of nonregular
  conductance midpoint symmetrization and gives a second simpler path witness.
  A finite exact regular-conductance screen of 924 midpoint comparisons finds
  no failure; the regular orbital conjecture remains open.

These counts are **EXACTLY COMPUTED FINITE EVIDENCE**, not a universal
reduction or theorem.

## Exact nonregular symmetrization witness

On the path

\[
0\mathbin{-}^{5}1\mathbin{-}^{1}2\mathbin{-}^{1}3\mathbin{-}^{1}4,
\]

let `sigma=(0 3)`.  With

\[
\bar W=\frac12(W+\sigma W\sigma^{-1}),
\]

the independent FLINT solve gives

\[
\rho_{\rm dB}(\bar W,2)-\rho_{\rm dB}(W,2)
=-
\frac{27235691462770866071897033062192847}
{6341472920592709123366290939507789100}<0.
\]

Thus permutation-orbit midpoint symmetrization is exactly false for
nonregular undirected conductances.  The earlier, independently implemented
phase-four certificate supplies a second connected-tree transposition
witness.  Neither witness addresses the symmetric-stochastic/regular subcase.

## Replay

Run `./replay.sh`.  The full finite corpus is intentionally hardware-bounded
and ordinarily completes in a few minutes on the project machine.
