# Research log: dilute pair--leaf hybrid

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication is used.

## Starting mechanism

- An exact weak `K_2` satellite supplies a dB gain whose Bd loss has slope
  strictly below two at `r=3/2`.
- A growing dilute population of hub leaves supplies the opposite leading
  correction `(+1/(r-1),-1)` per leaf after complete normalization.
- Matching the satellite and leaf counts can therefore make both leading
  corrections positive.

## Current obligations

1. Prove the fixed-finite-parameter weak-cut trace before taking population
   limits.
2. Control the core--pendant local process beyond establishment.
3. Prove the pair-gate probabilities and post-gate fixation uniformly on
   compact fitness intervals.
4. Make the diagonal graph family fitness-independent and explicit.

## Closure

- [PROVED] The finite positive-cut chain converges to the exact homogeneous-
  module trace by a block Schur-complement argument.
- [PROVED] In the dilute outer limit, one leaf contributes
  `(+1/(r-1),-1)` and one weak `K_2` satellite contributes the exact pair
  `(b(r,sigma),d(r,sigma))` displayed in the theorem.
- [PROVED] All errors are `o(q/N)` after the constructive least-integer
  diagonal, uniformly on the growing compact fitness intervals.
- [PROVED] Optimizing the feasible leaf/pair interval gives
  `R_hyb=1.5028569127905696...`, the isolated sextic root in the theorem.
- [PROVED] One fitness-independent family amplifies both update rules for
  every fixed `1<r<R_hyb`.  Hence `R_sim>3/2`.
- [INDEPENDENTLY REPLAYED] The labelled-event orbit lumping and the leading
  coefficient identities agree with the separate
  `threshold/endpoint_construction_v2` implementation.
- [HOSTILE AUDIT PASSED] The canonical least-integer iterated diagonal keeps
  every error at `o(q/N)`.  A separate logarithmic-cutoff proof validates the
  simpler count scale `C=q^4` with a least-dyadic positive coupling.
- [NARROW POST-PROOF AUDIT] The directly relevant 2024 construction reaches
  `1<r<1.2`; targeted searches found no prior claim of this mechanism or
  threshold.  This supports novelty but is not an exhaustive priority proof.
- [OPEN] Determine whether a richer combination raises the lower bound again
  or a universal obstruction matches it.
