# Smallest remaining theorem: rate-weighted current-target charging

The finite atlas and the embedded reaction-count Green theorem do not by
themselves close the stochastic proof.  The smallest unresolved interface is
the following.

## Rate-Weighted Current-Target Charging Theorem

Fix an escaping embedded labelled-reaction occupation in a terminal
three-species, two-linkage chart.  Suppose one linkage is in the available
branch of the certified bimolecular top-complex classification.  Every actual
reaction from that linkage creates an actual target mark, and from that mark
a fixed same-linkage target-following episode has the certified scalar-envelope
estimate.

Partition the physical path into:

1. current-target episodes begun immediately after actual reactions from the
   available linkage;
2. intervening reactions from the other linkage;
3. structural chart and workload exits.

Prove exactly one of:

1. the available-linkage reaction count is bounded, so its total bounded-jump
   displacement is negligible and the escaping occupation reduces to the
   other linkage;
2. after normalization by the available-linkage reaction count, the sum of
   **all** activation jumps, current-target episodes, intervening waiting
   rewards and finite phase corrections has strictly negative mean;
3. positive normalized structural-exit flux occurs;
4. the zero class carries one affine physical/phase invariant positive on the
   escape cone.

The accounting must be pathwise or Green-exact.  No reaction may be counted
both as the terminal deviation of one episode and as the uncharged activation
of the next.  The theorem must remain valid when:

- the available linkage is asymptotically rare;
- its first reaction is workload-increasing;
- a shielded linkage makes arbitrarily many faster neutral jumps;
- the activation probability is `O(1/N)`;
- the terminal target reward grows only like an iterated logarithm;
- inactive-coordinate boxes grow along the Green sequence.

## Why the preceding repair is insufficient

The false conditional-activation lemma conditioned on the first linkage
reaction and then applied the scalar envelope only after that reaction.  The
exact counterexample in
`failed_approaches/conditional_activation_counterexample.md` shows that the
conditioned block can have positive expected payoff tending to zero.  The
activation jump must instead be charged at its physical source-rate layer,
while the post-target episode must retain the carried-target probability
coupling.

A finite shell Dirichlet equation can calculate the value of a supplied
partition, but it does not construct this nonoverlapping partition or prove
its negative source-layer mean.  That construction is the remaining theorem.
