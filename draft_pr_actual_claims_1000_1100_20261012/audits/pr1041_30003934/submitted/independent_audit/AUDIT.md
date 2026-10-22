# Independent audit of the rank-one uniqueness reduction

## Scope and verdict

Audited on 2026-10-09. This is an independent mathematical audit of `HARDNESS_DRAFT.md`, initially read at SHA-256 `2d3599e9bc2b0b28141d3d034c357086dd99cd6a8ec4e061dc6a82744f4e0beb` (9,942 bytes). The target is explicitly encoded rational, variable-dimension bimatrix games with `rank(A+B)=1`; arbitrary degeneracy is allowed, and uniqueness means uniqueness of the strategy pair.

**Verdict on the mathematics: the proposed reduction is accepted subject to incorporating the source-preservation proof and the minor precision corrections stated below. No blocking counterexample or unresolved mathematical step was found.** In particular, the initial draft's source-quantifier gap has a rigorous solution: globally preserving strict residual path comparisons makes the perturbed SSP run a valid unperturbed SSP run. It is unnecessary to derive a separate mixed-state gap once the cited SSP lemma is used with its stated, unrestricted shortest-path choices.

The initial draft itself labels this point unresolved. That label cannot simply be deleted: replace it with the explicit argument in Section 2 of this audit. The audit does not authorize a stronger nondegeneracy-promise claim. It does not make any publication or queue change.

## 1. Primary source and the exact dependency

Primary source inspected: Yann Disser and Martin Skutella, *The Simplex Algorithm Is NP-Mighty*, ACM Transactions on Algorithms 15(1), Article 5 (November 2018), DOI `10.1145/3280847`, especially Section 3, Lemmas 3.1–3.2, and Corollary 1.7.

Public author-hosted PDF: https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf . The local inspected PDF has 553,046 bytes and SHA-256 `88cc527ec698aaa502a93c33183ae58b714a4879ca387b1101208c7dc329ff5a`. The public URL was independently opened successfully. The supplied extraction was inspected, with the network figure also visually checked in the PDF.

The needed source fact is the behavior of the constructed SSP execution, not an interpretation of Corollary 1.7 as a statement about all optimal flows. The construction has integral capacities; SSP has unit augmentations, and use of the distinguished arc occurs in a forward/backward pair exactly for a successful partition state. The SSP definition permits a shortest path, without prescribing a special tie rule. The source proof determines this behavior from shortest-path choices. No unique-optimum assumption is imported from that source.

**Rejected inference:** Corollary 1.7 by itself proves that every optimal flow in a no instance avoids the distinguished arc. Its selected-parametric-flow wording does not alone establish that quantifier. The strengthened property follows instead from the perturbation and uniqueness arguments below.

## 2. Closing the perturbation-preservation gap

The initial draft used the following binary perturbation. The final manuscript uses an equally valid ternary variant, checked at the end of this section.

Let `delta=epsilon_0/10` and enumerate the `p` original arcs by `i=0,...,p-1`. All original arc costs are integer multiples of `delta`:

- `a_i/2 = 5 w_i delta`;
- `epsilon_0/5 = 2 delta`;
- the half-integer part of an expensive arc is also a multiple of `delta`, since `delta=1/(240S)`.

Set `eta=delta/2^(p+4)` and add `eta 2^i` to arc `i`. Put `T=eta(2^p-1)`, so `T<delta/16`.

At any residual state, a simple residual path uses each original arc at most once, in its forward or reverse direction. Its perturbation has magnitude at most `T`. Thus the cost difference between two simple residual paths changes by at most `2T<delta/8`. Their original difference is an integer multiple of `delta`; every originally strict comparison is therefore preserved.

Consequently, at every state, a shortest path for the perturbed costs is a shortest path for the original costs. Suppose otherwise that the selected path were originally longer than some competing path. That strict comparison would survive perturbation, contradicting selection. Capacities and residual updates are unchanged. Inducting over augmentations, the entire perturbed execution is a legitimate original-cost SSP execution, using some permitted resolution of any original ties. The cited SSP lemma therefore applies to this entire execution, including each odd iteration after a gadget advances. A separate quantitative bound for those odd iterations is not needed.

This argument must concern residual paths globally, not merely the initial DAG's paths. The bound above does: reversed arcs receive the negative perturbation and are already included. Residual shortest walks can be chosen simple because an optimal flow has no negative residual cycle; zero-cost walks can be reduced to a simple path. Initially the graph is acyclic. Standard SSP optimality preserves the absence of negative residual cycles.

