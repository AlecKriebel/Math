# Independent analytic review — Zenodo 23430642

**Verdict: PASS at the stated hypotheses.** I found no substantive mathematical defect in the published reduction or membership argument after reconstructing the full proof, checking the load-bearing primary interfaces, building independent exact controls and replaying the supplied computational interfaces. This is an AI analytic review, not conventional human peer review, a formal proof certificate or a priority determination.

## Exact target and bound edition

The reviewed paper is *A flow reduction for equilibrium uniqueness in rank-one bimatrix games*, version **1.0**, dated **13 October 2026**, nine published pages. The target is **uniqueness of the entire mixed-strategy pair** in explicitly listed rational bimatrix games of variable positive dimensions, with **exact** rank(A+B)=1. Arbitrary degeneracy, zero probabilities and positive-dimensional equilibrium sets are included. The paper proves coNP-completeness of uniqueness and NP-completeness of nonuniqueness under polynomial many-one reductions. Hardness remains when a strict pure equilibrium is supplied.

This is not a result about unique payoff vectors, fixed dimensions, strongly NP-hardness or a nondegenerate-input promise. It does not contradict the polynomial algorithm for finding one equilibrium of a rank-one game.

| Immutable asset | SHA-256 |
|---|---|
| `sources/paper.pdf` | `3ba83c50a4a2369a70897ee165a43f56324aa31574cf9c199e664174cbce0449` |
| `sources/supportkit-v1.0.tar.gz` | `cd20964fe478365bd9c2db9b6cd8f6032aea0168073e7da21149865ec2f6d34c` |

Both hashes were checked against the fresh acquisition receipt before work. The final verdict additionally binds that receipt, raw record, full TeX, necessary support and all review evidence. All nine PDF pages and all 287 TeX lines were read. The corresponding PDF and TeX give the same mathematical argument. I also read the complete `SUPPLEMENT.md` to identify computational interfaces, then both executable helpers after completing my independent controls. No separate supporting mathematical reader PDF is needed by the current manuscript's proof.

## Reconstructed proof and attempted failure points

### 1. Source normalization and finite network

The source input is a nonempty list of positive integers. With S their sum, αᵢ=wᵢ/(24S), η=1/(24S) and δ=η/5, all αᵢ are positive lattice multiples of η, their sum is 1/24, and a nonzero signed sum has absolute value at least 5δ. The signed binary states enumerate all subsets; zero signed sum is exactly PARTITION. This normalization has polynomial binary length even when the weights are large.

The listed graph has V=4n+6 vertices and p=8n+7 arcs. The displayed source/sink order is a genuine topological ordering, including the bridge from the positive source base to the negative sink base. The source cut gives F=2^(n+1). The explicit zero-bridge maximum flow is feasible even at n=1: the top-level cheap/cross arcs each carry 2^(n−1), and conservation holds at both intermediate endpoints with lower arcs empty. Scaling supplies a zero-bridge feasible flow for every real demand in [0,F]. Because the original graph is acyclic, its only nonnegative value-zero flow is zero, irrespective of initially negative cheap-arc costs.

### 2. The source event is an all-path statement

The Disser–Skutella argument was checked in the complete author-hosted journal body, not inferred from the hardness theorem's title. Its state progression, signed costs, base adjustment, bridge direction and two-augmentation restoration agree with the current paper. At each level, the cheap phase runs the lower gadget forward and the crossed phase reverses it; the unused mixed connector routes are separated from the selected phase by a strict cost gap. The bounded signed perturbations and δ fit well inside that gap. The state interval [j−T−δ,j+T+δ] is separated from the next one because 2(T+δ)<1.

At synchronized even states the two whole-gadget paths have costs j±z+δ and the forward bridge path has cost j. At odd states the values are j±z−δ and j−2δ. When z is nonzero, its lattice gap dominates δ and a whole-gadget path wins; the companion step restores synchronization without bridge use. At z=0 the bridge path wins strictly and the next step reverses it. The recursive bottlenecks are one. These strict comparisons apply to every shortest-path choice; they are not a claim that an arbitrarily chosen, favorable tie-breaker suffices. My exhaustive small-state searches found one shortest path at each examined state, but the universal conclusion comes from the state argument and strict inequalities, not that sample observation.

The source's printed n=1 second-path expression omits its integer offset. Its two crossed arcs give 1−v₁ before the δ adjustment. The current paper expressly states that correction. Likewise, it restores the ±δ term in the source's post-adjustment envelope. Neither source exposition issue persists as a current-paper error. A forward bridge step begins at demand 2j; its midpoint has bridge flow 1/2 and q=2j+1/2≤F−3/2.

