# Reviewer checklist: twelve load-bearing interfaces

This checklist is intended for a skeptical expert reading of the Version 1.2.3
submission candidate. The deterministic tests are falsification aids; none
substitutes for the universal analytic argument.

## 1. Lifted state-cycle and reachability closure

For an enabled channel $y\to y'$ at $x=\rho+y$, verify that every edge
$z_j\to z_{j+1}$ on a weak-reversibility path from $y'$ back to $y$
lifts to the enabled population transition
$\rho+z_j\to \rho+z_{j+1}$. Check that stepwise return paths make accessibility
symmetric, so every reachability set is a closed communicating class.

**Falsification targets:** the zero complex, boundary populations, parity and
lattice restrictions, parallel labelled channels, equal population
displacements with different sources or targets, and absorbing singletons.
Confirm that this lemma needs weak reversibility but not one linkage class or
bimolecularity.

## 2. Anderson--Cappelletti--Kim proof comparison

Check the manuscript directly against the published Anderson, Cappelletti,
and Kim (2020) article. Section 6 should combine a tier criterion, a finite
reaction word, and a sampled-chain Foster argument. In the boundary case of
Section 6.1, verify that the pure-species hypothesis supplies either $S_v$ or
$2S_v$, D-tier maximality excludes $2S_v$, and the forced complex $S_v$
supplies the source-rate comparison. Internal numbering differs from the
arXiv version, so use the published article for any exact locator.

**Falsification target:** wording that lets $S_v$ or $2S_v$ supply the
final comparison, or that assigns the earlier hypothesis an unsupported
broader interpretation.

## 3. Marked reaction-channel construction

Verify that the augmented state records the target of the actual labelled
channel that fired, not a target inferred from the population displacement.
Check that the mark is enabled at the post-jump population, the augmented
kernel projects to the ordinary population embedded chain, and the reachable
augmented class is closed and irreducible. Channels may be combined only when
their source and target are both identical.

**Falsification targets:** parallel channels and equal population
displacements with different sources or targets.

## 4. Residual-factorial and source-entropy identities

For $\rho=x-t$, check that reachability gives $\rho\geq0$, and verify exactly
that a next channel $s\to u$ satisfies

\[
  V(x-s+u,u)-V(x,t)=\log\frac{(x)_t}{(x)_s}.
\]

Then check the source-probability rewrite before any entropy inequality is
applied. Sums must be over enabled sources, and $p_x(t)>0$. Confirm that the
Stirling comparison is only an asymptotic, target-shifted analogue of
pseudo-Helmholtz/Horn--Jackson entropy, not an identity with that function.

**Falsification targets:** $0$, $2A$, $A+B$, and mixed enabled and
disabled sources.

For the Anderson--Cappelletti--Kim Example 4.1 comparison, separately verify the cycle
$A\to A+B\to A+C\to C\to2B\to A$. At $x_n=(n,1,0)$, for $n\geq2$,
use their exact entropy-like function
$V_{\mathrm{ACK}}(x)=\sum_i[x_i(\log x_i-1)+1]$, with $0\log0=0$.
Its unshifted generator drift should be
$\kappa_1n(2\log2-1)\to+\infty$. For the explicitly reachable carried target
$A$ and fixed path $A\to A+B\to A+C\to C$, replay the complete exact episode
formula and obtain $-\alpha\log n+O(1)$, where

\[
 \alpha=
 \frac{\kappa_1}{\kappa_1+\kappa_2}
 \frac{2\kappa_2}{\kappa_1+2\kappa_2}
 \frac{\kappa_3}{\kappa_1+\kappa_2+\kappa_3}>0.
\]

No floating-point table is needed for this comparison.

## 5. Target-following episode recursion

For each directed path from the carried target to its selected terminal,
verify that the designated source is present, the residual stays fixed on
designated edges, and any deviation stops the episode immediately. The
continuation probability must be exactly the channel-choice factor times the
enabled-source probability. Check the zero-length case separately.

**Falsification targets:** an intermediate zero complex, parallel outgoing
channels, and a deviation whose target coincides with a later path vertex.

## 6. Scalar-envelope monotonicity and induction

For

\[
  F_q(M)=\sup_{0<p\leq1}\{\log p+C_0+qpM\},
\]

