# Technical summary

## Exact result

**Outcome S is proved.**  Every finite bimolecular weakly reversible
stochastic mass-action network with one linkage class is positive recurrent
on every closed communicating class, for every positive rate vector.

## Central mechanism

The proof records the target complex \(t\) of the most recent reaction and
removes it from the population, leaving a residual \(r=x-t\).  The common
potential

\[
V(x,t)=\sum_i\log((x_i-t_i)!)
\]

has the exact jump increment

\[
\Delta V=\log\frac{(x)_t}{(x)_s}
\]

when the next reaction source is \(s\).  Following the carried target costs
exactly zero; all reward is source switching.

For every possible terminal complex, a finite designated path creates an
episode of at most \(|\mathcal C|\) jumps.  A sharp scalar recursion proves
that if the terminal complex has vanishing source probability, the entire
episode has expected drift tending to \(-\infty\), despite arbitrarily many
intermediate propensity scales.

Every divergent state sequence admits a normalized-log direction \(w\).
Bimolecularity gives an exact alternative:

- a lower terminal complex exposes an enabled source of strictly larger
  \(w\)-weight; or
- a species-linear conservation law contradicts divergence inside the fixed
  communicating class.

The first alternative forces terminal source probability to zero.  A finite
bad-sequence contradiction then makes the finite episode family uniformly
negative outside one finite set.

## What was inherited

- nonexplosion of bimolecular weakly reversible stochastic mass-action
  systems;
- Phase-I target-lifting intuition;
- exact finite graph and conservation utilities from earlier phases.

The Phase-IV bounded-defect theorem is not used as a black box because its
last target-retention interface had not been fully certified.

## What is newly proved in Phase V

1. the exact target/source residual-factorial identity;
2. the source-probability entropy bound;
3. finite target-following episode recursion;
4. complete-credit scalar elimination;
5. normalized-log top availability or global conservation;
6. finite-family sequence-to-uniform Foster closure;
7. deterministic overshoot and physical-duration bounds;
8. finite trace-chain conversion to positive recurrence.

## Verification

Run from the project root:

```bash
PYTHONPATH=. pytest -q phase2_trigger_drain/tests \
  phase5_source_flag_closure/tests

PYTHONPATH=. python -m \
  phase5_source_flag_closure.src.phase5_independent_verifier
```

The exhaustive top-alternative certificate is in
`certificates/top_availability_audit.json`.

## Limitations

- The theorem is restricted to one linkage class.  The proof uses a directed
  path from every carried target to every chosen terminal complex, which is
  unavailable across distinct linkage classes.
- No claim of exponential ergodicity, product-form stationarity, or explicit
  stationary tail exponent is made.
- The finite exceptional set is defined exactly through episode expectations
  and proved finite by compactness; the current implementation does not give
  a polynomial-time bound on its radius.
- Nonexplosion is inherited rather than reproved.
