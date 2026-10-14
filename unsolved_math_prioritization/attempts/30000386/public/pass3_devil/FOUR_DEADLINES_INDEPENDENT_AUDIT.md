# Independent acceptance: four arbitrary known detonation times

## Verdict and pinned inputs

Accepted as a computer-assisted restricted theorem: every four prescribed known positive integers T1<T2<T3<T4 admit an online winning Angel strategy against arbitrary adaptive announcements restricted to those times. The original king-move speed, Angel-first order, one-per-round budget and repeated timestamps are preserved. This does not establish arbitrary finite deadline sets or resolve the unrestricted conjecture.

Proof audited:

- `pass3_deadlines/FOUR_DEADLINES.md`
- SHA-256 `08de8b73684d080eacf1d1f558f126bccb1e8a500d6e71d3802cf715c1c678e8`

Producer certificate:

- `pass3_deadlines/FOUR_DEADLINES_CERTIFICATE.json`
- SHA-256 `c295edb3319fc2f8b9a3ac780a749b998775e75dcc6cc57bb9abc4bf2fb43eb3`

No required mathematical correction was identified.

## 1. Exact profiles and phase semantics

The endpoint geometry and its legal child-center traversals are those accepted in the three-time audit. The exact concentration C_b is a supremum over all translated endpoint sets, so it bounds every adaptive update after a region is selected. The backward denominator reserves the boundary announcement and the maximum possible wait, w+1≤2a. Strict initial mass below D therefore gives strict terminal hazard below one.

The infinite profile cost bounds every first-deadline wait/traversal prefix. No enumeration of T1 is required. Every later lethal time is handled by its own robust phase boundary, and no phase contains an unprotected allowed lethal time in its interior.

Exact profiles give denominators at least as large as the prior mass/peak bounds. Nonnegative smoothing then gives kernels pointwise no larger than their matched conservative kernels. Thus importing the accepted one-stage cost 4/7, two-stage cost 4/5, and two-stage kernel mass 27/8 is justified.

## 2. Analytic exhaustion independently checked

### Case A: a≥32

From D≥9a²/5 and downstream mass≤27/8, each new non-point kernel has beta≤135/8 and alpha≤15/(8a²). The generic dyadic mass/peak sum is at most (8/3)sqrt(beta alpha)=15/a. Adding the point kernel cost gives 4/9+15/a≤263/288<1.

### Case B: b≥max(16,4a)

The middle denominator is at least27b²/7. Its non-point kernels therefore have peak≤7/(15b²)<1/(9a²), so they cannot alter any earliest-phase charge at a dyadic scale≤a. The earliest denominator is exactly5a²+2a.

The remaining kernels after that smoothing have beta≤243/40 and alpha≤21/(25b²). Their product coefficient is 5103/1000<25/4, giving an added cost strictly below 20/(3b). With baseline 4/7 and b≥16 this is below 83/84<1.

### Case C: neither A nor B, and c≥64

Failure of A and B implies a≤16 and b≤32, hence c≥2b and c≥4a. The last kernel has peak≤1/(5c²)<1/(9b²), so the middle denominator is exactly5b²+2b. Its additional far kernel has peak≤9/(25c²)<1/(9a²), so it cannot alter the earliest denominator either.

The baseline is exactly the three-time recurrence with cost≤4/5. The sole extra far kernel has beta≤189/25 and alpha≤21/(25c²); its added cost is at most 168/(25c). At c≥64 the total is at most 181/200<1.

### Coverage

Outside these three cases, a∈{1,2,4,8,16} and b,c∈{1,2,4,8,16,32}. The 180-case rectangle contains every remaining dyadic triple. Overlaps with analytic cases are harmless. Actual waits are smaller than or equal to the reserved worst waits in every regime.

## 3. Infinite-tail identity

For k≥1, the one-dimensional endpoint set is the interval [−2^(k+1)+1,2^(k+1)−1] with the multiples of 4 omitted. A translated endpoint set therefore omits one complete residue class modulo 4 and may also miss support outside its containing interval. Its captured mass is at most total mass minus the least residue-class mass.

If the window length is at least the kernel's support-interval length plus 3, there are at least four consecutive positions of a full-support window. These realize every omitted residue class. The upper bound is therefore attained. The captured mass is then independent of all larger dyadic scales, and the remaining contribution to F is an exact geometric series, not a truncation.

For a separable kernel p(x)p(y)/d, independent coordinate translations attain the square of the one-dimensional maximum. Positive denominators preserve all inequalities.

## 4. Independent rational replay

`replay_four_deadlines_independent.py` was written independently of the producer checker. It uses:

- recursive sparse coordinate sets and sparse integer convolutions;
- direct translated-window maximization using total and residue-class prefix sums, rather than the producer's polynomial-convolution maximizer;
- exact Fraction arithmetic for every concentration, denominator and cost;
- a minimal independently chosen exact-tail scale;
- direct verification of the tail identity at two scales for every generated kernel shape.

It regenerates all 180 parameter cases, checks all three denominators are positive, and proves each exact infinite cost is below one. Every regenerated denominator and cost matches the producer certificate. The maximum is 34777/50976 at (a,b,c)=(2,2,2).

The independent checker contains explicit runtime failures rather than assertions. Normal, python -O, and python -OO runs all passed. Replay outputs are retained beside this audit. These runs check the finite portion of the proof; the analytic exhaustion and tail identity above justify that the computation establishes the stated universal four-time theorem.

## 5. Quantifier boundary

The resulting strategy reads only already announced targets. Its normalizations depend on the known four deadlines, and every backward condition is robust against the announcement made after the current lethal move. The proof never selects a trajectory from a completed schedule or claims that an arbitrary preloaded trap is forceable.

No extrapolation from four deadlines to an unbounded number is accepted. The additional exact shape information repairs this four-time step, but the proof contains no invariant covering arbitrary repeated backward composition.
