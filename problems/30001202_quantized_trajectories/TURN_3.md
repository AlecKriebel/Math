# Turn3: compact pair-orbit criteria for uniform localization

AI-assisted proof attempt; independent review pending. This gives exact criteria for a specified closed observation relation, and sufficient conditions for arbitrary source cells. It does not claim that taking cell closures is lossless.

Let X be compact metric, f continuous on X with values in an ambient metric space containing X, and R⊂X×X closed. Consider two admissible trajectories in X that are R-related at every observed time. No forward invariance of all X is required.

## Forward localization criterion
The following are equivalent:
(A) For every ε>0 there exists L such that every pair of R-related trajectories of lengthL+1 has initial distance<ε.
(B) Every pair of infinite forward trajectories in X that remain R-related at all nonnegative times have identical initial states.

(A) implies(B) by restriction to lengthL and arbitrary ε. Conversely, if(A) fails, choose ε>0 and pairs of lengthL+1 with initial distance≥ε for unbounded L. Compactness and a diagonal subsequence give limiting values at every nonnegative time. Continuity preserves x_(j+1)=f(x_j), closedness preserves membership in R, and the initial separation≥ε survives. This contradicts(B).

## Central localization criterion, including noninvertible maps
The following are equivalent:
(C) For every ε>0 there exists L such that every pair of R-related trajectories indexed−L,...,L has central distance<ε.
(D) Every pair of bi-infinite trajectories in X remaining R-related at all integer times have identical states at time0.

The same diagonal compactness proof applies on the countable index set Z. It chooses compatible limiting trajectories; no inverse function or unique backward branch is assumed. If observations run from0 toT and min(t,T−t)≥L, restrict to the2L+1 window centered at t to obtain the corresponding diameter bound at time t.

## Application to the source's finite partition
Put R_cl=union_i (closure_X P_i)×(closure_X P_i). This relation is closed and contains every actual same-cell pair. If(B) holds for R_cl, all feasible Q_0 from lengthL+1 observed words have diameter≤ε for sufficiently large L (replace ε by ε/2 to pass safely from pairwise strict inequalities to a supremum). If(D) holds, the same is true for all Q_t at least L steps from both endpoints.

If every P_i is closed in X, R_cl equals the actual same-cell relation, so these are necessary AND sufficient criteria for the corresponding uniform shrinking property. Finite disjoint closed cells are a substantive additional assumption; in a connected X they cannot provide a nontrivial partition. We do not impose this on ordinary half-open quantizers silently. With general nonclosed cells the closure criterion is only sufficient: turn2 gives two fixed boundary points in R_cl with distinct actual labels, explaining why its uniform compactness shortcut fails.

For a familiar sufficient dynamical condition, suppose f:X→X is positively expansive: there exists c>0 such that any distinct x,y have d(f^j x,f^j y)>c for some j≥0. If each cell has diameter at mostδ<c, the same bound holds for its closure, so(B) follows. If f is a homeomorphism and is two-sided expansive, the analogous statement with j∈Z gives(D) and uniform central shrinking. This is the elementary generating-partition principle; no novelty claim or effective rate follows from it. The present proof explicitly handles the source's finite-horizon feasibility and its boundary caveat.

## Limits
These conditions depend on both the map and the observation geometry. Even expanding dynamics reveal nothing through a single cell that is mapped onto itself. The criterion does not assert polynomial-time verification or any explicit L(ε). It precisely separates compactness-based uniform localization from the pointwise code injectivity in turn2; quantitative hyperbolic estimates require further structure.
