# Author turn 2: a stable percolating deterministic equilibrium

**Scoped partial theorem, pending independent review. No stochastic lattice counterexample is claimed.**

A second possible approach was to prove that polynomial lattice growth forbids a stable percolating equilibrium of the deterministic WARM flow. The following explicit construction refutes that approach in its stated deterministic form. It also isolates the stochastic attainability gap.

## 1. Rates and support on the actual nearest-neighbor lattice

Take d=2, alpha=2 and q=1/16. Write vertices as (n,y) in Z². Set

p(0,0)=2q/(1+q)=2/17,

p(n,0)=[(1+q²)/(1+q)] q^(|n|-1), for n≠0,

p(n,y)=q^(|n|+|y|), for y≠0.

All rates are strictly positive, bounded above by1, and have infimum zero. No edges are removed from the underlying lattice. Define a nonnegative candidate weight vector x as follows:

- On the whole horizontal line y=0, the edge joining (n,0) to (n+1,0) has weight x_n=q^min(|n|,|n+1|)
- In every other horizontal row y≠0, pair (2k,y) with (2k+1,y), for every k in Z, and give that edge weight p(2k,y)+p(2k+1,y)
- Every other lattice edge has weight zero

Every vertex has at least one incident positive weight. The support has exactly one infinite component, the entire line y=0, and all other components are dimers. Both total rate and total positive-edge weight are finite. For example, the line mass is 2/(1-q)=32/15; the sum of off-line rates is 2q(1+q)/(1-q)²=34/225.

These zero equilibrium weights are not zero initial tallies. The stochastic problem retains N_e(0)=1 everywhere. The distinction is indispensable.

## 2. Exact equilibrium identity

Use logarithmic-time normalized flow

F_e(x) = -x_e + sum over v incident to e of p(v) x_e² / S_v(x),

where S_v(x)=sum over f incident to v of x_f². This is the alpha=2 WARM drift from the primary source. All its denominators are positive at the constructed x.

At an off-line matching edge only that edge has positive weight at either endpoint. Its reinforcement rate is therefore p(u)+p(v)=x_e. At every unsupported edge the numerator is zero, so F_e=0.

For a line edge n≥1, its weight is q^n, its inner endpoint has rate C q^(n-1), and its outer endpoint has rate C q^n, where C=(1+q²)/(1+q). The two selection probabilities are q²/(1+q²) and1/(1+q²). Therefore its total reinforcement rate is

C q^(n-1) q²/(1+q²) + C q^n/(1+q²) = q^n.

For the edge n=0, the central endpoint selects it with probability1/2, while its other endpoint has rate C and selects it with probability1/(1+q²). Thus its reinforcement rate is

q/(1+q) + C/(1+q²) = 1.

Reflection gives all negative-index line edges. Hence F_e(x)=0 for every edge of the full lattice, and x is an exact percolating equilibrium with admissible rates.

## 3. Linear stability in relative coordinates on the support face

Restrict the deterministic flow to the invariant face on which all unsupported edge weights stay zero. Let a supported edge's perturbed weight be x_e(1+h_e). The relative variables h belong to l-infinity of the supported edges. In a fixed small ball around h=0, the induced vector field is uniformly continuously differentiable: only the far-line, central-line, and dimer local forms occur, with scale canceled by relative coordinates. Thus the Banach-space ODE is locally well-defined without appealing to an unbounded infinite matrix.

For a line endpoint v, write a_ve=x_e²/S_v(x) at equilibrium. The relative Jacobian B has

B_ee=-1+D_e, where D_e=2 sum_v (p(v)/x_e) a_ve(1-a_ve),

and nonpositive off-diagonal entries. Their absolute row sum is exactly D_e, since each line endpoint has just one other supported edge. Direct substitution gives

D_e=32/257 for every noncentral line edge,

D_e=17/257 for the two edges incident to(0,0).

For dimers B_ee=-1 and all off-diagonal entries vanish. Consequently the l-infinity logarithmic norm of B is at most

max_e[-1+2D_e] = -193/257 <0.

This establishes uniform exponential stability of the linearized relative-coordinate system on the support face.

## 4. Explicit nonlinear neighborhood

The linear estimate can be upgraded on this same face without an unstated compactness argument. Let eta=1/100 and assume sup_e|h_e|≤eta. At a line endpoint define the perturbed choice probability

a_ve(h)=x_e²(1+h_e)² / sum_f x_f²(1+h_f)².

For its two incident supported edges e,f,

a_ve(h)a_vf(h) ≤ a_ve(0)a_vf(0) [(1+eta)/(1-eta)]^4.

Differentiating the relative drift shows that the diagonal positive correction plus the absolute off-diagonal row sum is at most

[2D_e/(1-eta)] [(1+eta)/(1-eta)]^4.

Uniformly over all line edges this is bounded by the exact rational number

665986566400 / 2444044428243 < 1/3.

The dimer correction is zero. The entire relative drift therefore has l-infinity logarithmic norm at most -2/3 throughout this ball. Integrating the Jacobian along the segment from0 to h, or using the upper right Dini derivative of the sup norm, gives

||h(tau)||_infinity ≤ exp(-2tau/3) ||h(0)||_infinity.

The estimate prevents exit from the ball and proves forward existence there. Thus the percolating equilibrium is locally exponentially attracting **within its invariant support face**, uniformly in the relative norm. Here tau is the deterministic logarithmic-time variable, not the stochastic physical clock.

## 5. Exact limitation: attainability from unit tallies

The construction neither proves a positive-probability stochastic realization nor rules it out. At each finite stochastic time every initial-unit edge still has positive tally. The process is not literally on the face used above. Moreover x_e tends to zero at infinity, so small coordinatewise or unweighted absolute errors do not imply small relative error uniformly over all edges.

Even proving stability against off-support perturbations would leave a further problem: reaching and remaining in an infinite relative neighborhood from all-one initialization. The finite-graph stochastic-approximation theorem cannot be applied to this countably infinite shrinking-scale configuration without new uniform estimates. A countable collection of separately positive-probability local startup events need not have positive intersection probability.

The useful conclusion is precise: an impossibility proof cannot rely merely on absence of stable percolating deterministic equilibria under the allowed rate hypotheses. The source-literal stochastic existence and uniqueness questions remain unresolved. Two substantive author turns used; three remain unless solved earlier. Completion estimate15%.

`verify_partial.py` checks the equilibrium values on finite coordinate controls, checks all displayed exact stability constants, and records 4,300 exact assertions. These controls support the symbolic proof; they do not simulate or certify infinite-time stochastic survival.
