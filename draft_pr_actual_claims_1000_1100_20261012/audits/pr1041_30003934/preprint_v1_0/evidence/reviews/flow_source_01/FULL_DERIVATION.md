# Independent flow/source derivation — PR 1041, problem 30003934

Scope: §§1–2 and flow-dependent size/interface claims of submitted PROOF.md, SHA-256 5392acc347fe0eaf8597ac619341b2946d21781e6118676248a4ee83baad6c1b, submitted head ad138ddd5bd1a51c0f225f03342c0c058873f790. This derivation was written before reading submitted independent_audit/AUDIT.md or FINAL_ACCEPTANCE.md. Other families' fresh reports were not read. Game conversion, uniform penalty, and rational certificate membership are outside this verdict.

The target hypothesis is a polynomial reduction from positive-integer PARTITION to rank-exactly-one rational-game NONUNIQUENESS, with a known strict default equilibrium and another equilibrium precisely for yes instances. My assigned necessary interface is a polynomial-size rational DAG whose perturbed fixed-value optimum is unique for every real q, never uses its bridge on no instances, and has a unique half-bridge optimum within the simplex parameter range on yes instances.

## 1. Fresh source identity and construction

Fresh downloads at UTC 2026-10-13T22:36:35.770940+00:00 (DS) and 22:36:37.451779+00:00 (Oberwolfach) have the same raw bytes as submitted provenance. DS: https://www2.mathematik.tu-darmstadt.de/~disser/pdfs/DisserSkutella18.pdf ; 553046 bytes; SHA-256 88cc527ec698aaa502a93c33183ae58b714a4879ca387b1101208c7dc329ff5a. This is the final ACM Transactions on Algorithms 15(1), Article 5 (November 2018), 19-page edition, DOI 10.1145/3280847, rather than the SODA abstract. Raw downloaded PDF, layout extraction, and inspection images are private review working material under sources/raw, not part of the proof edition.

I read Section 2 (printed 5:5–5:6), complete Section 3.1 (5:6–5:9), complete Section 3.2 (5:9–5:10), and the Corollary 1.7 statement and proof (5:5, 5:17). Visual inspection of PDF pages 7–10 checked Figure 1's four recursive arcs, Figure 2's residual orientations, Figure 3's +a-to−a bridge endpoints, the base ε/5 label, and Lemma 3.2's two cases. PDF page 17 was also visually checked. These page numbers are one-based PDF indices; their printed article numbers are 5:7 through 5:10 and 5:17.

Normalize w_i by a_i=w_i/(24S), S=sum w_i, ε=1/(24S). Then A=sum a_i=1/24<1/12, each a_i is a positive multiple of ε, and the signed sum a^[j]=sum_i (-1)^(bit_(i−1)(j)) a_i is zero iff the subset specified by j partitions the weights. This is an exact equivalence, unaffected by normalization.

For each of two signs v=±a, the submitted graph exactly matches Figure 1 and §3.2: base s0→t0 of capacity 1/cost δ=ε/5; four arcs at level i, the two cheap arcs of cost v_i/2 and the two crossed arcs of cost (2^i−1−v_i)/2, all capacity 2^(i−1); two exterior arcs capacity 2^n/cost 0. Figure 3's distinguished bridge has capacity 1/cost 0 and goes +s0→−t0. Counts are 2(2n+2)+2=4n+6 vertices and 2(4n+1)+4+1=8n+7 arcs. Order the global source first, all s_i from large i to small i in both gadgets next, all t_i from small i to large i next, and the global sink last. Every original arc increases this order, including the bridge, so the graph is a DAG despite its negative cheap costs in the −a gadget.

The source cut bounds q by 2·2^n. A zero-bridge maximum flow is explicit: in each gadget, put 2^(n−1) on each of its four level-n arcs, zero on every lower-level arc, and 2^n on each exterior connector. The two length-two paths at the top level obey conservation, so F=2^(n+1) is attained. Scaling this particular flow by q/F provides a zero-bridge feasible flow for every real 0≤q≤F. This existence does not require it to be a minimum-cost flow.

## 2. Source quantifier and bridge timing

