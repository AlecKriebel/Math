# Exact dB first-handoff obstruction for the reversed windmill scale

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.

## Outcome

The proposed simultaneous regime

\[
 c_i={\lambda_i\over p_i}\longrightarrow\infty
\]

on a density-one set of ordinary pair blades cannot preserve dB
amplification.  It fails before any booster is reached.

**PROVED.**  Consider any pair windmill with `N` blades, parameters
`p_i=a_i/A` and `lambda_i=a_i/b_i`, and fitness `r>1`.  If the initial mutant
is either vertex of blade `i`, while every other vertex is resident, then

\[
 \Pr_{\{x_i\}}(\text{fixation})
 \le 3r(r+1){p_i\over\lambda_i}                 \tag{1}
\]

whenever `lambda_i<=1`.  The bound is exact-process and makes no assumptions
about the number, weights, or clocks of the other blades.

Consequently, if a set `O_N` of `N-o(N)` blades satisfies

\[
 \min_{i\in O_N}{\lambda_i\over p_i}\longrightarrow\infty,
 \qquad \max_{i\in O_N}\lambda_i\le1,
\]

then

\[
 \rho_{\rm dB}(W_N,r)\longrightarrow0            \tag{2}
\]

for every fixed `r>1`.  In particular, making `lambda_i/p_i` large enough to
favor the Bd center-seeding race destroys dB establishment on the same
density-one ordinary population.  No post-seeding sweep argument can repair
this loss.

## Exact two-state calculation

Fix blade `i` and abbreviate `p=p_i`, `lambda=lambda_i`.  Stop the process
when either the resident center first becomes mutant or blade `i` becomes
entirely resident.  Global fixation is impossible unless the first event
occurs.

There are only two nonabsorbing types relevant before this stopping time:

- `M`: both vertices of blade `i` are mutant;
- `H`: exactly one vertex of blade `i` is mutant.

All other vertices remain resident.  Deaths outside the center and blade
`i` are self-loops and may be deleted.

From `M`, a center death seeds the center with probability

\[
 q_2={r p\over1+(r-1)p},                         \tag{3}
\]

whereas either blade death produces `H` with probability

\[
 x={\lambda\over r+\lambda}.                    \tag{4}
\]

From `H`, death of the mutant blade vertex causes immediate erasure.  Death
of the resident blade vertex restores `M` with probability

\[
 y={r\over r+\lambda},                           \tag{5}
\]

and a center death seeds the center with probability

\[
 q_1={r p\over2+(r-1)p}.                         \tag{6}
\]

Let `H_M,H_H` denote the probabilities of seeding the center before erasure
from these two states.  Deleting self-loops directly from the dB transition
rule gives

\[
 H_M={q_2+2xH_H\over q_2+2x},\qquad
 H_H={q_1+yH_M\over1+q_1+y}.                    \tag{7}
\]

Solving,

\[
 H_M=
 {q_2(1+q_1+y)+2xq_1
  \over q_2(1+q_1+y)+2x(1+q_1)}.                \tag{8}
\]

For `lambda<=1`,

\[
 q_2\le rp,\qquad q_1\le{rp\over2},\qquad
 x\ge{\lambda\over r+1},\qquad y\le1.
\]

Using the denominator lower bound `2x` in (8) yields

\[
 H_M
 \le {3rp\over2x}+{rp\over2}
 \le2r(r+1){p\over\lambda}.                    \tag{9}
\]

Equation (7), `q_1<=rp/2`, and `lambda<=1` then give

\[
 H_H\le q_1+H_M
 \le3r(r+1){p\over\lambda}.                    \tag{10}
\]

A single mutant at either vertex of blade `i` starts in state `H`, and its
fixation probability is at most the probability `H_H` of completing the
necessary first handoff.  This proves (1).  Notice that (7)--(10) already
include center deaths during pair resolution; no isolated-excursion or
time-scale approximation is used.

## Population consequence

Let

\[
 c_N=\min_{i\in O_N}{\lambda_i\over p_i}.
\]

The two singleton starts in each ordinary blade contribute at most
`3r(r+1)/c_N` apiece.  Every exceptional blade start and the center start
contribute at most one.  Therefore

\[
 \rho_{\rm dB}(W_N,r)
 \le {2|O_N|\over2N+1}{3r(r+1)\over c_N}
      +{2(N-|O_N|)+1\over2N+1}.                 \tag{11}
\]

Both terms tend to zero under the stated hypotheses, proving (2).

## Status

**PROVED:** the exact first-handoff equations (7), bound (1), and the
density-one obstruction (2).

**FALSIFIED:** the proposed modification with ordinary
`lambda_i/p_i -> infinity`, tiny total ordinary parent mass, and booster-led
post-seed fixation.  The dB process almost surely loses the ordinary mutant
before the center is seeded.

