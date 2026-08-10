# Independent proof reconstruction

This reconstruction was written from the exact stochastic model and the
released finite certificates, not by assuming the earlier candidate
manuscript.

## 1. Contradiction setup

Assume that one infinite closed irreducible population class has infinite
mean positive return count for its labelled embedded chain. The killed
transition-count construction yields probability occupations `nu_M`
escaping every finite population set. Bounded-test telescoping and bounded
reaction vectors give exact physical flow balance and a nonnegative endpoint
escape vector.

The occupation, rather than a selected state sequence, is pushed to the
compact active-set/source-flag descriptor. Disintegration and finite flow
decomposition give a terminal chart. Lower-cut averaging for its integer
workload gives nonnegative outward workload balance.

## 2. Independent reconstruction of the physical phase lemma

For each positive physical reaction retain its actual target and one
same-linkage return prefix. Build the finite bounded-coordinate/target phase
graph. If a closed phase class contained a positive edge but no negative
edge, its return certificate would remain inside the class and would have
positive initial reward but nonpositive total reward. One edge on that path
would be negative, contradiction. Thus every closed class is strict or
edgewise zero.

This argument uses no stationary distribution, rate comparison or future
conditioning.

## 3. Two independent debt proofs

### Stopped-drift proof

For positive aggregate physical debt,

\[
D_{k+1}-D_k\le-\mathbf1_{\{S_k\ge1\}}+A_k.
\]

Conditional service probability `p` and mean slower arrival `a<p` give
constant negative drift. Bounded-index optional stopping gives
`E tau_0 <= D_0/(p-a)`.

### Occupation-dual proof

If the mean debt return were infinite, finite-volume normalized transition
occupations would have a subsequential limit with zero interior flow
imbalance and nonnegative outward debt flux. Its mean debt increment would
be nonnegative. The service and arrival inequalities instead give

\[
\int \Delta D\,d\nu\le -p+a<0,
\]

a contradiction. This proof does not use optional stopping and independently
excludes a heavy-tailed critical debt occupation.

## 4. Physical reactivation

After service, the selector uses only the new population, actual target and
finite chart phase. A strict phase has another uniformly minorized service
path. A zero phase is transferred to the next slower physical trace. Loss of
support is an exit. No reaction origin or obligation history is needed.

Slower arrivals are controlled by compensators: the expected number of
carrier stages is geometric and the unprocessed hazard is at most
`epsilon_R` times the carrier hazard. This gives mean arrival
`O(epsilon_R)` and an exponential moment.

## 5. Finite source hierarchy

The fastest source layer has no positive edge. Inductively, a positive
layer event creates a faster actual target and is cleared through the already
processed layers. Effective edges are nonpositive. A strict finite recurrent
class has negative stationary mean. A zero class is edgewise zero and gives a
bounded phase coboundary. Vanishing reaction-count layers are observed at the
next slower normalization. Finiteness of the source set proves termination.

## 6. Boundary cases

Three active coordinates make every source enabled, so first-changing-layer
strict flux is direct.

For two active coordinates, the three independently reproduced atlas
implementations certify the invariant, deficiency-zero and service
exceptions. All remaining available linkages use the debt hierarchy.

For one active coordinate, exact rate polynomials separate quadratic,
linear and constant layers. Quadratic sources drain. Linear edges are
nonpositive. Constant births create actual faster targets. The finite
service-token alternative gives strict service or an affine invariant.

## 7. Return-time conclusion

Every terminal chart contradicts outward Green balance through strict
negative flux, structural exit, affine invariance, product-form stationarity
or service descent. Hence embedded return count is finite.

Total jump rate is uniformly bounded below on nonabsorbing states, so
physical return mean is finite. Population-increasing intensity is at most
linear in total population; a pure-birth comparison and finite-shell bounds
give nonexplosion. Positive recurrence and uniqueness follow.
