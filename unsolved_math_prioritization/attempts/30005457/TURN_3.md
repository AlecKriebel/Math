# Author turn 3: stochastic attainability and the topology barrier

**Partial negative result for a proposed proof strategy. Original stochastic percolation remains unresolved.**

The second turn supplied a percolating attracting equilibrium of the deterministic flow on its support face. This turn attempts to turn that construction into a positive-probability stochastic example. The usual finite-dimensional basin argument fails for a precise reason, stronger than merely lack of a cited infinite-dimensional theorem.

## 1. The constructed rate field has finite total activity

For the rates of turn2,

sum_v p(v) = 32/15 + 34/225 = 514/225.

The superposition of all the independent vertex clocks is therefore a Poisson process of finite rate514/225. One direct justification is to take an increasing exhaustion of the vertex set. The total ring count on a bounded interval increases to a random variable with finite expectation t sum_v p(v); it is therefore finite almost surely. Its probability generating function is the limit of the finite independent Poisson products, yielding the Poisson law with that summed rate. At each ring the vertex distribution is p(v)/(sum p), independently of the earlier ring locations.

In particular, only finitely many edge tallies have received any increment by any given finite time, almost surely. This does not imply that only finitely many edges survive forever: each individual positive-rate clock rings infinitely often over the infinite time horizon.

## 2. No entry into the proved attracting neighborhood

Let x* be the turn2 equilibrium and let E_line be its infinite positive-weight line. Its line weights approach zero at both ends. Under all-one initialization, for every finite t>0,

N_e(t)/t ≥ 1/t for every edge e.

Hence along E_line,

sup_e |N_e(t)/(t x*_e)-1| = infinity.

The stochastic scaled state is never in any bounded relative neighborhood of x*, at any finite time. This is a pathwise statement and does not require a probability estimate.

One might remove the initial baseline and use Y_e(t)=(N_e(t)-1)/t. That vector does have finite total mass at finite time, but only finitely many nonzero coordinates. Infinitely many edges in E_line then have Y_e(t)=0 and relative error exactly1. Thus

sup_(e in E_line) |Y_e(t)/x*_e-1| ≥1

almost surely at every finite time. In particular it never enters the relative radius1/100 neighborhood proved attracting in turn2. The same obstruction holds for every infinite-support positive target when the total clock rate is finite.

Therefore finite-dimensional positive-probability attraction cannot be imported by simply conditioning on a large finite initial segment of the trajectory. The candidate process does not enter the topology in which the attracting-neighborhood theorem was established.

## 3. Why weaker convergence does not repair the proof automatically

Coordinatewise convergence N_e(t)/t→x*_e remains logically possible: the order of the supremum over e and the limit in t cannot be interchanged. Likewise, convergence of Y(t) to x* in l1 is not excluded by the preceding result. The tail mass of x* is small, and finite-support vectors can approximate it in l1. Thus this is not a nonpercolation theorem and not an impossibility result for the candidate rate field.

However, the vector field is not uniformly well-conditioned near that tail in an unweighted norm. In the full graph, denominators are sums of squared local weights tending to zero at infinity. A perturbation that is small in absolute size can dominate every incident equilibrium weight sufficiently far away, change the local edge-choice ratios by order one, and fail to preserve the contraction established in relative coordinates. One must prove an appropriate weaker-topology attraction theorem rather than infer it from turn2's relative estimate.

The tail's stochastic startup is another independent issue. A finite set of desired early firings has positive probability, but prescribing increasingly many such events does not give a positive-probability intersection. The tree proof avoids this by supercritical branching, which the direct lattice-tree transfer in turn1 could not preserve. A valid moving-window construction would need summable failure estimates or a redundant percolation comparison on overlapping blocks. Neither estimate has been established here.

## 4. Outcome

This turn rigorously excludes the simple global-relative-basin stochastic-approximation argument for the explicit candidate. It leaves open whether that candidate, another rate field, or a cyclic/merging construction realizes stochastic percolation. The official uniqueness question is also unresolved. Three substantive author turns used; two remain unless solved earlier. Completion estimate remains15%.

Next route: investigate a moving-window or weighted-noise formulation that can use finite total activity without assuming uniform relative entry. The exact question is whether its error control can survive the increasingly delayed activation of the small-rate tail.
