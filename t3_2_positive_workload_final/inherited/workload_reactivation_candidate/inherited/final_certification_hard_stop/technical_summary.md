# Technical summary

## Objective

The project attempted to certify the candidate theorem that every
bimolecular weakly reversible network with at most three active species and
at most two linkage classes is positive recurrent on every closed class.

## Certified finite structure

The candidate's finite workload atlas survives three independent exact
implementations.  The common-invariant, deficiency-zero and two service
branches are unchanged.  The service endpoint is correctly stated as

\[
W_\tau\le W_0-1.
\]

## Certified infinite-state component

For an embedded labelled reaction chain killed on return or finite-volume
exit, normalized expected labelled transition counts form probability
measures, escape every fixed finite set when the mean return count is
infinite, and satisfy exact bounded-test and linear endpoint balance.  This
avoids integrating unbounded quadratic propensities under a time
normalization.

## Defect found

The proposed G3 repair conditioned on the first reaction from a selected
linkage and claimed that the activation channel plus the following
same-linkage target episode had expected payoff tending to minus infinity.
This is false even for

\[
0\to2A\to A\to0.
\]

Conditioning on `0->2A`, the complete fixed-path block has

\[
J_n=\frac{7\log n+1}{n^2}
     +O\!\left(\frac{\log n}{n^3}\right)>0
\]

for all sufficiently large `n`.  The physical chain remains positive
recurrent; the example refutes only the conditional activation implication.

## Remaining theorem

A correct proof must charge each activation jump, the post-target episode and
intervening shielded-linkage waiting exactly once at their physical
source-rate layers.  It must prove strict negative mean after normalization,
or linkage deletion, structural exit or an affine invariant.  This
rate-weighted current-target charging theorem is not yet proved.

## Consequence

The finite atlas is a certified partial result.  The T3-2 theorem and any
three-species counterexample remain unestablished.  No theorem manuscript or
priority audit is included.
