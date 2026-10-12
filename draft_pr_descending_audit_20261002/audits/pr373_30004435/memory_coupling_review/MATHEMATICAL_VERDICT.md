# Mathematical verdict, sealed before candidate program inspection

## Verdict and strongest checked conclusion

The universal proof in candidate TURN_3.md is valid **under its stated
history-uniform hypotheses**. It proves uniform total-variation convergence
of the whole remote future, uniqueness of a stationary compatible law when
one exists, and triviality of both completed one-sided tails. Its explicit
infinite-memory example meets the hypotheses and has a stationary compatible
law. RESULT.md correctly leaves the unrestricted probability-only method
question unresolved. This verdict is a review of the coupling mathematics,
not an overall PR disposition.

No candidate code, receipts, or old-review contents were read before this
verdict. The source-first baseline, sealed earlier, used a distinct pathwise
agreement-length/defective-renewal derivation. The candidate uses a forcing
block and stopping-time argument. The two derivations agree on the relevant
subclass and the limits of its scope.

## Claim-by-claim adversarial assessment

1. **Normalized all-histories version.** The candidate starts with a measurable
   probability vector at every left-infinite history, not merely an a.s.
   conditional kernel. Its continuity bounds are uniform in all such pairs.
   Compatibility is an a.s. statement for the stationary law, and existence is
   assumed. These are enough to generate path laws from every history and
   compare a conditional stationary future to an arbitrary other generated
   future. There is no unsupported claim that arbitrary stationary processes
   admit a version satisfying the assumptions.
2. **Overlap and maximal coupling.** TV<=v_0<1 means the pair's diagonal mass
   is at least epsilon=1-v_0. A fresh uniform can select diagonal mass first,
   so U<=epsilon forces equality for each pair. This is valid even when no
   single symbol or measure minorizes all histories. The candidate's common
   output branch is pair-specific and does not claim a global minorizer.
   Zero residual mass is handled by the diagonal-only coupling.
3. **Agreement forcing and monotonicity.** The first run of l generated
   agreements is a stopping time in the enlarged coupling filtration. Each
   disjoint block of l auxiliary uniforms all <=epsilon independently forces
   such a run. The bound (1-epsilon^l)^floor(n/l) follows for all n>=l. The
   stated v_k are nonincreasing; true agreement moduli have this property.
   The candidate's block proof does not rely on treating the actual agreement
   process as Markov. As a function of n, the displayed minimum is
   nonincreasing because each fixed-l expression decreases and the allowed
   l set grows.
4. **Any later failure.** At the stopping time tau the histories agree in at
   least l terminal coordinates. On surviving a further k-l agreements,
   the next failure probability is <=v_k. The probability of that first
   failure event is <=v_k even after conditioning on the entire history at
   tau. Summing these disjoint first-failure events, or first using a finite
   horizon and increasing it, yields the summable tail bound. No Markov
   property of the agreement-length process, and no stopping-time status of
   the final disagreement time, is assumed.
5. **Remote-future law, quantitative indices.** On tau<=n, any mismatch at
   a coordinate n+1,n+2,... is among the failures after tau. Thus for
   every l<=n the actual probability of any such future mismatch is at
   most (1-epsilon^l)^floor(n/l)+sum_{k>=l}v_k. Taking the finite minimum
   and capping it at 1 is valid. This controls the full countable product law
   directly. It is not inferred from convergence of single-coordinate laws.
   First choosing a fixed large l and then letting n tend to infinity proves
   convergence; no uniform rate in l is needed.
6. **Conditional future law and stationary symmetry.** Repeated conditional
   expectations yield the g product for each finite future word on a single
   common full-measure set, using the countable collection of words and
   times. Cylinder uniqueness extends to the entire conditional path law.
   Integrating the second history gives the conditional remote-future bound.
   Its covariance bound yields alpha mixing. Stationarity translates cuts;
   commutativity of the covariance expression permits the same argument
   for the past tail. No reversed-kernel hypotheses are silently imported.
   Cylinder density/monotone class gives independence of each tail event from
   the full field and hence its zero-one law. Completing fields causes no
   change modulo null sets (details in the independent baseline).
7. **Uniqueness.** Randomizing the two starting pasts according to two
   compatible stationary laws preserves the uniform coupling estimate.
   Stationarity equates their far-future finite-block laws to fixed-position
   block laws; the bound tending to zero makes those laws identical. The
   two-sided process law is determined by these finite blocks. No general
   existence statement is attached to this uniqueness result.
8. **Infinite-memory example.** For the candidate's binary g, the probability
   range is [1/4,3/4]. A pair agreeing on k terminal symbols differs by at
   most (1/2)sum_{j>k}2^-j=2^(-k-1), with equality for opposite unmatched
   tails. Thus epsilon=1/2 and the continuity tail is 2^-k. Each coefficient
   is nonzero, so no finite order describes this kernel on the whole history
   space. Uniform convergence makes g continuous. The append-symbol kernel
   is Feller on compact metrizable history space. Weak compactness of its
   Cesaro averages and the telescoping difference prove existence of an
   invariant history measure. Its two-sided stationary Markov extension has
   history coordinates consistent with past output symbols at every time,
   so its symbol process is compatible. The example therefore realizes the
   theorem's existence assumption rather than only defining a formal g.
9. **No stronger inference.** The candidate makes no finite-mean final
   coupling-time claim. The independently reconstructed return process shows
   why unweighted summability would not suffice for such a claim. It also
   makes no bilateral-tail conclusion and no automatic reduction of all
   stationary processes to these hypotheses. Those limitations are correct.

## Independent reproducible controls before code inspection

`independent_controls.py` was written before candidate mathematics was read.
It uses exact fractions to check maximal coupling on 225 rational pairs,
including identical marginals and zeros; distinguishes pairwise overlap from
global minorization; checks renewal/Markov recursion through 96 times and
213 domination transitions; and gives logical controls for coordinate versus
full-future convergence and finite time versus finite expectation. Its first
execution failed at a hand-entered expected-value assertion. The correct
value 19/7 replaced 47/21; the initial source and failure streams are retained.

`block_bound_controls.py` was written after the mathematical candidate read
and before any candidate program read. It computes **full infinite-future
disagreement** exactly in finite-memory approximations: after M straight
agreements two M-history states are identical, so a subsequent mismatch is
impossible. It compares the candidate's bound for all 64 pairs of binary
3-history states, n<=12, and the two extreme 4-history states, n<=32. All
5,520 displayed-bound comparisons pass. This finite evidence checks constants
and indices; it is not the universal proof.

## Exact remaining gap

Uniform overlap can fail even for a random constant bit or a stationary
periodic chain, and general conditional kernels need not have summable
history-uniform continuity. The candidate gives no entropy-free mechanism
removing these restrictions. The original all-stationary finite-alphabet
completed-tail method question therefore remains unresolved by this route.
No novelty, current-openness, or peer-review conclusion is made.
