# Reviewer checklist: ten load-bearing interfaces

This checklist is intended for a skeptical expert reading of the Version 1.0
publication candidate. The deterministic tests are useful falsification aids,
but none substitutes for the universal analytic argument.

## 1. Marked reaction-channel construction

**Manuscript location:** Section `sec:marked` and the technical appendix.

Verify that the augmented state records the target of the **actual labelled
channel that fired**, not a target inferred from the population displacement.
Check that the mark is enabled at the post-jump population, that the augmented
kernel projects to the ordinary population embedded chain, and that the
reachable augmented class is closed and irreducible. Channels may be combined
only when their source and target are both identical.

**Falsification targets:** parallel channels, equal population displacements
with different sources or targets, the zero complex, and boundary classes.

## 2. Residual-factorial and source-entropy identities

**Manuscript location:** Lemmas `lem:identity` and `lem:entropy`.

For \(r=x-t\), check reachability implies \(r\ge0\), and verify exactly that a
next channel \(s\to u\) satisfies

\[
  V(x-s+u,u)-V(x,t)=\log\frac{(x)_t}{(x)_s}.
\]

Then check the source-probability rewrite before any entropy inequality is
applied. Sums must be over enabled sources, and \(p_x(t)>0\). Confirm that the
Stirling comparison is described only as an asymptotic, target-shifted
analogue of pseudo-Helmholtz/Horn--Jackson entropy, not as an identity with
that function.

**Falsification targets:** \(0\), \(2A\), \(A+B\), and mixed enabled/disabled
sources.

## 3. Target-following episode recursion

**Manuscript location:** Lemma `lem:recursion`.

For each directed path from the carried target to its selected terminal,
verify that the designated source is literally present, the residual remains
fixed on designated edges, and any deviation stops the episode immediately.
The continuation probability must be exactly the channel-choice factor times
the enabled-source probability. Check the zero-length case separately.

**Falsification targets:** a path with an intermediate zero complex, parallel
outgoing channels, and a deviation whose target coincides with a later path
vertex.

## 4. Scalar-envelope monotonicity and induction

**Manuscript location:** Lemma `lem:envelope` and Proposition
`prop:propagation`.

For

\[
  F_q(M)=\sup_{0<p\le1}\{\log p+C_0+qpM\},
\]

verify the exact piecewise formula and equality at its branch boundary.
Monotonicity in \(M\) must follow directly because every affine function in
the supremum has slope \(qp\ge0\). Check that the backward induction uses this
fact in the form \(J_{k+1}\le M\Rightarrow J_k\le F_{q_k}(M)\), and that a
finite composition preserves divergence to \(-\infty\).

**Falsification target:** highly separated intermediate source probabilities;
a numerical calculus check is not a proof.

## 5. Logarithmic compactification

**Manuscript location:** Section `sec:compact` and Lemma
`lem:ff-asymptotic`.

Check normalized-log subsequence extraction and the falling-factorial
asymptotic for unary, mixed-binary, and pure-double sources. A coordinate that
diverges while its limiting normalized weight is zero must remain in the
divergent set; it is a slower tier, not a bounded species.

**Falsification targets:** two divergent coordinates on exponentially
different scales and a pure-double source on the slower coordinate.

## 6. Bimolecular top-complex alternative

**Manuscript location:** Lemmas `lem:top` and `lem:terminal`.

Audit every molecularity-at-most-two branch. Verify the equivalence
$y\in T\iff q_J(y)=1$, where $q_J(y)$ counts the particles in $y$ whose
species lie in $J$. Consequently, if every complex has exactly one
$J$-particle, all complexes are top and the all-top case already applies;
there is no independent non-all-top branch of that form. In the remaining
case, check that the proof produces either a useful vanishing-probability
terminal or a signed linear stoichiometric invariant that rules out divergence
within the fixed communicating class.

**Falsification targets:** one divergent particle with a bounded companion,
two divergent particles, zero complexes, and negative coefficients in the
signed invariant.

## 7. Exceptional set and rate degeneration

**Manuscript location:** Proposition `prop:K`, the quantitative-limitation
example, and `supplement/quantitative_limitations.md`.

For finiteness, verify the bad-sequence contradiction and subsequence choice
of one terminal complex. For nonemptiness, verify properness of \(V\), the
existence of a global minimizer, and the pathwise lower bound at episode
endpoints. Independently replay the exact recursion for

\[
  0\xrightarrow{\kappa_0}A
  \xrightarrow{\kappa_1}A+B
  \xrightarrow{\kappa_2}0
\]

from \((m,0)\) with carried target \(A\), obtaining

\[
  D_0(m,A)=-\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
  +O\!\left(\frac{\log m}{m}\right).
\]

Confirm that this supports only a qualitative, rate-dependent limitation. It
does not locate or bound \(K\) for a general network.

## 8. Random-time Foster summation

**Manuscript location:** the stopped-drift argument in Section
`sec:recurrence`.

With \(\sigma_K\) the episode-index hitting time, verify that

\[
  W_n=V(Y_{n\wedge\sigma_K})+(n\wedge\sigma_K)
\]

is a nonnegative supermartingale after any stated additive normalization of
\(V\). Check integrability before taking expectations, then apply monotone
convergence to obtain finite mean hitting of \(K\). Do not conflate first
hitting with positive return.

**Falsification targets:** unbounded one-episode increments, stopping at an
episode endpoint rather than an ordinary jump, and starting inside \(K\).

## 9. Finite trace-chain and absorbing classes

**Manuscript location:** Proposition `prop:trace` and the trace-chain appendix.

Verify finite mean \(K\)-to-\(K\) excursions, irreducibility of the finite
trace chain, the uniform finite-block probability of reaching a selected
marked state, and the Tonelli conversion from trace excursions to original
embedded jumps. The finite-set-to-one-state argument must remain present.

Absorbing singleton classes are separate: their stationary law is the point
mass at the absorbing state. Positive return-time conventions should be used
only for nonabsorbing irreducible classes.

## 10. CTMC conversion and stationary occupation

**Manuscript location:** Proposition `prop:ctmc` and equation
`eq:occupation-formula`.

Check projection of the marked return to a population return, the uniform
population-level lower bound on the total rate in a nonabsorbing class, and
the finite expected physical return time. For nonexplosion, verify that
recurrent visits to one population state contribute an almost surely
divergent subseries of independent positive exponential holding times.

Finally, verify that the return-cycle occupation measure is finite, normalizes
to one, and satisfies stationary balance, or that the cited regenerative CTMC
result applies exactly. This conclusion is restricted to an already-closed
communicating class and does not prove finite expected entry from an arbitrary
nonclosed initial state.

## Computational boundary

The exact tests should be replayed, including scalar-envelope monotonicity,
the removed redundant branch, the rate-degeneration recursion, finite-chain
occupation calibration, and absorbing singleton handling. Finite atlases and
fixed-seed stress tests do not prove the universal theorem, the finiteness of
\(K\), or any bound on its diameter or location; those conclusions come only
from the analytic proof.