### 3. Perturbation preserves the execution and isolates every real demand

For the original cost denominator lattice D, the added costs ρᵢ=1/(4D3ⁱ) have sum less than 1/(8D). Two simple residual path incidences differ coordinatewise by at most two, so their perturbation difference has magnitude less than 1/(4D). A nonzero original comparison has magnitude at least 1/D. Thus a perturbed shortest path is an original shortest path **in the same residual state**. Starting from the same zero flow and choosing the same path couples the original and perturbed executions; equal capacities give equal bottlenecks. Comparing paths across different executions would not establish this, but the paper does not make that mistake.

For a simple nontrivial residual cycle, the projected coefficients lie in {−1,0,1}. A nonzero original cost keeps its sign; an original zero cost receives a nonzero ternary perturbation because its first nonzero term strictly exceeds the finite tail. The forward/reverse formal two-cycle has zero projection and causes no flow change. If two distinct real-valued fixed-demand optima existed, their difference would admit a sign-conformal residual-cycle decomposition. Sign conformity excludes those formal zero-projection cycles. Optimality makes every used cycle nonnegative in cost, while the total cost difference is zero, forcing a nontrivial zero-cost cycle. This contradiction does not require integral flow or rational demand.

The interpolation argument also holds for real increments. A feasible flow difference of net value Δ decomposes into residual source-to-sink paths of total weight Δ plus circulations. The paths cost at least the shortest residual path and all cycles are nonnegative. Augmenting a shortest path by any amount up to its bottleneck attains that lower bound. Hence the entire fractional SSP curve, not just its integral vertices, consists of fixed-demand optima. Compact feasible sets give existence, and the cycle argument gives uniqueness. In a no instance every optimum therefore has zero bridge flow; in a yes instance the required half-bridge optimum exists.

Adding the topological potential makes every original cost strictly positive and changes the cost of every fixed-value flow by the same linear function of its value. Residual cycles receive zero shift. These operations neither change the optimizing flows nor reintroduce ties.

### 4. Simplex encoding is feasible, injective and retains the needed optima

The DAG path-length bound is ∑fᵢ≤Lq with L=V−1. For a simplex point the definitions give h=F(1−x₀), fᵢ=LFxᵢ and q=h−Kfₑ, with K=1/(2L). Consequently q≥h/2≥0, and q=0 occurs only at the distinguished pure row. Conversely, the explicit inverse uniquely determines every arc coordinate, the star coordinate and x₀ from (f,h). The single slack coordinate does not create multiple row strategies for the same flow data.

For every nonnegative λ in the stated interval, the scaled zero-bridge maximum flow gives a feasible simplex point. In no instances the unrestricted unique optimum has fₑ=0 and h=q=λ, so it survives the simplex restriction. Every restricted optimum must then be that optimum. For yes instances the forward midpoint has h=q+K/2<F and q<F−ε; the path-length bound makes the star coordinate nonnegative. Thus the witness survives the restriction. There is no need to assume all unrestricted optima survive on arbitrary yes-instance demands.

### 5. The uniform exact penalty controls the whole minimizer set

I derived the displayed LP dual directly: maximizing ν−(r+sλ)ᵀμ subject to μ≥0 and ν1≤c+Rᵀμ. Its feasible polyhedron depends on R,c, not λ. It is nonempty and pointed: nonnegativity forbids a two-sided line in μ, and the upper bounds then forbid a nonzero ν-line. Strong duality and bounded primal feasibility give an attained optimal face for each real λ. A nonempty pointed optimal face has a vertex, which is a vertex of the dual feasible polyhedron.

Clearing denominators in the dual constraints is sufficient; clearing an irrational λ would be both impossible and unnecessary. In dimension d₀=k+1, a vertex has d₀ independent active normals, even when its optimal face is lower dimensional or constraints are redundant. Integer determinant denominators have absolute value at least one, and the elementary numerator bound d₀!H₀^d₀ yields ∥μ∥₁≤C=k d₀!H₀^d₀ for an optimal vertex. M=C+1 is computable without enumerating vertices.

For any simplex x with maximum positive constraint violation Δₓ, dual feasibility gives cᵀx≥v(λ)−CΔₓ. Therefore its penalized objective is at least v(λ)+(M−C)Δₓ. Every infeasible point is strictly worse, while feasible points retain their original objective. This proves equality of **all** minimizer sets, not just existence of one feasible minimizer. The strict M>C is necessary; the supplied toy control correctly detects an infeasible tie when equality is allowed. The proof is uniform over irrational λ and over degenerate optimal faces.