**Accepted claim:** the perturbed SSP has the required distinguished-arc behavior, with exactly the original capacity-driven unit augmentation pattern.

Final-manuscript variant: let `D` be a common denominator of original costs, number arcs `i=1,...,p`, and use `rho_i=1/(4D 3^i)`. Then `sum rho_i<1/(8D)`, and a pairwise path-cost difference changes by less than `1/(4D)`, smaller than every nonzero original difference. The same valid-execution coupling applies. For a zero-original-cost simple cycle, the earliest nonzero ternary term dominates the absolute sum of all later terms, so its perturbed cost is nonzero. This is the perturbation implemented by the exact-arithmetic verification script. Both variants have polynomial encoding length.

## 3. All-optimum quantifiers, degeneracy, and half augmentation

For a sign-conformal simple residual cycle, the original cost is an integer multiple of `delta`. If it is nonzero, the perturbation of magnitude at most `T` cannot cancel it. If it is zero, the perturbation is a nonzero signed sum of distinct powers of two: the largest power strictly exceeds the sum of all lower powers. Thus such a cycle cannot have zero perturbed cost.

Precision correction: a formal two-edge traversal consisting of an original arc and its own reverse has zero cost under every cost assignment. Do not claim these purely cancelling traversals are absent. They do not affect the uniqueness argument. A nonzero difference `g-f` of two flows is represented using only the sign of each original arc's difference, so its residual circulation uses at most one direction of each original arc.

Fix any real feasible value `q`, including endpoints and breakpoints. If two distinct minimum-cost flows `f,g` existed, their sign-conformal difference would decompose into positive amounts of simple residual cycles for `f`. Every such cycle has nonnegative cost, because a negative cycle could be augmented slightly and improve `f`. Their total cost is zero because `f,g` have the same objective. Every cycle in the decomposition must therefore have zero cost, contradicting the preceding property. Hence every fixed-value optimum is unique. This proof is valid for fractional `q` and uses no nondegeneracy of the flow polytope.

In a no instance the perturbed SSP never uses `e`, so its unit-step interpolation has `f_e=0` for every `q` from zero through `F`. It is optimal throughout. Uniqueness now gives the required universal quantifier over all optima.

In a yes instance, a forward use of `e` begins after `2j` unit augmentations and raises its flow from zero to one. At the midpoint, `q=2j+1/2` and `f_e=1/2`. Because `0<=j<=2^n-1` and `F=2^(n+1)`,

`q <= F-3/2`.

The partial augmentation is optimal at its intermediate value. The full paired augmentation is completed before termination, so this is not an endpoint-only event.

**Accepted claims:** universal no-instance exclusion; yes-instance half-edge witness; all real parameter values; adequate distance from `F`.

## 4. Positive costs and polynomial source encoding

The potential transformation is valid on every fixed-value feasible flow:

`sum_(u,v) (r(v)-r(u)) f_(u,v) = (r(t)-r(s)) q`.

Thus adding `H(r(v)-r(u))` to each arc cost changes the fixed-`q` objective by a constant and preserves all optimizing flows. On every residual s-to-t path it similarly adds a path-independent constant. A topological ordering has `r(v)-r(u)>=1` on an original arc, so `H=1+max |cpert_i|` makes every original arc cost strictly positive. The graph is a DAG, including its distinguished cross arc: order all source-chain vertices before all sink-chain vertices.

There are `O(n)` vertices/arcs. The capacities `2^i` and `F` have `O(n)` bits. The perturbation denominators acquire only `O(p)` bits beyond the original denominators. Topological ranks, `H`, and the transformed costs have polynomial encoding length. Computing the reduction does not execute the exponentially long SSP run.

**Accepted claim:** the source network and its costs can be produced in polynomial time and size.

## 5. Simplex embedding and feasible range

The simplex has `p+2` coordinates. Here `h=F(1-x_0)` is linear when represented as `F sum_(i!=0) x_i`, so all matrix coefficients can be written without an extra affine variable. The map is injective:

`x_i=f_i/(LF)`, `x_*=h/F-sum_i f_i/(LF)`, `x_0=1-h/F`.

The unused mass is assigned to a single slack coordinate. There is therefore no artificial multiplicity of row strategies representing the same `(f,h)`.

For every simplex point, `sum f_i<=Lh` and `f_e<=Lh`. With `K=1/(2L)`,

`q=h-K f_e >= h/2 >=0`.