verify the exact piecewise formula and equality at its branch boundary.
Monotonicity in $M$ follows because every affine function in the supremum
has slope $qp\geq0$. Check that the backward induction uses
$J_{k+1}\leq M\Rightarrow J_k\leq F_{q_k}(M)$ and that a finite composition
preserves divergence to minus infinity.

**Falsification target:** highly separated intermediate source probabilities;
a numerical calculus check is not a proof.

## 7. Logarithmic compactification

Check normalized-log subsequence extraction and the falling-factorial
asymptotic for unary, mixed-binary, and pure-double sources. A coordinate that
diverges while its limiting normalized weight is zero must remain in the
divergent set; it is a slower tier, not a bounded species.

**Falsification targets:** two divergent coordinates on exponentially
different scales and a pure-double source on the slower coordinate.

## 8. Bimolecular top-complex alternative

Audit every molecularity-at-most-two branch. Verify the equivalence
$y\in\mathcal T\iff q_{\mathcal J}(y)=1$, where $q_{\mathcal J}(y)$ counts
particles in $y$ whose species lie in $\mathcal J$. If every complex has
exactly one $\mathcal J$-particle, all complexes are top. In the remaining
cases, check that the proof produces
either a useful vanishing-probability terminal or a signed linear
stoichiometric invariant ruling out divergence within the fixed class.

**Falsification targets:** one divergent particle with a bounded companion,
two divergent particles, zero complexes, and negative coefficients in the
signed invariant.

## 9. Exceptional set and rate degeneration

For finiteness of $K$, verify the bad-sequence contradiction and subsequence
selection of one terminal complex. For nonemptiness, verify properness of
$V$, existence of a global minimizer, and the pathwise lower bound at episode
endpoints. For

\[
  0\xrightarrow{\kappa_0}A
  \xrightarrow{\kappa_1}A+B
  \xrightarrow{\kappa_2}0,
\]

replay the exact recursion
$D_0(m,A)=a_m+p_m(b_m+q_mc_m)$. Check both

\[
  D_0(m,A)=-\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
  +O\!\left(\frac{\log m}{m}\right)
\]

for fixed positive rates as $m\to\infty$, and

\[
  D_0(m,A)\longrightarrow a_m(1+p_m)>0
  \quad\text{as }\kappa_2\downarrow0
\]

for fixed $m$. Confirm that this supports only a qualitative,
rate-dependent limitation and does not locate or bound $K$ generally.

## 10. Random-time Foster summation

With $\sigma_K$ the episode-index hitting time, verify that

\[
  W_n=V(Y_{n\wedge\sigma_K})+(n\wedge\sigma_K)
\]

is a nonnegative supermartingale after any stated additive normalization of
$V$. Check integrability before taking expectations, then use monotone
convergence to obtain finite mean hitting of $K$. Do not conflate first
hitting with positive return.

**Falsification targets:** unbounded one-episode increments, stopping at an
episode endpoint rather than an ordinary jump, and starting inside $K$.

## 11. Finite trace chain and absorbing singletons

Verify finite mean $K$-to-$K$ excursions, irreducibility of the finite
trace chain, the uniform finite-block probability of reaching a selected
marked state, and the Tonelli conversion from trace excursions to ordinary
embedded jumps. The finite-set-to-one-state argument must remain present.

Absorbing singleton reachability classes are separate and carry their
point-mass stationary laws. Positive return-time arguments concern only
nonabsorbing irreducible classes. Additional interface details are retained in
the standalone `manuscript/supplementary_note.pdf`.

## 12. CTMC conversion and stationary occupation

Check projection of the marked return to a population return and the uniform
population-level lower bound on total rate in a nonabsorbing class. For
nonexplosion, verify that recurrent visits to one population state contribute
an almost surely divergent subseries of independent positive exponential
holding times. This recovers nonexplosion; it is not presented as a new result
beyond the known broader bimolecular weakly reversible theorem.

Finally, verify that the return-cycle occupation measure is finite, normalizes
to one, and satisfies stationary balance, or that the cited regenerative CTMC
result applies exactly. By the lifted state-cycle lemma, the class reachable
from every initial population is already closed.

## Computational boundary

Replay the deterministic tests for state-cycle lifting, finite-network
reachability symmetry, scalar-envelope monotonicity, the corrected rate limit
and logarithmic coefficient, finite-chain occupation normalization, and
absorbing-singleton handling. No finite atlas proves the universal theorem, no
random test proves recurrence, and the verifier neither enumerates $K$ nor
certifies a useful bound on its diameter or location.