### 6. Exact rank one and full equilibrium correspondence

The penalty columns include a zero baseline, ensuring the maximum penalty is nonnegative. With bⱼ=−Msⱼ and B=−A+abᵀ, the two parameter-equality inequalities give b entries −M and M. Since a₀=−ε≠0, the matrix sum has rank **exactly one**, not merely at most one. The construction has m=8n+9 rows and N=16n+22 columns.

The auxiliary zero-sum row payoff is −cᵀx minus the chosen penalized residual. Maximizing its worst-column payoff therefore selects exactly the penalty minimizers. The scalar condition λ=aᵀx makes the original and auxiliary column payoff vectors coincide; the row change is a constant across rows. Thus both full best-response sets agree in both directions. This is the all-equilibria correspondence, with no support positivity or nondegeneracy assumption. Adsul et al.'s primary v4 Lemma 6 and Theorem 7 state the corresponding complete-set result; the manuscript's specialization is also proved directly.

### 7. Negative parameters leave precisely one strict pair

For λ<0 the diagnostic residual q−λ is strictly positive. Positive costs and q>0 away from pure row 0 imply every other simplex point has penalty objective strictly above −Mλ. Row 0 attains that value, so it is the only optimal row, and the scalar equation forces λ=−ε.

This by itself would not prove pair uniqueness. The paper additionally proves that the diagnostic column is the unique maximizing column against row 0: its original payoff is Mε>0, whereas baseline/conservation columns give zero, the opposite diagnostic gives −Mε, and capacity columns give −Muᵢ<0. Row 0 is its strict best response because every other row has payoff −cᵢ−Mqᵢ<0. All capacities are strictly positive. This exhausts the opposing strategies as well as the row strategies at the negative crossing.

### 8. Nonnegative crossings are exactly the bridge event

Every equilibrium parameter lies in [−ε,F−ε]. For a nonnegative candidate, the exact-penalty lemma applies and forces q=λ. The scalar condition reduces exactly to Kfₑ=ε, hence fₑ=1/2. At λ=0 the DAG permits only zero flow, so there is no crossing. A no PARTITION instance has no nonnegative crossing at all, for any row optimum or opposing strategy. The strict negative pair is therefore the unique equilibrium pair. A yes instance supplies a retained half-bridge row optimum and an auxiliary optimal opponent; finite zero-sum minimax gives such opponents, and any one pairs with that optimum. The scalar correspondence yields a distinct second equilibrium. It is unnecessary to enumerate or assert a finite number of other equilibria on yes instances.

### 9. Construction size and ordinary-language membership

All capacities and the possibly exponential numerical F have O(n) bits. The original denominators divide 240S; the ternary denominators add O(p) bits. Potentials, simplex coefficients and dual denominator clearing have polynomial binary length. Although M can be enormous numerically, log M is O(k log k+k log H₀), hence polynomial. Integer arithmetic can construct all explicitly listed matrix entries in polynomial time. The exponentially many SSP states are used only to prove correctness and are not executed by the reduction algorithm. These observations support ordinary, not strong, hardness.

For membership, the closed support cells X(I,J)×Y(I,J) are rational compact product polytopes. Declared support coordinates may vanish: equalities ensure all actually used actions are still best responses, so this closure adds no spurious pairs. Conversely each equilibrium is in its actual-support cell. The finite union need not be convex or polynomially sized.

Each nonempty cell is the convex hull of its vertices. If its overall union contains more than one pair, the union of cell vertices must contain two distinct pairs; otherwise every nonempty cell and its union would be the same singleton. Clearing all payoff denominators and using active independent equations bounds vertex numerators and denominators by d^(d/2)H₁^d. This gives polynomial-size rational witnesses even when the initial example is irrational or the equilibrium set is a continuum. Exact best-response inequalities, normalization and distinctness verify the witnesses in polynomial time.

Malformed and rank-invalid encodings are rejected by both defined languages. The complement of UNIQUENESS therefore has a polynomial invalid-input branch plus the two-pair NP certificate branch. Finite-game equilibrium existence makes valid rank-one games either unique or nonunique. The paper does not silently identify the two ordinary languages as complements on all strings. Exact rank is polynomially checked by the nonzero-pivot cross-product identities. The supplied-strict-equilibrium variant uses the same reduction, with polynomially checkable default data.

## Independent checks, then published replays

`independent_controls.py` was authored and run **before either packaged helper was read**. It constructs the network and game directly from the paper. It uses exact Fraction arithmetic, reverse shortest-distance labels with tight-edge path enumeration, residual potentials, cycle projections, simplex inverses and direct best-response inequalities. It imports no published helper or sibling code.