For every feasible network flow on the DAG, decomposition into source-to-sink paths gives `sum f_i<=Lq`, where `L=|V|-1`. There are no nonzero feasible circulations to invalidate this bound.

A zero-`e` maximum flow exists. Scaling it yields a feasible embedded point for every `lambda` in `[0,F]`. At a no instance the unique original optimum has `f_e=0`, so it is not removed by `h<=F`. At a yes instance the midpoint witness satisfies

`h=q+K/2 <= F-3/2+K/2 < F`,

since `L>=1` gives `K/2<=1/4`. It too survives the restriction. It is unnecessary to claim that every original optimal flow of every yes-instance parameter survives the restriction.

**Accepted claims:** injective simplex encoding; nonnegative `q` globally; uniform LP feasibility; no-instance optimum preserved; at least one yes-instance crossing preserved.

## 6. Uniform exact penalty: all minimizers, including degenerate LPs

The displayed dual is correct:

`mu>=0`, `nu 1 <= c+R^T mu`, maximize `nu-(r+s lambda)^T mu`.

Its feasible region does not depend on `lambda`. It is nonempty: choose `mu=0` and `nu<=min_i c_i`. It is pointed. Indeed, if a direction generates a line in it, `mu>=0` forces its `mu` coordinates to vanish, and the remaining inequalities force its `nu` coordinate to vanish as well.

For each `lambda` in `[0,F]`, the primal is feasible and compact, so it has finite attained optimum; LP strong duality supplies an attained dual optimum. The dual optimal face is a nonempty pointed polyhedron and hence has a vertex. A vertex of this face is a vertex of the dual polyhedron: a nontrivial convex decomposition in the whole polyhedron would, by optimality, lie in the same face. This remains true with redundant constraints, rank-deficient equalities, degenerate vertices, and positive-dimensional optimal faces.

After clearing denominators, a vertex is determined by `d_0=k+1` independent active equations. Their coefficients and right-hand sides are bounded by `H_0`. Cramer's rule gives an absolute bound `d_0! H_0^d_0` for every coordinate because the nonzero integer denominator determinant has absolute value at least one. Thus `C=k d_0! H_0^d_0` bounds the 1-norm of a selectable optimal `mu`, uniformly in `lambda`.

For `v=max(0,max_j(R_jx-r_j-s_j lambda))`, the selected dual vector gives

`c^T x >= LPopt - ||mu||_1 v`.

Therefore, with `M=C+1`,

`phi_lambda(x) >= LPopt + v`.

Every infeasible point has `v>0` and cannot minimize; every feasible LP optimum attains equality at `v=0`. This proves equality of the full minimizer sets, not merely existence of one feasible penalized minimizer. The integer `M` can be numerically enormous but has polynomial binary length. Clearing a polynomial list of polynomial-bit denominators by their product remains polynomial-bit.

**Accepted claim:** uniform, polynomially encoded, strict exact penalty for every parameter needed by the reduction.

## 7. Matrix signs, rank, and zero-sum equivalence

With the draft's definitions,

`-A_col(j)^T x + lambda b_j = c^T x + M(R_jx-r_j-s_j lambda)`.

The baseline column contributes `c^T x`; maximizing the displayed expressions gives exactly the penalized objective. Hence optimal row strategies of the auxiliary zero-sum game are exactly the penalized minimizers. There is no sign reversal or switched max/min.

The identity `A+B=a b^T` is exact. Both factors are nonzero: `a_0=-epsilon<0`, and the parameter equality is encoded with both signs, producing `b_j=+M` and `b_j=-M`. Thus the rank is exactly one, rather than merely at most one.

At `lambda=a^T x`, replacing `B` by `-A+1 lambda b^T` changes none of the column player's expected payoffs against `x`. Replacing `A` by `A-1 lambda b^T` changes each row's payoff against a fixed `y` by the same scalar. Both players' best-response sets are preserved. This establishes both directions of the equilibrium equivalence for arbitrary mixed strategies and degeneracy.

**Accepted claims:** exact penalty-game correspondence, exact rank one, and full equilibrium correspondence.

## 8. The default equilibrium really is one strategy pair

For `lambda<0`, the parameter violation `q-lambda` is everywhere positive. Positive transformed costs and `q>=h/2` imply

`phi_lambda(x) >= c^T x+M(q-lambda) >= -M lambda`.