Lemma 3.1's induction tracks the gadget's state, not an arbitrarily selected list of paths. The level-i construction first exhausts the two cheap connectors through the lower gadget, then uses the crossed connectors while reversing the lower gadget; the path costs are j+v^[j] before the base δ adjustment. Its strict separation between the two phases prevents a tie execution from leaving this recursive sequence. After the δ adjustment, the local marginal is j+v^[j]+(-1)^j δ, and the base arc is empty at even j and full at odd j.

The complete Lemma 3.2 proof does not prescribe a special tie rule. It considers a synchronized pair of gadget states j and compares the best path wholly in +a, the best path wholly in −a, and the best bridge path. Their costs at that synchronized state are, writing z=a^[j]:

| Base state | +a path | −a path | forward bridge path | forced next reverse bridge path when z=0 |
|---|---:|---:|---:|---:|
| empty, even j | j+z+δ | j−z+δ | j | j+2δ |
| full, odd j | j+z−δ | j−z−δ | j−2δ | j |

If z≠0, then |z|≥ε=5δ, so one whole-gadget path is strictly cheaper than the bridge path. Its next companion augmentation restores synchronization and also excludes the bridge. If z=0, the forward bridge path wins strictly; the next shortest augmentation uses the bridge backward and restores both gadgets to their next state. The proof's synchronization induction, not merely Corollary 1.7's selected-parametric-solution shorthand, applies to every legitimate SSP execution (a shortest residual simple s–t path, augmented by its bottleneck). All source gadget augmentations have bottleneck one. Thus bridge forward use has f_e:0→1 and the immediate next step has f_e:1→0. At the forward midpoint q=2j+1/2, f_e=1/2. Since j≤2^n−1, q≤F−3/2. The no case has no bridge use anywhere on the SSP curve.

Two source-local slips were verified visually and resolved directly, without changing the stated source theorem. In Lemma 3.1's i=1 base paragraph the second path is printed with cost −v1. Figure 1's two crossed arcs instead give 1−v1, as required by its general j+v^[j] formula. Also §3.2's post-adjustment envelope [j−A,j+A] should be [j−A−δ,j+A+δ]. The state-j versus state-(j+1) separation remains strict because 2(A+δ)<1 (indeed ε≤A and δ≤A/5). These are arithmetic/transcription slips in the upstream exposition, not an unsupported new source theorem. The submitted construction uses the correct arc formulas.

SSP's introductory nonnegative-cost restriction is also harmless here: its recursive −a cheap arcs are negative, but the initial DAG has no directed circulation and the zero flow is optimal at value zero. The standard shortest-augmentation argument below applies whenever the starting residual network has no negative cycle; alternatively the positive topological potential below can be applied before running SSP, preserving every comparison and flow.

## 3. Independent continuous optimum proof

Let f be optimal at real flow value q, P a shortest residual s–t path of cost ℓ, and Δ no larger than P's residual bottleneck. For any feasible g of value q+Δ, the sign-conformal residual representation of g−f is a nonnegative residual flow of divergence Δ at s and −Δ at t. Decompose it into s–t paths of total amount Δ and directed cycles. Every cycle has nonnegative cost because f is optimal (otherwise a sufficiently small circulation along it improves f). Every s–t path costs at least ℓ. Consequently c·(g−f)≥Δℓ. The flow f+Δχ_P attains exactly Δℓ, proving it optimal for every real 0≤Δ≤bottleneck, including fractional midpoints. Starting from the zero flow in a DAG gives induction along the entire SSP curve. This is an exact LP argument, not an integrality assumption or interpolation heuristic.

## 4. Comparison-preserving perturbation

Let D=lcm of the reduced denominators of all original arc costs, and let p=8n+7. Every original residual simple-path cost lies in (1/D)Z; so does every difference of such costs. Set ρ_i=1/(4D·3^i), i=1,…,p. The finite geometric series gives sum ρ_i<1/(8D). A residual simple path has projected coefficients in {−1,0,1}; a path difference has coefficients in {−2,…,2}, so its perturbation magnitude is less than 1/(4D). A nonzero original path comparison has magnitude at least 1/D and cannot change sign. Thus every perturbed shortest path belongs to the original shortest set in that same residual state.

