# Author approach 4: concave cyclic-polygon energy and gauge invariants

Status: a proved analytic lemma and a conditional injectivity criterion. The graph-combinatorial hypotheses below have not been proved for every critical graph, and no general injectivity theorem is claimed.

## Motivation and proposed construction

For each black vertex b of a contracted reduced plabic graph, list its strand labels cyclically. The positive angular gaps α_{b,e} around that vertex sum to π, and the critical edge weight is sin α_{b,e}. Define the Lobachevsky function on (0,π) by

    Λ(x)=−∫₀ˣ log(2 sin u) du,

and the energy

    E(θ)=Σ_b Σ_{e incident to b} Λ(α_{b,e}(θ)).

The gaps depend affinely on θ. The aim is to turn equality of boundary measurements into equality of ∇E and apply strict concavity.

## Lemma: strict concavity on each cyclic angle simplex

For r>=3, the function Σ_{i=1}^r Λ(α_i) is strictly concave on α_i>0, Σ_i α_i=π. Equivalently,

    Σ_i cot(α_i) z_i² > 0 whenever Σ_i z_i=0 and z is nonzero.

Proof. If every α_i<π/2, the assertion follows termwise. If one angle equals π/2, all other cotangents are positive and the constraint removes the possible zero direction. At most one angle can exceed π/2. Suppose it is α_r, and put β=Σ_{i<r}α_i=π−α_r<π/2. Weighted Cauchy–Schwarz gives

    Σ_{i<r} cot(α_i) z_i² >= (Σ_{i<r}z_i)² / Σ_{i<r}tan(α_i).

For at least two positive angles with total β<π/2, the tangent addition identity and induction give Σ_{i<r}tan(α_i)<tan β. Since cot α_r=−1/tan β and Σ_{i<r}z_i=−z_r, the claimed quadratic form is positive when z_r≠0. When z_r=0, positivity follows from at least one nonzero coordinate among the remaining positive-cotangent terms. Finally Λ''(x)=−cot x, proving strict concavity.

Thus E has negative-definite Hessian precisely when the only variation preserving every black-vertex gap is the permitted common rotation on each connected component.

## Conditional gauge-annihilation criterion

Let L be the linear map taking θ to all black-vertex gaps (constants π in wrap-around gaps are ignored in its derivative). Let U be the usual edge-by-interior-vertex gauge matrix: an entry is 1 when the edge meets that vertex. Boundary edges have fixed weight 1, so a gauge comparing two normalized critical weight systems has zero parameter at every white vertex adjacent to the boundary.

Assume:

1. For every allowed gauge vector u, Lᵀ Uu=0, restricting to non-boundary edges.
2. The kernel of L consists only of the componentwise rotations already removed from Θ_f.
3. Equality of positive boundary measurements on the chosen reduced graph is equivalence under these interior vertex gauges.

If Meas_f(θ)=Meas_f(η), then for some allowed u,

    log sin α(θ) − log sin α(η) = Uu.

Hence

    ∇E(θ)−∇E(η) = −Lᵀ Uu = 0.

By the proved strict concavity, θ=η. This is a sufficient criterion for interior injectivity. If the invariant gradient is continuously recovered on the measurement image, its locally nonsingular Jacobian also supplies continuity of the inverse.

## Progress on the missing combinatorics

Black-vertex gauge terms cancel automatically, because its angular gaps sum to π. For an interior white vertex they cancel if the black-defined oriented gap along every incident edge agrees consistently with the cyclic gap orientation at that white vertex. A plausible verification uses weak separation of adjacent face labels: an edge labeled {p,q} belongs to a black clique with union J and a white clique with intersection I, with J=I∪{p,q}. A black third label r and white third label s on opposite arcs would make {p,q} alternate with {r,s}, contradicting weak separation.

This observation is not promoted to a proof here. One must establish the exact clique/edge-label correspondence and orientation conventions for all relevant reduced graphs, handle all boundary and contracted configurations, and prove the kernel statement without circularly assuming the injectivity conjecture or the expected dimension of Crit_f. The source's general injectivity conjecture therefore remains unresolved in this report.

## Boundary obstruction to completing the campaign target

Even a complete proof of the above interior criterion would not identify images of compactification faces. At colliding angles the edge logarithms diverge, selected scale ratios survive (approach 3), and Hessian information alone gives neither a convex face realization nor the required stratification. Interior injectivity is useful but is not a substitute for the target.