At the distinguished row `x_0`, equality holds. Any other simplex point has `h>0`, hence `q>0`, so the first lower bound is strictly above `-M lambda`. The optimal row strategy is therefore unique for every negative parameter. Its only possible intersection with `lambda=h-epsilon` is `lambda=-epsilon`.

At that point, the `q-lambda` penalty column has strictly greater value than every other penalty column at `x_0`: conservation and baseline columns have zero, the opposite parameter column has `-epsilon`, and capacities have `-u_i<0`. Thus the optimal opposing strategy is the unique pure distinguished column. This step is essential: row uniqueness alone would not prove equilibrium-pair uniqueness.

Directly in the original bimatrix game, the distinguished column strictly favors row zero because every other row has `q_i>0`, and row zero strictly favors that column over every other column. Thus the default pair is a known strict pure equilibrium, independently of the partition answer.

**Accepted claims:** no extraneous negative-parameter equilibria; exactly one default strategy pair; strictness for both players.

## 9. Nonnegative crossings, endpoints, and complexity direction

Every original equilibrium has `lambda=a^T x=h-epsilon` in `[-epsilon,F-epsilon]`. For every nonnegative candidate parameter, the exact-penalty result applies because this interval lies in `[0,F]`. Network feasibility gives `q=lambda`. Combining the two equalities yields

`K f_e=epsilon`, equivalently `f_e=1/2`.

At `lambda=0`, the DAG's only zero-value feasible flow is zero, so no extra crossing occurs. There is no uncontrolled high-parameter tail because candidate `lambda<=F-epsilon<F`.

In a no partition instance, every original optimum has `f_e=0` and is retained by the simplex restriction. The restricted LP therefore has no minimizing flow with `f_e=1/2`. Only the strict default equilibrium remains.

In a yes partition instance the retained half-augmentation optimum gives an additional crossing. A finite zero-sum game always has an optimal opposing strategy, and pairing it with this row optimizer gives an additional original equilibrium. Its nonnegative parameter distinguishes it from the negative-parameter default.

Thus the map is a polynomial many-one reduction from PARTITION to NONUNIQUENESS, equivalently from its coNP-complete complement to UNIQUENESS. Together with the separately proved NP certificates for rational equilibrium nonuniqueness, it establishes coNP-completeness of the stated rank-one uniqueness problem. On the full language rather than a rank-one promise, invalid-rank inputs can be handled in polynomial time.

## 10. Required final-draft edits and claims not established

Required precision edits:

1. Replace the currently unresolved SSP robustness paragraph with the global grid-gap / valid-original-execution proof from Section 2.
2. Explicitly state that the source SSP statement has no special tie rule. Do not substitute the weaker selected-path statement of Corollary 1.7.
3. Qualify the no-zero-cycle assertion to exclude a formal original-arc/reverse-arc cancellation and use a sign-conformal decomposition for uniqueness.
4. Expand the dual-vertex existence justification to identify pointedness and its nonempty optimal face; do not assume nondegeneracy.
5. Preserve the all-minimizers conclusion of exact penalty and the unique opposing-column argument at the default equilibrium.

Rejected or outside-scope claims:

- Hardness from Corollary 1.7 alone, without resolving all-optimum quantifiers: rejected.
- Uniqueness of the default pair merely from uniqueness of its row strategy: rejected.
- A reduction polynomial in the numerical value of `F` or `M`: not required; their binary lengths are the relevant quantities.
- Hardness under a promise that the entire game is nondegenerate: not established here.
- A statement that every yes-instance parameter retains every original optimum inside the simplex: neither proved nor needed.
- Computational examples as proof of the general reduction: rejected. They are supplementary tests only.

No other mathematical correction requirement was identified in this audit.

## 11. Independent exact-arithmetic rerun

The author's script was independently inspected and run from its definitions. Its SHA-256 is `30058eb03038c92692bde0b7140c6e5bca9fe399fb0a1f66c71c52a2d81c14d1`. All six full matrix-construction results and all 39 network-sweep results were reproduced exactly, matching the original JSON output. Four auditor-selected full constructions were additionally tested: weights `[2,3,5]`, `[2,4,7]`, `[1,2,4,7]`, and `[1,3,6,11]`. All passed, including the exact default best-response inequalities, the outer-product identity, and the additional equilibrium best-response inequalities in the two yes cases. The determinant-bound penalty parameters had 5,400, 5,427, 7,552, and 7,602 bits respectively.

The independent results are recorded in `exact_rerun.json`. These are finite supplementary checks and do not establish the no-instance universal absence of other equilibria, which is proved in the preceding sections.