Couple executions state by state: both start at identical zero flows, a perturbed shortest path is an allowable original shortest path, and the residual bottleneck depends only on capacities and current flow. Augmenting that same path therefore gives the same next state. By induction the perturbed SSP execution is a legitimate source execution, so it has the universal bridge behavior in §2. An argument comparing different residual states would not suffice; the coupling explicitly keeps them identical.

For any simple residual cycle whose original projected vector σ∈{−1,0,1}^p is nonzero, its original cost is either a nonzero multiple of 1/D (so its sign persists), or zero. In the latter case choose the smallest k with σ_k≠0. The magnitude of ρ_k exceeds the finite sum of all later ρ_i, so sum σ_iρ_i≠0. Therefore no nontrivial projected simple cycle has zero perturbed cost. A formal two-cycle consisting of an original arc and its reverse has projected vector zero and changes no original flow; it must not be treated as evidence of nonuniqueness.

Now fix any real q and suppose f≠g are two perturbed optima. Their difference has zero divergence and can be decomposed sign-conformally into positive multiples of residual simple cycles of f. Sign-conformal means only the direction of g_i−f_i is used for each original arc, so a projected-zero formal two-cycle cannot occur in this decomposition. At least one cycle is nontrivial. Each cycle has nonnegative cost by optimality of f, and the weighted sum of their costs is c·(g−f)=0, so every occurring nontrivial cycle has cost zero, contradicting the previous paragraph. This proves uniqueness for every real q, with no restriction to integral q or vertices.

Thus the interpolated perturbed SSP curve is the unique unrestricted minimum-cost flow at each q. In a no instance every optimum has e=0. In a yes instance the forward midpoint is the unique optimum and has e=1/2 at q≤F−3/2.

## 5. Positive costs and bit complexity

For a topological order r and H=1+max_i|c_i+ρ_i|, set cbar_(u,v)=c_i+ρ_i+H(r(v)−r(u)). Since each difference is at least one, cbar_i≥1. Conservation gives the exact identity sum f_i H(r(v_i)−r(u_i))=H(r(t)−r(s))q. Hence fixed-value objectives shift by a constant, residual s–t path costs all shift by the same H(r(t)−r(s)), and residual cycles shift by zero. The perturbation's uniqueness and SSP comparisons survive the potential.

Here all normalized costs have denominators dividing 240S (cheap costs divide 48S; the base cost is 1/(120S)); D therefore has O(log S) bits, even though a generic denominator-lcm argument would also be polynomial. Each 3^i has O(p) bits. Capacities have O(n) bits, F has n+2 bits, costs up to order 2^n have O(n+log S+p) bits after perturbation and potential, and r has O(log n) bits. The graph is generated in polynomial time without executing its exponential SSP trajectory.

## 6. Simplex interface, including boundaries

Set L=|V|−1=4n+5 and K=1/(2L). Every nonnegative feasible DAG flow decomposes into s–t paths with total weight q and at most L arcs each, so sum_i f_i≤Lq. There are no circulation components because the original graph is acyclic. The bound also proves q=0 implies f=0. A general directed graph would need extra circulation control; this is precisely where the DAG assumption is used.

For x=(x0,x*,x1,…,xp) in the standard simplex, let h=F(1−x0), f_i=LF x_i, and q=h−K f_e. The simplex gives 0≤h≤F, f≥0, sum f≤Lh, and q≥h−K sum f≥h/2≥0. Conversely any such f,h has the unique coordinate representation x_i=f_i/(LF), x*=h/F−sum f/(LF), x0=1−h/F. Thus the map loses no flow information and introduces no free slack strategy.

At every real λ∈[0,F], the scaled zero-e maximum flow has q=h=λ and satisfies the simplex bound, all capacities, and conservation. The restricted LP is therefore feasible and compact, including λ=0 and λ=F.

