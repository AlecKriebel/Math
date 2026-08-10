# Global embedded-chain and CTMC closure

Assume that a closed irreducible class has infinite mean positive return in
the embedded labelled chain.  The certified reaction-count Green theorem and
`terminal_chart_localization.md` produce a nonzero terminal chart occupation
satisfying nonnegative outward workload balance.

There are four active-set cases.

1. **Three active coordinates.**  Every bimolecular source is enabled.  At
   the first occupied changing source layer, the first-changing-source
   theorem gives nonpositive physical workload increments and a strict
   negative channel with positive compact-cell flux.  This contradicts the
   workload balance.
2. **Two active coordinates.**  If a linkage is available, apply the
   rate-weighted current-target priority theorem.  If both are shielded, the
   certified atlas gives a common affine invariant, a deficiency-zero
   product-Poisson probability, or one of the two service systems.  The
   corrected service trial satisfies \(W_\tau\le W_0-1\).
3. **One active coordinate.**  Apply
   `one_active_current_target_theorem.md`.
4. **No active coordinate.**  The terminal chart is finite and cannot carry
   an escaping occupation.

Every alternative is incompatible with terminal escape: strict workload
flux has the wrong sign, structural exits contradict terminality, an affine
invariant is constant on the fixed communicating class, deficiency zero
already supplies a stationary probability, and the service/one-active trials
have finite-mean descent.

Therefore the embedded chain has finite expected positive return count.

At every nonabsorbing population state at least one enabled falling factorial
is a positive integer, so the total reaction rate is bounded below by the
minimum positive channel rate.  Finite expected embedded return count hence
implies finite expected physical return time.

For nonexplosion, molecularity-increasing reactions have source molecularity
zero or one; their aggregate rate is at most linear in total population.
Between two upward jumps, neutral and decreasing reactions remain in a finite
total-population shell, where the aggregate rate is finite.  Comparison of
the upward-jump clock with a linear pure-birth process excludes finite-time
accumulation.  The irreducible nonexplosive CTMC is therefore positive
recurrent and has a unique stationary probability on its closed class.