- **47 inputs**, including all positive weights 1–3 at lengths 1–3, length-four examples, an odd length-five no instance and a case with 10²⁰-scale weights.
- **788 unit augmentations and half-flow optimum certificates**, with exact capacity/conservation, reduced-cost certificates, original/perturbed shortest comparison in the same state, bridge parity and inverse-simplex checks.
- **12 exhaustive original-choice searches** for all length-one/two inputs with weights 1–3; 84 transitions examined. Those inputs had no ties. These searches are bounded corroboration of the universal state proof.
- **768 zero-cost cycle occurrences** inspected in small half-flow residual graphs; all had zero original projection, with no genuine zero-cost flow-change cycle.
- **Five full games**, **52 exact auxiliary equilibrium pairs**, and **eight positive original-game witness pairs**. The latter are generated at half-bridge parameters in the two selected yes cases. Each selected game also has its strict default directly checked. Constructed M values range from 1,545 to 5,331 bits.
- Negative controls show that M=1 can lose exactness in these networks, reversing the payoff outer-product sign destroys the default witness, one unique row can coexist with an opponent continuum in an exact-rank-one 1×2 game, and duplicated slack coordinates lose injectivity. These are boundary checks, not defects in the supplied construction.

The 62,760 individual assertions include repeated arc-capacity checks; they should not be read as 62,760 independent mathematical results. The evidence supports the reconstruction and exhibits exact witnesses, rather than replacing the quantified proof or enumerating all game equilibria.

After that run, I read the full two published helpers and copied **only their code** into disposable review directories. Both source copies remain byte-identical. The flow checker passed in normal and optimized modes: each recorded 37 inputs, 660 augmentations, 864 small-instance cycles, six original-choice searches and its four deliberate controls. The game checker passed in normal mode, producing six games and 204 auxiliary-pair checks, including its exact dual, rank/certificate, continuum and strict-penalty controls. Its assertions require normal mode; no optimized game run is claimed. All three processes exited zero with empty stderr. Fresh outputs and execution receipts are saved. Original published receipts were not used as results, and the absent historical six-game/39-network computations were not replayed.

## Primary sources, independence and limits

Fresh primary downloads and hashes are in `primary-source-receipts.json`:

- [Disser–Skutella, author-hosted journal body](https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf), SHA-256 `88cc527ec698aaa502a93c33183ae58b714a4879ca387b1101208c7dc329ff5a`: printed pages **5:5–5:10**, especially the definitions, Lemmas 3.1–3.2 and their complete proofs, and Figures 1–3 as extracted with the surrounding text. The controlling source is the journal edition. No claim is made to have inspected the exact SODA proceedings body or all 19 journal pages.
- [Adsul et al., arXiv v4](https://arxiv.org/abs/1812.04611v4), SHA-256 `14f221473a8a04f9863c3b49c79d230d362824327361b758530265550227c4e3`: printed pages **7–9**, Lemmas 4–6, Theorem 7 and the zero-sum LP interface in Lemma 8. Version/date and journal reference were also confirmed on the primary landing page. The mathematical full-set interface is checked in this version. I did not separately fetch the journal typesetting to certify its theorem-number mapping.

Standard finite-game existence, LP duality, flow decomposition and polytope facts are used in their usual stated finite-dimensional forms. The paper rederives its penalty and rational-witness bounds; they do not rely on an unexamined new theorem. Broader historical claims and prior-art comparisons involving Gilboa–Zemel, Conitzer–Sandholm, Erickson–Fox–Lkhamsuren, the Oberwolfach conjecture, unrecovered theses and priority gaps were not independently certified by this analytic review. No global novelty or firstness finding is made.

The necessary `SUPPLEMENT.md` mixes execution instructions with historical acceptance/review summaries, and the published main paper reports old AI review and source-audit activity. These were incidentally exposed while reading required materials. They were not adopted as mathematical evidence. The fresh source receipt also lists historical filenames and hashes, whose contents were not opened. No dedicated archived acceptance/audit/verdict reports, current sibling reports or sibling code were read. An attempt to delegate a separate primary-source check failed because the concurrent-agent limit was full; I completed that interface check directly.

The strongest verified result is the stated exact-rank-one, rational, variable-dimension, whole-pair coNP/NP completeness theorem, including the known strict default and arbitrary degeneracy. No substantive central gap remains in this analytic reconstruction. The finite checks are explicitly bounded; this is not proof-assistant verification or conventional human peer review. No source repair, site or spreadsheet edit, promotion, Git operation, publication action or outside contact occurred.