In a no instance its unique unrestricted perturbed optimum has f_e=0, so h=q=λ≤F and sum f≤Lλ. It is feasible for the restriction, which cannot improve the unrestricted optimum. Every restricted optimum is therefore this same unique flow and same unique simplex vector.

In a yes instance take the unique forward midpoint: f_e=1/2 and q=λ≤F−3/2. Set h=λ+K/2. Since K≤1/18 for n≥1, h<F. Since sum f≤Lq≤Lh, the unique simplex representation is feasible and remains optimal under the restriction. Also λ≤F−3/2<F−K/2, which fits the later game's required upper endpoint F−ε_game with ε_game=K/2. This is a constructive existence statement about the restricted optimum, conditional on the other family's correctly implementing the LP-to-game correspondence and penalty lemma.

## 7. Checks made independently of prior reports

flow_check.py is a newly written standard-library exact checker, not the manuscript's omitted computation/verify_reduction.py. It explicitly constructs rational arc lists; enumerates all simple residual s–t paths at each tested state; chooses the perturbed shortest path and checks membership in the original shortest set; verifies unit bottlenecks and immediate bridge reversal; checks flow conservation, capacities, the DAG path-sum bound, topological positivity and path-potential telescoping; checks every unit's half-flow optimality by exact Bellman–Ford residual dual reduced costs; and checks the midpoint simplex coordinates/range. It scales the explicit terminal zero-bridge flow at several extra rational values for feasibility. For n≤2 it enumerates all simple residual cycles at every half flow and distinguishes nonzero projection from the formal zero-projection two-cycle.

The checked positive cases comprise 37 distinct weight vectors with n=1,…,4, including all ordered triples in {1,2,3}^3, both odd-total and unequal-weight no instances, symmetric and multiple-solution yes instances, and binary-weight no instances. There are 660 exact augmentations and corresponding half-flow optimum checks. An additional exhaustive exploration of all original shortest-path branches covers six instances [1], [1,1], [1,2], [1,2,3], [1,2,4], [1,1,1,1]. All terminal executions satisfy the partition equivalence.

Four negative controls are required to pass: a yes instance [1,1] with δ set to zero admits an original SSP execution never using the bridge; a true projected-nonzero zero-cost residual cycle is detected; the harmless formal projected-zero two-cycle is detected separately; and an oversized perturbation produces a path that was not originally shortest. Runtime checks use explicit exceptions, not Python assert, so optimized mode cannot disable them. Both normal and -O receipts are retained. These checks are supplementary finite evidence. They do not prove all n, rational certificate membership, the penalty constant, or all game equilibria. The source proof plus deductions above supply the quantified argument.

The edition tree has exactly 11 files and supplies no executable, fixtures, or machine-readable check logs. Its historical six-game, 39-network, and later audit finite-check claims have not been replayed, simulated, or counted as present deliverables.

## 8. Historical source question

The complete von Stengel contribution in Oberwolfach Reports 38/2018, printed p.2332 (one-based PDF page 30), was read, including its five references. Fresh primary report: https://ems.press/content/serial-article-files/46760 ; 1014372 bytes; SHA-256 850879c0962050da5fb7f99dd0e2218dcc1cb2c9729266fdfd239c7ca1545003. It defines game rank as rank(A+B), relates rank-one equilibria to a parametric zero-sum/LP family, notes polynomial computation of one equilibrium despite possible exponential multiplicity, and poses coNP-hardness of equilibrium uniqueness as a conjecture. It does not prove the conjecture or promise nondegeneracy for the exact decision problem. This verifies historical target provenance, not current openness, novelty, priority, or completeness of a literature search.

## Provisional independent verdict before old-audit comparison

CLEAN in the assigned flow/source scope, conditional on the game/penalty/certificate families. The central all-optimal quantifier follows from the submitted comparison-preserving perturbation and sign-conformal cycle argument, rather than from the corollary shorthand. No unsupported equivalent central claim is imported. Two small upstream printed slips have explicit direct-algebra resolutions; a minor submitted wording ambiguity is that "original optimum" in §2 should mean the unrestricted perturbed/potential-shifted network optimum. None changes the reduction's flow interface. No overall coNP-completeness acceptance is issued by this scoped review.
